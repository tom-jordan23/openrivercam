set -u
# ISS-FIELD-015: verify the clock floor after install (plan section 9). READ-ONLY (journal reads may retry with sudo -n). Run through
# todo119_wake_runner.py in the first wake AFTER the install, and again one wake later (to see the shutdown-time `save`). UTC.
main() {
sec() { echo; echo "=== $1 ==="; }
FLOOR_BIN=/usr/local/bin/orc-clock-floor
echo "=== FLOOR VERIFY $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
up=$(cut -d' ' -f1 /proc/uptime | cut -d. -f1); echo "uptime s: $up   free: $(df -B1M --output=avail,pcent / | tail -1)"

sec "1. the unit this boot"
echo "  enabled=$(systemctl is-enabled orc-clock-floor.service 2>&1)  active=$(systemctl is-active orc-clock-floor.service 2>&1)  result=$(systemctl show orc-clock-floor.service -p Result --value 2>&1)"
systemctl show orc-clock-floor.service -p ActiveEnterTimestamp -p ExecMainStartTimestamp -p ExecMainExitTimestamp -p ExecMainStatus 2>&1 | sed 's/^/  /'
echo "  failed units: $(systemctl --failed --no-legend 2>/dev/null | wc -l)"; systemctl --failed --no-legend 2>/dev/null | cut -c1-150 | sed 's/^/    /'
echo "  journal (tag orc-clock-floor, this boot):"
j=$(timeout 20 journalctl -t orc-clock-floor -b --no-pager 2>&1); case "$j" in *"insufficient permissions"*|*"No journal files"*) j=$(timeout 20 sudo -n journalctl -t orc-clock-floor -b --no-pager 2>&1);; esac
printf '%s\n' "$j" | tail -12 | cut -c1-220 | sed 's/^/    /'

sec "2. what restore decided, and the floor file"
echo "  state file:"; sed 's/^/    /' /run/orc-clock-floor/state 2>&1
echo "  floor file: $(cat /var/lib/orc-clock-floor/floor 2>&1)   (as a time: $(date -u -d @$(cat /var/lib/orc-clock-floor/floor 2>/dev/null) '+%F %T' 2>&1))"
echo "  clock now : $(date -u +%s)   ($(date -u '+%F %T'))   chrony: $(timeout 5 chronyc tracking 2>&1 | grep -E 'Stratum|Leap status' | tr '\n' ';')"
echo "  RTC copy that wp5d made this boot:"; tr -d '\000' < /var/log/wp5d.log 2>/dev/null | grep -a "RTC\|system time\|SYS" | tail -3 | cut -c1-160 | sed 's/^/    /'

sec "3. boot ordering and cost"
echo "  critical chain of orc-api.service (before install it was @27.98s):"; systemd-analyze critical-chain orc-api.service 2>&1 | sed -n 1,10p | cut -c1-120 | sed 's/^/    /'
echo "  slowest units this boot:"; systemd-analyze blame 2>&1 | head -6 | sed 's/^/    /'
echo "  orc-clock-floor in blame: $(systemd-analyze blame 2>&1 | grep -i clock-floor)"

sec "4. sensors still logging with the new logger"
echo "  logger: $(sha256sum /usr/local/lib/orc-sensors/sensors_logger.py | cut -c1-16)  (new build hash starts 4bb8f93a)"
for f in /var/log/orc/sensors/sht40_$(date -u +%F).csv /var/log/orc/sensors/wittypi_$(date -u +%F).csv; do
  echo "  $f: $(wc -l < "$f" 2>&1) lines; last: $(tail -1 "$f" 2>&1 | cut -c1-110)"
done
echo "  orc-sensors service, last 8 journal lines:"; timeout 15 journalctl -u orc-sensors.service -n 8 --no-pager 2>&1 | cut -c1-170 | sed 's/^/    /'
echo "  any 'Traceback' or 'Error' from the logger in the last 30 min: $(timeout 15 journalctl -u orc-sensors.service --since '30 min ago' --no-pager 2>&1 | grep -ci 'traceback\|error')"
sec "5. did the previous wake's rows reach the station files and the uploader? (watermark = mtime of upload.state; files newer than it are PUT)"
echo "  upload.state mtime: $(stat -c '%y' /var/lib/orc-sensors/upload.state 2>&1)"
echo "  today's CSVs by mtime (newest first):"; ls -l --time-style=full-iso -t /var/log/orc/sensors/*_$(date -u +%F).csv 2>&1 | head -8 | awk '{print "    "$6" "$7" "$5" "$9}'
echo "  rows stamped 18:3x UTC today (the 18:30 wake), first 8:"; grep -h "$(date -u +%F)T18:3" /var/log/orc/sensors/*_$(date -u +%F).csv 2>/dev/null | head -8 | cut -c1-90 | sed 's/^/    /'
echo "  uploader / capture journal, last 45 min (tag orc-sensors-upload, orc-capture):"
u=$(timeout 20 journalctl --since '45 min ago' --no-pager 2>&1); case "$u" in *"insufficient permissions"*|*"No journal files"*) u=$(timeout 20 sudo -n journalctl --since '45 min ago' --no-pager 2>&1);; esac
printf '%s\n' "$u" | grep -i "orc-sensors-upload\|orc-capture" | tail -24 | cut -c1-200 | sed 's/^/    /'
echo; echo "=== END ==="
}
main </dev/null
