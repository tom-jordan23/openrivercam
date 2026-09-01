#!/usr/bin/env python3
"""TODO-119: which 5-second timeout fired, and how to re-drive the backlog.

STATUS: WRITTEN AND ARMED ON 2026-09-01, NEVER RUN. It was killed before the
21:30 UTC wake when the session ended — nothing may sit waiting on the station
without an active session. Re-arm it as the first station action of the next
session; the two grabs before it landed in 6-9 seconds each, so one wake is
ample.

THE FORK THIS RESOLVES
    orc_api 0.6.0 carries several timeouts and they disagree:

      schemas/base.py:23        sync_remote(..., timeout=5)          <- default
      schemas/video.py:476      sync_remote_wrapper(..., timeout=150)
      schemas/video.py:323      min(retry_timeout, 150) or 150
      schemas/callback_url.py:115,149,252   requests.post/get(..., timeout=5)
                                                                <- hardcoded

    The 08-23..08-27 failures say `read timeout=5`, so a 5 was in force. If it
    was the HARDCODED 5 on the token-refresh POST, the video upload itself was
    never reached and has a generous 150 s — the remedy is a one-line change to
    one call. If instead the 5 reached /api/video/, the upload is running with a
    timeout 30x shorter than the package's own default and the fault lies
    elsewhere. The bare "Read timed out" message carries no URL, so the
    traceback is the only thing that names the call. That is Q10.

THE OTHER HALF: HOW TO RE-DRIVE
    `queue.sync_videos_start_stop()` queries LOCAL, UPDATED and FAILED over a
    start/stop range and syncs with timeout=150. The boot scheduler never calls
    it — `schedulers.py:35` asks only for SyncStatus.QUEUE, which is why it
    reports 0 with 3,101 FAILED rows sitting there. `routers/video.py:548` does
    the same timeout computation, which suggests the re-drive is exposed as an
    HTTP endpoint on the station's own API. If it is, the backlog can be
    re-driven without hand-editing the database, and at 150 s rather than 5.
    That is Q11, and it is the one that decides what the options actually are.

READ-ONLY. sed and grep over site-packages, and one journalctl read. It writes
nothing on the station and starts nothing there.
"""
import subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import station_watch as sw  # noqa: E402

HOST, USER = "orc-sukabumi", "pi"
OUT = HERE.parents[2] / "data" / "station-forensics"

CMD = r"""
SP=$(ls -d /home/pi/venv/orc-os/lib/python3*/site-packages 2>/dev/null | head -1)
A=$SP/orc_api
echo '=== date ==='; date -u

echo '=== Q10: a COMPLETE traceback for a ReadTimeout in the window ==='
journalctl --since '2026-08-24' --until '2026-08-26' --no-pager -o cat 2>/dev/null \
 | grep -A 40 'Read timed out. (read timeout=5)' | head -60

echo '=== Q11: the re-drive endpoint in routers/video.py ==='
grep -n '@router' $A/routers/video.py | tail -20
echo '--- around the timeout computation ---'
sed -n '515,585p' $A/routers/video.py

echo '=== Q12: callback_url post/get/refresh and their timeouts ==='
sed -n '100,185p' $A/schemas/callback_url.py

echo '=== Q13: the live post-capture sync path ==='
sed -n '300,345p' $A/schemas/video.py
echo '--- sync_remote and its wrapper ---'
sed -n '415,500p' $A/schemas/video.py

echo '=== Q14: base.sync_remote, in full ==='
sed -n '15,60p' $A/schemas/base.py
echo '=== END ==='
"""


def log(m):
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%SZ')}] {m}", flush=True)


def main():
    log("waiting for tcp/22 on the next wake (TODO-119 sync source)")
    deadline = time.time() + 3300
    while time.time() < deadline:
        if sw.port_open(HOST, 22, timeout_s=2):
            log("tcp/22 OPEN — grabbing traceback + re-drive endpoint")
            pw = sw.load_password()
            env = sw.askpass_env(pw) if pw else None
            argv = ["ssh", "-o", f"BatchMode={'no' if pw else 'yes'}",
                    "-o", "StrictHostKeyChecking=accept-new",
                    "-o", "ConnectTimeout=5", "-o", "NumberOfPasswordPrompts=1",
                    f"{USER}@{HOST}", CMD]
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            dest = OUT / f"{HOST}-backlog119c-{stamp}.txt"
            # Plain text, not gzip+base64: a cut-off compressed transfer decodes
            # to nothing, while a cut-off plain one keeps its prefix, and the
            # sections are ordered so a short window still lands Q10 and Q11.
            with open(dest, "wb") as fh:
                try:
                    subprocess.run(argv, stdout=fh, stderr=subprocess.STDOUT,
                                   timeout=200, env=env)
                except subprocess.TimeoutExpired:
                    log("ssh timed out — keeping whatever streamed")
            size = dest.stat().st_size if dest.exists() else 0
            log(f"*** GRABBED backlog119c: {size} bytes -> {dest.name} ***")
            return 0 if size > 200 else 1
        time.sleep(1.0)
    log("no wake seen within the window")
    return 1


sys.exit(main())
