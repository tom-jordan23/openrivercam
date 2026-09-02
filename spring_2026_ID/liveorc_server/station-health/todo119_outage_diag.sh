set -u
DB=/home/pi/.ORC-OS/orc-os.db
echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# ---------------------------------------------------------------------------
# WHY
#   No video has uploaded since 2026-09-02 13:32 UTC and no sensor row has
#   landed since 13:30, yet the station is cycling normally on LTE. The first
#   wake to fail is the one right after the 12.61 GB reclaim committed at
#   14:02. This asks the station what the sync task is actually erroring on.
#
#   It is a CORRELATION under test, not a conclusion. The record has two prior
#   unexplained upload blackouts (07-29 -> 08-10, 08-23 -> 08-28), so a third
#   recurrence landing here by coincidence is entirely possible. Section C is
#   the discriminator: if the errors name files, and those files are ones the
#   reclaim removed, that is the mechanism. If the errors are transport, it is
#   the recurrence.
#
# READ-ONLY. sqlite SELECTs, journalctl and stat. Nothing is written.
# ---------------------------------------------------------------------------

echo "=== A. what the sync task has been saying since the reclaim ==="
journalctl --since "2026-09-02 13:30:00" --no-pager 2>/dev/null \
  | grep -iE "sync|upload|error|traceback|no such file|FileNotFound|exception" \
  | grep -viE "sensors\]" | tail -45 | sed 's/^/  /'
echo "  (empty here would itself be a finding: the task is not running at all)"

echo
echo "=== B. is the sync task even firing each boot ==="
journalctl --since "2026-09-02 13:30:00" --no-pager 2>/dev/null \
  | grep -iE "videos left to synchronize|Starting sync of videos|shutdown" \
  | tail -20 | sed 's/^/  /'

echo
echo "=== C. THE DISCRIMINATOR: do DB rows point at files that no longer exist ==="
# The reclaim deleted 1,403 clips it had verified as already SYNCED. If it also
# removed a file belonging to a row that is NOT SYNCED - or if ORC-OS stats
# SYNCED rows during a sync pass - the task can die on a missing path before
# reaching the current clip.
echo "  --- row counts by sync_status ---"
sqlite3 -column "$DB" "select ifnull(sync_status,'NULL') as status, count(*) from video group by 1 order by 2 desc;" 2>&1 | sed 's/^/    /'
echo "  --- the 12 most recent rows, and whether their file is on disk ---"
# The `file` column is RELATIVE to ORC-OS's upload directory, which is
# ~/.ORC-OS/uploads unless ORC_UPLOAD_DIRECTORY overrides it
# (orc_api/__init__.py:35-36). An earlier version of this script tested the
# relative path against the SSH working directory and reported every row as
# MISSING - a false negative that briefly looked like a major finding. Resolve
# the root first, and say which one was used.
ROOT=""
for cand in "${ORC_UPLOAD_DIRECTORY:-}" /home/pi/.ORC-OS/uploads /home/pi/.ORC-OS; do
  [ -n "$cand" ] && [ -d "$cand/videos" ] && { ROOT=$cand; break; }
done
if [ -z "$ROOT" ]; then
  echo "    CANNOT RESOLVE the upload root — existence check skipped rather than"
  echo "    reported wrongly. Candidates tried: \$ORC_UPLOAD_DIRECTORY,"
  echo "    /home/pi/.ORC-OS/uploads, /home/pi/.ORC-OS"
else
  echo "    upload root: $ROOT"
  sqlite3 "$DB" "select ifnull(sync_status,'NULL')||'|'||ifnull(file,'(nofile)')
                 from video order by id desc limit 12;" 2>&1 | while IFS='|' read -r st f; do
    if [ "$f" = "(nofile)" ]; then
      echo "    $st  (no file column)"
    elif [ -e "$ROOT/$f" ]; then
      echo "    $st  EXISTS  $(stat -c %s "$ROOT/$f" 2>/dev/null) B  $f"
    else
      echo "    $st  MISSING          $f"
    fi
  done
fi
echo "  (MISSING on a non-SYNCED row is the mechanism. MISSING on SYNCED rows"
echo "   only matters if the sync pass stats them, which section A would show.)"

echo
echo "=== D. is anything queued, and is the disk still healthy ==="
sqlite3 -column "$DB" "select ifnull(sync_status,'NULL'), count(*) from video
                       where sync_status in ('QUEUE','LOCAL','UPDATED') group by 1;" 2>&1 | sed 's/^/  /'
df -h / | sed 's/^/  /'

echo
echo "=== E. the sensor side: are today's CSVs being written and uploaded ==="
ls -la /var/log/orc/sensors/ 2>/dev/null | tail -6 | sed 's/^/  /'
echo "  --- last orc-sensors-upload attempts ---"
journalctl --since "2026-09-02 13:00:00" --no-pager 2>/dev/null \
  | grep -iE "sensors-upload|sensors\]" | tail -12 | sed 's/^/  /'

echo "=== END ==="
