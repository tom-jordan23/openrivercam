#!/usr/bin/env python3
"""Generate synthetic sensor CSVs for local sheets-export testing.

Writes files in exactly the shape a real station produces, so seeding a local
dev stack exercises the REAL ingest path (sensor-ingest's filename regex, CSV
parser, and upsert) rather than hand-inserting rows into the database.

Filenames and headers match pi/shared/etc/orc-sensors/*.conf:

    sht40_<date>.csv     timestamp,temp_c,humidity_pct
    ds18b20_<date>.csv   timestamp,temp_c
    rg15_<date>.csv      timestamp,totalacc_mm,interval_mm

Readings are emitted at INTERVAL_SEC=300 (288 rows/day), matching the
deployed stations.

Values are deterministic for a given (sensor, date) — a smooth diurnal curve
plus a fixed per-date offset, no RNG. Re-running the same command produces a
byte-identical file, so a re-seed can never look like new data.

This is a dev tool. It is never deployed to a station or to the server.

Usage:
    # one day of one sensor
    python3 seed_synthetic.py --sensor sht40 --date 2026-08-05 \
        --out devdata/sensors/sukabumi

    # every sensor, a range of days (inclusive)
    python3 seed_synthetic.py --sensor all --date 2026-08-01:2026-08-07 \
        --out devdata/sensors/sukabumi

    # inject a non-finite value to test the exporter's isfinite guard
    python3 seed_synthetic.py --sensor ds18b20 --date 2026-08-05 \
        --out devdata/sensors/sukabumi --inject-nan
"""
import argparse
import math
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

INTERVAL_SEC = 300

# header (minus the leading timestamp column) per sensor, from the station confs
SENSORS = {
    "sht40": ["temp_c", "humidity_pct"],
    "ds18b20": ["temp_c"],
    "rg15": ["totalacc_mm", "interval_mm"],
}


def _diurnal(frac_of_day: float, mean: float, amplitude: float) -> float:
    """Smooth daily cycle peaking mid-afternoon (frac 0.6)."""
    return mean + amplitude * math.sin(2 * math.pi * (frac_of_day - 0.35))


def build_rows(sensor: str, day: datetime, inject_nan: bool) -> list[list[str]]:
    """Deterministic readings for one sensor-day, oldest first."""
    # Fixed per-date offset so consecutive days differ but never randomly.
    day_offset = (day.toordinal() % 7) * 0.5
    rows = []
    total_acc = 0.0
    steps = 86400 // INTERVAL_SEC

    for i in range(steps):
        ts = day + timedelta(seconds=i * INTERVAL_SEC)
        frac = i / steps

        if sensor == "sht40":
            values = [
                f"{_diurnal(frac, 28.0 + day_offset, 4.0):.2f}",
                f"{_diurnal(frac, 72.0 - day_offset, -12.0):.2f}",
            ]
        elif sensor == "ds18b20":
            values = [f"{_diurnal(frac, 24.5 + day_offset, 3.0):.2f}"]
        elif sensor == "rg15":
            # A rain burst in the afternoon, mimicking a tropical pattern.
            interval = 0.2 if 0.55 < frac < 0.70 and i % 3 == 0 else 0.0
            total_acc += interval
            values = [f"{total_acc:.2f}", f"{interval:.2f}"]
        else:
            raise ValueError(f"unknown sensor {sensor}")

        rows.append([ts.strftime("%Y-%m-%dT%H:%M:%SZ")] + values)

    if inject_nan:
        # sensor-ingest does a bare float(), which happily accepts "nan".
        # The exporter must survive this rather than wedging on invalid JSON.
        rows[0][1] = "nan"

    return rows


def parse_dates(spec: str) -> list[datetime]:
    """'2026-08-05' or '2026-08-01:2026-08-07' (inclusive)."""
    if ":" in spec:
        start_s, end_s = spec.split(":", 1)
    else:
        start_s = end_s = spec
    start = datetime.strptime(start_s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    end = datetime.strptime(end_s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    if end < start:
        raise ValueError(f"end date {end_s} precedes start date {start_s}")
    days = []
    while start <= end:
        days.append(start)
        start += timedelta(days=1)
    return days


def main():
    ap = argparse.ArgumentParser(
        description="Dev tool: write synthetic station sensor CSVs for local testing."
    )
    ap.add_argument("--sensor", required=True,
                    choices=sorted(SENSORS) + ["all"],
                    help="sensor to generate, or 'all'")
    ap.add_argument("--date", required=True,
                    help="YYYY-MM-DD, or YYYY-MM-DD:YYYY-MM-DD for an inclusive range")
    ap.add_argument("--out", required=True, type=Path,
                    help="station directory, e.g. devdata/sensors/sukabumi")
    ap.add_argument("--inject-nan", action="store_true",
                    help="set the first reading to 'nan' to exercise the exporter's guard")
    args = ap.parse_args()

    try:
        days = parse_dates(args.date)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    sensors = sorted(SENSORS) if args.sensor == "all" else [args.sensor]
    args.out.mkdir(parents=True, exist_ok=True)

    written = 0
    for sensor in sensors:
        for day in days:
            rows = build_rows(sensor, day, args.inject_nan)
            path = args.out / f"{sensor}_{day.strftime('%Y-%m-%d')}.csv"
            with path.open("w", newline="") as fp:
                fp.write("timestamp," + ",".join(SENSORS[sensor]) + "\n")
                for row in rows:
                    fp.write(",".join(row) + "\n")
            print(f"wrote {path} ({len(rows)} rows)")
            written += len(rows)

    metrics = sum(len(SENSORS[s]) for s in sensors)
    print(f"\ntotal: {written} readings across {len(sensors)} sensor(s) x "
          f"{len(days)} day(s) = {written * metrics // len(sensors) if sensors else 0} "
          f"expected sensor_readings rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
