# ############################################################################
# TODO-119 trickle: queue ONE bounded window of backlog clips via the ORC-OS
# local API, so the station drains it on its own over following wakes.
#
# DEFAULT IS A DRY RUN. It calls nothing that changes state unless
# ORC_COMMIT=yes is injected, and it refuses to run at all without an explicit
# window. Firing it needs Tom's approval for that specific window
# (see TODO.md "Standing cautions").
#
# This does NOT write to the database directly. It calls
# POST /api/video/sync/, which is the path Tom chose on 2026-09-03 over a
# sync_status flip. That endpoint does write sync_status=QUEUE through the
# app's own code (queue.py:192) — that is the mechanism, not a side effect.
# ############################################################################
#
# HOW THE TRICKLE ACTUALLY WORKS
#   POST /api/video/sync/ selects LOCAL + UPDATED + FAILED rows in a time
#   window, flips them to QUEUE, and hands them to Celery. It does not upload
#   anything itself. Then, on EVERY subsequent boot,
#   startup_checks.check_and_restore_queued_syncs() finds every QUEUE row and
#   re-submits it. So one call sets up work that the station performs on its own
#   duty cycle, ~48 wakes a day, with nothing of ours running in between.
#
#   That is the whole trickle. No deploy, no station-side timer, no agent.
#
# THE CONTROL VARIABLE IS QUEUE DEPTH, AND THERE IS NO THROTTLE
#   check_and_restore_queued_syncs submits ALL queued rows every boot. Nothing
#   rate-limits it. Queue depth is the only regulator, so the size of the window
#   is the size of the commitment. `start` and `stop` are Optional[datetime] =
#   None upstream, defaulting to "beginning of records" -> "end of records": an
#   empty body would queue every un-synced row on the station. This script
#   therefore treats a missing bound as a fatal error, never as "all".
#
# DUPLICATES
#   The window is chosen by TIME, so it re-sends anything FAILED in range —
#   including the 92 clips the server already holds (LiveORC 500: row and bytes
#   committed, acknowledgement lost). Re-sending those makes duplicate server
#   rows, because nothing upstream constrains `timestamp`.
#
#   Use windows drawn from the 21 clean days in
#   findings/sukabumi_backlog_tsjoin_2026-09-16.csv — days whose only un-synced
#   clips are UPLOAD. 968 of the 1,171 clips (9.33 GB) sit on those days.
#   todo119_trickle_drive.py picks them; this script re-checks the count but
#   cannot re-derive cleanliness on its own, so do not hand it an arbitrary range.
#
# EXPECTED COST OF INTERRUPTION
#   A wake that ends mid-transfer leaves rows QUEUE and the next boot finishes
#   them, no re-flip needed, at a price of about one duplicated clip per
#   interruption (harness, orc_os_backlog_sync_starvation.md §7). That is the
#   known, bounded cost of the self-healing behaviour.
#
# INJECTED AT ARMING TIME, never committed:
#   ORC_PW            ORC-OS local password (from sukabumi_bringup/.env)
#   ORC_START         window start, 'YYYY-MM-DD HH:MM:SS' UTC   (MANDATORY)
#   ORC_STOP          window stop,  'YYYY-MM-DD HH:MM:SS' UTC   (MANDATORY)
#   ORC_MAX_CLIPS     refuse if the window holds more than this (default 60)
#   ORC_COMMIT        exactly "yes" to actually POST. Anything else = dry run.
#
# stdin is NOT the carrier: the wake runner pipes this whole script over stdin
# as `bash -s`, so a `read` here would consume the script. This file stays
# credential-free and is safe to commit as-is.

set -u
DB=/home/pi/.ORC-OS/orc-os.db
API=http://127.0.0.1:5000     # direct to uvicorn; nginx on :80 has
                              # proxy_read_timeout 30s and would cut the re-drive
CJ=$(mktemp /dev/shm/orc_cj.XXXXXX)   # tmpfs, never touches the SD card
trap 'rm -f "$CJ"' EXIT INT TERM

echo "=== TRICKLE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

PW="${ORC_PW:-}"; unset ORC_PW
START="${ORC_START:-}"
STOP="${ORC_STOP:-}"
MAXC="${ORC_MAX_CLIPS:-60}"
COMMIT="${ORC_COMMIT:-no}"

echo
echo "=== 0. GUARDS ==="
[ -n "$PW" ] || { echo "  ABORT: no password injected. Nothing sent."; exit 1; }
echo "  password injected at arming (len ${#PW}), not echoed"

# The footgun guard. A missing bound upstream means "all records", so refuse it.
if [ -z "$START" ] || [ -z "$STOP" ]; then
  echo "  ABORT: ORC_START and ORC_STOP are both mandatory."
  echo "         Upstream treats a missing bound as unbounded, which would queue"
  echo "         every un-synced row on the station. Refusing. Nothing sent."
  exit 2
fi
for v in "$START" "$STOP"; do
  date -u -d "$v" >/dev/null 2>&1 || { echo "  ABORT: unparseable bound '$v'."; exit 2; }
done
S_EPOCH=$(date -u -d "$START" +%s); T_EPOCH=$(date -u -d "$STOP" +%s)
SPAN=$(( T_EPOCH - S_EPOCH ))
echo "  window: $START -> $STOP  (${SPAN}s)"
if [ "$SPAN" -le 0 ]; then echo "  ABORT: stop is not after start."; exit 2; fi
# 36 h ceiling: a clean day is 24 h, so this allows one day plus slack and
# still refuses a typo that widens the window to a month.
if [ "$SPAN" -gt 129600 ]; then
  echo "  ABORT: window wider than 36 h. Refusing. Nothing sent."; exit 2
fi

Q=$(sqlite3 "file:$DB?mode=ro" "select count(*) from video where sync_status='QUEUE';" 2>&1)
echo "  QUEUE rows right now: $Q"
if [ "$Q" != "0" ]; then
  echo "  ABORT: $Q rows are already QUEUE — a batch is still draining."
  echo "         Not stacking on it. Let it finish, then re-arm."
  exit 3
fi

echo
echo "=== A. what this window WOULD touch (station DB, read-only) ==="
# Mirror of sync_videos_start_stop's selection: LOCAL, UPDATED, FAILED in range.
sqlite3 -separator '|' "file:$DB?mode=ro" "
  select ifnull(sync_status,'NULL'), count(*)
  from video
  where sync_status in ('LOCAL','UPDATED','FAILED')
    and timestamp >= '$START' and timestamp <= '$STOP'
  group by 1 order by 1;" 2>&1 | sed 's/^/    /'

N=$(sqlite3 "file:$DB?mode=ro" "
  select count(*) from video
  where sync_status in ('LOCAL','UPDATED','FAILED')
    and timestamp >= '$START' and timestamp <= '$STOP';" 2>&1)
echo "  clips in window: $N   (ceiling $MAXC)"
if ! [ "$N" -eq "$N" ] 2>/dev/null; then echo "  ABORT: could not count."; exit 4; fi
if [ "$N" -eq 0 ]; then echo "  Nothing to do in this window. Stopping."; exit 0; fi
if [ "$N" -gt "$MAXC" ]; then
  echo "  ABORT: $N exceeds the ceiling $MAXC. Narrow the window. Nothing sent."
  exit 4
fi

echo "  --- bytes actually on disk for those rows ---"
python3 - "$START" "$STOP" <<'PY' 2>&1 | sed 's/^/    /'
import sqlite3, os, sys
start, stop = sys.argv[1], sys.argv[2]
db = sqlite3.connect("file:/home/pi/.ORC-OS/orc-os.db?mode=ro", uri=True)
base = "/home/pi/.ORC-OS/uploads"
rows = db.execute(
    "select id, timestamp, sync_status, ifnull(file,'') from video "
    "where sync_status in ('LOCAL','UPDATED','FAILED') "
    "and timestamp >= ? and timestamp <= ? order by timestamp", (start, stop)).fetchall()
have = gone = 0; b = 0
for _id, ts, st, f in rows:
    p = os.path.join(base, f) if f else None
    if p and os.path.isfile(p):
        have += 1; b += os.path.getsize(p)
    else:
        gone += 1
print(f"with_file={have} missing_file={gone} bytes={b/1e6:.1f} MB")
if rows:
    print(f"first={rows[0][1]}  last={rows[-1][1]}")
# The exact ids, so the undo is knowable before anything is sent.
print("ids: " + ",".join(str(r[0]) for r in rows))
PY

echo
echo "=== B. sizing inputs (read them before choosing the next window) ==="
echo "  --- callback_url: retry_timeout feeds min(retry_timeout,150) upstream ---"
sqlite3 -line "file:$DB?mode=ro" "select created_at, token_expiration, retry_timeout
                                  from callback_url;" 2>&1 | sed 's/^/    /'
echo "  --- recent sync error classes (which timeout is really in force) ---"
journalctl --since '-3 days' --no-pager -o short-iso 2>/dev/null \
  | grep 'Error syncing video to remote site' \
  | grep -oE 'read timeout=[0-9.]+|ConnectTimeout|RemoteDisconnected|ConnectionReset|SSLError|Expecting value|Max retries' \
  | sort | uniq -c | sort -rn | sed 's/^/    /'

echo
echo "=== C. is the queue runner even available (redis + celery) ==="
# POST /sync/ calls await redis_available() first and fails if redis is down, so
# check before the commit rather than discovering it mid-wake.
#
# 2026-09-22: the first version probed GET /api/health/ unauthenticated and got
# 401 — the middleware exempts only the three /api/auth/ endpoints, so every
# other route needs the cookie. That told us the API is up and enforcing auth,
# and nothing about redis. redis-cli is not installed on the station either.
# So probe the socket and the processes directly, none of which needs auth.
RC=$(curl -s -o /dev/null -w '%{http_code}' --max-time 8 "$API/api/health/" 2>/dev/null)
echo "  GET /api/health/ (no cookie) -> HTTP ${RC:-000}   [401 = API up, auth enforced]"
if command -v ss >/dev/null 2>&1; then
  echo "  listeners on 6379: $(ss -ltn 2>/dev/null | grep -c ':6379' || echo 0)"
  ss -ltn 2>/dev/null | grep ':6379' | sed 's/^/    /'
else
  echo "  ss not present"
fi
if command -v redis-cli >/dev/null 2>&1; then
  echo "  redis-cli ping -> $(redis-cli ping 2>&1 | head -1)"
else
  # No client, so ask redis for its version over the raw socket. A reply at all
  # proves it is accepting connections.
  PONG=$( (exec 3<>/dev/tcp/127.0.0.1/6379 && printf 'PING\r\n' >&3 && head -c 16 <&3) 2>/dev/null | tr -d '\r\n')
  echo "  raw PING on 127.0.0.1:6379 -> '${PONG:-no reply}'   [+PONG = up]"
fi
echo "  processes:"
for p in redis celery; do
  echo "    $p: $(pgrep -caf "$p" 2>/dev/null || echo 0) match(es)"
done

if [ "$COMMIT" != "yes" ]; then
  echo
  echo "=== DRY RUN. No login, no POST, no state change. ==="
  echo "=== Re-arm with ORC_COMMIT=yes to fire this exact window. ==="
  echo "=== END ==="
  exit 0
fi

echo
echo "=== D. COMMIT — login, then POST /api/video/sync/ for this window ==="
# Upstream takes the password as a QUERY PARAMETER. Canary first: if uvicorn
# access-logs query strings, the password would land in the journal and then in
# this grab file.
CANARY="orcprobe$$-$(date +%s)"
curl -s -o /dev/null --max-time 6 "$API/api/auth/password_available/?probe=$CANARY" 2>/dev/null
sleep 2
LEAK=$(journalctl -u orc-os --since "-2min" --no-pager 2>/dev/null | grep -c "$CANARY" || true)
echo "  query-string canary occurrences in journal: ${LEAK:-0}"
if [ "${LEAK:-0}" != "0" ]; then
  echo "  ABORT: query strings ARE logged. NOTHING WAS SENT."; exit 5
fi

ENC=$(printf '%s' "$PW" | python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.stdin.read(),safe=''))")
CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 -c "$CJ" \
       -X POST "$API/api/auth/login/?password=$ENC" 2>/dev/null)
echo "  POST /api/auth/login/ -> HTTP $CODE"
[ "$CODE" = "200" ] || { echo "  login failed. Not retrying. Nothing synced."; exit 6; }

BODY=$(python3 - "$START" "$STOP" <<'PY'
import json, sys
s, t = sys.argv[1].replace(" ", "T"), sys.argv[2].replace(" ", "T")
print(json.dumps({"start": s, "stop": t, "sync_file": True, "sync_image": True}))
PY
)
echo "  body: $BODY"
OUT=$(curl -s -w '\n__HTTP__%{http_code}' --max-time 60 -b "$CJ" \
      -H 'Content-Type: application/json' \
      -X POST "$API/api/video/sync/" -d "$BODY" 2>&1)
SC=$(printf '%s' "$OUT" | sed -n 's/.*__HTTP__//p')
echo "  POST /api/video/sync/ -> HTTP ${SC:-000}"
printf '%s' "$OUT" | sed 's/__HTTP__.*//' | head -c 600 | sed 's/^/    /'

echo
echo "=== E. state immediately after ==="
sqlite3 -separator '|' "file:$DB?mode=ro" "select ifnull(sync_status,'NULL'), count(*)
                                           from video group by 1 order by 2 desc;" 2>&1 | sed 's/^/    /'
echo "  QUEUE now: $(sqlite3 "file:$DB?mode=ro" "select count(*) from video where sync_status='QUEUE';" 2>&1)"
echo
echo "  UNDO: the station will keep retrying QUEUE rows on every boot until they"
echo "  succeed. To stop the trickle, the QUEUE rows must go back to FAILED —"
echo "  that is a direct DB write and needs its own approval. The ids are listed"
echo "  in section A above."
echo "=== END ==="
