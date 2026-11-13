set -u
# ISS-FIELD-015 clock floor ROLLBACK. Run through todo119_wake_runner.py only on Tom's say-so.
# STATION WRITES, ROOT (sudo -n): disable the unit, restore the newest backed-up sensors_logger.py,
# remove the unit and the script, daemon-reload. Takes effect at the next boot. The schedule and the
# RTC are not touched, so no button press is needed. The floor file is left in place (harmless);
# to remove it too, delete /var/lib/orc-clock-floor/floor by hand.
# Does not start or stop anything mid-wake.

main() {
S="sudo -n"; BK=/var/lib/orc-clock-floor-backup
LOGGER=/usr/local/lib/orc-sensors/sensors_logger.py
echo "=== ISS015 FLOOR ROLLBACK $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
$S true 2>/dev/null || { echo "REFUSED: sudo -n is not available"; return 2; }
latest=$(ls -1t "$BK"/sensors_logger.py.* 2>/dev/null | head -1)
[ -n "$latest" ] || { echo "REFUSED: no backup of sensors_logger.py in $BK"; return 2; }
echo "backup to restore: $latest ($(sha256sum "$latest" | cut -c1-16))"
python3 -I -c "import sys; p=sys.argv[1]; compile(open(p).read(), p, 'exec')" "$latest" || { echo "REFUSED: backup does not compile"; return 2; }
$S systemctl disable orc-clock-floor.service 2>&1 | sed 's/^/  /'
mode=$(stat -c '%a' "$LOGGER"); own=$(stat -c '%U' "$LOGGER"); grp=$(stat -c '%G' "$LOGGER")
$S install -m "$mode" -o "$own" -g "$grp" "$latest" "$LOGGER.new" && $S mv -f "$LOGGER.new" "$LOGGER" || { echo "FAILED restoring logger"; return 1; }
$S rm -f /etc/systemd/system/orc-clock-floor.service /usr/local/bin/orc-clock-floor
$S systemctl daemon-reload
echo "logger now: $(sha256sum "$LOGGER" | cut -c1-16)   unit file: $(ls /etc/systemd/system/orc-clock-floor.service 2>&1 | tail -1)"
echo "RESULT: rolled back (effective at next boot). floor file left: $(cat /var/lib/orc-clock-floor/floor 2>&1)"
}
main </dev/null
