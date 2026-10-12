set -u
echo "=== REARM-LISTPASS $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# 2026-10-12, test 1 part 2: run orc-wp5-rearm's pass 1 (option 6, empty
# answer, Exit) once and keep the raw output, so the script's parsing can be
# tested offline against the real menu. Tom approved test 1.
#
# Why this is a no-op: wp5 v5.0.0 (uugear/Witty-Pi-5-Software 79f4e83, wp5.c
# choose_schedule_script) only uploads a name and sends CHOOSE_SCRIPT when
# request_input_number() returns true; input_number() returns false on an
# empty line. Listing does send the Witty Pi a LIST_FILES admin command, which
# reads its schedule directory and changes no setting.
#
# The status header is read before and after; the next shutdown/startup and
# "(in use)" must be identical, or the assumption above is wrong.

hdr() { printf '14\n' | sudo -n timeout 20 wp5 2>&1 | sed 's/\x1b\[[0-9;]*m//g' \
          | grep -E 'Version|Schedule next|schedule script' | sed 's/^/  /'; }

echo
echo "=== A. header before ==="
hdr

echo
echo "=== B. raw pass-1 output (6, empty, 14), exactly as orc-wp5-rearm feeds it ==="
t0=$(date +%s.%N)
printf '6\n\n14\n' | sudo -n timeout 30 wp5 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | cat -A
echo "  exit: ${PIPESTATUS[1]}  elapsed: $(awk -v a="$t0" -v b="$(date +%s.%N)" 'BEGIN{printf "%.1f", b-a}')s"

echo
echo "=== C. header after (must match A) ==="
hdr
echo "=== END ==="
