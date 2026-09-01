#!/usr/bin/env python3
"""TODO-119: is the re-drive actually usable, and is the token-refresh fault general?

WHAT THE 21:30 UTC GRAB SETTLED (backlog119c)
    Q10: the 5 that fired is the HARDCODED one. The traceback's innermost
    orc_api frame is callback_url.py:115 in get_set_refresh_tokens, which is
    `requests.post(url, data=data, timeout=5)` against /api/token/refresh/.
    The urllib3 frames above it end in do_handshake — it died in the TLS
    handshake, before any HTTP request was sent. No video bytes moved.

    Q11: yes. routers/video.py:530 exposes POST /api/video/sync/ taking
    start/stop/site, calling queue.sync_videos_start_stop.

WHY THAT IS NOT YET AN ANSWER
    Two things in the code make the re-drive's value conditional, and both are
    one cheap read away:

    1. routers/video.py:548 computes `timeout = min(url.retry_timeout, 150) if
       url.retry_timeout else 150`. If retry_timeout in the callback_url row is
       5, the re-drive runs at 5 s and is worth nothing. The 150 is a ceiling,
       not a floor. NOBODY HAS READ THAT VALUE.

    2. Worse, and structural: callback_url.post/get/patch each begin with
       `if self.token_expiration < datetime.now(): self.get_set_refresh_tokens()`
       and that refresh is hardcoded to 5 s — it does NOT take the caller's
       timeout. So a re-drive at 150 s still passes through a 5 s refresh at the
       front of every request whose token has expired. If the handshake is what
       stalls, the re-drive fails in exactly the same place.

    And the 08-24 04:02:58 sample is ONE traceback, taken at the drifting
    04:01-05:03 edge where the nightly success band ends. It may be the
    transition, not the rule. Counting the window decides that.

READ-ONLY. sqlite reads, grep/journalctl counts, and a listening-port check.
It writes nothing on the station and starts nothing there.
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
DB=$(ls /home/pi/.ORC-OS/orc-os.db 2>/dev/null | head -1)
echo '=== date ==='; date -u

echo '=== Q15: retry_timeout and token_expiration (decides if the re-drive is worth firing) ==='
if [ -n "$DB" ]; then
  sqlite3 -header -column "$DB" \
    "select id, substr(url,1,45) url, remote_site_id, retry_timeout, token_expiration from callback_url;" 2>&1
else
  echo "NO DB FOUND at /home/pi/.ORC-OS/orc-os.db"; ls -la /home/pi/.ORC-OS/ 2>&1 | head
fi

echo '=== Q16: is the token-refresh frame the rule or the exception, 08-23..08-28 ==='
L=$(journalctl --since '2026-08-23' --until '2026-08-28' --no-pager -o cat 2>/dev/null)
echo "ReadTimeout errors logged : $(printf '%s' "$L" | grep -c 'Read timed out')"
echo "  ...at get_set_refresh_tokens: $(printf '%s' "$L" | grep -c 'in get_set_refresh_tokens')"
echo "  ...at do_handshake          : $(printf '%s' "$L" | grep -c 'in do_handshake')"
echo "ConnectTimeout errors      : $(printf '%s' "$L" | grep -c 'ConnectTimeout')"
echo '--- innermost orc_api frame of every traceback in the window, tallied ---'
printf '%s' "$L" | grep -oE 'orc_api/schemas/[a-z_]+\.py", line [0-9]+, in [a-z_]+' | sort | uniq -c | sort -rn | head -15

echo '=== Q17: is the station API listening, and where ==='
ss -ltnp 2>/dev/null | head -20
echo '--- orc-os services ---'
systemctl list-units --type=service --no-pager 2>/dev/null | grep -i orc | head

echo '=== Q18: sync status tally right now ==='
if [ -n "$DB" ]; then
  sqlite3 -header -column "$DB" "select sync_status, count(*) n from video group by 1 order by 2 desc;" 2>&1
fi
echo '=== END ==='
"""


def log(m):
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%SZ')}] {m}", flush=True)


def main():
    log("waiting for tcp/22 on the next wake (TODO-119 re-drive viability)")
    deadline = time.time() + 3300
    while time.time() < deadline:
        if sw.port_open(HOST, 22, timeout_s=2):
            log("tcp/22 OPEN — reading retry_timeout, tallying the window")
            pw = sw.load_password()
            env = sw.askpass_env(pw) if pw else None
            argv = ["ssh", "-o", f"BatchMode={'no' if pw else 'yes'}",
                    "-o", "StrictHostKeyChecking=accept-new",
                    "-o", "ConnectTimeout=5", "-o", "NumberOfPasswordPrompts=1",
                    f"{USER}@{HOST}", CMD]
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            dest = OUT / f"{HOST}-redrive119d-{stamp}.txt"
            with open(dest, "wb") as fh:
                try:
                    subprocess.run(argv, stdout=fh, stderr=subprocess.STDOUT,
                                   timeout=200, env=env)
                except subprocess.TimeoutExpired:
                    log("ssh timed out — keeping whatever streamed")
            size = dest.stat().st_size if dest.exists() else 0
            log(f"*** GRABBED redrive119d: {size} bytes -> {dest.name} ***")
            return 0 if size > 200 else 1
        time.sleep(1.0)
    log("no wake seen within the window")
    return 1


sys.exit(main())
