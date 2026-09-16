set -u
DB=/home/pi/.ORC-OS/orc-os.db
BASE=/home/pi/.ORC-OS/uploads
# TODO-119: station half of the timestamp-level join (2026-09-16).
#
# The 09-03 per-day join was 0.4% coarse: enough to say the backlog is absent
# from the server, not enough to scope an upload. The 62 clips LiveORC 500'd on
# are FAILED here yet held there, and nothing constrains `timestamp` on the
# server, so re-sending them makes duplicate rows. This lists every row not
# marked SYNCED, with its exact timestamp and whether its file still exists, so
# the join can be done offline against the server's own timestamps.
#
# Run through todo119_wake_runner.py. Run it via bash -s.
# READ-ONLY. sqlite SELECTs on a read-only URI, and stat(1). No network request,
# no sync, no write.
echo "=== TSJOIN $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "=== counts by sync_status ==="
sqlite3 -separator '|' "file:$DB?mode=ro" "select ifnull(sync_status,'NULL'), count(*) from video group by 1 order by 2 desc;" 2>&1
df -h / | tail -1
echo "=== ROWS: id|timestamp|sync_status|remote_id|status|file|bytes (empty = file gone) ==="
sqlite3 -separator '|' "file:$DB?mode=ro" "
  select id, timestamp, ifnull(sync_status,'NULL'), ifnull(remote_id,''), ifnull(status,''), ifnull(file,'')
  from video where ifnull(sync_status,'') != 'SYNCED' order by timestamp;" 2>&1 |
while IFS='|' read -r id ts st rid pst f; do
  b=""
  [ -n "$f" ] && [ -f "$BASE/$f" ] && b=$(stat -c%s "$BASE/$f" 2>/dev/null)
  echo "$id|$ts|$st|$rid|$pst|$f|$b"
done
echo "=== END ROWS ==="
