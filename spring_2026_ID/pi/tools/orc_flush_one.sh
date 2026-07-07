#!/bin/bash
# orc_flush_one.sh — upload local CSVs for ONE sensor directly (idempotent).
#
# Targets a single sensor so a short wake window is enough, and does NOT
# fail-fast: it continues past a failed file, so every run makes forward
# progress. Bypasses the shared upload watermark (leaves it untouched).
# Read-only otherwise: no schedule/service/config changes.
#
#   ./orc_flush_one.sh [sensor] [since-date]
#     sensor      sensor prefix to upload   (default: sht40)
#     since-date  only files dated >= this  (default: all; e.g. 2026-06-19)
#
# Run as pi. Waits up to 90s for the LTE link, then uploads oldest-first.

set -uo pipefail
SENSOR="${1:-sht40}"
SINCE="${2:-}"
CACERT="/etc/orc/sensor-upload-ca.pem"
LOGDIR="/var/log/orc/sensors"
BASE="https://openrivercam.endlessprojects.info:8443/sensors"
STATION="$(hostname | sed 's/^orc-//')"

# --- token (from pi's per-site deploy file) ---
UPLOAD_TOKEN=""
for f in /home/pi/.orc_deploy_*; do [ -f "$f" ] && . "$f"; done
[ -n "${UPLOAD_TOKEN:-}" ] || { echo "FATAL: UPLOAD_TOKEN not found in /home/pi/.orc_deploy_*"; exit 1; }
[ -r "$CACERT" ] || { echo "FATAL: CA cert $CACERT not readable"; exit 1; }

# --- wait for link (up to 90s) ---
echo "waiting for upload endpoint..."
up=""
for i in $(seq 1 18); do
  if curl -sf --ipv4 --cacert "$CACERT" --connect-timeout 8 --max-time 12 "$BASE/health" >/dev/null 2>&1; then
    up=1; echo "link up."; break
  fi
  sleep 5
done
[ -n "$up" ] || { echo "FATAL: endpoint unreachable within 90s — LTE down. Nothing uploaded."; exit 1; }

# --- select files (oldest-first; optional since-date filter) ---
files=$(ls "$LOGDIR/${SENSOR}"_*.csv 2>/dev/null | sort | awk -F'[_.]' -v s="$SINCE" 's=="" || $2>=s')
[ -n "$files" ] || { echo "no $SENSOR files matching (since='${SINCE:-any}')"; exit 1; }
n=$(printf '%s\n' "$files" | wc -l | tr -d ' ')
echo "uploading $n ${SENSOR} file(s) to $BASE/upload/$STATION/  (since='${SINCE:-any}')"

ok=0; fail=0
while IFS= read -r f; do
  fn=$(basename "$f")
  if curl -sS -X PUT --ipv4 --data-binary "@${f}" \
       -H "Authorization: Bearer ${UPLOAD_TOKEN}" -H "Content-Type: text/csv" -H "Connection: close" \
       --cacert "$CACERT" --connect-timeout 10 --max-time 20 --fail --output /dev/null \
       "$BASE/upload/$STATION/$fn"; then
    ok=$((ok+1)); echo "  ok   $fn"
  else
    rc=$?; fail=$((fail+1)); echo "  FAIL $fn (curl exit $rc)"
  fi
done <<< "$files"

echo
echo "done: $ok uploaded, $fail failed"
[ "$fail" -eq 0 ] && echo "ALL $SENSOR files up. (If in maintenance mode, exit it now.)"
[ "$fail" -eq 0 ]
