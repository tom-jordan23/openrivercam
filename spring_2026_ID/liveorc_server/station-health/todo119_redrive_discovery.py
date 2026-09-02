#!/usr/bin/env python3
"""TODO-119: find how the re-drive can actually be invoked on the station.

WHY THIS COMES BEFORE THE PROBE
    Tom, 2026-09-02: run the backlog in small bites during the wake cycle,
    driven by a station-side job we own; and check duplicate behaviour before
    anything drives repeatedly. Both need something this session does not have:
    a working way to CALL the re-drive.

    What is known. routers/video.py:530 exposes POST /api/video/sync/ taking
    start/stop/site, on port 80, and GET /api/video/count/ returns 401 - so it
    is live and authenticated, and we do not know by what. Grab 119g then tried
    to import orc_api through two guessed interpreters and got NOT FOUND, so we
    do not know where the code runs either. One of those two has to give.

THE PROBE THIS UNBLOCKS
    Re-drive 20260703T093122.mp4, whose bytes are already on the server
    byte-identical as video id 2437. If the station comes back with remote_id
    2437 the path is idempotent; a new id above 3941 means it duplicates.
    Answerable entirely from the station side, with no server credentials.

    That clip is also one of the 57-of-62 arrived-but-unacknowledged clips
    sitting in ERROR state on the server, so the same probe shows whether a
    re-drive repairs a half-landed record or merely adds another.

READ-ONLY. Locates processes, interpreters and config; reads no video and
sends nothing. It does NOT fire the re-drive - that is the next step, and it is
gated on reading what this returns.
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
echo '=== date ==='; date -u

echo '=== D1: what is serving the API, and as what ==='
ss -ltnp 2>/dev/null | grep -E ':80 |:8000 |:8080 ' | head
echo '--- processes that look like ORC-OS ---'
ps -eo pid,user,args --no-headers 2>/dev/null | grep -iE 'uvicorn|gunicorn|orc|fastapi' | grep -v grep | head -10
echo '--- containers, if any ---'
(docker ps --format '{{.Names}}\t{{.Image}}\t{{.Ports}}' 2>&1 | head -6) || echo 'no docker'

echo '=== D2: where orc_api actually lives ==='
# 119g asked two guessed interpreters and got nothing. Search the filesystem.
find / -xdev -name 'callback_url.py' -path '*orc_api*' 2>/dev/null | head -3
find / -xdev -maxdepth 6 -type d -name 'orc_api' 2>/dev/null | head -3
echo '--- interpreters that can import it ---'
for PY in $(ls /home/pi/.venv*/bin/python3 /opt/*/bin/python3 /usr/bin/python3 2>/dev/null); do
  D=$("$PY" -c "import orc_api,os;print(os.path.dirname(orc_api.__file__))" 2>/dev/null) && echo "  $PY -> $D"
done

echo '=== D3: how the local API authenticates ==='
curl -s -o /dev/null -w 'GET  /api/video/count/  -> %{http_code}\n' --max-time 8 http://127.0.0.1/api/video/count/ 2>&1
curl -s --max-time 8 http://127.0.0.1/openapi.json 2>/dev/null |
  python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except Exception: print('  no openapi.json'); sys.exit()
sec=d.get('components',{}).get('securitySchemes')
print('  securitySchemes:', json.dumps(sec) if sec else 'none declared')
for p in ('/api/video/sync/','/api/token/','/api/login/'):
    if p in d.get('paths',{}): print('  path present:', p, list(d['paths'][p].keys()))
" 2>&1 | head -12
echo '--- local accounts table (names only, NO secrets) ---'
DB=$(ls /home/pi/.ORC-OS/orc-os.db 2>/dev/null | head -1)
sqlite3 "$DB" "select name from sqlite_master where type='table';" 2>&1 | tr '\n' ' '; echo
sqlite3 "$DB" "select group_concat(name,', ') from pragma_table_info('passwords');" 2>&1

echo '=== D4: the wake budget this must fit inside ==='
tail -3 /var/log/wp5d.log 2>/dev/null
echo "uptime: $(cat /proc/uptime | cut -d' ' -f1)s"
echo '=== END ==='
"""


def log(m):
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%SZ')}] {m}", flush=True)


def main():
    log("waiting for tcp/22 (TODO-119 re-drive discovery)")
    deadline = time.time() + 3300
    while time.time() < deadline:
        if sw.port_open(HOST, 22, timeout_s=2):
            log("tcp/22 OPEN — locating the re-drive invocation path")
            pw = sw.load_password()
            env = sw.askpass_env(pw) if pw else None
            argv = ["ssh", "-C", "-o", f"BatchMode={'no' if pw else 'yes'}",
                    "-o", "StrictHostKeyChecking=accept-new",
                    "-o", "ConnectTimeout=5", "-o", "NumberOfPasswordPrompts=1",
                    f"{USER}@{HOST}", CMD]
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            dest = OUT / f"{HOST}-redrivediscovery119h-{stamp}.txt"
            with open(dest, "wb") as fh:
                try:
                    subprocess.run(argv, stdout=fh, stderr=subprocess.STDOUT,
                                   timeout=220, env=env)
                except subprocess.TimeoutExpired:
                    log("ssh timed out — keeping whatever streamed")
            size = dest.stat().st_size if dest.exists() else 0
            log(f"*** GRABBED redrivediscovery119h: {size} bytes -> {dest.name} ***")
            return 0 if size > 200 else 1
        time.sleep(1.0)
    log("no wake seen within the window")
    return 1


sys.exit(main())
