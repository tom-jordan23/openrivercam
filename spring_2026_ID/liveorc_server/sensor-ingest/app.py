"""CSV sensor reading ingester.

Watches /data/<station>/*.csv (bind-mounted from /var/orc/sensors), parses
each file row-by-row, and upserts into a TimescaleDB hypertable. Idempotent
by composite unique key (ts, station, sensor, metric) — re-parsing a file
inserts only new rows.

Filename convention assumed:
    <sensor>_<YYYY-MM-DD>.csv
e.g.,
    sht40_2026-05-15.csv     -> sensor='sht40'
    rg15_2026-05-15.csv      -> sensor='rg15'
    ds18b20_2026-05-15.csv   -> sensor='ds18b20'

Station name comes from the parent directory.

CSV format expected:
    First column is a timestamp parseable by datetime.fromisoformat.
    Header row names the metric for each subsequent column.
    Values that don't parse as float are silently skipped.

Tables/indexes are created on startup (idempotent). The TimescaleDB
extension must be enabled in the target database — set up automatically
by the timescale/timescaledb-ha image.

Environment:
    DATA_DIR        Where sensor CSVs live. Default /data.
    PG_DSN          libpq connection string. Required.
    POLL_SECS       Seconds between polls. Default 30.
"""
import csv
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values

LOG = logging.getLogger("sensor-ingest")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
PG_DSN = os.environ["PG_DSN"]
POLL_SECS = int(os.environ.get("POLL_SECS", "30"))

FILENAME_RE = re.compile(r"^(?P<sensor>[a-z][a-z0-9_-]*)_(?P<date>\d{4}-\d{2}-\d{2})\.csv$")

SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS sensor_readings (
    ts       TIMESTAMPTZ      NOT NULL,
    station  TEXT             NOT NULL,
    sensor   TEXT             NOT NULL,
    metric   TEXT             NOT NULL,
    value    DOUBLE PRECISION NOT NULL
);

SELECT create_hypertable('sensor_readings', 'ts', if_not_exists => TRUE);

CREATE UNIQUE INDEX IF NOT EXISTS sensor_readings_uniq
    ON sensor_readings (ts, station, sensor, metric);

CREATE INDEX IF NOT EXISTS sensor_readings_by_dim
    ON sensor_readings (station, sensor, metric, ts DESC);
"""

INSERT_SQL = """
INSERT INTO sensor_readings (ts, station, sensor, metric, value)
VALUES %s
ON CONFLICT (ts, station, sensor, metric) DO NOTHING;
"""


def init_schema(conn):
    with conn.cursor() as cur:
        cur.execute(SCHEMA_SQL)
    conn.commit()
    LOG.info("schema initialized")


def parse_timestamp(s: str) -> datetime | None:
    s = s.strip()
    if not s:
        return None
    # Allow trailing 'Z' (Python <3.11 doesn't accept it in fromisoformat)
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        # Assume UTC if naive — stations are UTC by convention
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def parse_file(path: Path, station: str, sensor: str) -> list[tuple]:
    rows = []
    try:
        with path.open(newline="") as fp:
            reader = csv.DictReader(fp)
            if not reader.fieldnames:
                return rows
            ts_col = reader.fieldnames[0]
            for raw_row in reader:
                ts = parse_timestamp(raw_row.get(ts_col, ""))
                if ts is None:
                    continue
                for col, val in raw_row.items():
                    if col == ts_col or val is None:
                        continue
                    try:
                        v = float(val)
                    except (ValueError, TypeError):
                        continue
                    rows.append((ts, station, sensor, col.strip(), v))
    except Exception as e:
        LOG.warning("failed to parse %s: %s", path, e)
    return rows


def process_once(conn) -> dict[str, int]:
    stats = {"files": 0, "rows": 0, "skipped": 0}
    if not DATA_DIR.is_dir():
        LOG.warning("DATA_DIR %s does not exist yet", DATA_DIR)
        return stats
    for station_dir in sorted(DATA_DIR.iterdir()):
        if not station_dir.is_dir():
            continue
        station = station_dir.name
        for csv_path in sorted(station_dir.glob("*.csv")):
            m = FILENAME_RE.match(csv_path.name)
            if not m:
                stats["skipped"] += 1
                continue
            sensor = m.group("sensor")
            rows = parse_file(csv_path, station, sensor)
            if not rows:
                continue
            stats["files"] += 1
            with conn.cursor() as cur:
                execute_values(cur, INSERT_SQL, rows, page_size=500)
                inserted = cur.rowcount
            conn.commit()
            stats["rows"] += inserted if inserted >= 0 else 0
    return stats


def main():
    LOG.info("starting; DATA_DIR=%s POLL_SECS=%d", DATA_DIR, POLL_SECS)
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

    while True:
        try:
            stats = process_once(conn)
            if stats["rows"] > 0 or stats["skipped"] > 0:
                LOG.info("processed: files=%d new_rows=%d skipped_files=%d",
                         stats["files"], stats["rows"], stats["skipped"])
        except psycopg2.Error as e:
            LOG.error("DB error: %s — reconnecting", e)
            try:
                conn.close()
            except Exception:
                pass
            conn = psycopg2.connect(PG_DSN)
        except Exception as e:
            LOG.exception("unexpected error: %s", e)
        time.sleep(POLL_SECS)


if __name__ == "__main__":
    main()
