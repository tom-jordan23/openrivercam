set -u
DB=/home/pi/.ORC-OS/orc-os.db
BASE=/home/pi/.ORC-OS/uploads
echo "=== CHECKIN $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# Check-in of 2026-09-22, six days after the last station read.
#
# The server-side view this session is green: no outage in 12.5 days, all four
# sensor streams at 48/day, capture_result_code 1 on every capture, video
# current to 09-22 11:01 UTC. Three things are invisible from the server and
# are the whole reason for this grab:
#
#   1. DISK. The disk manager eats un-synced video oldest-first at min_free_space.
#      Un-synced video is the only copy. This is the one that destroys data
#      silently, so it is measured first.
#   2. The backlog trend against 2026-09-16 13:31 UTC:
#        SYNCED 3176, FAILED 3051, LOCAL 126; disk 72% / 17 GB free;
#        files extant 1263; UPLOAD 1171 clips / 11.29 GB.
#   3. Why 15 clips missed the server on 09-18..09-21 after eight perfect days.
#      Capture succeeded for every one, so it is the sync path.
#
# Also settles one outstanding resume item: the station's pyorc version, which
# the 09-14 harness comparison needed and never got.
#
# Priority order, because the wake ends on a timer: disk first, then counters,
# then the failure classes, then the cheap one-liners.
#
# READ-ONLY. sqlite SELECTs via a read-only URI, journalctl, /proc, df, stat,
# and `pip show`. Nothing is written, no network request is made, nothing is
# synced.

echo
echo "=== A. disk (baseline 09-16: 72% used, 17 GB free) ==="
df -h / | sed 's/^/  /'
echo "  --- ORC-OS min_free_space setting ---"
sqlite3 -column "file:$DB?mode=ro" "select name, value from settings
                                    where name like '%free%' or name like '%disk%';" 2>&1 | sed 's/^/  /'

echo
echo "=== B. rows by sync_status (baseline: SYNCED 3176, FAILED 3051, LOCAL 126) ==="
sqlite3 -separator '|' "file:$DB?mode=ro" "select ifnull(sync_status,'NULL'), count(*)
                                           from video group by 1 order by 2 desc;" 2>&1 | sed 's/^/  /'

echo
echo "=== C. un-synced rows that still have their file, and their bytes ==="
echo "    (baseline 09-16: 1263 extant, 1171 of them worth uploading = 11.29 GB)"
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
# Oldest surviving file is what the disk manager takes next.
r = db.execute("select timestamp, file from video where ifnull(sync_status,'') != 'SYNCED' "
               "and ifnull(file,'') != '' order by timestamp").fetchall()
for ts, f in r:
    if os.path.isfile(os.path.join(base, f)):
        print(f"oldest surviving un-synced clip: {ts}  {f}")
        break
PY

echo
echo "=== D. per day since 09-16 (UTC): day|FAILED|SYNCED|LOCAL|other|total ==="
sqlite3 -separator '|' "file:$DB?mode=ro" "
  select date(timestamp),
         sum(sync_status='FAILED'), sum(sync_status='SYNCED'),
         sum(sync_status='LOCAL'),
         sum(ifnull(sync_status,'') not in ('FAILED','SYNCED','LOCAL')),
         count(*)
  from video where timestamp >= '2026-09-16' group by 1 order by 1;" 2>&1 | sed 's/^/  /'
echo "  --- video.status (processing) since 09-16 ---"
sqlite3 -separator '|' "file:$DB?mode=ro" "
  select ifnull(status,'NULL'), count(*) from video
  where timestamp >= '2026-09-16' group by 1 order by 2 desc;" 2>&1 | sed 's/^/  /'

echo
echo "=== E. failed video syncs since 09-17, by error class ==="
echo "    (09-14 saw: 10 'Expecting value', 3 read timeout=5, 2 SSLError, 1 max retries)"
L=$(journalctl --since '2026-09-17 00:00:00' --no-pager -o short-iso 2>/dev/null \
    | grep 'Error syncing video to remote site')
echo "  total: $(printf '%s' "$L" | grep -c . )"
printf '%s' "$L" \
  | grep -oE 'read timeout=[0-9.]+|ConnectTimeout|RemoteDisconnected|ConnectionReset|SSLError|Expecting value|Max retries' \
  | sort | uniq -c | sort -rn | sed 's/^/    /'
echo "  --- per failure, most recent 25 (UTC) ---"
printf '%s' "$L" | tail -25 | awk '{t=$1; sub(/.*remote site: /,""); print "    " t "  " substr($0,1,100)}'
echo "  --- journal reach ---"
journalctl --no-pager -o short-iso 2>/dev/null | head -1 | cut -c1-30 | sed 's/^/    oldest: /'

echo
echo "=== F. pyorc version (outstanding from the 09-14 harness comparison) ==="
{ pip show pyopenrivercam 2>/dev/null || pip3 show pyopenrivercam 2>/dev/null; } \
  | grep -iE '^(name|version|location)' | sed 's/^/  /'
python3 -c "import pyorc; print('  pyorc.__version__:', getattr(pyorc,'__version__','?'))" 2>&1 | sed 's/^/  /'

echo
echo "=== G. boots and wakes, last lines of wp5d.log ==="
tail -6 /var/log/wp5d.log 2>&1 | cut -c1-160 | sed 's/^/  /'

echo
echo "=== H. link ==="
mmcli -m 0 2>/dev/null | grep -iE "state|signal quality|access tech|operator name" | head -5 | sed 's/^/  /'
echo "=== END ==="
