#!/usr/bin/env bash
# prod_reprocess.sh — run the Fit 6 reprocess against PROD LiveORC as an EPHEMERAL
# SIDECAR, so the serving webapp container is never modified.
#
# It launches a throwaway container from the same image as the running webapp, on the
# same docker network (to reach `db` + the S3/MinIO `storage`), pins a pyorc-compatible
# xarray, and runs reprocess_fit6.py. The JSONL log is written to ./reprocess-logs/ on
# the host (survives the --rm).
#
# Defaults: --site-id 4 --video-config-id 3 (Sukabumi / "Sukabumi IPB"). Anything you
# pass is appended and can override. DRY-RUN unless you pass --commit.
#
# Examples:
#   ./prod_reprocess.sh --limit 5                         # smoke dry-run (5 videos)
#   ./prod_reprocess.sh --recover                         # full dry-run (all site 4)
#   ./prod_reprocess.sh --commit --repoint --recover      # the real write (prompts first)
#   DETACH=1 ./prod_reprocess.sh --commit --repoint --recover    # long run, detached
#
# Tunables (env):
#   ENV_FILE   (default /opt/LiveORC/.env)   LiveORC env: DB + S3 creds
#   WEBAPP     (default liveorc_webapp)       running webapp container (for net+image)
#   NET, IMG   auto-detected from $WEBAPP; override if needed
#   XARRAY_PIN (default 2024.9.0)             pyorc 0.9.4 compatible xarray
#   SITE_ID, VC_ID  (default 4, 3)
#   DETACH=1   run in the background (docker run -d); follow with the printed command
#   FORCE=1    skip the --commit confirmation prompt
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="${ENV_FILE:-/opt/LiveORC/.env}"
WEBAPP="${WEBAPP:-liveorc_webapp}"
XARRAY_PIN="${XARRAY_PIN:-2024.9.0}"
SITE_ID="${SITE_ID:-4}"
VC_ID="${VC_ID:-3}"

# Use sudo for docker if the current user can't talk to the daemon (prod EC2 needs it).
DOCKER="docker"
if ! docker ps >/dev/null 2>&1; then DOCKER="sudo docker"; fi

[ -f "$SCRIPT_DIR/reprocess_fit6.py" ] || { echo "reprocess_fit6.py not next to this script"; exit 1; }
$DOCKER inspect "$WEBAPP" >/dev/null 2>&1 || { echo "webapp container '$WEBAPP' not found ($DOCKER ps)"; exit 1; }
if [ ! -r "$ENV_FILE" ] && ! sudo test -r "$ENV_FILE" 2>/dev/null; then
  echo "env file not readable: $ENV_FILE (set ENV_FILE=...)"; exit 1
fi

NET="${NET:-$($DOCKER inspect -f '{{range $k,$_ := .NetworkSettings.Networks}}{{$k}}{{end}}' "$WEBAPP")}"
IMG="${IMG:-$($DOCKER inspect -f '{{.Config.Image}}' "$WEBAPP")}"

mkdir -p "$SCRIPT_DIR/reprocess-logs"

# Confirm before any write.
if printf '%s ' "$@" | grep -qw -- --commit && [ "${FORCE:-0}" != "1" ]; then
  echo "About to run with --commit (WRITES to prod DB). Network=$NET Image=$IMG"
  echo "Make sure you ran backup_liveorc_db.sh first."
  read -r -p "Type COMMIT to proceed: " ans
  [ "$ans" = "COMMIT" ] || { echo "aborted."; exit 1; }
fi

RUNFLAGS=(--rm)
[ "${DETACH:-0}" = "1" ] && RUNFLAGS=(-d --name "orc-reprocess-$(date +%H%M%S)")

echo "==> sidecar: net=$NET image=$IMG env=$ENV_FILE  args: --site-id $SITE_ID --video-config-id $VC_ID $*"
set -x
$DOCKER run "${RUNFLAGS[@]}" --network "$NET" \
  --env-file "$ENV_FILE" \
  -e DJANGO_SETTINGS_MODULE=LiveORC.settings \
  -v "$SCRIPT_DIR/reprocess_fit6.py:/tmp/reprocess_fit6.py:ro" \
  -v "$SCRIPT_DIR/reprocess-logs:/out" \
  "$IMG" bash -lc 'pip install -q "xarray=='"$XARRAY_PIN"'" && exec python /tmp/reprocess_fit6.py "$@" --log-dir /out' \
  _ --site-id "$SITE_ID" --video-config-id "$VC_ID" "$@"
set +x

if [ "${DETACH:-0}" = "1" ]; then
  echo "==> detached. Follow:  $DOCKER logs -f \$($DOCKER ps -ql)    | log file lands in ./reprocess-logs/"
fi
