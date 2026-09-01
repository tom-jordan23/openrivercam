#!/usr/bin/env python3
"""wp5d_duty_cycle.py — measure the station's duty cycle from the Witty Pi log.

WHY THIS EXISTS
    ISS-FIELD-011 first concluded the station had been awake ~15 h/day at ~9x
    its energy budget during the 2026-08-28 outage. That came from wake-minutes
    INFERRED from the spacing of sensor rows on the server. It was wrong by an
    order of magnitude.

    /var/log/wp5d.log is the Witty Pi's own record of when it powered the Pi,
    so it measures the duty cycle directly rather than inferring it.

READING THE LOG CORRECTLY — two traps, both of which produced clean-looking
but entirely false tables before being caught:

    1. The daemon's "Witty Pi 5 daemon V5.0.0 started" line is written BEFORE
       the RTC is read back, so it carries a stale clock (2026-03-26 on this
       station). Anchoring a cycle on it yields durations in the tens of
       thousands of minutes. Anchor on "Startup reason", which is logged after
       "RTC has valid time, write RTC time into system...".

    2. A cycle ends at "Exit now.". If you instead take the last timestamped
       line before the next boot, you pick up the NEXT boot's post-RTC-sync
       lines and every cycle measures exactly the wake interval (30.0 min),
       healthy days included.

    The file also contains NUL bytes from unclean shutdowns, so it must be read
    as binary and stripped, not opened as text.

Read-only. Operates on a local copy of the log; touches nothing on the station.
"""
import re
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta

TS = re.compile(r"^\[(2026-\d\d-\d\d \d\d:\d\d:\d\d)\]")
MAX_CYCLE = timedelta(minutes=40)   # anything longer is a parse artefact


def cycles(path):
    """Yield (start_datetime, awake_minutes) for every complete boot cycle."""
    raw = open(path, "rb").read().replace(b"\x00", b"")
    start = None
    for line in raw.decode("utf-8", "replace").splitlines():
        m = TS.match(line)
        if not m:
            continue
        t = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
        if "Startup reason" in line:
            start = t
        elif "Exit now." in line and start and timedelta(0) <= t - start <= MAX_CYCLE:
            yield start, (t - start).total_seconds() / 60.0
            start = None


def main(path):
    per = defaultdict(list)
    for start, mins in cycles(path):
        per[start.date().isoformat()].append(mins)

    print("day,cycles,median_wake_min,max_wake_min,awake_min_per_day")
    for day in sorted(per):
        v = sorted(per[day])
        print(f"{day},{len(v)},{statistics.median(v):.2f},{v[-1]:.2f},{sum(v):.1f}")

    allv = [x for d in per for x in per[d]]
    print(f"# {len(allv)} cycles over {len(per)} days; "
          f"median {statistics.median(allv):.2f} min, max {max(allv):.1f} min; "
          f"{sum(1 for x in allv if x > 20)} cycles over 20 min", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"usage: {sys.argv[0]} <wp5d.log>")
    main(sys.argv[1])
