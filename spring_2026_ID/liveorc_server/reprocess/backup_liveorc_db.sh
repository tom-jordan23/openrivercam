#!/usr/bin/env bash
# backup_liveorc_db.sh — full + targeted backup of the LiveORC Postgres DB
# BEFORE any reprocessing of historical time_series. Read-only against the DB.
#
# Run ON the LiveORC host (AWS EC2 via SSM), where the `db` postgis container runs.
# Produces, under ./liveorc-backups/<timestamp>/ :
#   - liveorc_full.dump        full pg_dump (custom/compressed) — full-DB safety net
#   - api_timeseries.sql       targeted api_timeseries table (schema+data) — fast row-level restore
#   - api_timeseries.csv       targeted api_timeseries CSV — ANALYTICS BASELINE (pre-reprocess)
#   - api_video.csv            video<->time_series<->video_config map (CSV) for cross-checks
#   - manifest.txt             counts, sizes, sha256, DB identity
#
# Env (sourced from LiveORC's .env if present, else must be exported):
#   LORC_DB_USER, LORC_DB_PASS   (POSTGRES_USER/PASSWORD)   DB name is always "liveorc"
#   DB_CONTAINER  (default: db)  — the postgis container name
set -euo pipefail

DB_CONTAINER="${DB_CONTAINER:-db}"
DB_NAME="liveorc"
TS="$(date +%Y%m%d-%H%M%S)"
OUT="${OUT_DIR:-./liveorc-backups/$TS}"

# Try to pull creds from a LiveORC .env if not already in the environment.
for envf in "${LIVEORC_ENV:-}" /opt/LiveORC/.env ./.env; do
  if [ -n "${envf:-}" ] && [ -f "$envf" ] && [ -z "${LORC_DB_USER:-}" ]; then
    echo "Sourcing DB creds from $envf"
    set -a; . "$envf"; set +a
  fi
done

: "${LORC_DB_USER:?set LORC_DB_USER (or provide a LiveORC .env)}"
: "${LORC_DB_PASS:?set LORC_DB_PASS (or provide a LiveORC .env)}"

if ! docker ps --format '{{.Names}}' | grep -qx "$DB_CONTAINER"; then
  echo "ERROR: postgis container '$DB_CONTAINER' not running. Set DB_CONTAINER=..." >&2
  docker ps --format '  {{.Names}}\t{{.Image}}' >&2
  exit 1
fi

mkdir -p "$OUT"
echo "==> Backing up DB '$DB_NAME' from container '$DB_CONTAINER' into $OUT"

dx() { docker exec -e PGPASSWORD="$LORC_DB_PASS" "$DB_CONTAINER" "$@"; }

# 1) Full DB dump (custom format = compressed + selective restore later)
echo "  [1/4] full pg_dump (custom format)…"
dx pg_dump -U "$LORC_DB_USER" -d "$DB_NAME" -Fc > "$OUT/liveorc_full.dump"

# 2) Targeted api_timeseries SQL (schema + data) for a fast, surgical restore
echo "  [2/4] api_timeseries.sql (targeted)…"
dx pg_dump -U "$LORC_DB_USER" -d "$DB_NAME" -t api_timeseries --no-owner > "$OUT/api_timeseries.sql"

# 3) Targeted api_timeseries CSV — the analytics BASELINE (every column, all rows)
echo "  [3/4] api_timeseries.csv (analytics baseline)…"
dx psql -U "$LORC_DB_USER" -d "$DB_NAME" -At \
  -c "\copy (SELECT * FROM api_timeseries ORDER BY id) TO STDOUT WITH CSV HEADER" \
  > "$OUT/api_timeseries.csv"

# 4) video<->ts<->config map (for join in analytics and to confirm replace-in-place)
echo "  [4/4] api_video.csv (video↔ts↔config map)…"
dx psql -U "$LORC_DB_USER" -d "$DB_NAME" -At \
  -c "\copy (SELECT id, timestamp, status, file, video_config_id, time_series_id FROM api_video ORDER BY id) TO STDOUT WITH CSV HEADER" \
  > "$OUT/api_video.csv"

# Manifest
{
  echo "LiveORC DB backup"
  echo "timestamp:     $TS"
  echo "db_container:  $DB_CONTAINER"
  echo "db_name:       $DB_NAME"
  echo "pg_version:    $(dx psql -U "$LORC_DB_USER" -d "$DB_NAME" -At -c 'select version();' | head -1)"
  echo "ts_rows:       $(dx psql -U "$LORC_DB_USER" -d "$DB_NAME" -At -c 'select count(*) from api_timeseries;')"
  echo "video_rows:    $(dx psql -U "$LORC_DB_USER" -d "$DB_NAME" -At -c 'select count(*) from api_video;')"
  echo
  echo "files (sha256  size  name):"
  ( cd "$OUT" && for f in *; do printf '  %s  %8s  %s\n' "$(sha256sum "$f" | cut -c1-16)" "$(stat -c%s "$f")" "$f"; done )
} > "$OUT/manifest.txt"

cat "$OUT/manifest.txt"
echo
echo "==> Backup complete: $OUT"
echo "    Keep api_timeseries.csv — restore_liveorc_db.sh and analytics_reprocess.py both consume it."
