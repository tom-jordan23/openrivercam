# ############################################################################
# DO NOT RUN WITHOUT TOM'S EXPLICIT APPROVAL FOR THIS SPECIFIC OPERATION.
#
# This script WRITES to the station's ORC-OS database, which Tom classified as
# a high risk operation on 2026-09-03. He chose the local API re-drive
# (POST /api/video/sync/) precisely to avoid doing this. It is kept only
# because the API auth path is unresolved, and it is NOT the chosen approach.
#
# If the API route is blocked, the options are: resolve the blocker, have Tom
# run it, or do not do it. Falling back to this file is the drift that Tom
# caught on 2026-09-03. See TODO.md "Standing cautions".
# ############################################################################
set -u
DB=/home/pi/.ORC-OS/orc-os.db
BATCH=5
echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# FIRST REAL BATCH - flip the 5 newest FAILED clips to QUEUE. Tom approved this
# on 2026-09-03 after the throughput measurement came back at 2.33 MB/s
# effective (one 9.2 MB clip in 3.95 s, server-confirmed).
#
# WHY 5. The sync window is ~21 s per wake, after the scheduler's 60 s delay.
# At 3.95 s per clip that is ~5 clips, so this is one wake's worth - enough to
# validate the sync path end to end without committing to a rate. Cost ~46 MB.
#
# EXPECTED COST OF INTERRUPTION. The harness (orc_os_backlog_sync_starvation.md
# §7) measured that an interrupted batch self-heals - rows stay QUEUE and the
# next boot finishes them, no re-flip needed - at a price of ONE duplicated
# clip per interruption. 5 clips at ~4 s against a ~21 s window sits right on
# the edge, so expect roughly one duplicate. That is the known, bounded cost.
#
# REVERSIBLE. Flipping the rows back to FAILED undoes this entirely. The undo
# statement is printed at the end with the exact ids.
#
# GUARDS. Nothing is flipped unless every condition holds, and it says why.

ROOT=""
for cand in "${ORC_UPLOAD_DIRECTORY:-}" /home/pi/.ORC-OS/uploads /home/pi/.ORC-OS; do
  [ -n "$cand" ] && [ -d "$cand/videos" ] && { ROOT=$cand; break; }
done
if [ -z "$ROOT" ]; then echo "ABORT: cannot resolve upload root"; exit 1; fi
echo "upload root: $ROOT"

echo
echo "=== state before touching anything ==="
sqlite3 -column "$DB" "select ifnull(sync_status,'NULL'), count(*) from video group by 1 order by 2 desc;" 2>&1 | sed 's/^/  /'
Q=$(sqlite3 "$DB" "select count(*) from video where sync_status='QUEUE';" 2>&1)
echo "  QUEUE rows now: $Q"
if [ "$Q" != "0" ]; then echo "ABORT: $Q rows already QUEUE - a batch is in flight, not stacking on it"; exit 1; fi

# --- pick the batch: newest first, files present, skip the live clip ---------
echo
echo "=== choosing $BATCH clips: newest FAILED with an extant >1MB file ==="
IDS=""; TOTAL=0; N=0
for row in $(sqlite3 "$DB" "select id||'|'||ifnull(file,'') from video
                            where sync_status='FAILED' and file is not null
                            order by id desc limit 40 offset 2;" 2>/dev/null); do
  [ "$N" -ge "$BATCH" ] && break
  id=${row%%|*}; f=${row#*|}
  [ -n "$f" ] || continue
  if [ -e "$ROOT/$f" ]; then
    sz=$(stat -c %s "$ROOT/$f" 2>/dev/null || echo 0)
    if [ "$sz" -gt 1000000 ]; then
      IDS="$IDS${IDS:+,}$id"; TOTAL=$((TOTAL+sz)); N=$((N+1))
      echo "  [$N] id=$id  ${sz}B  $f"
    fi
  fi
done
if [ "$N" -ne "$BATCH" ]; then echo "ABORT: found only $N eligible clips, wanted $BATCH"; exit 1; fi
echo "  batch: $N clips, $TOTAL bytes ($(( TOTAL / 1048576 )) MiB)"

# --- the flip, one statement, explicit ids ----------------------------------
echo
echo "=== FLIP ==="
FLIP_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
sqlite3 -cmd ".timeout 8000" "$DB" "update video set sync_status='QUEUE' where id in ($IDS) and sync_status='FAILED';" 2>&1 | sed 's/^/  sqlite: /'
NOWQ=$(sqlite3 "$DB" "select count(*) from video where sync_status='QUEUE';" 2>&1)
echo "  flipped at: $FLIP_AT"
echo "  QUEUE rows now: $NOWQ  (must be $BATCH)"
if [ "$NOWQ" != "$BATCH" ]; then
  echo "  UNEXPECTED - expected $BATCH. Undo with the statement below before retrying."
fi

echo
echo "=== RECORD FOR STEP 2 ==="
echo "  BATCH_IDS=$IDS"
echo "  BATCH_BYTES=$TOTAL"
echo "  FLIPPED_AT=$FLIP_AT"
echo "  UNDO: sqlite3 $DB \"update video set sync_status='FAILED' where id in ($IDS);\""
echo "=== END ==="
