# ############################################################################
# DO NOT RUN WITHOUT TOM'S EXPLICIT APPROVAL FOR THIS SPECIFIC OPERATION.
#
# This script WRITES to the station's ORC-OS database - high risk, per Tom on
# 2026-09-03. The chosen mechanism is the local API re-drive, not a SQL flip.
# See TODO.md "Standing cautions".
# ############################################################################
set -u
DB=/home/pi/.ORC-OS/orc-os.db
echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# TIMED UPLOAD TEST, step 1 of 2 - flip exactly ONE clip FAILED -> QUEUE.
#
# Tom approved this specific test on 2026-09-03. It is the only state change
# made to the station in this session, and it is reversible: flipping the row
# back to FAILED undoes it.
#
# WHY ONE CLIP. The harness (findings/orc_os_backlog_sync_starvation.md §7)
# established that a QUEUE flip is picked up at t+60, drains newest-first, runs
# serially at one clip per link-time, and that batch size is exactly what you
# flip. It also established that an interrupted batch self-heals - rows stay
# QUEUE and the next boot finishes them - at a cost of ONE duplicated clip per
# interruption. With a batch of one, that is the whole exposure: at worst one
# duplicate video record on the server.
#
# WHAT IT ANSWERS. Throughput, which is unmeasured and which every estimate for
# the 10.69 GB backlog rests on; and whether a clip can complete inside the
# ~21 s sync window a wake actually provides.
#
# GUARDS. It refuses to flip unless every condition holds, and prints why.

# --- resolve the upload root; the `file` column is relative to it ------------
ROOT=""
for cand in "${ORC_UPLOAD_DIRECTORY:-}" /home/pi/.ORC-OS/uploads /home/pi/.ORC-OS; do
  [ -n "$cand" ] && [ -d "$cand/videos" ] && { ROOT=$cand; break; }
done
if [ -z "$ROOT" ]; then echo "ABORT: cannot resolve upload root"; exit 1; fi
echo "upload root: $ROOT"

echo
echo "=== current state before touching anything ==="
sqlite3 -column "$DB" "select ifnull(sync_status,'NULL'), count(*) from video group by 1 order by 2 desc;" 2>&1 | sed 's/^/  /'
echo "  QUEUE rows right now (must be 0, or something else is already draining):"
Q=$(sqlite3 "$DB" "select count(*) from video where sync_status='QUEUE';" 2>&1)
echo "    $Q"
if [ "$Q" != "0" ]; then echo "ABORT: $Q rows already QUEUE - not adding to an in-flight batch"; exit 1; fi

# --- choose the candidate ---------------------------------------------------
# Newest-first is Tom's ordering decision. Skip the 2 highest ids so we are not
# racing the live capture path for the clip it is currently working on.
echo
echo "=== choosing the newest FAILED clip whose file is present ==="
CAND=""
for row in $(sqlite3 "$DB" "select id||'|'||ifnull(file,'') from video
                            where sync_status='FAILED' and file is not null
                            order by id desc limit 12 offset 2;" 2>/dev/null); do
  id=${row%%|*}; f=${row#*|}
  [ -n "$f" ] || continue
  if [ -e "$ROOT/$f" ]; then
    sz=$(stat -c %s "$ROOT/$f" 2>/dev/null || echo 0)
    if [ "$sz" -gt 1000000 ]; then CAND="$id|$f|$sz"; break; fi
    echo "  skip id=$id - file only ${sz}B, too small to be a real clip"
  fi
done
if [ -z "$CAND" ]; then echo "ABORT: no FAILED row with an extant >1MB file in the newest 12"; exit 1; fi
ID=${CAND%%|*}; REST=${CAND#*|}; FILE=${REST%|*}; SIZE=${REST##*|}
echo "  candidate: id=$ID  size=${SIZE}B  $FILE"

# --- the flip ---------------------------------------------------------------
echo
echo "=== FLIP ==="
FLIP_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
sqlite3 -cmd ".timeout 8000" "$DB" "update video set sync_status='QUEUE' where id=$ID and sync_status='FAILED';" 2>&1 | sed 's/^/  sqlite: /'
NOW=$(sqlite3 "$DB" "select sync_status from video where id=$ID;" 2>&1)
echo "  flipped at:  $FLIP_AT"
echo "  id=$ID status is now: $NOW"
if [ "$NOW" != "QUEUE" ]; then echo "  FLIP DID NOT TAKE - nothing is queued, no upload will happen"; exit 1; fi
echo "  total QUEUE rows: $(sqlite3 "$DB" "select count(*) from video where sync_status='QUEUE';")  (must be 1)"

echo
echo "=== RECORD THESE FOR STEP 2 ==="
echo "  CLIP_ID=$ID"
echo "  CLIP_BYTES=$SIZE"
echo "  CLIP_FILE=$FILE"
echo "  FLIPPED_AT=$FLIP_AT"
echo "  to undo: sqlite3 $DB \"update video set sync_status='FAILED' where id=$ID;\""
echo "=== END ==="
