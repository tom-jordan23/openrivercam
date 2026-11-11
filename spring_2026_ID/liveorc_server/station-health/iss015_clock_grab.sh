set -u
# ISS-FIELD-015: read-only clock grab. Who sets the Pi's clock, what happens with
# no data, and where the sensors take their timestamps. Run through
# todo119_wake_runner.py (bash -s over ssh). Station times are UTC.
#
# READ-ONLY. No chronyc commands that change anything (no makestep, burst,
# add/delete); no hwclock write options; no wp5 menu choice except 14 (Exit).
# sudo -n is used only to retry journalctl and to read the hardware clock.
#
# Fits a ~2-3 min wake: ordered by value, every external call bounded. The body
# is a function run with stdin from /dev/null so nothing can eat the script from
# the ssh pipe.

main() {
S="sudo -n"
sec() { echo; echo "=== $1 ==="; }
jc() { local o o2; o=$(journalctl "$@" 2>&1) || { o2=$($S journalctl "$@" 2>&1) && o=$o2 || o="journalctl failed: $o | sudo: $o2"; }; printf '%s\n' "$o"; }

echo "=== ISS015 CLOCK GRAB $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "proc uptime s: $(cut -d' ' -f1 /proc/uptime)"

sec "1. clock jumps this boot (journal gaps > 5 min or backwards; PREV then CUR)"
jc -b -o short-unix --no-pager | awk '
  { t=$1+0; if (NR>1 && (t-p>300 || t<p)) { printf "JUMP %+.0f s\nPREV %s\nCUR  %s\n\n", t-p, pl, $0 } p=t; pl=$0 }' | head -n 60 \
  | while IFS= read -r l; do
      case "$l" in
        PREV\ *|CUR\ *) t=$(awk '{print $2}' <<<"$l"); t=${t%%.*}; [[ "$t" =~ ^[0-9]+$ ]] && printf '%s   [%s]\n' "${l:0:140}" "$(date -u -d @"$t" +%Y-%m-%dT%H:%M:%SZ)" || echo "${l:0:160}";;
        *) echo "$l";;
      esac; done

sec "2. who is keeping time (units)"
for u in chrony systemd-timesyncd fake-hwclock wp5d; do
  printf '  %-18s %s  (since %s)\n' "$u" "$(systemctl is-active $u 2>&1)" "$(systemctl show -p ActiveEnterTimestamp --value $u 2>&1)"
done

sec "3. chrony (read-only queries)"
echo "  --- tracking"; timeout 10 chronyc tracking 2>&1
echo "  --- sources"; timeout 10 chronyc sources -v 2>&1 | tail -n 20
echo "  --- sourcestats"; timeout 10 chronyc sourcestats 2>&1 | tail -n 10
echo "  --- activity"; timeout 10 chronyc activity 2>&1
echo "  --- chrony journal (this boot)"; jc -u chrony -b -o short-iso --no-pager | tail -n 40

sec "4. chrony config actually in force (comments stripped)"
for f in /etc/chrony/chrony.conf /etc/chrony/conf.d/*.conf /etc/chrony/sources.d/*.sources; do
  [ -f "$f" ] && { echo "  -- $f"; grep -vE '^\s*(#|$)' "$f" 2>&1; }
done

sec "5. timedatectl"
timeout 10 timedatectl 2>&1
timeout 10 timedatectl timesync-status 2>&1 | head -n 12

sec "6. hardware clocks (Linux RTC devices; the Witty Pi RTC is read in section 9)"
ls -l /dev/rtc* 2>&1
for r in /sys/class/rtc/*; do [ -d "$r" ] && echo "  $r: name=$(cat $r/name 2>&1) date=$(cat $r/date 2>&1) time=$(cat $r/time 2>&1)"; done
echo "  hwclock -r: $(timeout 10 $S hwclock -r 2>&1 | head -n 2)"

sec "7. boots and shutdowns (a second boot near :03 would show here)"
jc --list-boots --no-pager | tail -n 14
echo "  --- last -x"; timeout 10 last -x -n 16 --time-format iso 2>&1 | head -n 20

sec "8. wp5d.log (binary-safe): RTC/system writes and startup reasons"
tail -n 400 /var/log/wp5d.log 2>&1 | tr -d '\000' | grep -aE "RTC|Startup reason|[0-9]{2}:[0-9]{2}:[0-9]{2} (AM|PM) UTC|Network|NTP|time" | tail -n 30

sec "9. wp5 header (waits for orc-wp5-rearm; menu choice 14 = Exit)"
st=unknown; waited=0
for i in $(seq 1 60); do
  st=$(systemctl is-active orc-wp5-rearm 2>/dev/null)
  case "$st" in activating|reloading) ;; *) break ;; esac
  sleep 2; waited=$((i*2))
done
echo "  orc-wp5-rearm state: ${st:-unknown} (waited ${waited} s)"
hdr=$(printf '14\n' | timeout -k 2 20 wp5 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | head -n 60)
printf '%s\n' "$hdr" | grep -aE "SYS Time|RTC Time|Schedule next|V-IN"

sec "10. where the sensors get their timestamps"
grep -rnE "utcnow|datetime\.now|time\.time\(|strftime|isoformat|timestamp" /usr/local/lib/orc-sensors 2>/dev/null | cut -c1-170 | head -n 25
echo "  --- newest sensor log lines"
ls -t /var/log/orc/sensors 2>/dev/null | head -n 3
f=$(ls -t /var/log/orc/sensors/* 2>/dev/null | head -n 1); [ -n "$f" ] && tail -n 4 "$f" 2>&1 | cut -c1-200

sec "10b. files stranded by a wrong clock + the upload watermark"
echo "  watermark (upload.state): $(stat -c '%y' /var/lib/orc-sensors/upload.state 2>&1)"
echo "  sensor files NOT dated this month (a Jan/Mar file means rows were written under a wrong clock):"
ls -l --time-style=long-iso /var/log/orc/sensors 2>&1 | grep -E '_2026-0[1-9]-|_2026-10-' | tail -n 20
echo "  count of files older than the watermark (never uploaded by the find -newer rule):"
if [ -f /var/lib/orc-sensors/upload.state ]; then
  find /var/log/orc/sensors -type f ! -newer /var/lib/orc-sensors/upload.state 2>/dev/null | wc -l
fi

sec "10c. orc-clock-floor (present only after the ISS-FIELD-015 deploy)"
systemctl is-active orc-clock-floor 2>&1; systemctl is-enabled orc-clock-floor 2>&1
echo "  floor file: $(cat /var/lib/orc-clock-floor/floor 2>&1)  ->  $(d=$(cat /var/lib/orc-clock-floor/floor 2>/dev/null); [[ "$d" =~ ^[0-9]+$ ]] && date -u -d @"$d" +%Y-%m-%dT%H:%M:%SZ)"
echo "  state:"; cat /run/orc-clock-floor/state 2>&1 | sed 's/^/    /'
jc -t orc-clock-floor --no-pager -o short-iso | tail -n 12

sec "10d. station checkout (what a git pull there would meet). --no-optional-locks: nothing here writes to .git"
R=/home/pi/code/git/openrivercam
G="git --no-optional-locks -C $R"
echo "  path exists: $([ -d $R/.git ] && echo yes || echo NO)   owner: $(stat -c '%U' $R 2>&1)"
echo "  HEAD: $($G rev-parse HEAD 2>&1)"
echo "  branch: $($G rev-parse --abbrev-ref HEAD 2>&1)"
echo "  remotes:"; $G remote -v 2>&1 | sed 's/^/    /'
echo "  tracking: $($G rev-parse --abbrev-ref '@{upstream}' 2>&1)"
echo "  last commits:"; $G log -5 --format='    %h %ad %s' --date=short 2>&1
echo "  local changes (tracked files modified/deleted, untracked) - a pull must not trample these:"
$G status --porcelain=v1 2>&1 | head -n 40 | sed 's/^/    /'
echo "  diff vs HEAD (stat):"; $G diff --stat 2>&1 | tail -n 15 | sed 's/^/    /'
echo "  files under the overlay paths that differ from the repo's HEAD (installed copies, read-only compare):"
for f in usr/local/bin/orc-wp5-rearm usr/local/bin/orc-wake-ceiling; do
  if [ -f /$f ] && [ -f $R/spring_2026_ID/pi/sukabumi/$f ]; then cmp -s /$f $R/spring_2026_ID/pi/sukabumi/$f && echo "    $f: installed == checkout" || echo "    $f: installed DIFFERS from checkout"; fi
done
for f in usr/local/bin/orc-sensors-upload usr/local/lib/orc-sensors/sensors_logger.py; do
  src=$R/spring_2026_ID/pi/shared/$f
  if [ -f /$f ] && [ -f $src ]; then cmp -s /$f $src && echo "    $f: installed == checkout" || echo "    $f: installed DIFFERS from checkout"; fi
done

sec "11. SUMMARY"
sysd=$(date -u +%Y-%m-%d); rtcd=$(grep -aoE 'RTC Time: [0-9-]{10}' <<<"$hdr" | head -1 | cut -d' ' -f3)
echo "  system date: $sysd   Witty Pi RTC date: ${rtcd:-unreadable}"
if [ -n "$rtcd" ]; then
  a=$(date -u -d "$sysd" +%s 2>/dev/null); b=$(date -u -d "$rtcd" +%s 2>/dev/null)
  [[ "$a" =~ ^[0-9]+$ && "$b" =~ ^[0-9]+$ ]] && echo "  RTC is $(( (a-b)/86400 )) day(s) behind the system clock"
fi
echo "  chrony: $(timeout 10 chronyc tracking 2>&1 | grep -aE 'Reference ID|Leap status' | tr '\n' ';')"

echo; echo "=== ISS015 CLOCK GRAB DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
}

main < /dev/null
