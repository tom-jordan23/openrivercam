set -u
echo "=== REARM-FIRSTBOOT $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# 2026-10-12, test 4: first boot after orc-wp5-rearm and orc-wake-ceiling were
# deployed (17:31 UTC wake). READ-ONLY: journal, systemctl status, wp5 Exit.
# Questions: did the re-arm run on its own and succeed; how long did it hold
# orc-api back; is the wake-ceiling timer counting down; did capture still run.
#
# The runner gets in at ~35 s, when the re-arm (33 s by hand) may still be
# running and capture has not started. Wait to ~110 s of uptime; ORC-OS ended
# the 17:30 wake with this script's predecessor still connected at ~87 s, and
# its task now starts ~33 s later, so its shutdown should be ~160 s.
while [ "$(cut -d. -f1 /proc/uptime)" -lt 110 ]; do sleep 2; done
echo "waited to uptime $(cut -d' ' -f1 /proc/uptime)s"

echo
echo "=== A. re-arm this boot ==="
journalctl -b -t orc-wp5-rearm --no-pager -o short-iso 2>&1 | sed 's/^/  /'
echo "  result: $(systemctl show -p Result --value orc-wp5-rearm.service)"
systemctl show orc-wp5-rearm.service -p ExecMainStartTimestamp -p ExecMainExitTimestamp 2>&1 | sed 's/^/  /'
echo "  --- wp5-rearm.last ---"
cat /var/log/orc/wp5-rearm.last 2>&1 | sed 's/^/  /'

echo
echo "=== B. ordering: when did orc-api start (monotonic, s since boot) ==="
for u in wp5d.service orc-wp5-rearm.service orc-api.service orc-sensors.timer; do
  echo "  $u: active_enter=$(systemctl show -p ActiveEnterTimestampMonotonic --value $u 2>/dev/null | awk '{printf "%.1f", $1/1e6}')s inactive_enter=$(systemctl show -p InactiveEnterTimestampMonotonic --value $u 2>/dev/null | awk '{printf "%.1f", $1/1e6}')s"
done

echo
echo "=== C. wake-ceiling timer ==="
systemctl list-timers orc-wake-ceiling.timer --all --no-pager 2>&1 | sed 's/^/  /'

echo
echo "=== D. Witty Pi header ==="
printf '14\n' | sudo -n timeout 20 wp5 2>&1 | sed 's/\x1b\[[0-9;]*m//g' \
  | grep -E 'Schedule next|schedule script' | sed 's/^/  /'

echo
echo "=== E. capture this boot ==="
journalctl -b --no-pager -o short-iso 2>/dev/null \
  | grep -E 'capture_result|Syncing to remote site|Shutdown triggered' | cut -c1-180 | tail -6 | sed 's/^/  /'
echo "=== END ==="
