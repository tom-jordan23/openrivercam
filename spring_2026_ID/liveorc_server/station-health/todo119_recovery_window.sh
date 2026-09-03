set -u
echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# The outage ran 2026-09-02 13:32 -> ~2026-09-03 01:30 UTC and cleared with no
# intervention. Probing DNS and routing NOW measures a healthy system, so the
# only place the cause survives is the journal across the recovery moment.
#
# Priority order, because the wake is ~85 s and ends on a timer: the recovery
# window first, a healthy-state baseline second.
#
# READ-ONLY.

echo "=== A. the recovery window, 01:00-02:00 UTC — what changed ==="
journalctl --since "2026-09-03 01:00:00" --until "2026-09-03 02:00:00" --no-pager 2>/dev/null \
  | grep -iE "modem|mmcli|ModemManager|wwan|bearer|dns|resolve|network is unreachable|tailscal|sensors-upload|sync" \
  | head -60 | sed 's/^/  /'

echo
echo "=== B. did the modem re-attach or the bearer change, any time in the outage ==="
journalctl --since "2026-09-02 13:00:00" --no-pager 2>/dev/null \
  | grep -iE "ModemManager|bearer|registered|disconnect|reattach|APN|state changed" \
  | head -40 | sed 's/^/  /'

echo
echo "=== C. last failure and first success, orc-sensors-upload ==="
echo "  --- last WARN before recovery ---"
journalctl --since "2026-09-03 00:00:00" --no-pager 2>/dev/null \
  | grep -iE "orc-sensors-upload failed|sensors-upload" | head -20 | sed 's/^/    /'

echo
echo "=== D. healthy-state baseline, for comparison at the next recurrence ==="
H=openrivercam.endlessprojects.info
echo "  resolv.conf:"; grep -vE "^#|^$" /etc/resolv.conf 2>/dev/null | sed 's/^/    /'
echo "  getent v4: $(getent ahostsv4 $H 2>&1 | awk '{print $1}' | sort -u | tr '\n' ' ')"
echo "  getent v6: $(getent ahostsv6 $H 2>&1 | awk '{print $1}' | sort -u | tr '\n' ' ')"
echo "  default v4: $(ip -4 route show default 2>/dev/null | head -1)"
echo "  wwan0 v4: $(ip -4 -o addr show wwan0 2>/dev/null | awk '{print $4}' | tr '\n' ' ')"
mmcli -m 0 2>/dev/null | grep -iE "state|signal|access tech|operator" | head -5 | sed 's/^/    /'

echo
echo "=== E. did the video backlog change, or is it still starved ==="
sqlite3 -column /home/pi/.ORC-OS/orc-os.db \
  "select ifnull(sync_status,'NULL'), count(*) from video group by 1 order by 2 desc;" 2>&1 | sed 's/^/  /'
echo "  (FAILED was 2995 during the outage. If it is still climbing, new clips"
echo "   are failing; if it stopped and SYNCED is rising, live sync recovered."
echo "   Either way the historic FAILED backlog is NOT retried - schedulers.py:35.)"
echo "=== END ==="
