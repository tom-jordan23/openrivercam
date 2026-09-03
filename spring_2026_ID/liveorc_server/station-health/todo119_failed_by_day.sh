set -u
DB=/home/pi/.ORC-OS/orc-os.db
echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

# TODO-119 Track 2. The server holds rows for Sukabumi that the station records
# as FAILED - four confirmed on 2026-09-03. This is the station half of the
# join: one line per day, so it can be paired against the server's per-day
# inventory to say which days actually need re-driving.
#
# Small on purpose. Counts only, no file lists, no journal.
# READ-ONLY: sqlite SELECTs.

echo "=== A. totals by sync_status ==="
sqlite3 -column "$DB" "select ifnull(sync_status,'NULL'), count(*) from video group by 1 order by 2 desc;" 2>&1 | sed 's/^/  /'

echo
echo "=== B. one line per day: day|FAILED|SYNCED|LOCAL|total ==="
sqlite3 -separator '|' "$DB" "
  select date(timestamp),
         sum(sync_status='FAILED'), sum(sync_status='SYNCED'),
         sum(sync_status='LOCAL'), count(*)
  from video group by 1 order by 1;" 2>&1 | sed 's/^/  /'

echo
echo "=== C. span ==="
sqlite3 -column "$DB" "select min(timestamp), max(timestamp), count(*) from video;" 2>&1 | sed 's/^/  /'
echo "=== END ==="
