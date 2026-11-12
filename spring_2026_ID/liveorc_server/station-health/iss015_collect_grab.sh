set -u
# ISS-FIELD-015: final read-only COLLECTION grab (2026-11-12). Run through
# todo119_wake_runner.py (bash -s over ssh) at a wake while the network is up.
# Station times are UTC. The Witty Pi RTC reads January, so offline wakes carry
# January dates; early-boot journal times read 2026-03-26.
#
# READ-ONLY. No writes of any kind. No wp5, no chronyc, no timedatectl, no hwclock,
# no git fetch/pull, no ORC-OS API or database access. sudo -n only retries journalctl.
# Fits a 2-3 minute wake: cheap, high-value reads first; every external call bounded.
# The body is a function run with stdin from /dev/null so nothing eats the script
# from the ssh pipe.
#
# QUESTIONS IT ANSWERS (see ISS-FIELD-015_STATUS_2026-11-12.md section 6):
#   1. Did the Pi keep waking while the network was down?     -> section 1 (wp5d.log)
#   2. Which sensor files are stranded, how many rows?        -> section 2
#   3. What is in the video directory, and how is it dated?   -> section 3
#   4. Are the 11-11 boot journals still there?               -> sections 4, 5
#   5. Why was there no network, and when did NTP work?       -> sections 5b, 6
#   (section 1 also lists everything wp5d logged during the 10-21..11-11 silence)
#   6. What would a deploy change?                            -> section 7 (hashes)
#
# Test hooks (unset in production): ISS015_SENS_DIR, ISS015_WP5D_LOG, ISS015_ORC_HOME,
# ISS015_CHECKOUT, ISS015_ROOT, ISS015_WATERMARK.

main() {
S="sudo -n"
SENS="${ISS015_SENS_DIR:-/var/log/orc/sensors}"
WP5D="${ISS015_WP5D_LOG:-/var/log/wp5d.log}"
ORCH="${ISS015_ORC_HOME:-/home/pi/.ORC-OS}"
CK="${ISS015_CHECKOUT:-/home/pi/code/git/openrivercam}"
ROOT="${ISS015_ROOT:-}"
WM="${ISS015_WATERMARK:-/var/lib/orc-sensors/upload.state}"
sec() { echo; echo "=== $1 ==="; }
jc() { local o o2; o=$(timeout 25 journalctl "$@" 2>&1) || { o2=$(timeout 25 $S journalctl "$@" 2>&1) && o=$o2 || o="journalctl failed: $o | sudo: $o2"; }; printf '%s\n' "$o"; }

echo "=== ISS015 COLLECTION GRAB $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "proc uptime s: $(cut -d' ' -f1 /proc/uptime)   df /: $(df -h / | tail -1 | awk '{print $3" used of "$2" ("$5")"}')"

sec "1. WAKES THE STATION RECORDED ITSELF (wp5d.log, binary-safe): startups per RTC date and reason"
if [ -r "$WP5D" ]; then
  tr -d '\000' < "$WP5D" | grep -a "Startup reason" | awk '{d=substr($1,2,10); r=$0; sub(/.*Startup reason: /,"",r); c[d" | "r]++} END{for(k in c) print c[k]" | "k}' | sort -t'|' -k2 | tail -n 60
  echo "  first startup line: $(tr -d '\000' < "$WP5D" | grep -a 'Startup reason' | head -n 1)"
  echo "  last startup line : $(tr -d '\000' < "$WP5D" | grep -a 'Startup reason' | tail -n 1)"
  echo "  Button Click entries (presses), last 10:"; tr -d '\000' < "$WP5D" | grep -a "Button Click" | tail -n 10 | sed 's/^/    /'
  echo "  lines in wp5d.log dated 2026-10-21 14:3x .. 2026-11-10 (the 21-day silence; none = the daemon logged nothing):"
  tr -d '\000' < "$WP5D" | grep -aE '^\[2026-10-(2[1-9]|3[01]) |^\[2026-11-(0[0-9]|10) ' | grep -avE 'Caught signal|Exit now' | tail -n 30 | sed 's/^/    /'
  echo "  NON-ROUTINE wp5d events anywhere in the log (voltage, temperature, power, alarms, errors), last 40:"
  tr -d '\000' < "$WP5D" | grep -aviE 'Startup reason|Caught signal|Exit now|daemon V|System: Linux|Running on|Connected to|RTC has valid|Done :\)|^[A-Z][a-z]{2} [A-Z][a-z]{2} [ 0-9]|^$' | tail -n 40 | cut -c1-170 | sed 's/^/    /'
  echo "  all startup events, last 90 (RTC date; Jan = no NTP step that wake):"
  tr -d '\000' < "$WP5D" | grep -a "Startup reason" | tail -n 90 | sed 's/^/    /'
else
  echo "  $WP5D not readable"
fi

sec "2. SENSOR FILES: inventory, then every suspect file with rows and first/last timestamps"
echo "  watermark (upload.state) mtime: $(stat -c '%y' "$WM" 2>&1)"
echo "  files per name-month:"; ls "$SENS" 2>/dev/null | sed -nE 's/.*_([0-9]{4}-[0-9]{2})-[0-9]{2}\.csv$/\1/p' | sort | uniq -c | sed 's/^/    /'
echo "  SUSPECT files (name date 2026-01..03, 2026-07, or 2026-10-22..31):"
ls "$SENS" 2>/dev/null | grep -E '_2026-(0[1-3]|07)-|_2026-10-(2[2-9]|3[01])\.csv$' | while read -r f; do
  p="$SENS/$f"
  printf '    %-30s %6s B rows=%-5s mtime=%s first=%s last=%s\n' "$f" "$(stat -c %s "$p")" "$(( $(wc -l < "$p") - 1 ))" "$(stat -c %y "$p" | cut -c1-19)" "$(sed -n 2p "$p" | cut -c1-32)" "$(tail -n 1 "$p" | cut -c1-32)"
done
echo "  files dated 2026-11-* : rows and mtime (a file NOT newer than the watermark is skipped by the uploader):"
ls "$SENS" 2>/dev/null | grep -E '_2026-11-' | while read -r f; do
  p="$SENS/$f"; flag=""; [ -f "$WM" ] && [ ! "$p" -nt "$WM" ] && flag=" NOT-NEWER-THAN-WATERMARK"
  printf '    %-30s %6s B rows=%-5s mtime=%s%s\n' "$f" "$(stat -c %s "$p")" "$(( $(wc -l < "$p") - 1 ))" "$(stat -c %y "$p" | cut -c1-19)" "$flag"
done

sec "3. VIDEOS ON THE STATION (file level only; no ORC-OS API or database access)"
VD=$(timeout 15 find "$ORCH" -maxdepth 4 -type d -name videos 2>/dev/null | head -n 3)
echo "  video directories: ${VD:-none found under $ORCH}"
for d in $VD; do
  echo "  $d: files=$(timeout 20 find "$d" -type f 2>/dev/null | wc -l)  bytes=$(timeout 20 du -sb "$d" 2>/dev/null | cut -f1)"
  echo "    files by mtime date (Jan/Mar/Jul dates = written under a wrong clock):"
  timeout 20 find "$d" -type f -printf '%TY-%Tm-%Td\n' 2>/dev/null | sort | uniq -c | tail -n 40 | sed 's/^/      /'
  echo "    oldest and newest:"; timeout 20 find "$d" -type f -printf '%TY-%Tm-%Td %TH:%TM %p\n' 2>/dev/null | sort | sed -n '1p;$p' | cut -c1-150 | sed 's/^/      /'
done

sec "4. BOOT LIST SUMMARY + JOURNAL LIMITS (are the 11-11 journals still there?)"
BL=$(jc --list-boots --no-pager)
echo "  boots in the journal: $(printf '%s\n' "$BL" | grep -c '^ *-\?[0-9]')"
echo "  boots by END date:"; printf '%s\n' "$BL" | awk 'NF>=6 {print $(NF-2)}' | sort | uniq -c | tail -n 30 | sed 's/^/    /'
echo "  oldest 3 / newest 8:"; printf '%s\n' "$BL" | head -n 3 | sed 's/^/    /'; printf '%s\n' "$BL" | tail -n 8 | sed 's/^/    /'
echo "  disk usage:"; jc --disk-usage | sed 's/^/    /'
echo "  journald config:"; grep -hvE '^\s*(#|$)' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/*.conf 2>&1 | sed 's/^/    /'

sec "5. KEY LINES OF THE 11-11 BOOTS (chosen by END time; 'not in journal' = rotated out)"
findboot() { printf '%s\n' "$BL" | awk -v pat="$1" '$0 ~ pat { id=$1 } END { print id }'; }
for spec in "press 07:5x|2026-11-11 07:5[0-9]:[0-9][0-9] UTC$" "12:00 wake|2026-11-11 12:0[0-9]:[0-9][0-9] UTC$" "17:00 wake|2026-11-11 17:0[0-9]:[0-9][0-9] UTC$"; do
  label=${spec%%|*}; pat=${spec#*|}; id=$(findboot "$pat")
  if [ -z "$id" ]; then echo "  [$label] NOT IN JOURNAL (no boot ended matching $pat)"; continue; fi
  echo "  [$label] boot $id"
  echo "    chrony / network lines:"; jc -b "$id" -o short-iso --no-pager | grep -aE "chronyd|tailscaled.*(login|connected|control)|wwan0|ModemManager.*(registered|disconnect)" | head -n 14 | cut -c1-165 | sed 's/^/      /'
  echo "    last 25 lines:"; jc -b "$id" -n 25 -o short-iso --no-pager | cut -c1-165 | sed 's/^/      /'
done

sec "5b. WHY NO NETWORK? the most recent OFFLINE boot (journal end date Jan 2026) against this ONLINE boot"
lastboot() { printf '%s\n' "$BL" | awk -v pat="$1" '$0 ~ pat { id=$1 } END { print id }'; }
OFF=$(lastboot "2026-01-[0-9][0-9] [0-9:]{8} UTC$")
netgrep() { grep -aE "ModemManager|NetworkManager.*(telkomsel|wwan0|activation|state change|dhcp|IPv4|IPv6|disconnect|failed|timed out)|tailscaled.*(netcheck|control|login|DERP|dial|unreachable|no route)|chronyd|systemd-resolved.*(timeout|failed|server)|dnsmasq" ; }
if [ -n "$OFF" ]; then
  OFFJ=$(timeout 25 journalctl -b "$OFF" -o short-iso --no-pager 2>&1 || timeout 25 $S journalctl -b "$OFF" -o short-iso --no-pager 2>&1)
  echo "  OFFLINE boot $OFF: modem / network / DNS / tailscale / chrony lines (first 40):"; printf '%s\n' "$OFFJ" | netgrep | head -n 40 | cut -c1-170 | sed 's/^/    /'
  echo "  OFFLINE boot $OFF: upload / sync attempts (orc-api, orc-sensors-upload, orc-capture), last 20:"
  printf '%s\n' "$OFFJ" | grep -aiE "orc-sensors-upload|orc-capture|orc-api.*(upload|sync|fail|error|timeout)|curl" | tail -n 20 | cut -c1-170 | sed 's/^/    /'
else
  echo "  no boot with a January end date in the journal (offline boots rotated out, or none)"
fi
ONJ=$(timeout 25 journalctl -b 0 -o short-iso --no-pager 2>&1 || timeout 25 $S journalctl -b 0 -o short-iso --no-pager 2>&1)
echo "  THIS (online) boot: the same lines, first 30:"; printf '%s\n' "$ONJ" | netgrep | head -n 30 | cut -c1-170 | sed 's/^/    /'

sec "6. NTP OUTCOME PER BOOT (chrony journal, all boots): stepped = network ok; no selectable sources = no network"
jc -u chrony -o short-iso --no-pager | grep -aE "was stepped|no selectable sources|Backward time jump|Selected source" | tail -n 120 | cut -c1-150

sec "7. INSTALLED OVERLAY FILE HASHES (compare locally with the repo to see what a deploy would change)"
echo "  checkout HEAD: $(git --no-optional-locks -C "$CK" rev-parse HEAD 2>&1)"
( cd "$CK/spring_2026_ID/pi" 2>/dev/null && find sukabumi shared -type f \( -path '*/usr/*' -o -path '*/etc/*' \) 2>/dev/null | sort ) | while read -r rel; do
  inst="/${rel#*/}"
  if [ -f "$ROOT$inst" ]; then sha256sum "$ROOT$inst" | awk -v p="$inst" '{print $1"  "p}'; else echo "MISSING                                                           $inst"; fi
done | head -n 200

echo; echo "=== ISS015 COLLECTION GRAB DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
}

main < /dev/null
