#!/usr/bin/env bash
# prod_analytics.sh — run the before/after impact report on a reprocess log.
# Defaults to the most recent log in ./reprocess-logs/. Writes a report dir next to it.
#
#   ./prod_analytics.sh                       # newest log
#   ./prod_analytics.sh reprocess-logs/reprocess_dry_<stamp>.jsonl
#
# Plots need matplotlib; without it you still get the full text report.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG="${1:-$(ls -t "$SCRIPT_DIR"/reprocess-logs/*.jsonl 2>/dev/null | head -1)}"
[ -n "${LOG:-}" ] && [ -f "$LOG" ] || { echo "no log found (pass one explicitly)"; exit 1; }
OUT="$SCRIPT_DIR/report-$(basename "$LOG" .jsonl)"
python3 "$SCRIPT_DIR/analytics_reprocess.py" "$LOG" --out "$OUT"
echo "==> report: $OUT/REPORT.md"
