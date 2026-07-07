#!/bin/bash
# orc_collect.sh — READ-ONLY diagnostic collector for the ORC sensor pipeline.
#
# Gathers everything needed to root-cause the sensor-upload / logger gaps into
# a single text file for scp. Does NOT restart services, run the uploader,
# advance any watermark, or touch the Witty Pi schedule. Safe to run while the
# station is actively capturing. Run with sudo so it can read root-owned logs.
#
#   sudo bash /tmp/orc_collect.sh
#
# The only "active" probes are: an i2cdetect bus scan, vcgencmd reads, and a
# GET to the /sensors/health endpoint. All read-only. Delete those lines if you
# want a purely passive run.

OUT="/tmp/orc_collect_$(hostname)_$(date -u +%Y%m%dT%H%M%SZ).txt"

run(){
  echo
  echo "\$ $1"
  timeout 60 bash -c "$1" 2>&1 | sed 's/^/    /'
  rc=${PIPESTATUS[0]}
  [ "$rc" = 0 ] || echo "    [rc=$rc]"
}
hdr(){ echo; echo; echo "################################################################"; echo "## $1"; echo "################################################################"; }

{
echo "ORC sensor pipeline diagnostic bundle"
echo "collected (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "host: $(hostname)   user: $(id -un)"
echo "NOTE: read-only collection. No services restarted, no uploads run, no schedule changed."

hdr "1. HOST / CLOCK  (clock matters: is_due() compares CSV timestamps)"
run 'uname -a; uptime'
run 'date -u "+%Y-%m-%dT%H:%M:%SZ (UTC)"; date "+%F %T %Z (local)"'
run 'timedatectl'

hdr "2. DISK  (a full /var silently stops CSV writes)"
run 'df -h'
run 'df -i | grep -E "Filesystem|/$|/var"'
run 'du -sh /var/log/orc/sensors 2>/dev/null'

hdr "3. LOCAL SENSOR CSVs  (the ground truth: what is still being written?)"
run 'ls -la --time-style=full-iso /var/log/orc/sensors/'
run 'for s in sht40 rg15 ds18b20; do echo "$s: count=$(ls /var/log/orc/sensors/${s}_*.csv 2>/dev/null | wc -l) first=$(ls /var/log/orc/sensors/${s}_*.csv 2>/dev/null | head -1 | xargs -r basename) last=$(ls /var/log/orc/sensors/${s}_*.csv 2>/dev/null | tail -1 | xargs -r basename)"; done'
run 'today=$(date +%F); for s in sht40 rg15 ds18b20; do f=/var/log/orc/sensors/${s}_${today}.csv; if [ -f "$f" ]; then echo "$s TODAY ($today): $(wc -l <"$f") lines; last row: $(tail -1 "$f")"; else echo "$s TODAY ($today): NO FILE (not writing today)"; fi; done'
run 'for s in sht40 rg15 ds18b20; do f=$(ls -t /var/log/orc/sensors/${s}_*.csv 2>/dev/null | head -1); echo "--- newest $s: $f ---"; if [ -n "$f" ]; then echo "[head]"; head -3 "$f"; echo "[tail]"; tail -3 "$f"; else echo "no files"; fi; done'

hdr "4. LOGGER SERVICE  (orc-sensors.timer -> orc-sensors -> sensors_logger.py)"
run 'systemctl status orc-sensors.timer --no-pager | head -8'
run 'systemctl status orc-sensors.service --no-pager | head -15'
run 'systemctl is-enabled orc-sensors.timer orc-sensors.service'
run 'systemctl list-timers --all --no-pager | grep -iE "NEXT|orc"'
run 'ls -l /etc/systemd/system/ | grep -i orc'

hdr "5. LOGGER JOURNAL  (WHY sht40 died 05-15 and rg15 died 06-15 lives here)"
run 'journalctl --disk-usage'
run 'echo "journal coverage (oldest orc-sensors line):"; journalctl -u orc-sensors -o short-iso --no-pager | head -2'
run 'echo "--- last 300 logger lines ---"; journalctl -u orc-sensors -o short-iso --no-pager -n 300'
run 'echo "--- all logger error/exception lines (whole retained journal) ---"; journalctl -u orc-sensors -o short-iso --no-pager | grep -iE "error|exception|traceback|mismatch|no response|no .*device|errno|i2c|timeout" | tail -150'
run 'echo "== sht40 death window 2026-05-14..05-16 (if journal retained) =="; journalctl -u orc-sensors -o short-iso --no-pager --since 2026-05-14 --until 2026-05-16 | grep -iE "sht40|error|exception" | tail -80'
run 'echo "== rg15 death window 2026-06-14..06-16 (if journal retained) =="; journalctl -u orc-sensors -o short-iso --no-pager --since 2026-06-14 --until 2026-06-16 | grep -iE "rg15|error|exception" | tail -80'

hdr "6. SENSOR HARDWARE  (is each chip electrically present right now?)"
run 'echo "i2cdetect bus 1 (SHT40 should answer at 0x44):"; i2cdetect -y -r 1 2>&1 || echo "i2c-tools missing or no bus"'
run 'echo "1-wire devices (DS18B20 = 28-*):"; ls -l /sys/bus/w1/devices/ 2>&1'
run 'for d in /sys/bus/w1/devices/28-*; do [ -e "$d" ] && { echo "$d temperature:"; cat "$d/temperature" 2>&1; }; done'
run 'echo "device nodes:"; ls -l /dev/ttyAMA0 /dev/serial0 /dev/i2c-1 2>&1'
run 'echo "config.txt overlays:"; grep -iE "w1|i2c|uart|dtoverlay|dtparam|serial" /boot/firmware/config.txt 2>/dev/null || grep -iE "w1|i2c|uart|dtoverlay|dtparam|serial" /boot/config.txt 2>&1'
run 'echo "kernel bus/power errors:"; dmesg 2>/dev/null | grep -iE "voltage|throttl|brownout|i2c|w1_|onewire|ttyAMA|serial|hwmon" | tail -60'

hdr "7. POWER / THROTTLE  (solar station; sparse readings hint at undervoltage)"
run 'vcgencmd get_throttled 2>&1; echo "(0x0 = clean. bit0/16 = undervoltage now/past)"'
run 'vcgencmd measure_temp 2>&1; vcgencmd measure_volts 2>&1'

hdr "8. UPLOAD STATE  (watermark + what is queued but not yet sent)"
run 'stat -c "watermark: %n  mtime=%y" /var/lib/orc-sensors/upload.state 2>&1'
run 'if [ -f /var/lib/orc-sensors/upload.state ]; then echo "files NEWER than watermark = queued to upload:"; find /var/log/orc/sensors -type f -newer /var/lib/orc-sensors/upload.state 2>/dev/null | sort; else echo "NO watermark file present"; fi'
run 'echo "rg15 totalacc state:"; cat /var/lib/orc-sensors/rg15_totalacc.txt 2>&1'

hdr "9. UPLOAD JOURNAL  (orc-sensors-upload logs via logger -t; success/curl-exit history)"
run 'echo "coverage (oldest upload line):"; journalctl -t orc-sensors-upload -o short-iso --no-pager | head -2'
run 'echo "--- last 200 upload lines ---"; journalctl -t orc-sensors-upload -o short-iso --no-pager -n 200'
run 'echo "--- upload error lines ---"; journalctl -t orc-sensors-upload -o short-iso --no-pager | grep -iE "error|fail|curl|refus|watermark" | tail -100'

hdr "10. UPLOAD CONNECTIVITY  (read-only GET to /sensors/health; tests TLS pin + NAT64 path)"
run 'echo "IPv4 (what the script uses):"; curl -sS --ipv4 --cacert /etc/orc/sensor-upload-ca.pem --connect-timeout 10 --max-time 20 https://openrivercam.endlessprojects.info:8443/sensors/health; echo'
run 'echo "default/IPv6 path (expected to hang/fail if NAT64 MTU issue):"; curl -sS --cacert /etc/orc/sensor-upload-ca.pem --connect-timeout 10 --max-time 20 https://openrivercam.endlessprojects.info:8443/sensors/health; echo'
run 'curl -sS -o /dev/null -w "ipv4 timing: connect=%{time_connect}s tls=%{time_appconnect}s total=%{time_total}s http=%{http_code}\n" --ipv4 --cacert /etc/orc/sensor-upload-ca.pem --connect-timeout 10 --max-time 20 https://openrivercam.endlessprojects.info:8443/sensors/health'
run 'getent ahosts openrivercam.endlessprojects.info'
run 'ip -brief addr 2>/dev/null; echo; ip route get 8.8.8.8 2>/dev/null'

hdr "11. UPLOAD AUTH / CERT  (presence only; values redacted)"
run 'for f in /home/pi/.orc_deploy_*; do [ -f "$f" ] && echo "$f present; UPLOAD_TOKEN defined: $(grep -q "^UPLOAD_TOKEN=" "$f" && echo yes || echo NO); keys present: $(grep -oE "^[A-Z_]+=" "$f" | tr "\n" " ")"; done'
run 'echo "pinned CA cert:"; openssl x509 -in /etc/orc/sensor-upload-ca.pem -noout -subject -issuer -dates 2>&1'

hdr "12. CONFIG ON STATION  (may differ from repo)"
run 'ls -l /etc/orc-sensors/; for c in /etc/orc-sensors/*.conf; do echo "--- $c ---"; cat "$c"; done'
run 'echo "--- /etc/orc/sensors-upload.conf ---"; cat /etc/orc/sensors-upload.conf 2>&1'

hdr "13. DEPLOYED CODE  (sha + full, to diff against repo / detect uncommitted drift)"
run 'for p in /usr/local/bin/orc-sensors /usr/local/bin/orc-sensors-upload /usr/local/lib/orc-sensors/sensors_logger.py /usr/local/bin/orc-capture; do echo "== $p =="; ls -l "$p" 2>&1; sha256sum "$p" 2>&1; done'
run 'echo "===== sensors_logger.py ====="; cat /usr/local/lib/orc-sensors/sensors_logger.py 2>&1'
run 'echo "===== orc-sensors-upload ====="; cat /usr/local/bin/orc-sensors-upload 2>&1'
run 'echo "===== orc-sensors ====="; cat /usr/local/bin/orc-sensors 2>&1'
run 'echo "===== orc-capture (orchestrator: upload step + shutdown timing) ====="; cat /usr/local/bin/orc-capture 2>&1'

hdr "14. CAPTURE / CYCLE ORCHESTRATION  (how/when upload is invoked; shutdown pressure)"
run 'systemctl status "orc-capture*" --no-pager 2>&1 | head -20'
run 'ls -l /etc/systemd/system/ | grep -iE "capture|cycle|orc"'
run 'echo "--- last 120 orc-capture journal lines ---"; journalctl -t orc-capture -o short-iso --no-pager -n 120 2>&1'
run 'echo "crontabs referencing orc:"; crontab -l 2>/dev/null | grep -i orc; for u in pi root; do echo "[$u]"; crontab -u $u -l 2>/dev/null | grep -i orc; done; grep -rIl orc /etc/cron* 2>/dev/null'

hdr "15. WITTY PI SCHEDULE  (READ-ONLY: files only, no wittyPi utility invoked)"
run 'ls -l /home/pi/wittypi/ 2>/dev/null | head -20'
run 'for f in /home/pi/wittypi/schedule.wpi /home/pi/wittypi/.schedule; do echo "--- $f ---"; cat "$f" 2>&1; done'
run 'echo "--- wittyPi.log (tail) ---"; tail -60 /home/pi/wittypi/wittyPi.log 2>&1'
run 'echo "recent boots (wake cadence):"; journalctl --list-boots --no-pager 2>&1 | tail -25'

echo
echo "################################################################"
echo "## END OF BUNDLE"
echo "################################################################"
} > "$OUT" 2>&1

# Belt-and-braces secret redaction (values are never intentionally printed).
sed -i -E "s/((TOKEN|PASSWORD|PASSWD|PASS|SECRET|Bearer)[A-Za-z_]*[=:] *)[^ ,;\"']+/\1<REDACTED>/Ig" "$OUT"

echo "WROTE: $OUT"
ls -lh "$OUT"
echo "Lines: $(wc -l < "$OUT")"
echo
echo "scp it back with (from your laptop):"
echo "  scp <pi-user>@<pi-host>:$OUT ."
