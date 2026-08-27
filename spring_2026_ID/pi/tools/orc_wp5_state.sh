#!/bin/bash
# orc_wp5_state.sh — READ-ONLY fast grab of Witty Pi 5 power state. ISS-FIELD-008.
#
# WHY
#   Sukabumi misses a wake and stays down for days (TODO-116). Every theory we
#   have — a load brownout during camera capture, a recovery-voltage threshold
#   that cannot be reached, an alarm left in the past — is decided by state that
#   lives ONLY on the Witty Pi and is not in any upload. The station is awake
#   about two minutes per 30-minute cycle, so there is no leisurely SSH session
#   in which to go look.
#
#   This is the first thing to run when the station comes back, before anything
#   else touches it. It is ordered by value, not by tidiness: if it is killed
#   half way through, the half that ran is the half that mattered.
#
#   `orc_collect.sh` is the thorough bundle and should follow if there is time.
#   This is deliberately the 15-second version.
#
# WHAT IT TOUCHES
#   Nothing. Reads files, runs `vcgencmd`, and drives the `wp5` menu with a
#   timeout to print status. It does not change the schedule, the thresholds,
#   the RTC, or any service. Safe while capturing.
#
# USAGE
#   ssh pi@orc-sukabumi 'sudo bash -s' < orc_wp5_state.sh > wp5-state.txt
#
# Paths are DISCOVERED, not assumed. Witty Pi 4 kept things in ~/wittypi; the
# Witty Pi 5 `wp5` package may not, and guessing wrong is how a two-minute
# window gets wasted on an empty file.

set -u

say() { printf '\n===== %s =====\n' "$*"; }
try() { timeout 10 bash -c "$*" 2>&1 || echo "(failed or timed out: $*)"; }

echo "orc_wp5_state — $(date -u +%Y-%m-%dT%H:%M:%SZ) — $(hostname)"
echo "uptime: $(uptime -p 2>/dev/null)  since: $(uptime -s 2>/dev/null)"

# 1. Undervoltage. The single most decisive bit we can read: bit 0 = undervolt
#    now, bit 16 = undervolt has occurred since boot. If the brownout theory is
#    right this is where it shows up first.
say "1. THROTTLE / UNDERVOLTAGE"
try 'vcgencmd get_throttled; echo "(0x0 = clean; bit0 = undervolt now; bit16 = undervolt occurred)"'
try 'vcgencmd measure_volts; vcgencmd measure_temp'

# 2. Why did this boot happen? Alarm, voltage recovery, or button — this is the
#    answer to the whole TODO-116 mechanism question, and it is only here.
say "2. WITTY PI LOGS (power-on reason)"
try 'ls -la /home/pi/wittypi/ /var/lib/wittypi/ /var/log/wittypi/ /etc/wittypi/ 2>/dev/null'
try 'find / -xdev \( -iname "*wittypi*" -o -iname "wp5*" \) -not -path "*/proc/*" 2>/dev/null | head -40'
for f in /home/pi/wittypi/wittyPi.log /var/log/wittypi/wittyPi.log \
         /var/log/wp5.log /var/log/wittypi.log; do
    [ -f "$f" ] && { say "log: $f"; try "tail -80 '$f'"; }
done

# 3. The alarm state. "Next startup in the past with nothing to re-arm it" is
#    the TODO-116 latch hypothesis; this either shows it or kills it.
say "3. WP5 STATUS / SCHEDULE / THRESHOLDS"
try 'systemctl status wp5d --no-pager -l | head -20'
# The wp5 CLI is an interactive menu and the option numbers are NOT documented
# in this repo — the docs only ever cite 5, 6, 7 and 14. So capture the bare
# menu FIRST: it lists every option by number, which is how we learn where the
# low-voltage cutoff and recovery voltage actually live. Guessing a number and
# getting a different screen wastes the window.
try 'printf "q\n" | timeout 8 wp5'
#
# ONLY options this repo documents as reads are exercised below. Do NOT sweep
# unknown option numbers looking for the thresholds:
#   - Option 1 is a WRITE. deploy.sh runs `printf '1\n14\n' | wp5` to sync the
#     RTC from the system clock, so selecting 1 changes the device.
#   - The threshold screens are setters. They prompt for a value, and on
#     Witty Pi a low-voltage threshold of 0 means DISABLED. Feeding stray input
#     to a setter risks disabling the cutoff on a LiFePO4 pack, which is how you
#     over-discharge it. Not a acceptable risk for a diagnostic.
# Read the menu text captured above, identify the right numbers, then add them
# here deliberately. One extra wake window is cheap; a mutated power config is
# not.
try 'echo "14" | timeout 8 wp5 2>&1 | head -20'   # documented: shows RTC time
try 'echo "7"  | timeout 8 wp5 2>&1 | head -30'   # documented: schedule status
try 'timeout 8 wp5 --help; timeout 8 wp5 -h'
try 'cat /home/pi/wittypi/schedule.wpi /home/pi/wittypi/.schedule 2>/dev/null'
try 'ls -la /home/pi/wittypi/schedules/ /etc/wittypi/schedules/ 2>/dev/null'
# Whatever holds the low-voltage cutoff and recovery voltage, it is a config
# file somewhere under one of these trees. Dump small files wholesale.
try 'for d in /home/pi/wittypi /etc/wittypi /var/lib/wittypi; do
       [ -d "$d" ] && find "$d" -maxdepth 2 -type f -size -32k \
         \( -name "*.conf" -o -name "*.json" -o -name "*.txt" -o -name ".*" \) \
         -exec sh -c "echo; echo \"--- {} ---\"; cat {}" \; ;
     done'

# 4. The I2C device itself, in case the userland tooling has moved on.
say "4. I2C"
try 'i2cdetect -y 1'

# 5. How the PREVIOUS session ended. A clean shutdown looks different from a
#    power cut, and that distinction is the trigger half of TODO-116.
say "5. PREVIOUS BOOT TAIL"
try 'journalctl -b -1 -n 40 --no-pager'
try 'last -x -n 15 2>/dev/null'
try 'journalctl -b 0 -n 40 --no-pager | tail -40'

# 6. Capture chain — the video yield collapsed while off-schedule boots rose,
#    so whether the relay/camera came up this cycle is part of the same picture.
say "6. CAPTURE CHAIN"
try 'journalctl -b 0 -u orc-capture --no-pager -n 40'
try 'pinctrl get 24 2>/dev/null; poe-relay status 2>/dev/null'

say "7. ORC-OS SHUTDOWN SETTINGS"
try 'python3 -c "
import sqlite3
c=sqlite3.connect(\"/home/pi/.ORC-OS/orc-os.db\").cursor()
c.execute(\"SELECT reboot_after, shutdown_after_task, active FROM settings\")
print(c.fetchone())
"'

echo
echo "===== END ====="
