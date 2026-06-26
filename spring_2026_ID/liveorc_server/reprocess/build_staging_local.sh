#!/usr/bin/env bash
# build_staging_local.sh — stand up a LOCAL throwaway LiveORC to validate the
# reprocess toolkit for free (no second EC2). Postgis (so a prod dump restores)
# + FileSystemStorage (simplest media). Nothing here touches prod.
#
# Prereqs you bring (pulled from AWS once, via SSM/scp):
#   - a prod DB backup dir from backup_liveorc_db.sh  (has liveorc_full.dump)
#   - a handful of real Sukabumi video files, arranged under --media-src by their
#     DB `file` relative path (e.g. media-src/<site>/<...>/clip.mp4). Get the exact
#     relative paths + ids from the SELECT this script prints at the end.
#
# Usage:
#   LIVEORC_REPO=/tmp/LiveORC ./build_staging_local.sh <prod_backup_dir> <site_id> [media_src]
#
# Then validate (dry-run) inside the local webapp container:
#   docker cp reprocess_fit6.py liveorc_webapp:/tmp/
#   docker exec -it liveorc_webapp python /tmp/reprocess_fit6.py \
#       --site-id <site_id> --video-config-id <FIT6_VC_ID> --ids <sample_ids>
set -euo pipefail

BACKUP_DIR="${1:?prod backup dir (from backup_liveorc_db.sh)}"
SITE_ID="${2:?Sukabumi site id}"
MEDIA_SRC="${3:-}"
REPO="${LIVEORC_REPO:-/tmp/LiveORC}"
SAMPLE_N="${SAMPLE_N:-25}"
DUMP="$BACKUP_DIR/liveorc_full.dump"

[ -d "$REPO" ] || { echo "LiveORC repo not at $REPO (set LIVEORC_REPO)"; exit 1; }
[ -f "$DUMP" ] || { echo "missing $DUMP"; exit 1; }

# Staging env: postgis + LOCAL filesystem storage (empty LORC_STORAGE_HOST → FS).
# Distinct ports so it won't clash with the local ORC-OS dev stack.
cat > "$REPO/.env" <<'ENV'
LORC_HOST=localhost
LORC_PORT=8010
LORC_DB_DIR=lorc_data_staging
LORC_DB_HOST=db
LORC_DB_PORT=5433
LORC_DB_USER=liveorc_dbuser
LORC_DB_PASS=liveorc_dbsecret
LORC_STORAGE_DIR=lorc_media_staging
LORC_STORAGE_HOST=
LORC_SSL=NO
LORC_DEV=NO
LORC_DEBUG=YES
LORC_DEFAULT_NODES=0
ENV
echo "==> wrote staging $REPO/.env (postgis :5433, web :8010, FileSystemStorage)"

cd "$REPO"
echo "==> bringing up local LiveORC (postgis)…"
set -a; . ./.env; set +a
./liveorc.sh start --hostname localhost --detached || ./liveorc.sh start --detached || true

echo "==> waiting for db container to be healthy…"
for i in $(seq 1 60); do
  if docker exec -e PGPASSWORD="$LORC_DB_PASS" db pg_isready -U "$LORC_DB_USER" -d liveorc >/dev/null 2>&1; then
    echo "   db ready"; break; fi; sleep 2
  [ "$i" = 60 ] && { echo "db not ready — check 'docker ps' / liveorc.sh logs"; exit 1; }
done

echo "==> restoring prod dump into the LOCAL staging db…"
docker exec -i -e PGPASSWORD="$LORC_DB_PASS" db \
  psql -U "$LORC_DB_USER" -d liveorc -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" >/dev/null
docker exec -i -e PGPASSWORD="$LORC_DB_PASS" db \
  pg_restore -U "$LORC_DB_USER" -d liveorc --no-owner < "$DUMP" || \
  echo "   (pg_restore reported warnings — usually benign extension/owner notes)"

q() { docker exec -i -e PGPASSWORD="$LORC_DB_PASS" db psql -U "$LORC_DB_USER" -d liveorc -At -c "$1"; }

echo "==> staging counts:"
q "SELECT 'videos='||count(*) FROM api_video
   UNION ALL SELECT 'timeseries='||count(*) FROM api_timeseries
   UNION ALL SELECT 'site_videos='||count(*) FROM api_video v
            JOIN api_videoconfig c ON v.video_config_id=c.id WHERE c.site_id=$SITE_ID;"

# Optional: stage provided sample media into the FS media volume.
if [ -n "$MEDIA_SRC" ] && [ -d "$MEDIA_SRC" ]; then
  # container media root is the mounted volume; copy under it preserving rel paths
  echo "==> copying sample media from $MEDIA_SRC into the webapp media volume…"
  docker cp "$MEDIA_SRC/." liveorc_webapp:/liveorc/data/media/ && echo "   media copied"
else
  echo "==> NO media_src given — videos won't resolve until you stage files. Pull these and re-run with a media_src:"
fi

echo
echo "==> sample video ids + relative file paths for site $SITE_ID (pull these from prod):"
q "SELECT v.id||'  '||v.file FROM api_video v
   JOIN api_videoconfig c ON v.video_config_id=c.id
   WHERE c.site_id=$SITE_ID AND v.file IS NOT NULL
   ORDER BY v.timestamp LIMIT $SAMPLE_N;"
echo
echo "==> find the Fit 6 VideoConfig id:"
q "SELECT c.id||'  '||c.name FROM api_videoconfig c WHERE c.site_id=$SITE_ID;"
echo
echo "==> local staging ready. Web UI: http://localhost:8010/admin/  (webapp container: liveorc_webapp)"
echo "    Next: docker cp reprocess_fit6.py liveorc_webapp:/tmp/ && docker exec -it liveorc_webapp \\"
echo "          python /tmp/reprocess_fit6.py --site-id $SITE_ID --video-config-id <FIT6_VC_ID> --ids <ids>"
