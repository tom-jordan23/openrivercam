set -u
DB=/home/pi/.ORC-OS/orc-os.db
echo "=== CHECKIN $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# Check-in of 2026-10-12: root cause of ISS-FIELD-013, first contact since the
# station came back.
#
# Server-side, already established (Grafana, 2026-10-12 12:40 UTC):
#   - sensor rows run to 10-02 23:32 WIB (16:32 UTC), buffered and uploaded
#     later. The station kept cycling through the quota outage; V-IN 12.4-12.9 V
#     on its last wakes. The battery-exhaustion hypothesis is not supported.
#   - no rows at all 10-02 23:32 -> 10-09 10:32 WIB.
#   - 10-09 10:32 WIB: power_on_reason 2 (button), one cycle, then nothing.
#   - 10-10 10:02 WIB: reason 2 again, then reason 1 (schedule) from 10:30 on.
#   This is what the 42.6-day schedule-list exhaustion predicts (TODO-116).
#
# What only the station can confirm, in priority order (the wake ends on a timer):
#   A. what the Witty Pi now has armed, and whether the schedule clock restarted
#   B. whether orc-wp5-rearm / orc-wake-ceiling are deployed, or 10-10 was by hand
#   C. wp5d.log from 10-01: the last scheduled boot, the gap, the two button boots
#   D. boot list: no boot between 10-02 16:32 and 10-09 03:32 UTC
#   E. how the 10-02 last boot and the 10-09 button boot ended
#   F. disk and backlog (the TODO-119 purge clock was due 10-04..10-07)
#
# Times on the station are UTC.
#
# READ-ONLY. wp5 is driven with option 14 (Exit) only, which prints the status
# header and changes nothing; this is pass 3 of orc-wp5-rearm. sqlite via a
# read-only URI. No network requests, nothing synced, nothing restarted.

echo
echo "=== A. Witty Pi status header (wp5, option 14 = Exit only) ==="
printf '14\n' | sudo -n timeout 20 wp5 2>&1 | sed 's/\x1b\[[0-9;]*m//g' \
  | grep -E 'Version|Schedule next|schedule script|threshold|Time|Vin|Vout' | head -20 | sed 's/^/  /'

echo
echo "=== B. re-arm and wake-ceiling deployment ==="
for u in orc-wp5-rearm.service orc-wake-ceiling.timer; do
  echo "  $u: enabled=$(systemctl is-enabled $u 2>&1) active=$(systemctl is-active $u 2>&1)"
done
ls -la /usr/local/bin/orc-wp5-rearm /usr/local/bin/orc-wake-ceiling /etc/orc-wp5-rearm.conf 2>&1 | sed 's/^/  /'
echo "  --- /var/log/orc/wp5-rearm.last ---"
cat /var/log/orc/wp5-rearm.last 2>&1 | sed 's/^/  /'
echo "  --- journal tag orc-wp5-rearm, last 10 ---"
journalctl -t orc-wp5-rearm -n 10 --no-pager -o short-iso 2>&1 | sed 's/^/  /'

echo
echo "=== C. wp5d.log from 2026-10-01 (reasons, script, alarms; not every line) ==="
awk '$1 >= "[2026-10-01"' /var/log/wp5d.log 2>/dev/null \
  | grep -iE 'reason|script|schedule|future|alarm|shutdown|daemon .* started|low voltage|recover' \
  | cut -c1-160 | sed 's/^/  /'
echo "  --- lines since 10-01: $(awk '$1 >= "[2026-10-01"' /var/log/wp5d.log 2>/dev/null | wc -l) ---"

echo
echo "=== D. boots since 10-01 (journal) ==="
journalctl --list-boots --no-pager 2>/dev/null | awk '$0 ~ /2026-10-(0[1-9]|1[0-2])/' | sed 's/^/  /'

echo
echo "=== E1. end of the last scheduled boot before the outage (10-02 ~16:30 UTC) ==="
journalctl --since '2026-10-02 16:25' --until '2026-10-02 17:15' --no-pager -o short-iso 2>/dev/null \
  | grep -iE 'wp5|witty|shutdown|power.?off|orc-|reboot|halt' | tail -25 | cut -c1-200 | sed 's/^/  /'
echo "=== E2. the 10-09 button boot (~03:32 UTC): what ran and how it ended ==="
journalctl --since '2026-10-09 03:25' --until '2026-10-09 04:15' --no-pager -o short-iso 2>/dev/null \
  | grep -iE 'wp5|witty|shutdown|power.?off|orc-|maintenance|reboot|halt' | tail -30 | cut -c1-200 | sed 's/^/  /'
echo "=== E3. the 10-10 first boot (~03:02 UTC) ==="
journalctl --since '2026-10-10 02:55' --until '2026-10-10 03:35' --no-pager -o short-iso 2>/dev/null \
  | grep -iE 'wp5|witty|shutdown|power.?off|orc-|maintenance|sudo|ssh' | tail -30 | cut -c1-200 | sed 's/^/  /'

echo
echo "=== F. disk and backlog (09-27 baseline in checkin0927) ==="
df -B1M / | sed 's/^/  /'
sqlite3 -separator '|' "file:$DB?mode=ro" "select ifnull(sync_status,'NULL'), count(*)
                                           from video group by 1 order by 2 desc;" 2>&1 | sed 's/^/  /'
python3 - <<'PY' 2>&1 | sed 's/^/  /'
import sqlite3, os
db = sqlite3.connect("file:/home/pi/.ORC-OS/orc-os.db?mode=ro", uri=True)
base = "/home/pi/.ORC-OS/uploads"
r = db.execute("select timestamp, file from video where ifnull(sync_status,'') != 'SYNCED' "
               "and ifnull(file,'') != '' order by timestamp").fetchall()
have = [(ts, f) for ts, f in r if os.path.isfile(os.path.join(base, f))]
print(f"un-synced rows with a file field: {len(r)}; file still on disk: {len(have)}")
if have:
    print(f"oldest surviving un-synced clip: {have[0][0]}  {have[0][1]}")
PY

echo
echo "=== G. throttle and link ==="
vcgencmd get_throttled 2>&1 | sed 's/^/  /'
mmcli -m 0 2>/dev/null | grep -iE "state|signal quality|access tech" | head -4 | sed 's/^/  /'
echo "=== END ==="
