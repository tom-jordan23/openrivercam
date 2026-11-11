set -u
# ISS-FIELD-015: PRESS-BOOT RECOVERY + EVIDENCE. Run through todo119_wake_runner.py
# (bash -s over ssh) at the first boot after the team presses the Witty Pi button.
# Station times are UTC; early-boot journal times read 2026-03-26.
#
# PRIORITY (Tom, 2026-11-11): re-establish the wake. Evidence comes second.
#
# THIS SCRIPT WRITES TO THE STATION. It needs Tom's explicit approval before it is armed.
# Its writes, all in the recovery block R and nowhere else:
#   1. systemctl stop orc-sensors.timer orc-sensors.service   (so no wp5 status read
#      overlaps the activation; ISS-FIELD-015 path 3. They restart at the next boot.)
#   2. rm -f /var/lib/orc-wp5-rearm/last-ok                  (the re-arm's own stamp; missing = "due")
#   3. systemctl start orc-wp5-rearm                          (the SAME script that runs at every
#      boot: re-activates prod_30.wpi, ~35 s, then reads the header back)
# It never calls wp5 itself, never writes the RTC, never edits the schedule by hand.
#
# WHY FORCE IT. orc-wp5-rearm re-arms at boot only if its stamp is missing/older than 23 h/in the
# future, or the header shows nothing armed. At the press boot the stamp is ~16-21 h old and the
# header shows an armed startup, so it would say "not due". An armed header is also not proof the
# wake will happen: at 12:00:50 on 11-11 it showed [11 12:30:00] and no wake came.
#
# GUARDS: no passwordless sudo -> no writes. Uptime > MAX_UP s -> no writes (ORC-OS powers the Pi
# off 2-3 min after boot; an activation cut by that could leave the startup empty). A wp5 process
# still running after 10 s -> no writes (never start an activation over another wp5). At most two
# attempts. Success = the new journal line says "OK: activated" AND shows a next startup.
#
# The remainder is the files-and-journal-only evidence grab (no wp5, no chronyc): when/how the
# 12:00 boot ended, whether boots happened in the 12:03-17:00 gap, the 17:00 wake, wp5d.log.
# The body is a function run with stdin from /dev/null so nothing eats the script from the ssh pipe.

main() {
S="sudo -n"
sec() { echo; echo "=== $1 ==="; }
jc() { local o o2; o=$(journalctl "$@" 2>&1) || { o2=$($S journalctl "$@" 2>&1) && o=$o2 || o="journalctl failed: $o | sudo: $o2"; }; printf '%s\n' "$o"; }

echo "=== ISS015 PRESS-BOOT RECOVERY + EVIDENCE $(date -u +%Y-%m-%dT%H:%M:%SZ) (clock may be stale early in boot) ==="
echo "proc uptime s: $(cut -d' ' -f1 ${ISS015_UPTIME_FILE:-/proc/uptime})"

MAX_UP=110
rearm_new_lines() { journalctl -t orc-wp5-rearm -b 0 --no-pager -o cat 2>/dev/null; }

sec "R. RECOVERY: force a fresh schedule activation (before anything else)"
RESULT="not attempted"
if $S true 2>/dev/null; then
  echo "  sudo -n: works"
  # 1. let the boot-time re-arm finish; it started ~4 s into boot
  for i in $(seq 1 30); do
    st=$(systemctl is-active orc-wp5-rearm 2>/dev/null)
    case "$st" in activating|reloading) sleep 2;; *) break;; esac
  done
  echo "  boot-time re-arm state: ${st:-unknown}; its result this boot:"
  rearm_new_lines | sed 's/^/    /'
  up=$(cut -d. -f1 ${ISS015_UPTIME_FILE:-/proc/uptime})
  if [ "$up" -gt "$MAX_UP" ]; then
    RESULT="SKIPPED: uptime ${up}s > ${MAX_UP}s (too close to ORC-OS shutdown to risk an activation)"
  else
    # 2. nothing may read wp5 while it activates
    $S systemctl stop orc-sensors.timer orc-sensors.service 2>&1 | sed 's/^/    stop: /'
    w=0; while pgrep -x wp5 >/dev/null 2>&1 && [ "$w" -lt 10 ]; do sleep 1; w=$((w+1)); done
    if pgrep -x wp5 >/dev/null 2>&1; then
      RESULT="ABORTED: a wp5 process was still running after 10 s; not starting an activation over it"
    else
      RESULT="FAILED"
      for attempt in 1 2; do
        n0=$(rearm_new_lines | wc -l)
        $S rm -f /var/lib/orc-wp5-rearm/last-ok
        echo "  attempt $attempt at uptime $(cut -d. -f1 ${ISS015_UPTIME_FILE:-/proc/uptime})s: stamp removed, starting orc-wp5-rearm"
        timeout 110 $S systemctl start orc-wp5-rearm; rc=$?
        new=$(rearm_new_lines | tail -n +$((n0 + 1)))
        printf '%s\n' "$new" | sed 's/^/    journal: /'
        if grep -q "OK: activated" <<<"$new" && grep -qE "Schedule next startup *\[[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\]" <<<"$new"; then
          RESULT="OK (attempt $attempt, rc=$rc): $(grep -oE 'Schedule next (shutdown|startup) *\[[^]]*\]' <<<"$new" | tr '\n' ' ')"
          break
        fi
        echo "  attempt $attempt did not show 'OK: activated' with a next startup (rc=$rc)"
        sleep 3
      done
    fi
  fi
else
  RESULT="SKIPPED: sudo -n does not work for this user; no writes made"
fi
echo "  RECOVERY RESULT: $RESULT"
echo "  RTC-copy lines of this boot (wp5d.log): $(tail -n 8 /var/log/wp5d.log 2>/dev/null | tr -d '\000' | grep -aE '^[A-Z][a-z]{2} [A-Z][a-z]{2} |Startup reason' | tail -n 2 | tr '\n' ' ')"
case "$RESULT" in OK*) ;; *) echo "  !! WAKE NOT RE-ESTABLISHED BY THIS SCRIPT - a second press, or an attended session, is needed";; esac

sec "1. boot list (end time of each boot = its last journal entry)"
BL=$(jc --list-boots --no-pager)
printf '%s\n' "$BL" | tail -n 14
# Boots are found by END time, not by -1/-2: after the 2026-11-11 stop the station booted again
# (17:00) so "previous boot" is no longer the 12:00 boot. Falls back to -1/-2/-10 if not found.
findboot() { printf '%s\n' "$BL" | awk -v pat="$1" '$0 ~ pat { id=$1 } END { print id }'; }
B_STOP=$(findboot "2026-11-11 12:0[0-9]:[0-9][0-9] UTC$");  [ -n "$B_STOP" ] || B_STOP=-1
B_NORM=$(findboot "2026-11-11 11:3[0-9]:[0-9][0-9] UTC$");  [ -n "$B_NORM" ] || B_NORM=-2
B_PRESS=$(findboot "2026-11-11 07:5[0-9]:[0-9][0-9] UTC$"); [ -n "$B_PRESS" ] || B_PRESS=-10
B_1700=$(findboot "2026-11-11 17:0[0-9]:[0-9][0-9] UTC$");  [ -n "$B_1700" ] || B_1700=-1
echo "  boot index used: stopped(12:0x)=$B_STOP  17:0x=$B_1700  normal(11:3x)=$B_NORM  press(07:5x)=$B_PRESS"
echo "  boots that ended 12:03-17:00 (any boot here means the Pi powered on during the gap):"
printf '%s\n' "$BL" | awk '$0 ~ /2026-11-11 (12:[0-5][0-9]|1[3-6]:[0-5][0-9]|17:00):[0-9][0-9] UTC$/ && $0 !~ /12:0[0-2]:[0-9][0-9] UTC$/' | head -n 20

sec "2. LAST 80 LINES OF THE STOPPED BOOT (the 12:00 boot, chosen by end time)"
jc -b "$B_STOP" -n 80 -o short-iso --no-pager

sec "2b. THE 17:00 WAKE (Tailscale showed it online only ~40 s): its last 60 lines and kernel tail"
jc -b "$B_1700" -n 60 -o short-iso --no-pager | cut -c1-170
echo "  --- kernel, last 25 of that boot"; jc -b "$B_1700" -k -n 25 -o short-iso --no-pager | cut -c1-170

sec "4. orc-wp5-rearm journal (last 14 lines: pre-change headers of the 12:00 boot and this boot)"
jc -t orc-wp5-rearm --no-pager -o short-iso | tail -n 14

sec "5. wp5d.log tail (binary-safe)"
tail -n 60 /var/log/wp5d.log 2>&1 | tr -d '\000'

# Read the stopped boot's journal ONCE into memory (nothing written to disk) and search the copy.
PB=$(timeout 25 journalctl -b "$B_STOP" -o short-iso --no-pager 2>&1) || PB=$(timeout 25 $S journalctl -b "$B_STOP" -o short-iso --no-pager 2>&1)
PBU=$(timeout 25 journalctl -b "$B_STOP" -o short-unix --no-pager 2>&1) || PBU=$(timeout 25 $S journalctl -b "$B_STOP" -o short-unix --no-pager 2>&1)
echo "  (read stopped boot: $(printf '%s\n' "$PB" | wc -l) lines)"

sec "3. previous boot: power / shutdown / voltage / kill keywords (last 25)"
printf '%s\n' "$PB" | grep -iE "shutdown|poweroff|power-off|reboot|under-voltage|undervoltage|throttl|oom|out of memory|killed process|panic|watchdog|wp5d_poweroff|orc-wake-ceiling|Caught signal" | tail -n 25

sec "3b. WAS IT US? the 12:00 boot around our grab (12:00:44-12:00:50): ssh sessions, sudo, kernel"
echo "  --- ssh logins/logouts in the stopped boot"
printf '%s\n' "$PB" | grep -E "sshd.*(Accepted|session opened|session closed|Disconnected|Connection closed)" | tail -n 12 | cut -c1-170
echo "  --- sudo sessions in the stopped boot"
printf '%s\n' "$PB" | grep -E "sudo.*(session opened|session closed|COMMAND)" | tail -n 16 | cut -c1-170
echo "  --- kernel messages, last 50 of the stopped boot (i2c / usb / voltage / mmc errors would show here)"
jc -b "$B_STOP" -k -n 50 -o short-iso --no-pager | cut -c1-170

sec "3c. WAS IT NTP/CLOCK? clock jumps in the stopped boot, and chrony's own log (journal only, no chronyc)"
echo "  --- chrony journal, stopped boot"
printf '%s\n' "$PB" | grep -E "chronyd|chrony\[" | tail -n 25 | cut -c1-170
echo "  --- journal time jumps > 5 min or backwards, stopped boot (PREV / CUR)"
printf '%s\n' "$PBU" | awk '{ t=$1+0; if (NR>1 && (t-p>300 || t<p) && t>1700000000) { printf "JUMP %+.0f s\nPREV %s\nCUR  %s\n\n", t-p, substr(pl,1,150), substr($0,1,150) } p=t; pl=$0 }' | head -n 40
echo "  --- orc-sensors and upload in the stopped boot (wp5 sampling errors, missing batches)"
printf '%s\n' "$PB" | grep -E "orc-sensors|orc-sensors-upload|orc-capture" | tail -n 25 | cut -c1-170

sec "3d. COMPARISON: how a normal wake ends (11:30, no grab) and how the button-press wake ended (07:51, grabbed, survived)"
echo "  --- boots chosen by end time (see section 1): normal=$B_NORM press=$B_PRESS"
echo "  --- last 25 lines of the 11:3x boot"; jc -b "$B_NORM" -n 25 -o short-iso --no-pager | cut -c1-170
echo "  --- last 25 lines of the 07:5x boot"; jc -b "$B_PRESS" -n 25 -o short-iso --no-pager | cut -c1-170

sec "6. Witty Pi sensor rows from the 12:00 wake (voltage and boot reason up to the end)"
tail -n 8 /var/log/orc/sensors/wittypi_2026-11-11.csv 2>&1 | cut -c1-200
echo "  sensor files today:"; ls -l --time-style=full-iso /var/log/orc/sensors 2>&1 | grep "2026-11-1[01]" | tail -n 12

sec "7. files stranded by a wrong clock + the upload watermark"
echo "  watermark: $(stat -c '%y' /var/lib/orc-sensors/upload.state 2>&1)"
echo "  sensor files not dated this month:"
ls -l --time-style=long-iso /var/log/orc/sensors 2>&1 | grep -E '_2026-0[1-9]-|_2026-10-' | tail -n 20
echo "  files older than the watermark (find -newer would not upload them):"
[ -f /var/lib/orc-sensors/upload.state ] && find /var/log/orc/sensors -type f ! -newer /var/lib/orc-sensors/upload.state 2>/dev/null | wc -l

sec "8. this boot's power flags (no menu access)"
timeout 5 vcgencmd get_throttled 2>&1

sec "9. station checkout (what a git pull there would meet). --no-optional-locks: nothing here writes to .git"
R=/home/pi/code/git/openrivercam
G="git --no-optional-locks -C $R"
echo "  path exists: $([ -d $R/.git ] && echo yes || echo NO)   owner: $(stat -c '%U' $R 2>&1)"
echo "  HEAD: $($G rev-parse HEAD 2>&1)"
echo "  branch: $($G rev-parse --abbrev-ref HEAD 2>&1)   upstream: $($G rev-parse --abbrev-ref '@{upstream}' 2>&1)"
echo "  remotes:"; $G remote -v 2>&1 | sed 's/^/    /'
echo "  last commits:"; $G log -5 --format='    %h %ad %s' --date=short 2>&1
echo "  local changes (a pull must not trample these):"; $G status --porcelain=v1 2>&1 | head -n 40 | sed 's/^/    /'
echo "  diff vs HEAD (stat):"; $G diff --stat 2>&1 | tail -n 15 | sed 's/^/    /'
for f in usr/local/bin/orc-wp5-rearm usr/local/bin/orc-wake-ceiling; do
  [ -f /$f ] && [ -f $R/spring_2026_ID/pi/sukabumi/$f ] && { cmp -s /$f $R/spring_2026_ID/pi/sukabumi/$f && echo "    $f: installed == checkout" || echo "    $f: installed DIFFERS from checkout"; }
done
for f in usr/local/bin/orc-sensors-upload usr/local/lib/orc-sensors/sensors_logger.py; do
  src=$R/spring_2026_ID/pi/shared/$f
  [ -f /$f ] && [ -f $src ] && { cmp -s /$f $src && echo "    $f: installed == checkout" || echo "    $f: installed DIFFERS from checkout"; }
done

echo; echo "=== ISS015 PRESS-BOOT RECOVERY + EVIDENCE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
}

main < /dev/null
