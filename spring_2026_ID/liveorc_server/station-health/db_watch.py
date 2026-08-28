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

last = None
while True:
    try:
        r = sg.query(Q, G, CA)[1][0]
        cur = (r["last_wib"], int(r["n"]))
    except SystemExit as e:
        print(f"[{now()}] QUERY FAILED: {e}", flush=True); time.sleep(120); continue
    except Exception as e:
        print(f"[{now()}] QUERY ERROR: {type(e).__name__} {e}", flush=True); time.sleep(120); continue
    if last is None:
        print(f"[{now()}] baseline: newest row {cur[0]} WIB, {cur[1]} rows total", flush=True)
    elif cur != last:
        d = cur[1] - last[1]
        print(f"[{now()}] *** NEW SENSOR DATA *** newest row now {cur[0]} WIB "
              f"(was {last[0]}), +{d} rows — THE STATION IS AWAKE OR JUST WAS", flush=True)
    last = cur
    time.sleep(60)
