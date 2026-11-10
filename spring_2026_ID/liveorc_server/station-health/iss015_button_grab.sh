set -u
# ISS-FIELD-015: one read-only grab on the first boot after the button press.
# Fed over stdin as `bash -s` by todo119_wake_runner.py. Station times are UTC.
#
# READ-ONLY. No station changes at all (Tom dropped the /run/orc-stay-awake
# touch on 2026-11-10: the 12-min ceiling is one-shot, a normal wake ends ~2-3 min
# after boot when ORC-OS powers the Pi off, and the file would not stop that).
# sudo -n is used only to retry journalctl when pi cannot read the journal.
#
# ORDER. Journal reads first (they never talk to the Witty Pi and hold the
# decisive evidence: the re-arm's "re-arm due" line records the header BEFORE it
# changes anything). The wp5 header read comes last, after orc-wp5-rearm has
# finished, so it cannot overlap an activation (an untested path in
# ISS-FIELD-015). The whole script must fit in a normal wake: ORC-OS powers the
# Pi off ~2-3 min after boot, so everything here is bounded and ordered by value.
#
# The body is a function run with stdin from /dev/null: bash reads the whole
# definition before running anything, so no command can eat the rest of the
# script from the ssh pipe, and an ssh drop cannot cut the script mid-read.

main() {
S="sudo -n"
MAX_AHEAD_S=$((26*3600))   # a legit next startup is on the 30-min grid; allow a long night gap
sec() { echo; echo "=== $1 ==="; }
# journalctl as pi; retry with sudo if that failed (a pipeline's status would be tail's)
jc() { local o o2; o=$(journalctl "$@" 2>&1) || { o2=$($S journalctl "$@" 2>&1) && o=$o2 || o="journalctl failed: $o | sudo: $o2"; }; printf '%s\n' "$o"; }

echo "=== ISS015 GRAB $(date -u +%Y-%m-%dT%H:%M:%SZ) (system clock may be stale early in boot) ==="
echo "uptime: $(uptime)"
echo "proc uptime s: $(cut -d' ' -f1 /proc/uptime)"

sec "0. state"
echo "  orc-maintenance-mode: $(ls /run/orc-maintenance-mode 2>&1)"
echo "  orc-stay-awake: $(ls /run/orc-stay-awake 2>&1)"

sec "1. orc-wp5-rearm journal (all boots; 're-arm due' line = header BEFORE the change)"
jc -t orc-wp5-rearm --no-pager -o short-iso | tail -n 300

sec "2. journalctl --list-boots (end time of the 2026-10-21 14:30 boot)"
jc --list-boots --no-pager | tail -n 40

sec "3. wp5d.log: 2026-10-21 and the last 60 lines"
grep -n "^\[2026-10-21" /var/log/wp5d.log 2>&1 | tail -n 80
echo "  --- tail ---"
tail -n 60 /var/log/wp5d.log 2>&1

sec "4. rearm state files"
ls -l --time-style=full-iso /var/log/orc/wp5-rearm.last /var/lib/orc-wp5-rearm/last-ok 2>&1
echo "  last-ok: $(cat /var/lib/orc-wp5-rearm/last-ok 2>&1)"
echo "  rearm.last:"; cat /var/log/orc/wp5-rearm.last 2>&1
echo "  conf:"; cat /etc/orc-wp5-rearm.conf 2>&1

sec "5. schedule.skd / schedule.act mtime and size"
timeout 20 find /home/pi /opt /usr/local -xdev \( -name 'schedule.skd' -o -name 'schedule.act' \) \
  -exec ls -l --time-style=full-iso {} + 2>&1 | head -n 10

sec "6. other context (read-only)"
echo "  orc-wake-ceiling:"; jc -t orc-wake-ceiling --no-pager -o short-iso | tail -n 8
echo "  tailscale:"; timeout 10 tailscale status 2>&1 | head -n 4
echo "  df /:"; df -h / | tail -1

sec "7. wp5 header only (waits for orc-wp5-rearm to finish; menu choice 14 = Exit)"
st=unknown; waited=0
for i in $(seq 1 60); do
  st=$(systemctl is-active orc-wp5-rearm 2>/dev/null)
  case "$st" in activating|reloading) ;; *) break ;; esac
  sleep 2; waited=$((i*2))
done
echo "  orc-wp5-rearm state: ${st:-unknown} (waited ${waited} s)"
hdr=""
for try in 1 2; do
  hdr=$(printf '14\n' | timeout -k 2 20 wp5 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | head -n 60)
  grep -q 'RTC Time:' <<<"$hdr" && break
  echo "  (header read $try gave no RTC line; $([ $try = 1 ] && echo retrying in 5 s || echo giving up))"; sleep 5
done
printf '%s\n' "$hdr" | head -n 40

sec "8. VERDICT (is a next startup armed, and plausible?)"
rtc=$(grep -oE 'RTC Time: [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}' <<<"$hdr" | head -1 | cut -d' ' -f3-)
su=$(grep -oE 'Schedule next startup.*' <<<"$hdr" | head -1)
inuse=0; grep -qE 'Choose schedule script \(in use\)' <<<"$hdr" && inuse=1
verdict=UNKNOWN; why="header unreadable (wp5 failed, timed out, or no RTC line)"
if [ -n "$rtc" ] && grep -q 'Schedule next startup' <<<"$hdr"; then
  rtc_e=$(date -u -d "$rtc" +%s 2>/dev/null)
  if [[ "$su" =~ \[([0-9]{2})\ ([0-9]{2}:[0-9]{2}:[0-9]{2})\] ]]; then
    dd=${BASH_REMATCH[1]}; tt=${BASH_REMATCH[2]}
    ym=${rtc:0:7}; rdd=${rtc:8:2}; rtt=${rtc:11:8}
    cand=$(date -u -d "$ym-$dd $tt" +%s 2>/dev/null)
    # day-of-month earlier than the RTC's (or same day, not later) means next month
    if [ "$((10#$dd))" -lt "$((10#$rdd))" ] || { [ "$dd" = "$rdd" ] && [[ ! "$tt" > "$rtt" ]]; }; then
      nym=$(date -u -d "$ym-01 +1 month" +%Y-%m 2>/dev/null)
      cand=$(date -u -d "$nym-$dd $tt" +%s 2>/dev/null)
    fi
    if ! [[ "$cand" =~ ^[0-9]+$ && "$rtc_e" =~ ^[0-9]+$ ]]; then
      verdict=SUSPECT; why="startup '$su' does not parse against RTC '$rtc'"
    else
      delta=$((cand - rtc_e))
      if [ "$delta" -le 0 ] || [ "$delta" -gt "$MAX_AHEAD_S" ]; then
        verdict=SUSPECT; why="startup ${dd} ${tt} is ${delta} s from RTC ${rtc} (past, or more than $((MAX_AHEAD_S/3600)) h ahead: a missed alarm looks like this)"
      elif [ "$inuse" != 1 ]; then
        verdict=SUSPECT; why="startup armed (${delta} s ahead) but no schedule script is marked '(in use)'"
      else
        verdict=ARMED; why="next startup ${dd} ${tt} is ${delta} s after RTC ${rtc}; script in use"
      fi
    fi
  else
    verdict=NOT_ARMED; why="'Schedule next startup' has no [dd hh:mm:ss] - startup is EMPTY (hypothesis 1)"
  fi
fi
echo "  VERDICT: $verdict - $why"
case "$verdict" in
  ARMED) echo "  Next startup is armed: the Pi should power off normally and wake on the grid.";;
  UNKNOWN) echo "  Header unreadable: re-read it by hand if the Pi is still up.";;
  *) echo "  ACTION NEEDED: no usable next startup. The Pi will probably power off ~2-3 min after boot (ORC-OS) and may not wake again; a second press is then needed."
     echo "  Recovery that held before (ISS-FIELD-013): sudo wp5 -> 6 (Choose schedule script) -> re-pick the script. That is a schedule write: Tom's approval first.";;
esac

echo; echo "=== ISS015 GRAB DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
}

main < /dev/null
