"""Hourly TimescaleDB -> Google Sheets exporter.

Appends un-exported rows from sensor_readings to a Google Sheet in
append-only long format: ts, station, sensor, metric, value.

Cursor design — why there is no ts watermark:
    Sensor CSVs arrive late and backfill. In July 2026 weeks of stalled
    uploads were replayed (TODO-103), inserting rows with OLD ts values long
    after newer rows already existed. A max(ts) cursor would have silently
    skipped every one of them.

    Instead we keep a ledger table, sensor_exports, keyed on
    (ts, station, sensor, metric), and select work via anti-join. This
    mirrors sensor-ingest: idempotency delegated to a unique key, zero local
    state, and no assumption that data arrives in ts order.

    sensor_readings is NEVER altered by this service. Its only write is to
    sensor_exports, a table sensor-ingest has never heard of, so a bug here
    cannot affect ingestion.

Delivery semantics — at-least-once, by choice:
    Sheets appends are not idempotent and have no idempotency key. Rows are
    appended FIRST and marked exported SECOND, so a crash — or an ambiguous
    HTTP response where the append succeeded but the reply was lost — will
    re-append that batch next cycle. Duplicates, never loss: a duplicate is
    one 'Data > Data cleanup > Remove duplicates' away, a missing row is
    undetectable.

    Blast radius is one batch (EXPORT_BATCH_ROWS). A 'sheets append ok' log
    line with no following 'marked exported' names the duplicated batch and
    its exact cell range.

Environment:
    PG_DSN                     libpq connection string. Required.
    SHEETS_SPREADSHEET_ID      Target spreadsheet ID. Required.
    SHEETS_TAB                 Target tab name. Default readings.
    SHEETS_KEY_FILE            Service-account JSON key. Default /secrets/sheets-sa.json.
    SHEETS_VALUE_INPUT_OPTION  RAW or USER_ENTERED. Default USER_ENTERED.
    EXPORT_INTERVAL_SECS       Seconds between runs. Default 3600.
    EXPORT_BATCH_ROWS          Rows per Sheets append. Default 2000.
    EXPORT_BATCH_PAUSE_SECS    Pause between appends (write quota). Default 1.5.
    EXPORT_MAX_ROWS_PER_RUN    Cap on rows exported per run. Default 200000.
    EXPORT_MIN_TS              Optional ts floor, ISO-8601. NOT a cursor; it
                               never advances. Default unset.
    EXPORT_MODE                live | dry-run | preview. Default live.
    SHEET_ROW_WARN             Warn above this sheet row count. Default 750000.
"""
import logging
import math
import os
import re
import sys
import time
from datetime import timezone

import psycopg2
from psycopg2.extras import execute_values
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

LOG = logging.getLogger("sheets-export")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

PG_DSN = os.environ["PG_DSN"]
# .get(), not [...]: compose passes this as ${SHEETS_SPREADSHEET_ID:-}, which
# sets an EMPTY string rather than leaving the variable unset, so a KeyError
# would never fire. main() rejects the empty value explicitly instead.
SPREADSHEET_ID = os.environ.get("SHEETS_SPREADSHEET_ID", "").strip()
SHEET_TAB = os.environ.get("SHEETS_TAB", "readings")
KEY_FILE = os.environ.get("SHEETS_KEY_FILE", "/secrets/sheets-sa.json")
VALUE_INPUT_OPTION = os.environ.get("SHEETS_VALUE_INPUT_OPTION", "USER_ENTERED")
INTERVAL_SECS = int(os.environ.get("EXPORT_INTERVAL_SECS", "3600"))
BATCH_ROWS = int(os.environ.get("EXPORT_BATCH_ROWS", "2000"))
BATCH_PAUSE_SECS = float(os.environ.get("EXPORT_BATCH_PAUSE_SECS", "1.5"))
MAX_ROWS_PER_RUN = int(os.environ.get("EXPORT_MAX_ROWS_PER_RUN", "200000"))
EXPORT_MIN_TS = os.environ.get("EXPORT_MIN_TS", "").strip() or None
EXPORT_MODE = os.environ.get("EXPORT_MODE", "live")
SHEET_ROW_WARN = int(os.environ.get("SHEET_ROW_WARN", "750000"))

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Trailing row number of an updatedRange like "readings!A101:E2100" -> 2100.
# Gives us the sheet's row count for free on every append, with no extra call.
UPDATED_RANGE_RE = re.compile(r":[A-Z]+(\d+)$")

# Sheets caps a spreadsheet at 10,000,000 cells; at 5 columns that is 2M rows.
SHEET_HARD_LIMIT_ROWS = 2_000_000

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS sensor_exports (
    ts          TIMESTAMPTZ NOT NULL,
    station     TEXT        NOT NULL,
    sensor      TEXT        NOT NULL,
    metric      TEXT        NOT NULL,
    exported_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (ts, station, sensor, metric)
);
"""

# Column order of the PK matches sensor_readings_uniq so the anti-join probe
# and the ordered scan line up.
#
# NOT EXISTS rather than LEFT JOIN ... IS NULL: identical plans, but it states
# the intent and can't be silently converted to an inner join by someone later
# adding a predicate on the right-hand table.
#
# No OFFSET: each batch marks its rows before the next fetch, so the anti-join
# self-advances. That is what makes a mid-run failure safe.
SELECT_SQL = """
SELECT r.ts, r.station, r.sensor, r.metric, r.value
FROM sensor_readings r
WHERE r.ts >= COALESCE(%s::timestamptz, '-infinity'::timestamptz)
  AND NOT EXISTS (
        SELECT 1
        FROM sensor_exports e
        WHERE e.ts      = r.ts
          AND e.station = r.station
          AND e.sensor  = r.sensor
          AND e.metric  = r.metric
      )
ORDER BY r.ts, r.station, r.sensor, r.metric
LIMIT %s;
"""

INSERT_SQL = """
INSERT INTO sensor_exports (ts, station, sensor, metric)
VALUES %s
ON CONFLICT (ts, station, sensor, metric) DO NOTHING;
"""


def init_schema(conn):
    with conn.cursor() as cur:
        cur.execute(SCHEMA_SQL)
    conn.commit()
    LOG.info("schema initialized")


def build_sheets_client():
    """Sheets service, or None when the mode never touches the API.

    Exits rather than returning None in live mode: a None client would make
    append_rows() a silent no-op while mark_exported() still advanced the
    ledger, permanently skipping those rows. Failing to start is the safe
    outcome — Docker's restart backoff keeps the retry loop from spinning.

    preview builds a real client so check_sheet_access() can prove the key
    loads, the sheet is shared, and the timezone is UTC — that check is the
    whole reason preview runs before live. It stays safe because process_once()
    returns before append_rows() in preview mode. Only dry-run, which never
    contacts the API at all, gets a None client.
    """
    if EXPORT_MODE == "dry-run":
        return None
    try:
        creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    except Exception as e:
        LOG.error("cannot load service-account key %s: %s — check the file exists "
                  "and is readable by uid 1001 (chown 1001:1001, chmod 0400)",
                  KEY_FILE, e)
        sys.exit(1)
    # cache_discovery=False: the container runs non-root with no writable
    # volume, so the discovery cache can't be written anyway.
    # static_discovery=True: use the document bundled in the wheel instead of
    # fetching it at startup — one less network dependency on container start.
    return build("sheets", "v4", credentials=creds,
                 cache_discovery=False, static_discovery=True)


def check_sheet_access(svc):
    """Prove auth AND document sharing at startup, not an hour later.

    Logs rather than exits: `restart: unless-stopped` would otherwise hot-loop
    against a permanent misconfiguration (e.g. sheet not shared).
    """
    if svc is None:
        return
    try:
        meta = svc.spreadsheets().get(
            spreadsheetId=SPREADSHEET_ID,
            fields="properties(title,timeZone)",
        ).execute(num_retries=3)
        props = meta.get("properties", {})
        tz = props.get("timeZone")
        LOG.info("sheet ok title=%s tz=%s", props.get("title"), tz)
        if tz not in (None, "Etc/UTC", "UTC", "Etc/GMT"):
            LOG.warning("sheet timezone is %s, not UTC — timestamps will render "
                        "shifted; set File > Settings > Time zone to UTC", tz)
    except Exception as e:
        LOG.error("cannot access spreadsheet %s: %s — check the sheet is shared "
                  "with the service account as Editor", SPREADSHEET_ID, e)


def fetch_batch(conn, limit: int) -> list[tuple]:
    """Un-exported readings, oldest first."""
    started = time.monotonic()
    with conn.cursor() as cur:
        cur.execute(SELECT_SQL, (EXPORT_MIN_TS, limit))
        rows = cur.fetchall()
    # The anti-join is unbounded by design (a bounded window would reintroduce
    # the ts-cursor bug). Log its cost so degradation is visible rather than
    # discovered.
    query_ms = int((time.monotonic() - started) * 1000)
    if rows:
        LOG.info("fetched rows=%d span=%s..%s query_ms=%d",
                 len(rows), rows[0][0], rows[-1][0], query_ms)
    return rows


def format_rows(rows: list[tuple]) -> list[list]:
    """DB rows -> Sheets cell values."""
    values = []
    for ts, station, sensor, metric, value in rows:
        # Space separator, no offset: Sheets' USER_ENTERED parser does not
        # reliably accept ISO-8601 with 'T' and '+00:00', and would leave the
        # column as text. This form becomes a real datetime cell.
        ts_str = ts.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        # sensor-ingest does a bare float(), which accepts "nan"/"inf".
        # json.dumps emits bare NaN, which is invalid JSON — Google rejects the
        # whole batch, so one bad reading would wedge the exporter forever.
        cell = value if value is not None and math.isfinite(value) else ""
        values.append([ts_str, station, sensor, metric, cell])
    return values


def append_rows(svc, values: list[list]) -> dict:
    if svc is None:
        # Belt-and-braces: in live mode a missing client must never look like
        # a successful append, or mark_exported() would retire rows that were
        # never written. build_sheets_client() already exits on this path.
        if EXPORT_MODE == "live":
            raise RuntimeError("live mode with no sheets client — refusing to "
                               "mark rows exported that were never appended")
        return {"updatedRange": "DRY_RUN", "updatedRows": len(values)}
    resp = svc.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_TAB}!A:E",
        valueInputOption=VALUE_INPUT_OPTION,
        # INSERT_ROWS, not the default OVERWRITE: OVERWRITE would silently
        # clobber anything a human has put below the table.
        insertDataOption="INSERT_ROWS",
        includeValuesInResponse=False,
        body={"values": values},
        fields="updates(updatedRange,updatedRows)",
    ).execute(num_retries=5)
    return resp.get("updates", {})


def mark_exported(conn, rows: list[tuple]) -> None:
    keys = [(ts, station, sensor, metric) for ts, station, sensor, metric, _ in rows]
    with conn.cursor() as cur:
        execute_values(cur, INSERT_SQL, keys, page_size=500)
    conn.commit()


def process_once(conn, svc) -> dict[str, int]:
    stats = {"batches": 0, "rows": 0, "sheet_rows": 0, "pending": 0}
    while stats["rows"] < MAX_ROWS_PER_RUN:
        rows = fetch_batch(conn, BATCH_ROWS)
        if not rows:
            break

        if EXPORT_MODE == "preview":
            LOG.info("PREVIEW would export rows=%d first_ts=%s last_ts=%s "
                     "(no append, no mark)", len(rows), rows[0][0], rows[-1][0])
            stats["pending"] = len(rows)
            break

        values = format_rows(rows)

        # Pre-flight the DB immediately before the non-idempotent append, so
        # the most likely mark-failure (a dead connection) lands BEFORE the
        # write and costs a no-op instead of a duplicated batch.
        with conn.cursor() as cur:
            cur.execute("SELECT 1")

        updates = append_rows(svc, values)
        # --- WINDOW OPEN: nothing between here and mark_exported may raise ---
        LOG.info("sheets append ok rows=%d first_ts=%s last_ts=%s updated_range=%s",
                 len(rows), rows[0][0], rows[-1][0], updates.get("updatedRange"))
        mark_exported(conn, rows)
        # --- WINDOW CLOSED ---
        LOG.info("marked exported rows=%d", len(rows))

        if updates.get("updatedRows") not in (None, len(rows)):
            LOG.error("sheets updatedRows=%s but sent rows=%d",
                      updates.get("updatedRows"), len(rows))

        stats["batches"] += 1
        stats["rows"] += len(rows)
        m = UPDATED_RANGE_RE.search(updates.get("updatedRange") or "")
        if m:
            stats["sheet_rows"] = int(m.group(1))

        if len(rows) < BATCH_ROWS:
            break
        time.sleep(BATCH_PAUSE_SECS)
    else:
        LOG.warning("run capped at max_rows=%d; remainder exports next cycle",
                    MAX_ROWS_PER_RUN)

    if stats["sheet_rows"] > SHEET_ROW_WARN:
        LOG.warning("sheet is large rows=%d hard_limit_rows=%d — plan a rollover "
                    "(create a new sheet, change SHEETS_SPREADSHEET_ID)",
                    stats["sheet_rows"], SHEET_HARD_LIMIT_ROWS)
    return stats


def main():
    LOG.info("starting; mode=%s interval=%ds batch=%d tab=%s",
             EXPORT_MODE, INTERVAL_SECS, BATCH_ROWS, SHEET_TAB)
    if EXPORT_MODE not in ("live", "dry-run", "preview"):
        LOG.error("EXPORT_MODE=%s is not one of live|dry-run|preview; exiting", EXPORT_MODE)
        sys.exit(1)
    # Exit rather than run: with an empty ID every Sheets call 404s, and the
    # main loop would swallow that as a retryable HttpError and spin hourly
    # forever. Docker's restart backoff makes a hard exit the visible failure.
    if not SPREADSHEET_ID:
        LOG.error("SHEETS_SPREADSHEET_ID is empty — set it in .env "
                  "(the /d/<ID>/ segment of the sheet URL); exiting")
        sys.exit(1)
    if EXPORT_MODE == "dry-run":
        LOG.warning("DRY RUN — rows will be MARKED EXPORTED but NOT written to "
                    "sheets; never use this on the AWS host")

    # Retry initial DB connect (timescale container may not be ready yet)
    for attempt in range(30):
        try:
            conn = psycopg2.connect(PG_DSN)
            break
        except psycopg2.OperationalError as e:
            LOG.info("DB not ready (attempt %d): %s — sleeping 2s", attempt + 1, e)
            time.sleep(2)
    else:
        LOG.error("could not connect to DB after 30 attempts; exiting")
        sys.exit(1)

    init_schema(conn)
    svc = build_sheets_client()
    check_sheet_access(svc)

    while True:
        try:
            started = time.monotonic()
            stats = process_once(conn, svc)
            # Logged every run, including zero-row runs: at one run per hour,
            # "idle" and "dead" are otherwise indistinguishable in the logs.
            LOG.info("exported: batches=%d rows=%d elapsed_s=%.1f",
                     stats["batches"], stats["rows"], time.monotonic() - started)
        except psycopg2.Error as e:
            LOG.error("DB error: %s — reconnecting", e)
            try:
                conn.close()
            except Exception:
                pass
            conn = psycopg2.connect(PG_DSN)
        except HttpError as e:
            # Deliberate third tier: the steady-state failure here is a
            # permanent 403 (sheet not shared). LOG.exception would print a
            # full traceback every hour forever; one ERROR line is operable.
            LOG.error("sheets API error: %s — retrying next cycle", e)
        except Exception as e:
            LOG.exception("unexpected error: %s", e)
        time.sleep(INTERVAL_SECS)


if __name__ == "__main__":
    main()
