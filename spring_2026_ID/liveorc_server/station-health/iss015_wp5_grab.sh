set -u
# ISS-FIELD-015: read-only Witty Pi 5 software/RTC grab (2026-11-12). Run through
# todo119_wake_runner.py (bash -s over ssh). Station times are UTC; offline wakes carry
# January dates (the RTC month reads 01 for November).
#
# READ-ONLY and HARDWARE-FREE: no wp5, no wp5d control, no i2cget/i2cdetect, no chronyc,
# no writes, no ORC-OS API. Files, package metadata and the journal only. sudo -n only
# retries journalctl. See research/witty_pi_5_rtc_month_investigation_2026-11-12.md.
#
# QUESTIONS: which wp5 build is installed (the 5.0.0 software cannot show the firmware
# version)? Was there I2C trouble in wp5d.log near 10-21? What did the daemon journal around
# the two presses and an offline wake? Does anything else on the box touch the RTC or
# the clock? What were the voltage rows of the last wake before the silence?
# The body is a function run with stdin from /dev/null.

main() {
S="sudo -n"
sec() { echo; echo "=== $1 ==="; }
jc() { local o o2; o=$(timeout 25 journalctl "$@" 2>&1) || { o2=$(timeout 25 $S journalctl "$@" 2>&1) && o=$o2 || o="journalctl failed: $o | sudo: $o2"; }; printf '%s\n' "$o"; }
WP5D="${ISS015_WP5D_LOG:-/var/log/wp5d.log}"
SENS="${ISS015_SENS_DIR:-/var/log/orc/sensors}"

echo "=== ISS015 WP5 GRAB $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "proc uptime s: $(cut -d' ' -f1 /proc/uptime)"

sec "1. installed wp5 package and binaries (no firmware version is shown by software 5.0.0)"
dpkg -s wp5 2>&1 | grep -E '^(Package|Status|Version|Installed-Size|Depends|Description):' | head -8
echo "  other i2c/wittypi packages:"; dpkg -l 2>/dev/null | awk '/wp5|wittypi|i2c-tools|python3-smbus|libi2c/ {print "    "$2" "$3}' | head -10
for b in wp5 wp5d; do
  p=$(command -v $b 2>/dev/null || ls /usr/bin/$b /usr/sbin/$b /usr/local/bin/$b 2>/dev/null | head -1)
  if [ -n "${p:-}" ] && [ -e "$p" ]; then
    echo "  $b: $p  $(stat -c '%s bytes, mtime %y' "$p" | cut -c1-60)  sha256=$(sha256sum "$p" | cut -c1-16)"
    echo "    strings of interest:"; timeout 10 strings -n 8 "$p" 2>/dev/null | grep -iE "firmware|RTC (has|is)|network time|version|i2c_get|lock" | head -12 | sed 's/^/      /'
  else echo "  $b: not found"; fi
done
echo "  package file list (first 30):"; dpkg -L wp5 2>/dev/null | head -30 | sed 's/^/    /'
echo "  package changelog / docs:"; ls -la /usr/share/doc/wp5* 2>&1 | head -8 | sed 's/^/    /'
for f in /usr/share/doc/wp5/changelog* /usr/share/doc/wp5/README*; do [ -f "$f" ] && { echo "  -- $f"; (zcat -f "$f" 2>/dev/null || cat "$f") | head -25 | sed 's/^/    /'; }; done

sec "2. daemon units"
for u in wp5d wp5d_poweroff wp5d_reboot; do echo "  -- $u: $(systemctl is-enabled $u 2>&1) / $(systemctl is-active $u 2>&1)"; systemctl cat $u 2>&1 | grep -vE '^\s*(#|$)' | head -16 | sed 's/^/    /'; done

sec "3. I2C trouble recorded by wp5d, per date (whole log, binary-safe)"
if [ -r "$WP5D" ]; then
  echo "  lines matching i2c_ per date (top 40):"
  tr -d '\000' < "$WP5D" | grep -a 'i2c_' | awk '{d=substr($1,2,10); c[d]++} END{for(k in c) print c[k]" "k}' | sort -k2 | tail -n 40 | sed 's/^/    /'
  echo "  total i2c_ lines: $(tr -d '\000' < "$WP5D" | grep -ac 'i2c_')   of $(tr -d '\000' < "$WP5D" | wc -l) lines"
  echo "  first 3 and last 6 i2c_ lines:"; tr -d '\000' < "$WP5D" | grep -a 'i2c_' | sed -n '1,3p' | sed 's/^/    /'; tr -d '\000' < "$WP5D" | grep -a 'i2c_' | tail -n 6 | cut -c1-160 | sed 's/^/    /'
  echo "  distinct i2c_ message shapes (register numbers collapsed):"; tr -d '\000' < "$WP5D" | grep -a 'i2c_' | sed -E 's/^\[[^]]*\] //; s/Reg[0-9]+/RegN/g; s/0x[0-9a-fA-F]+/0xN/g; s/attempt [0-9]+/attempt N/' | sort | uniq -c | sort -rn | head -8 | sed 's/^/    /'
else echo "  $WP5D not readable"; fi

sec "4. wp5d journal around the presses and an offline wake (service messages and any I2C errors)"
for win in "2026-01-11 07:50:00|2026-01-11 08:05:00|11-11 press boot (RTC date Jan 11)" "2026-01-12 03:38:00|2026-01-12 03:55:00|11-12 press 03:41:50 (RTC date Jan 12)" "2026-01-12 12:00:00|2026-01-12 12:06:00|11-12 12:00 wake, offline"; do
  a=${win%%|*}; rest=${win#*|}; b=${rest%%|*}; label=${rest#*|}
  echo "  [$label]"; jc -u wp5d --since "$a" --until "$b" -o short-iso --no-pager | head -n 40 | cut -c1-170 | sed 's/^/    /'
done

sec "5. kernel, I2C devices and boot config"
echo "  i2c tools: $(command -v i2cdetect i2cget 2>/dev/null | tr '\n' ' ')"; ls -l /dev/i2c* 2>&1 | sed 's/^/    /'
echo "  rtc devices: $(ls /sys/class/rtc 2>&1 | tr '\n' ' ')  rtc0=$(cat /sys/class/rtc/rtc0/name 2>&1)"
echo "  modules:"; lsmod 2>/dev/null | grep -iE 'i2c|rtc' | sed 's/^/    /'
echo "  kernel lines about i2c/rtc/wittypi this boot:"; jc -k -b 0 -o short-iso --no-pager | grep -iE 'i2c|rtc|wittypi|witty' | head -12 | cut -c1-165 | sed 's/^/    /'
echo "  /boot/firmware/config.txt (non-comment):"; grep -vE '^\s*(#|$)' /boot/firmware/config.txt 2>&1 | head -30 | sed 's/^/    /'

sec "6. voltage rows of the last wake before the 21-day silence (wittypi_2026-10-21.csv)"
f="$SENS/wittypi_2026-10-21.csv"
if [ -r "$f" ]; then
  echo "  header: $(head -n 1 "$f" | cut -c1-200)"; echo "  rows: $(( $(wc -l < "$f") - 1 ))"; echo "  last 6 rows:"; tail -n 6 "$f" | cut -c1-170 | sed 's/^/    /'
  echo "  Vin column min/max over the day (column 2):"; awk -F, 'NR>1 && $2+0>0 {if(min==""||$2<min)min=$2; if($2>max)max=$2} END{print "    min="min" max="max}' "$f"
else echo "  $f not present"; fi

sec "7. anything else on the box that writes the RTC or the clock (names and matching lines only)"
timeout 20 grep -rIEn '\bwp5\b|hwclock|date -s|date --set|timedatectl set|chronyc (makestep|settime)|ntpdate' /etc/cron* /etc/systemd/system /etc/rc.local /usr/local/bin /usr/local/sbin /usr/local/lib /etc/NetworkManager/dispatcher.d /etc/network 2>/dev/null | grep -vE 'orc-wp5-rearm|sensors_logger.py|^\S+:[0-9]+:\s*#' | cut -c1-170 | head -30
echo "  (end)"

echo; echo "=== ISS015 WP5 GRAB DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
}

main < /dev/null
