set -u
# ISS-FIELD-015: plain data collection, 2026-11-12. Run through todo119_wake_runner.py.
# READ-ONLY and HARDWARE-FREE: it copies, lists and counts. No wp5, no I2C, no chronyc, no
# writes, no ORC-OS API/database. No analysis logic on purpose; analysis happens on the workstation.
# Most time-sensitive question first: ORC-OS deletes the OLDEST videos first (sync-blind) once free
# space < min_free_space (5.0 GB), the disk is ~90% full, and the offline wakes' videos carry
# January dates, so they sit at the front of that queue.
# Big encoded artifacts come LAST so a short wake loses only those.
main() {
sec() { echo; echo "=== $1 ==="; }
V=/home/pi/.ORC-OS/uploads/videos
echo "=== ISS015 DATA GRAB $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime s: $(cut -d' ' -f1 /proc/uptime)"

sec "1. DISK"
df -B1 / | sed 's/^/  /'; df -h / | sed 's/^/  /'

sec "2. VIDEOS BY DATE DIRECTORY (files, mp4 count, bytes; oldest first)"
timeout 45 find "$V" -type f -printf '%P %s\n' 2>/dev/null | awk '{split($1,a,"/"); d=a[1]; n[d]++; b[d]+=$2; if ($1 ~ /\.mp4$/) m[d]++} END{for(d in n) printf "  %s files=%d mp4=%d bytes=%d\n", d, n[d], m[d], b[d]}' | sort
echo "  total files: $(timeout 30 find "$V" -type f 2>/dev/null | wc -l)"

sec "3. ORC-OS DISK MANAGER: where min_free_space is set and how it picks what to delete"
timeout 20 grep -rIn "min_free_space" /home/pi/.ORC-OS 2>/dev/null | grep -v '\.log:' | head -8 | cut -c1-200 | sed 's/^/  /'
F=$(timeout 40 grep -rIl "min_free_space" /home/pi/venv/orc-os/lib 2>/dev/null | grep -E '\.py$' | head -3)
echo "  code files mentioning it: ${F:-none found}"
for f in $F; do
  echo "  -- $f"
  grep -n -B4 -A40 "min_free_space" "$f" 2>/dev/null | grep -viE 'pass|token|secret' | head -110 | cut -c1-170 | sed 's/^/    /'
done

sec "4. UNITS AND ENVIRONMENT (secrets masked)"
for u in orc-api orc-sensors.timer orc-sensors.service chrony wp5d orc-capture.service orc-wake-ceiling.timer; do
  echo "  -- $u"; systemctl cat "$u" 2>&1 | grep -vE '^\s*(#|$)' | grep -viE 'pass|token|secret|key' | head -24 | sed 's/^/    /'
done
echo "  -- critical chain of orc-api.service"; systemd-analyze critical-chain orc-api.service --no-pager 2>&1 | head -24 | sed 's/^/    /'
echo "  python: $(python3 --version 2>&1)"; echo "  $(uptime)"; free -m | sed 's/^/  /'
echo "  rearm state:"; ls -la /var/lib/orc-wp5-rearm 2>&1 | sed 's/^/    /'; cat /var/log/orc/wp5-rearm.last 2>&1 | sed 's/^/    /'; grep -vE '^\s*(#|$)' /etc/orc-wp5-rearm.conf 2>&1 | sed 's/^/    /'
echo "  /var/lib/chrony and /var/lib/orc-sensors:"; ls -la /var/lib/chrony /var/lib/orc-sensors 2>&1 | sed 's/^/    /'

sec "5. ARTIFACT: wp5d.log, filtered to startups, shutdowns, I2C lines, signals, button, daemon starts (gzip+base64)"
if [ -r /var/log/wp5d.log ]; then
  echo "  raw lines in the log: $(tr -d '\000' < /var/log/wp5d.log | wc -l)   bytes: $(stat -c %s /var/log/wp5d.log)"
  echo "BEGIN_WP5D_B64"; tr -d '\000' < /var/log/wp5d.log | grep -a -E 'Startup reason|Shutdown reason|i2c_|Detected shutdown|Caught signal|daemon V|RTC has|Button' | gzip -9 -c | base64 -w0; echo; echo "END_WP5D_B64"
else echo "  /var/log/wp5d.log not readable"; fi

sec "6. ARTIFACT: journalctl --list-boots (gzip+base64)"
echo "BEGIN_BOOTS_B64"; { journalctl --list-boots --no-pager 2>/dev/null || sudo -n journalctl --list-boots --no-pager 2>/dev/null; } | gzip -9 -c | base64 -w0; echo; echo "END_BOOTS_B64"

echo; echo "=== ISS015 DATA GRAB DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
}
main < /dev/null
