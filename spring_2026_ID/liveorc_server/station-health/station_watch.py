#!/usr/bin/env python3
"""station_watch.py — wait for Sukabumi to come back, then grab its power state.

WHY
    ISS-FIELD-008 / TODO-116. The station is down, and every theory about why
    is decided by state that exists only on the Witty Pi: the power-on reason,
    the alarm time, the two voltage thresholds, the undervolt bits. None of it
    is uploaded. To read it, someone has to be logged in while the station is
    awake — and in production it is awake about two minutes in every thirty.

    A person cannot win that race; they would have to sit on a terminal for
    however many days it takes. A poller can. This watches for the station to
    reappear and runs the collector within seconds, unattended.

    It is written for the case where the station comes back **on its own**,
    which is the open question — every recovery so far landed in Indonesian
    business hours, which is what a person pressing the button looks like, not
    a voltage threshold. If it never fires, that is itself the answer.

WHAT IT TOUCHES
    Locally: a state file and an output directory. Remotely: one SSH session
    that runs a read-only collector. It changes nothing on the station — not
    the schedule, not the thresholds, not a service. See orc_wp5_state.sh.

    The Grafana query is anonymous and read-only (see station_gaps.py).

USAGE
    ./station_watch.py                      # poll until it comes back
    ./station_watch.py --once               # single check, for cron/systemd
    ./station_watch.py --dry-run            # report state, never SSH

    Leave it running in a terminal, or install the systemd user unit in
    station-watch.service.

WHY TWO SIGNALS
    Tailscale sees the station join the tailnet within seconds of boot, but
    only while this machine is on the same tailnet and the node is not
    expired. The sensor row is authoritative and independent of the local
    machine but lags by however long the upload takes. Either one firing is
    enough; requiring both would lose the race we are trying to win.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
COLLECTOR = REPO_ROOT / "pi/tools/orc_wp5_state.sh"
FULL_BUNDLE = REPO_ROOT / "pi/tools/orc_collect.sh"

DEFAULT_HOST = "orc-sukabumi"
DEFAULT_USER = "pi"
DEFAULT_STATE = Path.home() / ".cache/orc-station-watch.json"
DEFAULT_OUT = REPO_ROOT.parent / "data/station-forensics"

sys.path.insert(0, str(HERE))
import station_gaps as sg  # noqa: E402


def tailscale_online(host):
    """True if the node is on the tailnet right now.

    Absence is not evidence of a down station — this machine may be off the
    tailnet itself — so a False here only ever defers to the sensor signal.
    """
    try:
        out = subprocess.run(
            ["tailscale", "status", "--json"], capture_output=True, text=True, timeout=15
        )
        if out.returncode != 0:
            return None
        peers = json.loads(out.stdout).get("Peer", {}) or {}
        for p in peers.values():
            names = [p.get("HostName", ""), p.get("DNSName", "").split(".")[0]]
            if host in names:
                return bool(p.get("Online"))
        return None
    except Exception:
        return None


def sensor_age_minutes(station):
    """Minutes since the last sensor row, or None if unreachable."""
    sql = (
        "SELECT EXTRACT(epoch FROM (now() - max(ts))) / 60.0 AS age_min "
        f"FROM sensor_readings WHERE station = '{station}'"
    )
    try:
        rows = sg.query(sql, sg.DEFAULT_GRAFANA, sg.DEFAULT_CA, timeout=30)[1]
    except SystemExit:
        return None
    if not rows or rows[0]["age_min"] is None:
        return None
    return float(rows[0]["age_min"])


def collect(user, host, outdir, full=False):
    """Run the read-only collectors over SSH, newest-value-first.

    orc_wp5_state.sh is ordered so that a truncated run still yields the
    decisive parts. The full bundle is attempted second and is allowed to fail:
    losing it costs nothing that the first grab did not already secure.
    """
    outdir.mkdir(parents=True, exist_ok=True)
    ok = False
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    results = []

    jobs = [("wp5-state", COLLECTOR)]
    if full:
        jobs.append(("collect", FULL_BUNDLE))

    for name, script in jobs:
        if not script.is_file():
            results.append(f"{name}: MISSING {script}")
            continue
        dest = outdir / f"{host}-{name}-{stamp}.txt"
        cmd = [
            "ssh",
            "-o", "BatchMode=yes",
            "-o", "StrictHostKeyChecking=accept-new",
            "-o", "ConnectTimeout=10",
            f"{user}@{host}",
            "sudo bash -s",
        ]
        try:
            with open(script, "rb") as fh, open(dest, "wb") as out:
                p = subprocess.run(cmd, stdin=fh, stdout=out,
                                   stderr=subprocess.STDOUT, timeout=150)
            size = dest.stat().st_size
            results.append(f"{name}: rc={p.returncode} {size}B -> {dest}")
            if name == "wp5-state" and p.returncode == 0 and size > 2000:
                ok = True
        except subprocess.TimeoutExpired:
            results.append(f"{name}: TIMEOUT (partial output kept) -> {dest}")
        except Exception as exc:
            results.append(f"{name}: FAILED {exc}")
    return results, ok


def load_state(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def save_state(path, state):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2))


def check(args):
    """One evaluation. Returns (is_up, human_readable_reason)."""
    ts_online = tailscale_online(args.host)
    age = sensor_age_minutes(args.station)

    reasons = []
    reasons.append(
        "tailscale=" + {True: "ONLINE", False: "offline", None: "unknown"}[ts_online]
    )
    reasons.append("sensor_age=" + ("unknown" if age is None else f"{age:.0f}m"))

    fresh = age is not None and age <= args.fresh_min
    # Tailscale is the only real-time signal. A fresh sensor row means the
    # station was alive within the cycle, NOT that it is powered on now — it is
    # awake ~2 min in 30. Falling back to freshness when Tailscale cannot see
    # the node at all keeps this useful off-tailnet, but never overrides it.
    up = fresh if ts_online is None else ts_online
    return up, ", ".join(reasons)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--station", default="sukabumi")
    ap.add_argument("--host", default=DEFAULT_HOST, help="Tailscale name to SSH to")
    ap.add_argument("--user", default=DEFAULT_USER)
    ap.add_argument("--interval", type=int, default=60, help="seconds between polls")
    ap.add_argument(
        "--fresh-min",
        type=float,
        default=35.0,
        help="a sensor row newer than this many minutes means the station is up "
             "(default 35: one 30-minute cycle plus slack)",
    )
    ap.add_argument("--once", action="store_true", help="check once and exit")
    ap.add_argument("--dry-run", action="store_true", help="never SSH; just report")
    ap.add_argument("--full", action="store_true",
                    help="also run the slower orc_collect.sh bundle")
    ap.add_argument("--state", type=Path, default=DEFAULT_STATE)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    state = load_state(args.state)
    was_up = state.get("up", False)
    already = state.get("collected_for_boot", False)

    while True:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
        up, why = check(args)

        if up and not was_up:
            print(f"[{now}] *** STATION IS BACK *** ({why})", flush=True)
            already = False
        elif not up and was_up:
            print(f"[{now}] station went down ({why})", flush=True)
        else:
            print(f"[{now}] {'up' if up else 'down'} ({why})", flush=True)

        if up and not already:
            if args.dry_run:
                print("  --dry-run: would collect now", flush=True)
            else:
                print("  collecting...", flush=True)
                lines, ok = collect(args.user, args.host, args.out, args.full)
                for line in lines:
                    print("  " + line, flush=True)
                # Only a real grab ends the hunt. A refused or timed-out SSH
                # means we lost this window, not that the job is done.
                already = ok
                if not ok:
                    print("  grab failed — will retry on the next wake", flush=True)

        was_up = up
        state.update({"up": up, "collected_for_boot": already, "last_check": now})
        save_state(args.state, state)

        if args.once:
            return 0 if up else 1
        time.sleep(args.interval)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nstopped.")
