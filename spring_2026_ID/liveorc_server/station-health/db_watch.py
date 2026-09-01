#!/usr/bin/env python3
"""Emit an event whenever Sukabumi's sensor data advances on the server.

WHY THIS EXISTS ALONGSIDE station_watch.py
    station_watch triggers on tcp/22 over Tailscale, on the stated grounds that
    a fresh sensor row proves the station booted "within the last cycle, not
    that it is powered on now". On 2026-08-28 that cost us the wake: the
    station came up, pushed sensor CSVs to LiveORC over the public internet,
    and was seen by the Tailscale control plane — while tcp/22 never opened and
    the tailnet path carried tx 11232 rx 0. SSH was never going to work, so the
    tcp/22 trigger is not a superset of "the station is alive". It is a
    different, narrower question.

    The upload path and the SSH path fail independently. Watching only the SSH
    path makes a live station look dead.

Read-only: one anonymous Grafana query per poll, same endpoint as station_gaps.
"""
import sys, time
sys.path.insert(0, "/home/tjordan/code/git/openrivercam/spring_2026_ID/liveorc_server/station-health")
import station_gaps as sg
from datetime import datetime, timezone

CA, G = sg.DEFAULT_CA, sg.DEFAULT_GRAFANA
Q = ("SELECT to_char(max(ts) AT TIME ZONE 'Asia/Jakarta','MM-DD HH24:MI:SS') last_wib, "
     "count(*) n FROM sensor_readings WHERE station='sukabumi'")

def now(): return datetime.now(timezone.utc).strftime("%H:%M:%SZ")

# ISS-FIELD-011 changed what this should watch for. While the station was
# unreachable, "data advanced" was the signal. Now that it is cycling again,
# max(ts) advances every 30 minutes and reporting each one is ~48 events a day
# of noise — the first version of this watch was killed for exactly that.
#
# The useful signal is the inverse: data STOPPING. A 4.8-day uplink outage began
# as one missed upload, and nothing anywhere noticed for five days. So alert on
# staleness crossing a threshold, and once more when it clears.
STALE_MIN = 95.0     # three missed cycles on a 30-minute duty cycle
stale = False

last = None
while True:
    try:
        r = sg.query(Q, G, CA)[1][0]
        cur = (r["last_wib"], int(r["n"]))
    except SystemExit as e:
        print(f"[{now()}] QUERY FAILED: {e}", flush=True); time.sleep(120); continue
    except Exception as e:
        print(f"[{now()}] QUERY ERROR: {type(e).__name__} {e}", flush=True); time.sleep(120); continue
    age = None
    try:
        a = sg.query("SELECT EXTRACT(epoch FROM (now()-max(ts)))/60 m FROM sensor_readings "
                     "WHERE station='sukabumi'", G, CA)[1][0]["m"]
        age = float(a)
    except Exception:
        pass

    if last is None:
        print(f"[{now()}] baseline: newest row {cur[0]} WIB, {cur[1]} rows, "
              f"age {age:.0f} min" if age is not None else
              f"[{now()}] baseline: newest row {cur[0]} WIB, {cur[1]} rows", flush=True)
        stale = age is not None and age > STALE_MIN
    elif age is not None:
        if age > STALE_MIN and not stale:
            print(f"[{now()}] *** SENSOR UPLOAD STALLED *** no new row for "
                  f"{age:.0f} min (newest {cur[0]} WIB). This is how the 4.8-day "
                  f"ISS-FIELD-011 outage began.", flush=True)
            stale = True
        elif age <= STALE_MIN and stale:
            d = cur[1] - last[1]
            print(f"[{now()}] *** UPLOADS RESUMED *** newest row {cur[0]} WIB, "
                  f"+{d} rows since the stall began", flush=True)
            stale = False
    last = cur
    time.sleep(60)
