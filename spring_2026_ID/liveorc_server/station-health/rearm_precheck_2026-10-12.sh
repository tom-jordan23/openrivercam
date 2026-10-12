set -u
echo "=== REARM-PRECHECK $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# 2026-10-12, test 1 (part 1 of 2) before deploying orc-wp5-rearm and
# orc-wake-ceiling (9b2e78f). Tom approved.
#
# Part 1 (this wake) is strictly read-only:
#   A. the vendor wp5 source, so we can read what option 6 does with an empty
#      answer BEFORE anything feeds it one (orc-wp5-rearm's pass 1 assumes it
#      is a no-op; nobody has confirmed that)
#   B. wp5d_poweroff.service, which orc-wake-ceiling relies on to arm the next
#      startup when it runs `systemctl poweroff`
#   C. systemd-analyze verify on the three new units, from the pulled checkout
#      (verify only parses; nothing is installed or loaded)
# Part 2 (a later wake, only if A shows it is safe): run the option-6 list
# pass and capture its raw output.

REPO=/home/pi/code/git/openrivercam/spring_2026_ID/pi/sukabumi

echo
echo "=== B. wp5d_poweroff.service and wp5d ==="
systemctl cat wp5d_poweroff.service 2>&1 | head -30 | sed 's/^/  /'
echo "  enabled=$(systemctl is-enabled wp5d_poweroff.service 2>&1)"
systemctl cat wp5d.service 2>&1 | grep -vE '^\s*#|^\s*$' | head -20 | sed 's/^/  /'

echo
echo "=== C. systemd-analyze verify (new units, from the checkout) ==="
for u in orc-wp5-rearm.service orc-wake-ceiling.service orc-wake-ceiling.timer; do
  echo "  --- $u ---"
  timeout 30 systemd-analyze verify "$REPO/etc/systemd/system/$u" 2>&1 | head -10 | sed 's/^/    /'
  echo "    exit: ${PIPESTATUS[0]}"
done
echo "  --- units named in After/Before exist? ---"
for u in wp5d.service orc-api.service orc-sensors.timer; do
  echo "  $u: $(systemctl show -p LoadState --value $u 2>&1)"
done

echo
echo "=== A. vendor wp5 source ==="
W=$(command -v wp5 2>&1); R=$(readlink -f "$W" 2>&1)
echo "  wp5: $W -> $R"
file "$R" 2>&1 | sed 's/^/  /'
dpkg -S "$R" 2>&1 | head -2 | sed 's/^/  /'
DIR=$(dirname "$R")
# Files the menu sources, then the menu itself, then those files. Text only,
# each capped so a surprise binary or huge file cannot eat the window.
SRC=$(grep -hoE '^\s*(source|\.)\s+[^ ;]+' "$R" 2>/dev/null | awk '{print $2}' | sort -u)
echo "  sourced: $SRC"
for f in "$R" $SRC; do
  f=$(eval echo "$f" 2>/dev/null)
  [ -f "$f" ] || f="$DIR/$(basename "$f")"
  echo
  echo "##### FILE $f ($(wc -c < "$f" 2>/dev/null) bytes) #####"
  if file "$f" 2>/dev/null | grep -q text; then
    head -c 200000 "$f"
  else
    echo "(not text; skipped)"
  fi
done
echo
echo "=== END ==="
