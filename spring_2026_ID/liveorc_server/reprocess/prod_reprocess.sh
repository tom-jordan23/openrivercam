#!/usr/bin/env bash
# prod_reprocess.sh — run the Fit 6 reprocess against PROD LiveORC.
#
# It runs INSIDE the running webapp container via `docker exec`, so it inherits the
# webapp's real env (prod uses local FileSystemStorage, NOT S3), DB, and media volume.
#
# pyorc 0.9.4 needs an older xarray than the image ships, AND pyorc runs velocimetry in
# a `pyorc` CLI SUBPROCESS (system python) — so a venv pin wouldn't reach it. Instead we
# install the pinned xarray into an ISOLATED dir and put it first on PYTHONPATH, which
# the subprocess inherits. The webapp's installed packages are NOT modified.
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
XPIN_DIR="/tmp/orc-xarray-pin"          # isolated xarray install (shadows via PYTHONPATH)
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

# Build the in-container command: install the pinned xarray into an isolated dir
# (--no-deps so numpy/pandas stay the system ones), prepend it to PYTHONPATH so both
# this process AND the pyorc CLI subprocess pick it up, then run the reprocessor.
INNER='set -e
mkdir -p "'"$XPIN_DIR"'" "'"$CLOG"'"
if [ ! -d "'"$XPIN_DIR"'/xarray" ]; then pip install -q --target "'"$XPIN_DIR"'" --no-deps "xarray=='"$XARRAY_PIN"'"; fi
export PYTHONPATH="'"$XPIN_DIR"'${PYTHONPATH:+:$PYTHONPATH}"
exec python /tmp/reprocess_fit6.py "$@" --log-dir "'"$CLOG"'"'

echo "==> exec in $WEBAPP (isolated xarray==$XARRAY_PIN via PYTHONPATH)  args: --site-id $SITE_ID --video-config-id $VC_ID $*"

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
