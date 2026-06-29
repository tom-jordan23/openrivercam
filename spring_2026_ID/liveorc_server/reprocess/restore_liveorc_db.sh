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
    echo "*** WARNING: this restores ONLY api_timeseries. It does NOT undo changes the"
    echo "*** reprocess made to api_video (--repoint sets video_config/status; --recover"
    echo "*** links new rows). If your commit used --repoint or --recover, use '$0 full'"
    echo "*** instead — otherwise videos are left repointed / linked to deleted rows."
    read -r -p "Proceed with api_timeseries-only restore anyway? Type YES: " ok2
    [ "$ok2" = "YES" ] || { echo "aborted — use: $0 full $BACKUP_DIR"; exit 1; }
    echo "==> targeted restore of api_timeseries…"
    # Use DELETE under replica role (FK triggers off) — NOT 'TRUNCATE ... CASCADE',
    # which would also truncate api_video (it FK-references api_timeseries).
    {
      echo "BEGIN;"
      echo "SET session_replication_role = replica;"   # disable FK enforcement for the swap
      echo "DELETE FROM api_timeseries;"               # no CASCADE -> api_video untouched
      # load the snapshot's data rows (strip the dump's table/sequence DDL)
      grep -vE '^(DROP TABLE|CREATE TABLE|ALTER TABLE ONLY api_timeseries\b.*(OWNER|PRIMARY KEY|CONSTRAINT)|CREATE SEQUENCE|ALTER SEQUENCE.*OWNED)' "$SQL" || true
      echo "SET session_replication_role = DEFAULT;"
      echo "COMMIT;"
    } | dx psql -U "$LORC_DB_USER" -d "$DB_NAME" -v ON_ERROR_STOP=1
    echo "    rows now: $(dx psql -U "$LORC_DB_USER" -d "$DB_NAME" -At -c 'select count(*) from api_timeseries;')"
    echo "NOTE: any recovered videos now point to deleted rows — run '$0 full' if that matters."
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
