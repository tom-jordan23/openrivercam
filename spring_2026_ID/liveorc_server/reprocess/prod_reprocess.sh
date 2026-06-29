#!/usr/bin/env bash
# prod_reprocess.sh — run the Fit 6 reprocess against PROD LiveORC.
#
# It runs INSIDE the running webapp container via `docker exec` (that container already
# resolves `db` and the S3/MinIO `storage` service and holds the S3 creds — a separate
# sidecar can't reliably resolve `storage`). To avoid disturbing the serving app, the
# pyorc-compatible xarray pin goes into a throwaway `--system-site-packages` VENV, so
# the webapp's own installed packages are NOT modified (only our venv shadows xarray).
#
# Defaults: --site-id 4 --video-config-id 3 (Sukabumi / "Sukabumi IPB"). Anything you
# pass is appended and can override. DRY-RUN unless you pass --commit. Logs are copied
# back to ./reprocess-logs/ on the host.
#
# Examples:
#   ./prod_reprocess.sh --limit 5                        # smoke dry-run (5 videos)
#   ./prod_reprocess.sh --recover                        # full dry-run (all site 4)
#   ./prod_reprocess.sh --commit --repoint --recover     # the real write (prompts first)
#   DETACH=1 ./prod_reprocess.sh --commit --repoint --recover   # long run, in background
#
# Tunables (env): WEBAPP (default liveorc_webapp), XARRAY_PIN (default 2024.9.0),
#   SITE_ID (4), VC_ID (3), DETACH=1 (background), FORCE=1 (skip --commit prompt).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WEBAPP="${WEBAPP:-liveorc_webapp}"
XARRAY_PIN="${XARRAY_PIN:-2024.9.0}"
SITE_ID="${SITE_ID:-4}"
VC_ID="${VC_ID:-3}"
VENV="/tmp/orc-reprocess-venv"
CLOG="/tmp/orc-reprocess-logs"          # log dir inside the container

DOCKER="docker"
if ! docker ps >/dev/null 2>&1; then DOCKER="sudo docker"; fi

[ -f "$SCRIPT_DIR/reprocess_fit6.py" ] || { echo "reprocess_fit6.py not next to this script"; exit 1; }
$DOCKER inspect "$WEBAPP" >/dev/null 2>&1 || { echo "webapp container '$WEBAPP' not found ($DOCKER ps)"; exit 1; }

# Confirm before any write.
if printf '%s ' "$@" | grep -qw -- --commit && [ "${FORCE:-0}" != "1" ]; then
  echo "About to run with --commit (WRITES to prod DB) inside container '$WEBAPP'."
  echo "Make sure you ran backup_liveorc_db.sh first."
  read -r -p "Type COMMIT to proceed: " ans
  [ "$ans" = "COMMIT" ] || { echo "aborted."; exit 1; }
fi

# Stage the (latest) reprocessor into the container.
$DOCKER cp "$SCRIPT_DIR/reprocess_fit6.py" "$WEBAPP:/tmp/reprocess_fit6.py"

# Build the in-container command: make a system-site-packages venv (so pyorc/django are
# inherited), pin xarray ONLY in that venv, run the reprocessor.
INNER='set -e
if [ ! -x "'"$VENV"'/bin/python" ]; then python -m venv --system-site-packages "'"$VENV"'"; fi
"'"$VENV"'/bin/pip" install -q "xarray=='"$XARRAY_PIN"'"
mkdir -p "'"$CLOG"'"
exec "'"$VENV"'/bin/python" /tmp/reprocess_fit6.py "$@" --log-dir "'"$CLOG"'"'

echo "==> exec in $WEBAPP (venv xarray==$XARRAY_PIN)  args: --site-id $SITE_ID --video-config-id $VC_ID $*"

if [ "${DETACH:-0}" = "1" ]; then
  $DOCKER exec -d "$WEBAPP" bash -lc "$INNER" _ --site-id "$SITE_ID" --video-config-id "$VC_ID" "$@"
  echo "==> detached. Monitor:   $DOCKER exec $WEBAPP sh -c 'tail -f $CLOG/\$(ls -t $CLOG | head -1)'"
  echo "    When done, pull logs: $DOCKER cp $WEBAPP:$CLOG/. $SCRIPT_DIR/reprocess-logs/"
  exit 0
fi

set +e
$DOCKER exec "$WEBAPP" bash -lc "$INNER" _ --site-id "$SITE_ID" --video-config-id "$VC_ID" "$@"
rc=$?
set -e

# Pull logs back to the host regardless of exit code.
mkdir -p "$SCRIPT_DIR/reprocess-logs"
$DOCKER cp "$WEBAPP:$CLOG/." "$SCRIPT_DIR/reprocess-logs/" 2>/dev/null || true
echo "==> logs in $SCRIPT_DIR/reprocess-logs/   (exit $rc)"
exit $rc
