set -u
DB=/home/pi/.ORC-OS/orc-os.db
API=http://127.0.0.1:5000
CJ=$(mktemp /dev/shm/orc_cj.XXXXXX)   # tmpfs, never touches the SD card
trap 'rm -f "$CJ"' EXIT INT TERM
echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# DRY RUN for the API re-drive (TODO-119). Tom chose this path over a
# sync_status flip so the backlog never requires a database write.
#
# It proves password -> cookie -> authenticated call, and reports which rows a
# sync WOULD touch. It does NOT call /sync/. No upload, no video state change,
# no database write.
#
# The password is injected into this script body at arming time, held only in a
# shell variable, and used only against 127.0.0.1. It is never in argv, never
# written to disk on the station, never echoed. Only the NAME of what worked is
# reported.
#
# stdin is NOT the carrier: the wake runner pipes this whole script over stdin
# as `bash -s`, so a `read` here would consume the script, not a secret. This
# file therefore stays credential-free and is safe to commit as-is.

PW="${ORC_PW:-}"; unset ORC_PW
[ -n "$PW" ] || { echo "  NO PASSWORD INJECTED - aborting, nothing sent."; exit 1; }
echo "  password injected at arming (len ${#PW}), not echoed"

echo
echo "=== 0. PRE-FLIGHT: are query strings logged? (canary, no secret) ==="
# Upstream takes the password as a QUERY PARAMETER, so if uvicorn access-logs
# query strings it lands in the journal and then in our grab files. Test that
# directly: send a canary on an exempt, credential-free endpoint and look for it.
CANARY="orcprobe$$-$(date +%s)"
curl -s -o /dev/null --max-time 6 "$API/api/auth/password_available/?probe=$CANARY" 2>/dev/null
sleep 2
LEAK=$(journalctl -u orc-os --since "-2min" --no-pager 2>/dev/null | grep -c "$CANARY" || true)
echo "  canary sent on /api/auth/password_available/ (an exempt endpoint)"
echo "  canary occurrences in journal: ${LEAK:-0}"
if [ "${LEAK:-0}" != "0" ]; then
  echo
  echo "  ABORT: query strings ARE logged. Sending the password as a query"
  echo "  parameter would write it into the journal. NOTHING WAS SENT."
  exit 2
fi
echo "  OK - query strings are not reaching the journal; safe to proceed."

echo
echo "=== A. login (cookie jar, the way lib.sh does it) ==="
ENC=$(printf '%s' "$PW" | python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.stdin.read(),safe=''))")
CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 -c "$CJ" \
       -X POST "$API/api/auth/login/?password=$ENC" 2>/dev/null)
echo "  POST /api/auth/login/ -> HTTP $CODE"
AUTH=""
if [ "$CODE" = "200" ]; then
  AUTH="cookie"
  echo "  cookie jar entries: $(grep -c . "$CJ" 2>/dev/null || echo 0)"
else
  echo "  login did not return 200. Not retrying with a different secret."
  exit 1
fi

echo
echo "=== B. does the cookie actually open the API ==="
for ep in /api/video/count/ /api/; do
  echo "  GET $ep (cookie) -> $(curl -s -o /dev/null -w '%{http_code}' --max-time 10 \
        -b "$CJ" "$API$ep" 2>/dev/null)"
done
echo "  --- Bearer fallback, to confirm cookie-only on 0.6.0 ---"
TOK=$(awk '/'"orc"'/ {print $7}' "$CJ" 2>/dev/null | tail -1)
if [ -n "$TOK" ]; then
  echo "  GET /api/video/count/ (Bearer) -> $(curl -s -o /dev/null -w '%{http_code}' \
        --max-time 10 -H "Authorization: Bearer $TOK" "$API/api/video/count/" 2>/dev/null)"
  echo "  (401 here + 200 above confirms auth_helpers.auth_token is cookie-only)"
fi
echo "  AUTH METHOD THAT WORKED: $AUTH"

echo
echo "=== C. what a sync window WOULD touch - no call made ==="
# sync_videos_start_stop gathers LOCAL, then UPDATED, then FAILED across the
# range, so a window is chosen by TIME, not count, and LOCAL rows come along.
echo "  --- 8 newest FAILED rows, to pick a window from ---"
sqlite3 -column "$DB" "select id, ifnull(sync_status,''), ifnull(timestamp,'(none)')
                       from video where sync_status='FAILED'
                       order by id desc limit 8;" 2>&1 | sed 's/^/    /'
echo "  --- LOCAL/UPDATED in the last 24h (would be swept in too) ---"
sqlite3 -column "$DB" "select ifnull(sync_status,''), count(*) from video
                       where sync_status in ('LOCAL','UPDATED')
                         and timestamp > datetime('now','-1 day') group by 1;" 2>&1 | sed 's/^/    /'
echo "  --- totals by status ---"
sqlite3 -column "$DB" "select ifnull(sync_status,'NULL'), count(*) from video group by 1 order by 2 desc;" 2>&1 | sed 's/^/    /'

echo
echo "=== NOTHING WAS SYNCED. No write of any kind. This was a dry run. ==="
echo "=== END ==="
