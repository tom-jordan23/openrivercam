#!/bin/bash
# orc_flush_sensors.sh — recover queued sensor CSVs by flushing the upload backlog.
#
# Runs the EXISTING /usr/local/bin/orc-sensors-upload with connectivity confirmed
# up, retrying until the watermark advances. Read-only otherwise: does NOT touch
# the capture schedule, systemd services, or any config.
#
# RUN AS THE pi USER, WHILE IN MAINTENANCE MODE (so the ~2-min duty-cycle sleep
# cannot cut the flush off partway). EXIT MAINTENANCE MODE when it finishes.
#
#   ./orc_flush_sensors.sh
#
# Exit codes: 0 = flushed OK, 1 = link never came up / upload never succeeded.

set -uo pipefail

HEALTH_URL="https://openrivercam.endlessprojects.info:8443/sensors/health"
CACERT="/etc/orc/sensor-upload-ca.pem"
UPLOADER="/usr/local/bin/orc-sensors-upload"
STATE="/var/lib/orc-sensors/upload.state"
LOGDIR="/var/log/orc/sensors"
WAIT_LINK_SECS=120      # wait up to this long for LTE/DNS after boot
MAX_ATTEMPTS=6          # uploader retries once the link is up

say(){ printf '\n=== %s ===\n' "$*"; }
queued(){ find "$LOGDIR" -type f -newer "$STATE" 2>/dev/null | wc -l | tr -d ' '; }
reachable(){ curl -sS --ipv4 --cacert "$CACERT" --connect-timeout 8 --max-time 15 "$HEALTH_URL" 2>/dev/null | grep -q '"ok":true'; }

echo "orc_flush_sensors — $(date -u +%FT%TZ)  (user: $(id -un))"
echo "REMINDER: be in MAINTENANCE MODE now; EXIT it when this finishes."

# ---- sanity ----
if [ "$(id -un)" != "pi" ]; then
  echo
  echo "WARNING: not running as 'pi' (you are '$(id -un)'). Running the uploader as"
  echo "         root makes the watermark root-owned and can break the normal cycle."
  echo "         Prefer:  su - pi -c '$(readlink -f "$0")'"
  read -r -p "Continue anyway? [y/N] " a; [ "$a" = y ] || { echo "aborted."; exit 1; }
fi
for f in "$CACERT" "$UPLOADER"; do
  [ -e "$f" ] || { echo "FATAL: missing $f"; exit 1; }
done

# ---- A. wait for connectivity ----
say "A. waiting for upload endpoint (up to ${WAIT_LINK_SECS}s)"
ok=""; deadline=$(( $(date +%s) + WAIT_LINK_SECS ))
while [ "$(date +%s)" -lt "$deadline" ]; do
  if reachable; then echo "reachable."; ok=1; break; fi
  echo "  link not up yet, retrying in 5s..."; sleep 5
done
if [ -z "$ok" ]; then
  echo "FATAL: endpoint unreachable within ${WAIT_LINK_SECS}s — LTE link down. Nothing uploaded."
  exit 1
fi

# ---- B. before ----
say "B. before"
wm_before=$(stat -c %y "$STATE" 2>/dev/null || echo MISSING)
echo "watermark BEFORE: $wm_before"
echo "queued files:     $(queued)"

# ---- C. flush with retries ----
say "C. flushing backlog (up to ${MAX_ATTEMPTS} attempts)"
success=""
for i in $(seq 1 "$MAX_ATTEMPTS"); do
  echo "--- attempt $i ---"
  if "$UPLOADER"; then success=1; echo ">>> uploader completed on attempt $i"; break; fi
  echo ">>> attempt $i failed; waiting 5s and re-checking link"
  sleep 5
  reachable || echo "   (warning: link check failed before retry)"
done

# ---- D. after ----
say "D. after"
wm_after=$(stat -c %y "$STATE" 2>/dev/null || echo MISSING)
echo "watermark AFTER:  $wm_after"
echo "still queued:     $(queued)"
echo "newest local row per sensor:"
for s in sht40 rg15 ds18b20; do
  f=$(ls -t "$LOGDIR/${s}"_*.csv 2>/dev/null | head -1)
  [ -n "$f" ] && echo "  $s: $(tail -1 "$f")"
done

# ---- verdict ----
say "RESULT"
if [ -n "$success" ]; then
  echo "OK — uploader completed and watermark advanced ($wm_before -> $wm_after)."
  q=$(queued); [ "$q" -gt 0 ] && echo "($q file(s) were appended during the run; the next cycle sends them — normal.)"
  echo ">>> Now EXIT MAINTENANCE MODE."
  exit 0
fi
echo "FAILED after ${MAX_ATTEMPTS} attempts — watermark did not advance."
echo "Diagnose with:"
echo "  curl -sS --ipv4 --cacert $CACERT $HEALTH_URL ; echo"
echo "  journalctl -t orc-sensors-upload -n 20 --no-pager"
exit 1
