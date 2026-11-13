set -u
# ISS-FIELD-015: read the Witty Pi 5 firmware version over I2C (registers 0, 1, 2 ONLY).
# Run through todo119_wake_runner.py (bash -s over ssh) in the first ~2 minutes of a wake.
# Station times are UTC. NOT RUN YET: needs Tom's go for the first direct I2C access.
#
# WHY: software 5.0.0 cannot show the firmware version, and versions before v1.5 have an internal
# I2C pointer race that can corrupt register reads/writes and has overwritten the RTC minute
# register "in practice" (firmware v1.5 release note). See
# research/witty_pi_5_rtc_month_investigation_2026-11-12.md.
#
# WHAT THIS READS (checked against the vendor firmware source, tags v1.0 to v1.7, 2026-11-13):
#   reg 0 = firmware id (0x51 Witty Pi 5 HAT+, 0x52 Mini), reg 1 = major, reg 2 = minor.
#   Each is a compile-time constant returned by get_read_only_register(): no internal I2C
#   access, no flag cleared, no state changed (the only effect is the slave's activity timestamp).
# WHAT IT NEVER TOUCHES: any other register (66 and 71 have read side effects), any write,
#   i2cset, i2cdetect, wp5, wp5d, the RTC, the schedule, the ORC-OS API.
# SAFEGUARDS: refuses if the wake is old (shutdown work is heavy), if a poweroff job is queued,
#   or if the id register is not 0x51/0x52 (then registers 1 and 2 are not read). Each read is one
#   i2cget with an explicit register byte, under the vendor's flock lock. One retry per register.
#   No timeout wrapper on i2cget: killing it between phases could leave a stale register pointer.
# Env overrides (for tests only): ISS015_I2CGET ISS015_LOCK ISS015_BUS ISS015_ADDR ISS015_UPTIME_FILE
#   ISS015_MAX_UPTIME_S ISS015_SKIP_JOBS_CHECK.

main() {
I2CGET="${ISS015_I2CGET:-i2cget}"
LOCK="${ISS015_LOCK:-/var/lock/wittypi5_i2c.lock}"
BUS="${ISS015_BUS:-1}"
ADDR="${ISS015_ADDR:-0x51}"
UPF="${ISS015_UPTIME_FILE:-/proc/uptime}"
MAXUP="${ISS015_MAX_UPTIME_S:-120}"

echo "=== ISS015 FW VERSION READ $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
up=$(cut -d' ' -f1 "$UPF" 2>/dev/null | cut -d. -f1)
echo "uptime s: ${up:-unknown}   bus: /dev/i2c-$BUS   addr: $ADDR   lock: $LOCK"

# --- preconditions: refuse rather than guess ---
if [ -z "${up:-}" ]; then echo "REFUSED: cannot read uptime"; return 2; fi
if [ "$up" -gt "$MAXUP" ]; then echo "REFUSED: wake is ${up}s old (limit ${MAXUP}s); shutdown work may be starting"; return 2; fi
if [ -z "${ISS015_SKIP_JOBS_CHECK:-}" ]; then
  jobs=$(systemctl list-jobs --no-legend 2>/dev/null | grep -Ei 'poweroff|shutdown|reboot|halt' || true)
  if [ -n "$jobs" ]; then echo "REFUSED: a shutdown/poweroff job is queued:"; printf '%s\n' "$jobs" | sed 's/^/  /'; return 2; fi
fi
if ! command -v "$I2CGET" >/dev/null 2>&1; then
  # Debian installs i2c-tools in /usr/sbin, which is not on a non-root ssh PATH (11-13 first attempt).
  for d in /usr/sbin /sbin /usr/bin; do [ -x "$d/$I2CGET" ] && { I2CGET="$d/$I2CGET"; break; }; done
fi
if ! command -v "$I2CGET" >/dev/null 2>&1; then echo "REFUSED: $I2CGET not found (PATH=$PATH)"; return 2; fi
echo "i2cget: $I2CGET   user: $(id -un) groups: $(id -Gn)"
if [ -z "${ISS015_I2CGET:-}" ]; then
  if [ ! -e "/dev/i2c-$BUS" ]; then echo "REFUSED: /dev/i2c-$BUS missing"; return 2; fi
  if [ ! -r "/dev/i2c-$BUS" ] || [ ! -w "/dev/i2c-$BUS" ]; then
    echo "REFUSED: no read/write access to /dev/i2c-$BUS ($(ls -l "/dev/i2c-$BUS")); not escalating"; return 2
  fi
fi
if [ ! -e "$LOCK" ]; then echo "REFUSED: lock file $LOCK missing (the vendor tools create it; do not read without it)"; return 2; fi
exec 9<"$LOCK" || { echo "REFUSED: cannot open $LOCK (permission); not escalating"; return 2; }

# --- one allow-listed read: only registers 0, 1, 2 ---
rd() {
  local reg=$1 out rc try
  case "$reg" in 0|1|2) ;; *) echo "BUG: register $reg is not allow-listed" >&2; return 99 ;; esac
  for try in 1 2; do
    if ! flock -w 5 9; then echo "  reg $reg: lock not acquired in 5 s (try $try)" >&2; sleep 3; continue; fi
    out=$("$I2CGET" -y "$BUS" "$ADDR" "$reg" b 2>&1); rc=$?
    flock -u 9
    if [ $rc -eq 0 ] && printf '%s' "$out" | grep -Eq '^0x[0-9a-fA-F]{1,2}$'; then printf '%s' "$out"; return 0; fi
    echo "  reg $reg: try $try failed rc=$rc: $out" >&2; sleep 3
  done
  return 1
}

id=$(rd 0) || { echo "RESULT: could not read register 0; stopping, nothing else read"; return 1; }
echo "reg 0 (firmware id): $id"
case "$id" in
  0x51) echo "  = Witty Pi 5 HAT+" ;;
  0x52)      echo "  = Witty Pi 5 Mini" ;;
  *) echo "RESULT: id $id is neither 0x51 nor 0x52; layout may differ, NOT reading registers 1 and 2"; return 1 ;;
esac
maj=$(rd 1) || { echo "RESULT: reg 1 unreadable"; return 1; }
min=$(rd 2) || { echo "RESULT: reg 2 unreadable"; return 1; }
echo "reg 1 (major): $maj"; echo "reg 2 (minor): $min"
echo "RESULT: firmware v$((maj)).$((min))   (v1.2 and v1.2.1 both report minor 2)"
if [ $((maj)) -gt 1 ] || { [ $((maj)) -eq 1 ] && [ $((min)) -ge 5 ]; }; then
  echo "  v1.5 (pointer-race fix) or later: yes"
else
  echo "  v1.5 (pointer-race fix) or later: NO - the internal pointer race is present"
fi
}
main </dev/null
