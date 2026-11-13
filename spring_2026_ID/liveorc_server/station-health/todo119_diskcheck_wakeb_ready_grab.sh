set -u
# 2026-11-13, after the orphaned-plot deletion: (1) did the disk manager see the freed space? (2) what does clock-floor wake B still depend
# on that has not been read from the real station? READ-ONLY (stdout only; sudo -n only for `sudo -n -l`). Run through todo119_wake_runner.py.
# Station times are UTC. Env overrides (tests only): ISS_SKIP_JOURNAL.
main() {
sec() { echo; echo "=== $1 ==="; }
echo "=== DISKCHECK + WAKE-B READINESS $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "  free: $(df -B1M --output=avail,pcent / 2>/dev/null | tail -1)   (MiB avail, use%)   uptime s: $(cut -d' ' -f1 /proc/uptime | cut -d. -f1)"

sec "1. ORC-OS disk manager (journal of orc-api): free space at each wake check, and any purge"
if [ -z "${ISS_SKIP_JOURNAL:-}" ]; then
  jl=$(timeout 40 journalctl -u orc-api --since "8 hours ago" --no-pager 2>&1)
  case "$jl" in *"insufficient permissions"*|*"No journal files"*) jl=$(timeout 40 sudo -n journalctl -u orc-api --since "8 hours ago" --no-pager 2>&1) ;; esac
  echo "  checks (Available space is sufficient (X GB)), last 14:"
  printf '%s\n' "$jl" | grep "Available space is sufficient" | tail -14 | sed -E 's/^(.{15}).*(disk_management) - INFO - /    \1 /' | cut -c1-120
  echo "  purge activity in the last 8 hours:"
  echo "    'purging media folder' lines: $(printf '%s\n' "$jl" | grep -c 'purging media folder')   'Purged ' lines: $(printf '%s\n' "$jl" | grep -c 'Purged ')   'No files can be deleted': $(printf '%s\n' "$jl" | grep -c 'No files can be deleted')"
  printf '%s\n' "$jl" | grep "Purged \|purging media folder" | tail -4 | cut -c1-200 | sed 's/^/    /'
fi

sec "2. does /tmp survive a reboot? (wake A stages into /tmp/orc-floor-stage; every wake is a reboot)"
echo "  /tmp filesystem: $(findmnt -no FSTYPE,SIZE,OPTIONS /tmp 2>&1 | cut -c1-120)"
ls -la /tmp/orc-floor-stage /var/tmp/orc-floor-stage 2>&1 | head -6 | sed 's/^/  /'
echo "  tmpfiles rules for /tmp:"; grep -hv '^#\|^$' /usr/lib/tmpfiles.d/tmp.conf /etc/tmpfiles.d/tmp.conf 2>/dev/null | sed 's/^/    /'

sec "3. can wake B do its root steps? (sudo -n only lists what is allowed)"
echo "  sudo -n true: $(sudo -n true 2>&1 && echo ok)"
sudo -n -l 2>&1 | head -12 | cut -c1-170 | sed 's/^/  /'

sec "4. targets, tools and current state"
ls -ld /usr/local/bin /etc/systemd/system /usr/local/lib/orc-sensors /var/lib 2>&1 | sed 's/^/  /'
echo "  installed logger: $(sha256sum /usr/local/lib/orc-sensors/sensors_logger.py 2>&1 | cut -c1-64)  $(stat -c '%a %U:%G' /usr/local/lib/orc-sensors/sensors_logger.py 2>&1)"
echo "  expected OLD    : 8fe3b052dc1c3b4f895a93f2148cd4a3b9f599b8b7d4555f06c1bb3da3550a98"
for t in install base64 sha256sum systemd-analyze python3 mv cp sync env; do printf '  %-16s %s\n' "$t" "$(command -v $t || echo MISSING)"; done
echo "  floor files present?  script: $(ls /usr/local/bin/orc-clock-floor 2>&1 | head -1)   unit: $(ls /etc/systemd/system/orc-clock-floor.service 2>&1 | head -1)   state dir: $(ls -d /var/lib/orc-clock-floor 2>&1 | head -1)"
echo "  system state: $(systemctl is-system-running 2>&1)   failed units: $(systemctl --failed --no-legend 2>/dev/null | wc -l)"
systemctl --failed --no-legend 2>/dev/null | cut -c1-150 | sed 's/^/    /'
echo "  next orc-sensors tick:"; systemctl list-timers orc-sensors.timer --no-legend 2>&1 | cut -c1-150 | sed 's/^/    /'

sec "5. how soon after boot does chrony sync? (decides whether wake B's floor seed can succeed in the first minute)"
echo "  now: uptime $(cut -d' ' -f1 /proc/uptime | cut -d. -f1) s; $(timeout 5 chronyc tracking 2>&1 | grep -E 'Stratum|Leap status|Reference ID' | tr '\n' ';')"
timeout 20 journalctl -u chrony -b --no-pager 2>&1 | grep -i "selected source\|System clock wrong\|System clock was stepped\|Source .* online" | head -6 | cut -c1-170 | sed 's/^/    /'
echo; echo "=== END ==="
}
main </dev/null
