#!/usr/bin/env python3
"""TODO-119: split the 416 ReadTimeouts by their timeout VALUE, and fix the clock question.

WHAT redrive119d SETTLED
    retry_timeout = 0.0. In `min(retry_timeout,150) if retry_timeout else 150`
    0.0 is FALSY, so both the live capture path (video.py) and the re-drive
    (routers/video.py:548) resolve to 150, not 5. The upload already had 150 s.

    And the window does NOT reduce to token refresh. Innermost frames across
    08-23..08-28: 139 at callback_url.py:115 get_set_refresh_tokens (the
    hardcoded 5), but 78 at callback_url.py:172 -- the real data POST, which
    carries the caller's 150. Both paths fail. 253 of the stalls are at
    do_handshake, more than the 139 refreshes, so the handshake hangs on the
    data path too.

WHAT THAT LEAVES AMBIGUOUS, AND WHY IT DECIDES THE REMEDY
    Q16 counted 'Read timed out' without reading the number after it. If the 78
    data-POST failures logged `read timeout=150`, then the handshake was hanging
    longer than 150 s and raising the hardcoded 5 fixes 139 failures out of 217
    -- useful but not sufficient. If they logged `read timeout=5` instead, then
    something is overriding the 150 and the whole diagnosis moves. The number is
    printed on every line; nobody has tallied it.

    Separately: token_expiration reads 2026-09-01 23:02:08, and the comparison
    `self.token_expiration < datetime.now()` is naive local time. Whether that
    timestamp is an hour ahead or six hours stale depends on the station's
    timezone, which we have never recorded -- only `date -u`. If it is stale,
    every request pays the hardcoded 5 s refresh first.

READ-ONLY. Log counts, `date`, and one GET against the station's own API.
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
echo '=== date: local, UTC, and the zone (decides the token_expiration reading) ==='
date; date -u; timedatectl 2>/dev/null | head -6

echo '=== Q19: every "read timeout=N" in 08-23..08-28, tallied by N ==='
L=$(journalctl --since '2026-08-23' --until '2026-08-28' --no-pager -o cat 2>/dev/null)
printf '%s' "$L" | grep -oE 'read timeout=[0-9.]+' | sort | uniq -c | sort -rn

echo '--- and the same for the ERROR summary lines only (one per failed sync) ---'
printf '%s' "$L" | grep 'Error syncing video to remote site' \
 | grep -oE 'read timeout=[0-9.]+|ConnectTimeout|RemoteDisconnected|ConnectionReset|SSLError' \
 | sort | uniq -c | sort -rn

echo '=== Q20: token_expiration vs the naive now() the code compares against ==='
python3 - <<'PY' 2>&1
from datetime import datetime
print("naive datetime.now() on this box:", datetime.now())
PY

echo '=== Q21: is POST /api/video/sync/ actually served here (GET probe only) ==='
for u in http://localhost/api/video/count/ http://localhost:8000/api/video/count/; do
  echo -n "$u -> "
  curl -s -o /dev/null -w '%{http_code}\n' --max-time 5 "$u" 2>&1 || echo curl-failed
done
echo '--- what serves :80 ---'
ss -ltnp 2>/dev/null | grep ':80 ' | head -3
echo '=== END ==='
"""


def log(m):
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%SZ')}] {m}", flush=True)


def main():
    log("waiting for tcp/22 on the next wake (TODO-119 timeout split)")
    deadline = time.time() + 3300
    while time.time() < deadline:
        if sw.port_open(HOST, 22, timeout_s=2):
            log("tcp/22 OPEN — tallying read timeout values, reading the clock")
            pw = sw.load_password()
            env = sw.askpass_env(pw) if pw else None
            argv = ["ssh", "-o", f"BatchMode={'no' if pw else 'yes'}",
                    "-o", "StrictHostKeyChecking=accept-new",
                    "-o", "ConnectTimeout=5", "-o", "NumberOfPasswordPrompts=1",
                    f"{USER}@{HOST}", CMD]
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            dest = OUT / f"{HOST}-timeoutsplit119e-{stamp}.txt"
            with open(dest, "wb") as fh:
                try:
                    subprocess.run(argv, stdout=fh, stderr=subprocess.STDOUT,
                                   timeout=200, env=env)
                except subprocess.TimeoutExpired:
                    log("ssh timed out — keeping whatever streamed")
            size = dest.stat().st_size if dest.exists() else 0
            log(f"*** GRABBED timeoutsplit119e: {size} bytes -> {dest.name} ***")
            return 0 if size > 200 else 1
        time.sleep(1.0)
    log("no wake seen within the window")
    return 1


sys.exit(main())
