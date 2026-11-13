set -u
# ISS-FIELD-015: print the EXACT unit files (with drop-ins) that the clock-floor unit is ordered against, so that
# verify_floor_unit_offline.py can check for ordering cycles on a workstation. READ-ONLY: `systemctl cat` and `systemctl show` only.
# Station times are UTC. Run through todo119_wake_runner.py.
main() {
echo "=== UNITS DUMP $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
for u in orc-api.service orc-sensors.service orc-sensors.timer wp5d.service chrony.service orc-wp5-rearm.service orc-wp5-ceiling.service \
         orc-maintenance-check.service orc-sensors-upload.service orc-sensors-upload.timer; do
  if systemctl cat "$u" >/dev/null 2>&1; then
    echo "@@@ UNIT $u"
    systemctl cat "$u" 2>&1
    echo "@@@ SHOW $u"
    systemctl show "$u" -p After -p Before -p Requires -p Wants -p WantedBy -p Conflicts -p BindsTo -p PartOf 2>&1
  else echo "@@@ ABSENT $u"; fi
done
echo "@@@ ALL orc-* units installed:"; systemctl list-unit-files 'orc-*' --no-legend 2>&1 | cut -c1-100
echo "=== END ==="
}
main </dev/null
