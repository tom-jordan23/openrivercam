set -u
DB=/home/pi/.ORC-OS/orc-os.db
echo "=== CHECKIN $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# Check-in of 2026-09-27, five days after the 09-22 read.
#
# Nothing has been sent to the station since 09-22: the trickle was not fired,
# so QUEUE should still be 0 and the backlog should only have grown. The point
# of this grab is the purge clock (TODO-119 "REVISED 2026-09-22"): 13 G free on
# 09-22 at ~554 MB/day puts free space near 10 G today and the disk manager's
# first bite at 2026-10-04..10-07. The measured slope, not the estimate, is what
# the deadline should be quoted from.
#
# Baseline 2026-09-22 11:30 UTC:
#   disk 77% used, 13 G free
#   SYNCED 3427, FAILED 3084, LOCAL 126, QUEUE 0
#   FAILED with file: 1295 = 12.50 GB; oldest surviving un-synced 2026-07-03 09:31
#   sync failures 09-17..09-22: 18 read timeout=150, 11 Expecting value
#
# Priority order, because the wake ends on a timer: disk, counters, the
# oldest-survivor check (the first sign the purge has started), then the rest.
#
# READ-ONLY. sqlite SELECTs via a read-only URI, journalctl, /proc, df, stat.
# Nothing is written, no network request is made, nothing is synced.

echo
echo "=== A. disk (09-22: 77% used, 13 G free) ==="
df -B1M / | sed 's/^/  /'
echo "  --- settings table (09-22's name/value query failed: wrong columns) ---"
sqlite3 -line "file:$DB?mode=ro" "select * from settings limit 1;" 2>&1 \
  | grep -iE 'free|disk|space' | sed 's/^/  /'

echo
echo "=== B. rows by sync_status (09-22: SYNCED 3427, FAILED 3084, LOCAL 126, QUEUE 0) ==="
sqlite3 -separator '|' "file:$DB?mode=ro" "select ifnull(sync_status,'NULL'), count(*)
                                           from video group by 1 order by 2 desc;" 2>&1 | sed 's/^/  /'

echo
echo "=== C. un-synced rows with their file (09-22: FAILED 1295 = 12.50 GB; oldest 07-03 09:31) ==="
python3 - <<'PY' 2>&1 | sed 's/^/  /'
import sqlite3, os
db = sqlite3.connect("file:/home/pi/.ORC-OS/orc-os.db?mode=ro", uri=True)
base = "/home/pi/.ORC-OS/uploads"
rows = db.execute("select sync_status, file from video "
                  "where ifnull(sync_status,'') != 'SYNCED'").fetchall()
tot = {}
for st, f in rows:
    n, have, b = tot.get(st, (0, 0, 0))
    p = os.path.join(base, f) if f else None
    if p and os.path.isfile(p):
        have += 1; b += os.path.getsize(p)
    tot[st] = (n + 1, have, b)
for st, (n, have, b) in sorted(tot.items(), key=lambda x: str(x[0])):
    print(f"{st}: rows={n} with_file={have} bytes={b/1e9:.2f} GB")
# If the oldest survivor has moved past 07-03, the disk manager has started.
r = db.execute("select timestamp, file from video where ifnull(sync_status,'') != 'SYNCED' "
               "and ifnull(file,'') != '' order by timestamp").fetchall()
for ts, f in r:
    if os.path.isfile(os.path.join(base, f)):
        print(f"oldest surviving un-synced clip: {ts}  {f}")
        break
PY

echo
echo "=== D. per day since 09-21 (UTC): day|FAILED|SYNCED|LOCAL|other|total ==="
sqlite3 -separator '|' "file:$DB?mode=ro" "
  select date(timestamp),
         sum(sync_status='FAILED'), sum(sync_status='SYNCED'),
         sum(sync_status='LOCAL'),
         sum(ifnull(sync_status,'') not in ('FAILED','SYNCED','LOCAL')),
         count(*)
  from video where timestamp >= '2026-09-21' group by 1 order by 1;" 2>&1 | sed 's/^/  /'

echo
echo "=== E. failed video syncs since 09-22 12:00 UTC, by error class ==="
L=$(journalctl --since '2026-09-22 12:00:00' --no-pager -o short-iso 2>/dev/null \
    | grep 'Error syncing video to remote site')
echo "  total: $(printf '%s' "$L" | grep -c . )"
printf '%s' "$L" \
  | grep -oE 'read timeout=[0-9.]+|ConnectTimeout|RemoteDisconnected|ConnectionReset|SSLError|Expecting value|Max retries' \
  | sort | uniq -c | sort -rn | sed 's/^/    /'

echo
echo "=== G. boots and wakes, last lines of wp5d.log ==="
tail -4 /var/log/wp5d.log 2>&1 | cut -c1-160 | sed 's/^/  /'

echo
echo "=== H. link ==="
mmcli -m 0 2>/dev/null | grep -iE "state|signal quality|access tech|operator name" | head -5 | sed 's/^/  /'
echo "=== END ==="
