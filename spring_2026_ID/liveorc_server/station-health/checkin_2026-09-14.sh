set -u
DB=/home/pi/.ORC-OS/orc-os.db
echo "=== CHECKIN $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# Check-in of 2026-09-14, eleven days after the last station read.
#
# Baseline to compare against (2026-09-03 17:30 UTC, sample z3):
#   SYNCED 2599, FAILED 3012, live failure rate zero across eleven captures.
#
# Priority order, because the wake ends on a timer: counters first, then what
# happened per day since, then why anything failed, then disk and link.
#
# READ-ONLY. sqlite SELECTs (via a read-only URI), journalctl, /proc, df.
# Nothing is written, no network request is made, nothing is synced.

echo
echo "=== A. rows by sync_status (baseline: SYNCED 2599, FAILED 3012) ==="
sqlite3 -column "file:$DB?mode=ro" "select ifnull(sync_status,'NULL'), count(*)
                                    from video group by 1 order by 2 desc;" 2>&1 | sed 's/^/  /'

echo
echo "=== B. per day since 09-03 (UTC): day|FAILED|SYNCED|LOCAL|other|total ==="
sqlite3 -separator '|' "file:$DB?mode=ro" "
  select date(timestamp),
         sum(sync_status='FAILED'), sum(sync_status='SYNCED'),
         sum(sync_status='LOCAL'),
         sum(ifnull(sync_status,'') not in ('FAILED','SYNCED','LOCAL')),
         count(*)
  from video where timestamp >= '2026-09-03' group by 1 order by 1;" 2>&1 | sed 's/^/  /'
echo "  --- video.status (processing) since 09-03 ---"
sqlite3 -separator '|' "file:$DB?mode=ro" "
  select ifnull(status,'NULL'), count(*) from video
  where timestamp >= '2026-09-03' group by 1 order by 2 desc;" 2>&1 | sed 's/^/  /'

echo
echo "=== C. failed video syncs since 09-03 17:30 UTC, by error class ==="
L=$(journalctl --since '2026-09-03 17:30:00' --no-pager -o short-iso 2>/dev/null \
    | grep 'Error syncing video to remote site')
echo "  total: $(printf '%s' "$L" | grep -c . )"
printf '%s' "$L" \
  | grep -oE 'read timeout=[0-9.]+|ConnectTimeout|RemoteDisconnected|ConnectionReset|SSLError|Expecting value|Max retries' \
  | sort | uniq -c | sort -rn | sed 's/^/    /'
echo "  --- per failure, most recent 40 (UTC) ---"
printf '%s' "$L" | tail -40 | awk '{t=$1; sub(/.*remote site: /,""); print "    " t "  " substr($0,1,110)}'

echo
echo "=== D. token row ==="
sqlite3 -line "file:$DB?mode=ro" "select created_at, token_expiration, retry_timeout from callback_url;" 2>&1 | sed 's/^/  /'

echo
echo "=== E. disk, and how much un-synced video still has its file ==="
df -h / | sed 's/^/  /'
python3 - <<'PY' 2>&1 | sed 's/^/  /'
import sqlite3, os
db = sqlite3.connect("file:/home/pi/.ORC-OS/orc-os.db?mode=ro", uri=True)
base = "/home/pi/.ORC-OS/uploads"
rows = db.execute("select sync_status, file from video where ifnull(sync_status,'') != 'SYNCED'").fetchall()
tot = {}
for st, f in rows:
    n, have, b = tot.get(st, (0, 0, 0))
    p = os.path.join(base, f) if f else None
    if p and os.path.isfile(p):
        have += 1; b += os.path.getsize(p)
    tot[st] = (n + 1, have, b)
for st, (n, have, b) in sorted(tot.items(), key=lambda x: str(x[0])):
    print(f"{st}: rows={n} with_file={have} bytes={b/1e9:.2f} GB")
PY

echo
echo "=== F. boots and wakes, last lines of wp5d.log ==="
tail -8 /var/log/wp5d.log 2>&1 | cut -c1-160 | sed 's/^/  /'
echo "  boots recorded since 09-03: $(journalctl --list-boots --no-pager 2>/dev/null | awk '$4>="2026-09-03"' | wc -l)"

echo
echo "=== G. link ==="
mmcli -m 0 2>/dev/null | grep -iE "state|signal quality|access tech|operator name" | head -5 | sed 's/^/  /'
echo "=== END ==="
