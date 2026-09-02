#!/usr/bin/env python3
"""TODO-119: run one prepared script inside a single station wake.

WHY A RUNNER RATHER THAN ANOTHER BESPOKE GRAB
    The plan Tom approved on 2026-09-02 has several station-side steps, each of
    which has to fit inside a ~2 minute wake: verify the reclaim list, fire the
    idempotency probe, read its result, then drive the backlog in bites. Writing
    a fresh pounce script per step duplicates the wake-catching logic and gets
    the timeout wrong eventually. This takes the script as an argument.

    The script is fed over stdin as `bash -s`, so it can carry its own data -
    the 1,403-entry reclaim list travels with it, under ssh -C.

SAFETY
    This runner will happily run whatever it is handed, so the caution lives in
    the scripts, not here. The wake-1 script re-measures every reclaim candidate
    on the station's own disk before anything could be removed, and deletes
    nothing; the reclaim list is treated as a claim to be tested, not an
    instruction to obey.

USAGE
    todo119_wake_runner.py <script.sh> <label> [--timeout SEC]
"""
import argparse, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import station_watch as sw  # noqa: E402

HOST, USER = "orc-sukabumi", "pi"
OUT = HERE.parents[2] / "data" / "station-forensics"


def log(m):
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%SZ')}] {m}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script"); ap.add_argument("label")
    ap.add_argument("--timeout", type=int, default=220)
    ap.add_argument("--wait", type=int, default=3300)
    a = ap.parse_args()
    body = Path(a.script).read_bytes()
    log(f"waiting for tcp/22 — {a.label} ({len(body)/1024:.1f} KB script)")
    deadline = time.time() + a.wait
    while time.time() < deadline:
        if sw.port_open(HOST, 22, timeout_s=2):
            log("tcp/22 OPEN — running")
            pw = sw.load_password()
            env = sw.askpass_env(pw) if pw else None
            argv = ["ssh", "-C", "-o", f"BatchMode={'no' if pw else 'yes'}",
                    "-o", "StrictHostKeyChecking=accept-new",
                    "-o", "ConnectTimeout=5", "-o", "NumberOfPasswordPrompts=1",
                    f"{USER}@{HOST}", "bash -s"]
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            dest = OUT / f"{HOST}-{a.label}-{stamp}.txt"
            with open(dest, "wb") as fh:
                try:
                    subprocess.run(argv, input=body, stdout=fh,
                                   stderr=subprocess.STDOUT, timeout=a.timeout, env=env)
                except subprocess.TimeoutExpired:
                    log("ssh timed out — keeping whatever streamed")
            size = dest.stat().st_size if dest.exists() else 0
            log(f"*** {a.label}: {size} bytes -> {dest.name} ***")
            return 0 if size > 200 else 1
        time.sleep(1.0)
    log("no wake seen within the window")
    return 1


sys.exit(main())
