#!/usr/bin/env python3
"""station_gaps.py — reconstruct a station's boot history from its sensor rows.

WHY
    ISS-FIELD-008 / TODO-116: Sukabumi periodically misses a Witty Pi wake and
    then stays down — for days — until someone at site presses the button. For
    four months that was a paragraph of anecdote. It is not: the station writes
    a sensor row every wake, so the *absence* of rows is a precise record of
    when it was down, and the spacing between them is a precise record of when
    it booted more often than the schedule allows.

    Nobody noticed 25 days of downtime out of 118. Nobody noticed the station
    restarting every 5 minutes through the night of 2026-08-25. Both were
    sitting in the database the whole time. This script exists so that
    "is it up, how long was it down, and is it booting when it shouldn't"
    is one command instead of a research project.

    Two distinct signals, deliberately reported separately:

      outages       gaps longer than the duty cycle — a missed wake, the
                    TODO-116 failure. Onset and recovery are printed in site
                    local time because that is what makes the pattern legible
                    (failures cluster pre-dawn at the bottom of the battery's
                    discharge; recoveries cluster in local business hours,
                    which is what a human pressing a button looks like).

      extra boots   gaps far SHORTER than the duty cycle — the station woke
                    when the schedule said it should be off. There is no quiet
                    baseline to compare against: this has run in episodes since
                    at least 2026-05-07 (332 in May, 20 in June, 5 in July, 49
                    in August), so ALWAYS look at a long window before calling
                    any month a change. Something is starting the Pi that isn't
                    the alarm — a voltage threshold, or the Witty Pi re-powering
                    inside its own ON window. Timestamps alone cannot tell those
                    apart; the wp5 power-on-reason log on the Pi is what
                    separates them.

                    Note what this signal is NOT: episodes have passed with no
                    outage after them (2026-05-07..09), and the 2026-08-15
                    outage arrived out of a completely clean cadence. It is not
                    a reliable precursor and must not be built into an alarm as
                    though it were.

WHAT IT TOUCHES
    Nothing. It runs one read-only SQL query through Grafana's anonymous
    datasource proxy (GF_AUTH_ANONYMOUS_ENABLED, role Viewer), which needs no
    credentials, no SSH and no Session Manager session. See liveorc_server's
    README for why that endpoint is reachable at all.

    The Grafana cert is self-signed, so the committed CA is required.

USAGE
    ./station_gaps.py                             # sukabumi, all history
    ./station_gaps.py --since 2026-08-20          # since a date
    ./station_gaps.py --cycle-min 15              # station is on prod_15
    ./station_gaps.py --json                      # machine-readable

Read-only. Safe to re-run.
"""

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CA = REPO_ROOT / "pi/shared/etc/orc/sensor-upload-ca.pem"
DEFAULT_GRAFANA = os.environ.get(
    "ORC_GRAFANA", "https://openrivercam.endlessprojects.info:9443"
)
DATASOURCE_UID = "timescale"

# Site local time. Both Indonesian sites are WIB (UTC+7); the query asks
# Postgres to do the conversion so we never guess at DST that doesn't exist.
DEFAULT_TZ = "Asia/Jakarta"


def query(sql, grafana, ca_path, timeout=90):
    """Run one raw SQL statement through the Grafana datasource proxy.

    Returns (columns, rows). Grafana frames are column-major; this zips them
    back into rows so callers can think in rows.
    """
    body = json.dumps(
        {
            "queries": [
                {
                    "refId": "A",
                    "datasource": {
                        "uid": DATASOURCE_UID,
                        "type": "grafana-postgresql-datasource",
                    },
                    "format": "table",
                    "rawSql": sql,
                    "rawQuery": True,
                }
            ],
            # Ignored for rawSql, but Grafana rejects the request without them.
            "from": "now-1h",
            "to": "now",
        }
    ).encode()

    ctx = ssl.create_default_context(cafile=str(ca_path))
    req = urllib.request.Request(
        f"{grafana}/api/ds/query",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            payload = json.load(resp)
    except urllib.error.URLError as exc:
        sys.exit(f"error: cannot reach Grafana at {grafana}: {exc}")

    result = payload.get("results", {}).get("A", {})
    if "frames" not in result:
        sys.exit(f"error: query failed: {json.dumps(result)[:400]}")

    frame = result["frames"][0]
    cols = [f["name"] for f in frame["schema"]["fields"]]
    vals = frame["data"]["values"]
    return cols, ([] if not vals else [dict(zip(cols, r)) for r in zip(*vals)])


def fetch_gaps(station, since, tz, grafana, ca_path):
    """Every interval between consecutive distinct sample times, in minutes.

    DISTINCT matters: one wake writes ~5 rows (one per sensor/metric) within a
    second or two of each other. Collapsing to the second turns those into a
    single event, which is what a "boot" means here.
    """
    where = [f"station = '{station}'"]
    if since:
        where.append(f"ts >= '{since}'")
    clause = " AND ".join(where)

    sql = (
        "WITH t AS ("
        f"  SELECT DISTINCT date_trunc('second', ts) AS ts"
        f"  FROM sensor_readings WHERE {clause}"
        "), g AS ("
        "  SELECT ts, lag(ts) OVER (ORDER BY ts) AS prev FROM t"
        ") SELECT "
        f"  to_char(prev AT TIME ZONE '{tz}', 'YYYY-MM-DD HH24:MI') AS from_local, "
        f"  to_char(ts   AT TIME ZONE '{tz}', 'YYYY-MM-DD HH24:MI') AS to_local, "
        "  EXTRACT(epoch FROM (ts - prev)) / 60.0 AS gap_min "
        "FROM g WHERE prev IS NOT NULL ORDER BY prev"
    )
    return query(sql, grafana, ca_path)[1]


def fetch_last_seen(station, tz, grafana, ca_path):
    sql = (
        "SELECT "
        f"  to_char(max(ts) AT TIME ZONE '{tz}', 'YYYY-MM-DD HH24:MI') AS last_local, "
        "  EXTRACT(epoch FROM (now() - max(ts))) / 60.0 AS age_min "
        f"FROM sensor_readings WHERE station = '{station}'"
    )
    rows = query(sql, grafana, ca_path)[1]
    return rows[0] if rows else None


def summarise(gaps, cycle_min, outage_factor, extra_floor_min):
    """Split intervals into outages and extra boots.

    An outage is anything longer than outage_factor whole cycles — generous
    enough that a late wake or a slow shutdown is not mistaken for a failure.
    An extra boot is anything shorter than half a cycle but longer than
    extra_floor_min, which filters the multi-second spread within one wake.
    """
    outage_threshold = cycle_min * outage_factor
    extra_ceiling = cycle_min / 2.0

    outages, extras, normal = [], [], 0
    for row in gaps:
        minutes = float(row["gap_min"])
        if minutes > outage_threshold:
            outages.append({**row, "gap_min": minutes})
        elif extra_floor_min < minutes < extra_ceiling:
            extras.append({**row, "gap_min": minutes})
        else:
            normal += 1
    return outages, extras, normal


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--station", default="sukabumi")
    ap.add_argument("--since", help="ISO date/timestamp lower bound, e.g. 2026-08-20")
    ap.add_argument(
        "--cycle-min",
        type=float,
        default=30.0,
        help="duty cycle in minutes; Sukabumi runs prod_30 (default: 30)",
    )
    ap.add_argument(
        "--outage-factor",
        type=float,
        default=1.5,
        help="an outage is a gap longer than this many cycles (default: 1.5)",
    )
    ap.add_argument(
        "--extra-floor-min",
        type=float,
        default=1.5,
        help="ignore gaps shorter than this; they are one wake's own rows (default: 1.5)",
    )
    ap.add_argument("--tz", default=DEFAULT_TZ, help=f"site local tz (default: {DEFAULT_TZ})")
    ap.add_argument("--grafana", default=DEFAULT_GRAFANA)
    ap.add_argument("--ca", type=Path, default=DEFAULT_CA)
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a report")
    args = ap.parse_args()

    if not args.ca.is_file():
        sys.exit(f"error: CA not found at {args.ca}")

    gaps = fetch_gaps(args.station, args.since, args.tz, args.grafana, args.ca)
    if not gaps:
        sys.exit(f"no sensor rows for station '{args.station}'")

    outages, extras, normal = summarise(
        gaps, args.cycle_min, args.outage_factor, args.extra_floor_min
    )
    last = fetch_last_seen(args.station, args.tz, args.grafana, args.ca)

    down_min = sum(o["gap_min"] for o in outages)
    span_min = sum(float(g["gap_min"]) for g in gaps)

    if args.json:
        json.dump(
            {
                "station": args.station,
                "last_seen_local": last and last["last_local"],
                "last_seen_age_min": last and round(float(last["age_min"]), 1),
                "cycle_min": args.cycle_min,
                "normal_wakes": normal,
                "downtime_min": round(down_min, 1),
                "span_min": round(span_min, 1),
                "outages": outages,
                "extra_boots": extras,
            },
            sys.stdout,
            indent=2,
        )
        print()
        return

    tzname = args.tz.split("/")[-1]
    print(f"station: {args.station}   cycle: {args.cycle_min:g} min   times: {tzname}")
    if last:
        age_h = float(last["age_min"]) / 60.0
        state = "UP" if age_h < (args.cycle_min * args.outage_factor) / 60.0 else "DOWN"
        print(f"last sensor row: {last['last_local']}  ({age_h:.1f} h ago)  -> {state}")

    print(f"\n--- outages (gap > {args.cycle_min * args.outage_factor:g} min) ---")
    if not outages:
        print("  none")
    for o in outages:
        hours = o["gap_min"] / 60.0
        dur = f"{hours:.1f} h" if hours < 48 else f"{hours / 24:.1f} d"
        print(f"  {o['from_local']} -> {o['to_local']}   {dur:>8}")

    if span_min:
        print(
            f"\n  {len(outages)} outages, {down_min / 60 / 24:.1f} d down "
            f"of {span_min / 60 / 24:.1f} d observed  ({down_min / span_min * 100:.0f}%)"
        )

    print(
        f"\n--- extra boots ({args.extra_floor_min:g} < gap < "
        f"{args.cycle_min / 2:g} min — station woke off-schedule) ---"
    )
    if not extras:
        print("  none")
    else:
        by_day = {}
        for e in extras:
            by_day.setdefault(e["to_local"][:10], []).append(e)
        for day in sorted(by_day):
            times = " ".join(x["to_local"][11:] for x in by_day[day][:12])
            more = "" if len(by_day[day]) <= 12 else f" +{len(by_day[day]) - 12} more"
            print(f"  {day}  {len(by_day[day]):>3}  {times}{more}")
        print(
            "\n  A step change here is not self-explaining. Voltage-recovery restarts "
            "and\n  the Witty Pi re-powering inside its own ON window look identical "
            "from\n  timestamps — read the wp5 power-on-reason log on the Pi to tell them "
            "apart."
        )

    print(f"\n  {normal} wakes at the expected cadence.")


if __name__ == "__main__":
    main()
