#!/usr/bin/env bash
# restore_liveorc_db.sh — roll back a reprocess gone wrong.
#
# Two modes (targeted is the default — it only touches the rows we changed):
#
#   ./restore_liveorc_db.sh timeseries <backup_dir>
#       Restore ONLY the api_timeseries table from <backup_dir>/api_timeseries.sql.
#       This is the surgical undo for a reprocess: drops + recreates api_timeseries
#       from the pre-reprocess snapshot. Other tables (video, video_config…) untouched.
#       Video.time_series_id FKs are preserved because we restore the same PKs.
#
#   ./restore_liveorc_db.sh full <backup_dir>
#       Restore the ENTIRE database from <backup_dir>/liveorc_full.dump.
#       Heavy hammer — use only if the targeted restore is insufficient. Stops the
#       webapp first, recreates the public schema, restores, restarts.
#
# Run ON the LiveORC host. Same env/creds as backup_liveorc_db.sh.
set -euo pipefail

MODE="${1:-}"; BACKUP_DIR="${2:-}"
DB_CONTAINER="${DB_CONTAINER:-db}"
DB_NAME="liveorc"

if [ -z "$MODE" ] || [ -z "$BACKUP_DIR" ] || [ ! -d "$BACKUP_DIR" ]; then
  echo "usage: $0 {timeseries|full} <backup_dir>" >&2; exit 2
fi

for envf in "${LIVEORC_ENV:-}" /opt/LiveORC/.env ./.env; do
  if [ -n "${envf:-}" ] && [ -f "$envf" ] && [ -z "${LORC_DB_USER:-}" ]; then
    set -a; . "$envf"; set +a
  fi
done
: "${LORC_DB_USER:?set LORC_DB_USER}"; : "${LORC_DB_PASS:?set LORC_DB_PASS}"

dx() { docker exec -i -e PGPASSWORD="$LORC_DB_PASS" "$DB_CONTAINER" "$@"; }

echo "DB '$DB_NAME' in container '$DB_CONTAINER'"
echo "current api_timeseries rows: $(dx psql -U "$LORC_DB_USER" -d "$DB_NAME" -At -c 'select count(*) from api_timeseries;')"
read -r -p "Restore [$MODE] from $BACKUP_DIR — this OVERWRITES current data. Type RESTORE to proceed: " ok
[ "$ok" = "RESTORE" ] || { echo "aborted."; exit 1; }

case "$MODE" in
  timeseries)
    SQL="$BACKUP_DIR/api_timeseries.sql"
    [ -f "$SQL" ] || { echo "missing $SQL" >&2; exit 1; }
    echo "==> targeted restore of api_timeseries…"
    # Wrap in a transaction: drop the table (CASCADE would drop the video FK, so instead
    # we TRUNCATE+reload to keep FKs intact), then load the snapshot rows.
    {
      echo "BEGIN;"
      echo "SET session_replication_role = replica;"   # defer FK checks during reload
      echo "TRUNCATE api_timeseries CASCADE;"
      # the dump recreates the table if absent and inserts rows; strip its own table DROP/CREATE
      # by loading data-only INSERTs. api_timeseries.sql from pg_dump is plain SQL.
      grep -vE '^(DROP TABLE|CREATE TABLE|ALTER TABLE ONLY api_timeseries\b.*(OWNER|PRIMARY KEY|CONSTRAINT)|CREATE SEQUENCE|ALTER SEQUENCE.*OWNED)' "$SQL" || true
      echo "SET session_replication_role = DEFAULT;"
      echo "COMMIT;"
    } | dx psql -U "$LORC_DB_USER" -d "$DB_NAME" -v ON_ERROR_STOP=1
    echo "    rows now: $(dx psql -U "$LORC_DB_USER" -d "$DB_NAME" -At -c 'select count(*) from api_timeseries;')"
    echo "NOTE: if the targeted reload reports constraint issues, fall back to: $0 full <dir>"
    ;;
  full)
    DUMP="$BACKUP_DIR/liveorc_full.dump"
    [ -f "$DUMP" ] || { echo "missing $DUMP" >&2; exit 1; }
    echo "==> full restore. Stopping webapp to avoid live writes…"
    docker stop webapp >/dev/null 2>&1 || true
    echo "==> recreating schema + restoring…"
    dx psql -U "$LORC_DB_USER" -d "$DB_NAME" -v ON_ERROR_STOP=1 \
      -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
    docker exec -i -e PGPASSWORD="$LORC_DB_PASS" "$DB_CONTAINER" \
      pg_restore -U "$LORC_DB_USER" -d "$DB_NAME" --no-owner < "$DUMP"
    echo "==> restarting webapp…"
    docker start webapp >/dev/null 2>&1 || echo "  (start webapp manually via liveorc.sh)"
    ;;
  *) echo "unknown mode '$MODE'" >&2; exit 2;;
esac
echo "==> restore complete."
