set -u
echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# Is this an upload outage, a capture outage, or a power problem? The station
# has been recording all three locally the whole time - the CSVs never needed
# the network. Small files, so take them whole rather than summarising on the
# station where a mistake is invisible.
S=/var/log/orc/sensors

echo "=== A. capture result per cycle, today (does the camera keep failing) ==="
echo "  codes: 1=delivered, 5=all-attempts-failed"
cat $S/orccapture_2026-09-02.csv 2>/dev/null | sed 's/^/  /'

echo
echo "=== B. battery, today, whole file (is the outage tracking the discharge) ==="
cat $S/wittypi_2026-09-02.csv 2>/dev/null | sed 's/^/  /'

echo
echo "=== C. yesterday's battery for comparison (was last night this low too) ==="
# If 09-01 fell just as far overnight WITHOUT an outage, voltage is not the
# discriminator and the power story is dead.
cat $S/wittypi_2026-09-01.csv 2>/dev/null | sed 's/^/  /'

echo
echo "=== D. capture results yesterday, same comparison ==="
cat $S/orccapture_2026-09-01.csv 2>/dev/null | sed 's/^/  /'

echo "=== END ==="
