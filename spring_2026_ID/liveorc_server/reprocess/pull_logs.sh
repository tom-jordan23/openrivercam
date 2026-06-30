#!/usr/bin/env bash
# pull_logs.sh — recover a detached/overnight reprocess run's results.
#
# A DETACH=1 run writes its JSONL/.progress to /tmp/orc-reprocess-logs INSIDE the
# webapp container and does NOT auto-copy them to the host (unlike a foreground run).
# This pulls them out, tells you whether the run is still going, and — crucially —
# whether it was a DRY-RUN or a real --commit, plus the per-status counts.
#
# Read-only on the DB: it only inspects the container and copies log files to the host.
#
#   ./pull_logs.sh
#
# Tunables (env): WEBAPP (liveorc_webapp), CLOG (/tmp/orc-reprocess-logs).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WEBAPP="${WEBAPP:-liveorc_webapp}"
CLOG="${CLOG:-/tmp/orc-reprocess-logs}"
DEST="$SCRIPT_DIR/reprocess-logs"

DOCKER="docker"
if ! docker ps >/dev/null 2>&1; then DOCKER="sudo docker"; fi
$DOCKER inspect "$WEBAPP" >/dev/null 2>&1 || { echo "webapp container '$WEBAPP' not found ($DOCKER ps)"; exit 1; }

echo "== Is a reprocess still running? =="
if $DOCKER exec "$WEBAPP" sh -c 'ps -eo pid,etime,cmd | grep [r]eprocess_fit6'; then
  echo "  -> STILL RUNNING (above). The .jsonl below is partial; re-run this when ps is empty."
else
  echo "  -> not running (finished, or never started)."
fi

echo
echo "== Latest progress line (% done + ETA) =="
$DOCKER exec "$WEBAPP" sh -c "cat $CLOG/*.progress 2>/dev/null || echo '  (no .progress yet)'"

echo
echo "== Log files in the container ($CLOG) =="
if ! $DOCKER exec "$WEBAPP" sh -c "ls -la $CLOG 2>/dev/null"; then
  echo "  (nothing in $CLOG — the overnight job may have used a different WEBAPP/CLOG)"
  exit 1
fi

echo
echo "== Pulling them to the host ($DEST) =="
mkdir -p "$DEST"
$DOCKER cp "$WEBAPP:$CLOG/." "$DEST/"
echo "  done."

# Summarize the newest log we just pulled.
NEWEST="$(ls -t "$DEST"/*.jsonl 2>/dev/null | head -1 || true)"
[ -n "${NEWEST:-}" ] || { echo "No .jsonl on host after copy."; exit 0; }

echo
echo "== Newest log: $(basename "$NEWEST") =="
case "$(basename "$NEWEST")" in
  reprocess_commit_*) echo "  MODE: --commit  ***this run WROTE to the prod DB***" ;;
  reprocess_dry_*)    echo "  MODE: dry-run   (DB untouched)" ;;
  *)                  echo "  MODE: unknown (unexpected filename)" ;;
esac
echo "  videos in log: $(wc -l < "$NEWEST")"
echo "  status breakdown:"
# group by the JSON "status" field without needing jq
grep -o '"status": *"[^"]*"' "$NEWEST" | sed 's/.*"status": *"//;s/"//' \
  | sort | uniq -c | sed 's/^/    /'

echo
echo "Next: ./prod_analytics.sh   (reads this newest log)"
