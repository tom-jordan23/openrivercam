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
sec "6. VIDEO pipeline (a separate path from the sensor rows): ORC-OS DB rows and files, last 3 hours"
DB=/home/pi/.ORC-OS/orc-os.db; V=/home/pi/.ORC-OS/uploads/videos
if command -v sqlite3 >/dev/null && [ -r "$DB" ]; then
  echo "  newest 8 video rows (id | timestamp | status | sync_status):"
  sqlite3 -separator ' | ' "file:$DB?mode=ro" "SELECT id,timestamp,status,ifnull(sync_status,'NULL') FROM video ORDER BY id DESC LIMIT 8;" 2>&1 | sed 's/^/    /'
  echo "  last 3 hours by (status, sync_status):"
  sqlite3 -separator ' | ' "file:$DB?mode=ro" "SELECT status, ifnull(sync_status,'NULL'), count(*) FROM video WHERE timestamp > datetime('now','-3 hours') GROUP BY 1,2;" 2>&1 | sed 's/^/    /'
  echo "  sync_status totals now: $(sqlite3 -separator '=' "file:$DB?mode=ro" "SELECT s, n FROM (SELECT ifnull(sync_status,'NULL') AS s, count(*) AS n FROM video GROUP BY ifnull(sync_status,'NULL'));" 2>&1 | tr '\n' ' ')"
fi
echo "  mp4 files written in the last 3 hours (time size path):"
timeout 30 find "$V" -xdev -name '*.mp4' -mmin -180 -printf '    %TY-%Tm-%Td %TT %s %P\n' 2>/dev/null | sort | tail -8
echo "  sync lines in the orc-api journal, last 2 hours:"
sj=$(timeout 25 journalctl -u orc-api --since '2 hours ago' --no-pager 2>&1); case "$sj" in *"insufficient permissions"*|*"No journal files"*) sj=$(timeout 25 sudo -n journalctl -u orc-api --since '2 hours ago' --no-pager 2>&1);; esac
printf '%s\n' "$sj" | grep -i "sync\|upload\|queue" | tail -10 | cut -c1-210 | sed 's/^/    /'
sec "7. early-boot guard: rows deferred this boot, and any row stamped inside the floor-clock window (there should be none)"
fl=$(cat /var/lib/orc-clock-floor/floor 2>/dev/null)
if [ -n "$fl" ]; then
  lo=$(date -u -d "@$fl" +%Y-%m-%dT%H:%M:%S); hi=$(date -u -d "@$((fl + 120))" +%Y-%m-%dT%H:%M:%S)
  echo "  floor file = $lo (the previous shutdown). Rows in today's CSVs stamped in ($lo, $hi]:"
  n=0; for f in /var/log/orc/sensors/*_$(date -u +%F).csv; do
    awk -F, -v lo="$lo" -v hi="$hi" -v f="$(basename "$f")" 'NR>1 && substr($1,1,19) > lo && substr($1,1,19) <= hi {print "    MISLABELLED? " f ": " substr($0,1,90)}' "$f"
  done | tee /dev/stderr 2>/dev/null | wc -l | sed 's/^/  count: /'
fi
echo "  'deferred' lines this boot (journal; the stamps on early lines come from the floor-set clock):"
dj=$(timeout 25 journalctl -b --no-pager 2>&1); case "$dj" in *"insufficient permissions"*|*"No journal files"*) dj=$(timeout 25 sudo -n journalctl -b --no-pager 2>&1);; esac
printf '%s\n' "$dj" | grep -i "deferred" | head -12 | cut -c1-220 | sed 's/^/    /'
echo "  deferred lines: $(printf '%s\n' "$dj" | grep -ci 'deferred')   guard state now: $(PYTHONDONTWRITEBYTECODE=1 python3 -I -c "
import importlib.util, sys
sys.dont_write_bytecode = True
sp = importlib.util.spec_from_file_location('sl', '/usr/local/lib/orc-sensors/sensors_logger.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
print('uptime', m._uptime_s(), 'restored', m._floor_set_clock(), 'synced', m._chrony_synced(), 'untrusted', m.clock_untrusted())" 2>&1)"
echo "  which sensor rows were written this boot, by journal time (orc-capture-sensors / orc-sensors):"
printf '%s\n' "$dj" | grep -i "\[orc-sensors\] \(orccapture\|wittypi\|sht40\|rg15\|ds18b20\):" | cut -c1-120 | head -12 | sed 's/^/    /'
echo; echo "=== END ==="
}
main </dev/null
