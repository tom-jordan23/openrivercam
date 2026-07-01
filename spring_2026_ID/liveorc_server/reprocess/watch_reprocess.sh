#!/usr/bin/env bash
# watch_reprocess.sh — live progress monitor for a detached reprocess run.
#
# Polls the running reprocess and prints a timestamped progress line every
# INTERVAL seconds, then stops automatically when the run finishes. It reads
# the NEWEST reprocess_commit_*.progress inside the webapp container, so you
# don't have to know the run's timestamp.
#
# Read-only: only inspects the container. Ctrl-C stops the watcher, NOT the
# reprocess (that runs detached inside the container).
#
#   ./watch_reprocess.sh                 # watch the newest commit run
#   KIND=dry ./watch_reprocess.sh        # watch a dry-run instead
#   INTERVAL=60 ./watch_reprocess.sh     # poll every 60s (default 30)
#
# Tunables (env): WEBAPP (liveorc_webapp), CLOG (/tmp/orc-reprocess-logs),
#   KIND (commit|dry, default commit), INTERVAL (seconds, default 30).
set -euo pipefail

WEBAPP="${WEBAPP:-liveorc_webapp}"
CLOG="${CLOG:-/tmp/orc-reprocess-logs}"
KIND="${KIND:-commit}"
INTERVAL="${INTERVAL:-30}"

DOCKER="docker"
if ! docker ps >/dev/null 2>&1; then DOCKER="sudo docker"; fi

# newest matching .progress file inside the container (empty string if none yet)
newest_progress() {
  $DOCKER exec "$WEBAPP" sh -c "ls -t $CLOG/reprocess_${KIND}_*.progress 2>/dev/null | head -1"
}
running() {
  $DOCKER exec "$WEBAPP" sh -c 'ps -eo args | grep -q "[r]eprocess_fit6"'
}

echo "watching newest reprocess_${KIND}_*.progress in $WEBAPP (every ${INTERVAL}s; Ctrl-C to stop the watcher only)"
while running; do
  pf="$(newest_progress || true)"
  if [ -n "$pf" ]; then
    line="$($DOCKER exec "$WEBAPP" cat "$pf" 2>/dev/null || true)"
    echo "[$(date +%H:%M:%S)] ${line:-<no progress line yet>}"
  else
    echo "[$(date +%H:%M:%S)] <no .progress file yet — first video still processing>"
  fi
  sleep "$INTERVAL"
done

echo "== reprocess not running =="
pf="$(newest_progress || true)"
[ -n "$pf" ] && $DOCKER exec "$WEBAPP" cat "$pf" || echo "(no progress file found)"
echo "Next: ./pull_logs.sh && ./prod_analytics.sh"
