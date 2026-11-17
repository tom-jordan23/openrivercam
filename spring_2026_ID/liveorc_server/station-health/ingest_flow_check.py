#!/usr/bin/env python3
"""ingest_flow_check.py — are sensor rows still arriving after a server change?

WHY
    The Grafana lock-down (lockdown-grafana.sh) must not disturb the sensor
    path. The host script proves what it can on the host. This is the part
    only time can show: that the station's NEXT wakes still reach the
    database. Run it from the workstation; it needs no host access and never
    touches the station.

USAGE
    ./ingest_flow_check.py --since 2026-11-18T09:30:00Z
    ./ingest_flow_check.py --since 2026-11-18T09:30:00Z --station sukabumi

Needs the Grafana credentials described in station_gaps.py.

HOW TO READ IT
    The station sleeps between wakes and its rows arrive about one wake late,
    so "no rows yet" within two wake intervals of --since is not a failure.
    The report prints the usual spacing between wakes so that can be judged.
    Exit 0 if every sensor has rows after --since, 2 if some do not, 1 on error.

Read-only.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import station_gaps as sg  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--since", required=True, help="UTC time of the server change, ISO 8601")
    ap.add_argument("--station", default="sukabumi")
    ap.add_argument("--grafana", default=sg.DEFAULT_GRAFANA)
    ap.add_argument("--ca", type=Path, default=sg.DEFAULT_CA)
    a = ap.parse_args()
    if not re.fullmatch(r"[0-9T:\-Z.+]+", a.since):
        sys.exit("error: --since must look like 2026-11-18T09:30:00Z")
    if not re.fullmatch(r"[a-z0-9_-]+", a.station):
        sys.exit("error: bad station name")

    _, rows = sg.query(
        f"""SELECT sensor,
                   max(ts)::text AS newest,
                   count(*) FILTER (WHERE ts >= '{a.since}'::timestamptz) AS since_rows,
                   count(*) FILTER (WHERE ts >= now() - interval '24 hours') AS last_24h
            FROM sensor_readings WHERE station = '{a.station}'
            GROUP BY sensor ORDER BY sensor""",
        a.grafana, a.ca, timeout=60)
    if not rows:
        sys.exit(f"error: no rows at all for station {a.station}")

    _, gaps = sg.query(
        f"""WITH t AS (SELECT DISTINCT ts FROM sensor_readings
                       WHERE station = '{a.station}' AND ts > now() - interval '24 hours')
            SELECT round(extract(epoch FROM percentile_cont(0.5) WITHIN GROUP
                   (ORDER BY gap))/60)::int AS median_min
            FROM (SELECT ts - lag(ts) OVER (ORDER BY ts) AS gap FROM t) g
            WHERE gap > interval '1 minute'""",
        a.grafana, a.ca, timeout=60)
    med = gaps[0]["median_min"] if gaps and gaps[0].get("median_min") is not None else None

    print(f"station {a.station}, since {a.since}")
    print(f"  usual spacing between wakes (last 24 h, median): {med} min" if med else "  usual spacing: unknown")
    print(f"  {'sensor':<12} {'newest row (UTC)':<36} {'rows since':>10} {'last 24h':>9}")
    missing = 0
    for r in rows:
        flag = "" if r["since_rows"] else "   <- none yet"
        missing += 0 if r["since_rows"] else 1
        print(f"  {r['sensor']:<12} {r['newest']:<36} {r['since_rows']:>10} {r['last_24h']:>9}{flag}")
    if missing:
        print(f"\n{missing} sensor(s) have no rows since {a.since}. Judge against the spacing above;"
              " allow two wakes plus the one-wake lag.")
        sys.exit(2)
    print("\nOK: every sensor has rows after the change.")


if __name__ == "__main__":
    main()
