#!/usr/bin/env bash
# run_reprocess.sh — wrapper that guarantees a pyorc-compatible environment, then
# runs reprocess_fit6.py inside a LiveORC container.
#
# WHY: the stock LiveORC image ships pyorc 0.9.4 but an xarray years newer than it
# supports (e.g. 2026.x on Python 3.14), which crashes pyorc's transect step with
# "Passing a Dataset as data_vars ... is not supported". pyorc 0.9.4 leaves xarray
# unpinned, so we must pin a compatible version (validated: 2024.9.0, same family the
# station runs). This wrapper installs that pin (idempotent) before running.
#
# STAGING (default): exec into the local liveorc_webapp container.
#   ./run_reprocess.sh --site-id 4 --video-config-id 3 --start 2026-05-16T00:00:00 ...
#
# PROD: do NOT permanently mutate the serving webapp. Prefer an EPHEMERAL SIDECAR
# from the same image, joined to the liveorc network, with the DB + storage env
# mirrored from the webapp (so it reaches `db` and reads videos from S3/MinIO):
#
#   NET=$(docker inspect -f '{{range $k,$_ := .NetworkSettings.Networks}}{{$k}}{{end}}' liveorc_webapp)
#   docker run --rm --network "$NET" \
#     --env-file /opt/LiveORC/.env \
#     -v "$PWD/reprocess_fit6.py:/tmp/reprocess_fit6.py" \
#     localdevices/liveorc bash -lc \
#       "pip install -q xarray==2024.9.0 && python /tmp/reprocess_fit6.py --site-id 4 --video-config-id 3 ... "
#   # add --commit only after the dry-run + analytics look right.
set -euo pipefail

CONTAINER="${CONTAINER:-liveorc_webapp}"
XARRAY_PIN="${XARRAY_PIN:-2024.9.0}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

docker exec "$CONTAINER" python -c "import sys,xarray; sys.exit(0 if xarray.__version__=='$XARRAY_PIN' else 1)" 2>/dev/null \
  || { echo "==> pinning xarray==$XARRAY_PIN in $CONTAINER (pyorc 0.9.4 compatibility)"; \
       docker exec "$CONTAINER" pip install -q "xarray==$XARRAY_PIN"; }

docker cp "$SCRIPT_DIR/reprocess_fit6.py" "$CONTAINER:/tmp/reprocess_fit6.py"
exec docker exec "$CONTAINER" python /tmp/reprocess_fit6.py "$@"
