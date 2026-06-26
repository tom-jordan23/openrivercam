#!/usr/bin/env bash
# stage_load.sh — load a prod snapshot into an ISOLATED staging LiveORC so the
# reprocess toolkit can be validated without touching production.
#
# Prereq: a SECOND LiveORC stack already running, isolated from prod by a distinct
# compose project name, DB data dir, DB port and web port (see REPROCESS_RUNBOOK.md
# "Phase 0 — staging"). This script only LOADS data into it:
#   1) restores the prod full dump into the staging DB
#   2) stages a SAMPLE of real Sukabumi media so videos actually resolve on disk
#   3) prints a sanity summary (row counts, sample videos resolvable)
#
# Usage:
#   STAGE_DB_CONTAINER=db-staging STAGE_WEBAPP=webapp-staging \
#   STAGE_MEDIA_DIR=/opt/LiveORC-staging/media  PROD_MEDIA_DIR=/opt/LiveORC/media \
#   ./stage_load.sh <prod_backup_dir> <site_id> [sample_n]
set -euo pipefail

BACKUP_DIR="${1:?prod backup dir (from backup_liveorc_db.sh)}"
SITE_ID="${2:?Sukabumi site id}"
SAMPLE_N="${3:-25}"
DB="${STAGE_DB_CONTAINER:?set STAGE_DB_CONTAINER (staging postgis container)}"
WEBAPP="${STAGE_WEBAPP:?set STAGE_WEBAPP (staging webapp container)}"
PROD_MEDIA="${PROD_MEDIA_DIR:?set PROD_MEDIA_DIR}"
STAGE_MEDIA="${STAGE_MEDIA_DIR:?set STAGE_MEDIA_DIR}"
DB_NAME="liveorc"

for envf in "${STAGE_ENV:-}" ./.env; do
  [ -n "${envf:-}" ] && [ -f "$envf" ] && [ -z "${LORC_DB_USER:-}" ] && { set -a; . "$envf"; set +a; }
done
: "${LORC_DB_USER:?}"; : "${LORC_DB_PASS:?}"

dxi() { docker exec -i -e PGPASSWORD="$LORC_DB_PASS" "$DB" "$@"; }

echo "==> [1/3] restoring prod dump into STAGING DB ($DB)…"
dxi psql -U "$LORC_DB_USER" -d "$DB_NAME" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" >/dev/null
docker exec -i -e PGPASSWORD="$LORC_DB_PASS" "$DB" \
  pg_restore -U "$LORC_DB_USER" -d "$DB_NAME" --no-owner < "$BACKUP_DIR/liveorc_full.dump"

echo "==> [2/3] staging $SAMPLE_N sample media files for site $SITE_ID…"
# pull a spread of the site's video file paths from the staging DB (relative to MEDIA_ROOT)
mapfile -t FILES < <(dxi psql -U "$LORC_DB_USER" -d "$DB_NAME" -At -c \
  "SELECT v.file FROM api_video v JOIN api_videoconfig c ON v.video_config_id=c.id
   WHERE c.site_id=$SITE_ID AND v.file IS NOT NULL
   ORDER BY v.timestamp LIMIT $SAMPLE_N;")
n=0
for rel in "${FILES[@]}"; do
  src="$PROD_MEDIA/$rel"; dst="$STAGE_MEDIA/$rel"
  if [ -f "$src" ]; then mkdir -p "$(dirname "$dst")"; cp -n "$src" "$dst" && n=$((n+1))
  else echo "  WARN missing prod media: $rel"; fi
done
echo "    staged $n / ${#FILES[@]} files into $STAGE_MEDIA"

echo "==> [3/3] sanity summary"
dxi psql -U "$LORC_DB_USER" -d "$DB_NAME" -c \
  "SELECT (SELECT count(*) FROM api_video) AS videos,
          (SELECT count(*) FROM api_timeseries) AS timeseries,
          (SELECT count(*) FROM api_video v JOIN api_videoconfig c ON v.video_config_id=c.id WHERE c.site_id=$SITE_ID) AS site_videos;"
echo "==> staging loaded. Run reprocess_fit6.py --dry-run against the STAGING webapp ($WEBAPP) on --ids of the staged sample."
echo "    Tip: get the staged ids with the same SELECT (add v.id)."
