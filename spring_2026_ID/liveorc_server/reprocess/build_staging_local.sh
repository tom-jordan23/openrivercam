#!/usr/bin/env bash
# build_staging_local.sh — stand up a LOCAL throwaway LiveORC to validate the
# reprocess toolkit for free (no second EC2). Postgis (so a prod dump restores)
# + FileSystemStorage (simplest media). Nothing here touches prod.
#
# Two stages, so you can build the infra before the prod data is in hand:
#
#   # 1) bring up the empty local stack now (webapp + postgis, no minio/rabbitmq):
#   LIVEORC_REPO=/tmp/LiveORC ./build_staging_local.sh
#
#   # 2) later, once you've pulled a prod snapshot from AWS, load it:
#   ./build_staging_local.sh --backup liveorc-backups/<ts> --site <SITE_ID> [--media ./media-src]
#
# Prereqs for stage 2 (pulled from AWS once, via SSM/scp):
#   - a prod DB backup dir from backup_liveorc_db.sh  (has liveorc_full.dump)
#   - a handful of real Sukabumi video files arranged under --media by their DB
#     `file` relative path (this script prints the exact ids + paths to fetch).
set -euo pipefail

REPO="${LIVEORC_REPO:-/tmp/LiveORC}"
SAMPLE_N="${SAMPLE_N:-25}"
BACKUP_DIR=""; SITE_ID=""; MEDIA_SRC=""
while [ $# -gt 0 ]; do
  case "$1" in
    --backup) BACKUP_DIR="$2"; shift 2;;
    --site)   SITE_ID="$2"; shift 2;;
    --media)  MEDIA_SRC="$2"; shift 2;;
    # legacy positional form: <backup_dir> <site_id> [media_src]
    *) if [ -z "$BACKUP_DIR" ]; then BACKUP_DIR="$1"
       elif [ -z "$SITE_ID" ]; then SITE_ID="$1"
       elif [ -z "$MEDIA_SRC" ]; then MEDIA_SRC="$1"; fi; shift;;
  esac
done

[ -d "$REPO" ] || { echo "LiveORC repo not at $REPO (set LIVEORC_REPO)"; exit 1; }
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Absolutize paths NOW, before we cd into the repo (otherwise relative --backup/--media
# would resolve against $REPO and break).
[ -n "$BACKUP_DIR" ] && { [ -d "$BACKUP_DIR" ] || { echo "no such backup dir: $BACKUP_DIR"; exit 1; }; BACKUP_DIR="$(cd "$BACKUP_DIR" && pwd)"; }
[ -n "$MEDIA_SRC" ]  && { [ -d "$MEDIA_SRC"  ] || { echo "no such media dir: $MEDIA_SRC"; exit 1; };  MEDIA_SRC="$(cd "$MEDIA_SRC" && pwd)"; }

# Staging env: postgis + LOCAL filesystem storage (empty LORC_STORAGE_HOST → FS),
# no rabbitmq (empty LORC_RABBITMQ_HOST), no nodes. Distinct ports so it won't clash
# with the local ORC-OS dev stack.
cat > "$REPO/.env" <<'ENV'
LORC_HOST=localhost
LORC_PORT=8010
LORC_DB_DIR=./lorc_data_staging
LORC_DB_HOST=db
# NOTE: LORC_DB_PORT is BOTH the host publish port AND the port Django uses to reach
# `db` over the docker network, where postgres listens on 5432. So it must be 5432
# (do not bump it to avoid a host clash — that breaks the internal connection).
LORC_DB_PORT=5432
LORC_DB_USER=liveorc_dbuser
LORC_DB_PASS=liveorc_dbsecret
LORC_STORAGE_DIR=./lorc_media_staging
LORC_STORAGE_HOST=
LORC_RABBITMQ_HOST=
LORC_SSL=NO
LORC_DEV=NO
LORC_DEBUG=YES
LORC_DEFAULT_NODES=0
ENV
echo "==> wrote staging $REPO/.env (postgis :5433, web :8010, FileSystemStorage, no minio/rabbitmq)"

cd "$REPO"
set -a; . ./.env; set +a
mkdir -p "$LORC_STORAGE_DIR" "$LORC_DB_DIR"

echo "==> bringing up local LiveORC (webapp + postgis)…"
./liveorc.sh start --hostname localhost --detached || ./liveorc.sh start --detached

echo "==> waiting for db to accept connections…"
for i in $(seq 1 60); do
  if docker exec -e PGPASSWORD="$LORC_DB_PASS" db pg_isready -U "$LORC_DB_USER" -d liveorc >/dev/null 2>&1; then
    echo "   db ready"; break; fi; sleep 2
  [ "$i" = 60 ] && { echo "db not ready — check 'docker ps' / 'docker logs liveorc_webapp'"; exit 1; }
done

q() { docker exec -i -e PGPASSWORD="$LORC_DB_PASS" db psql -U "$LORC_DB_USER" -d liveorc -At -c "$1"; }

# ---- stage 2: restore a prod snapshot, if one was provided ------------------
if [ -n "$BACKUP_DIR" ]; then
  DUMP="$BACKUP_DIR/liveorc_full.dump"
  [ -f "$DUMP" ] || { echo "missing $DUMP"; exit 1; }
  echo "==> restoring prod dump into the LOCAL staging db…"
  q "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" >/dev/null
  docker exec -i -e PGPASSWORD="$LORC_DB_PASS" db \
    pg_restore -U "$LORC_DB_USER" -d liveorc --no-owner < "$DUMP" || \
    echo "   (pg_restore reported warnings — usually benign extension/owner notes)"

  echo "==> staging counts:"
  q "SELECT 'videos='||count(*) FROM api_video
     UNION ALL SELECT 'timeseries='||count(*) FROM api_timeseries;"

  if [ -n "$MEDIA_SRC" ] && [ -d "$MEDIA_SRC" ]; then
    # NOTE: stage into Django's MEDIA_ROOT (/liveorc/media), NOT the compose volume
    # mount (/liveorc/data/media) — FS storage resolves files against MEDIA_ROOT.
    # MEDIA_SRC must mirror the DB `file` paths, e.g. MEDIA_SRC/videos/4/<date>/<clip>.mp4
    echo "==> copying sample media from $MEDIA_SRC into MEDIA_ROOT (/liveorc/media)…"
    docker exec liveorc_webapp mkdir -p /liveorc/media
    docker cp "$MEDIA_SRC/." liveorc_webapp:/liveorc/media/ && echo "   media copied"
  fi

  if [ -n "$SITE_ID" ]; then
    echo "==> sample video ids + relative file paths for site $SITE_ID (pull these from prod MinIO):"
    q "SELECT v.id||'  '||v.file FROM api_video v
       JOIN api_videoconfig c ON v.video_config_id=c.id
       WHERE c.site_id=$SITE_ID AND v.file IS NOT NULL
       ORDER BY v.timestamp LIMIT $SAMPLE_N;"
    echo "==> VideoConfigs at site $SITE_ID (find the Fit 6 id):"
    q "SELECT c.id||'  '||c.name FROM api_videoconfig c WHERE c.site_id=$SITE_ID;"
  else
    echo "==> (no --site given) all sites:"
    q "SELECT id||'  '||name FROM api_site ORDER BY id;"
  fi
else
  echo "==> empty stack is up (no --backup given). Schema created by start.sh migrate."
  echo "    Load real data later:"
  echo "      ./build_staging_local.sh --backup liveorc-backups/<ts> --site <SITE_ID> --media ./media-src"
fi

echo
echo "==> pinning a pyorc-compatible xarray (image ships one too new for pyorc 0.9.4)…"
XARRAY_PIN="${XARRAY_PIN:-2024.9.0}"
docker exec liveorc_webapp python -c "import sys,xarray; sys.exit(0 if xarray.__version__=='$XARRAY_PIN' else 1)" 2>/dev/null \
  || docker exec liveorc_webapp pip install -q "xarray==$XARRAY_PIN" || echo "   WARN: xarray pin failed"

echo "==> validating the reprocess engine inside the webapp container…"
docker cp "$SCRIPT_DIR/reprocess_fit6.py" liveorc_webapp:/tmp/reprocess_fit6.py 2>/dev/null || true
docker exec liveorc_webapp python -c \
  "import django,pyorc,xarray; from pyorc.service import velocity_flow_subprocess; print('pyorc',pyorc.__version__,'xarray',xarray.__version__,'+ Django + velocity_flow_subprocess OK')" \
  || echo "   WARN: engine import failed — check the image has pyorc"

echo
echo "==> local staging ready. Web UI: http://localhost:8010/admin/  (container: liveorc_webapp)"
echo "    Reprocess dry-run (once data+config are loaded):"
echo "      docker exec -it liveorc_webapp python /tmp/reprocess_fit6.py \\"
echo "          --site-id <SITE_ID> --video-config-id <FIT6_VC_ID> --ids <ids>"
