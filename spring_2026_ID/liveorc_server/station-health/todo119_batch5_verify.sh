set -u
DB=/home/pi/.ORC-OS/orc-os.db
echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# STEP 2 of the 5-clip batch - READ-ONLY. Reads what happened; changes nothing.
#
# It answers the question the raw PUT could not: does ORC-OS's OWN sync path
# complete inside a wake? The raw probe moved 9.2 MB in 3.95 s, but it skipped
# the multipart encoding and the token refresh that the real path carries.

echo "=== A. where the batch ended up ==="
sqlite3 -column "$DB" "select ifnull(sync_status,'NULL'), count(*) from video group by 1 order by 2 desc;" 2>&1 | sed 's/^/  /'
echo "  QUEUE remaining (0 = the batch drained; >0 = still working or stalled):"
sqlite3 "$DB" "select count(*) from video where sync_status='QUEUE';" 2>&1 | sed 's/^/    /'

echo
echo "=== B. the sync task's own account, this wake and last ==="
journalctl --since "-45 min" --no-pager 2>/dev/null \
  | grep -iE "synchroniz|Starting sync|submitted to the executor|Shutdown triggered|sync_status|Failed to submit" \
  | tail -40 | sed 's/^/  /'

echo
echo "=== C. per-clip timing, if the log carries it ==="
# Successive "submitted to the executor" lines bracket one clip's transfer, so
# their spacing is the per-clip cost on the REAL path - the number that decides
# how many clips a wake can actually drain.
journalctl --since "-45 min" --no-pager 2>/dev/null \
  | grep -iE "submitted to the executor|videos left to synchronize" \
  | awk '{print $1" "$2" "$3"  "$0}' | tail -20 | sed 's/^/  /'

echo
echo "=== D. any errors raised against the batch ==="
journalctl --since "-45 min" --no-pager 2>/dev/null \
  | grep -iE "error|traceback|timeout|refused|reset|exception" \
  | grep -viE "pipewire|wireplumber|RTKit|pangolin|tailscal|bootstrapDNS" \
  | tail -25 | sed 's/^/  /'

echo
echo "=== E. did SYNCED actually rise, and by how much ==="
echo "  SYNCED was 2589 at 2026-09-03 12:30 UTC, before this batch."
sqlite3 "$DB" "select 'SYNCED now: '||count(*) from video where sync_status='SYNCED';" 2>&1 | sed 's/^/  /'
echo "  (+5 means the whole batch landed. Less means partial - and the rows that"
echo "   did NOT land should still read QUEUE in section A, which is the"
echo "   self-healing the harness measured, not a loss.)"
echo "=== END ==="
