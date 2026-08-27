#!/bin/bash
# orc_deploy_wittypi_sensor.sh — install the Witty Pi power-rail sensor.
# ISS-FIELD-008 / TODO-116.
#
# WHY
#   `sensor_readings` carries ds18b20, rg15 and sht40 and nothing electrical, so
#   "the battery is the problem" has been unfalsifiable for four months. This
#   adds vin/vout/iout to the existing upload path, which makes the overnight
#   discharge curve visible on the server and separates the four competing
#   explanations (worn pack / BMS tripping on imbalance / cutoff wrong for
#   LiFePO4 / parasitic load).
#
#   No server-side change is needed: orc-sensors-upload ships any CSV in the
#   log dir, and sensor-ingest derives sensor and metric names from the filename
#   and header row with no whitelist.
#
# WHY IT IS SHAPED LIKE THIS
#   The station is awake under a minute per cycle, so this is ONE ssh round trip
#   with both files inlined — no scp handshakes, no second connection.
#
#   It replaces sensors_logger.py, which every other sensor depends on. A syntax
#   error there would silently end sht40/rg15/ds18b20 logging too, and we would
#   not find out until the graphs went flat. So: back up, py_compile the
#   candidate BEFORE it goes live, and roll back automatically if it fails.
#
# WHAT IT TOUCHES
#   /usr/local/lib/orc-sensors/sensors_logger.py  (replaced, backup kept)
#   /etc/orc-sensors/wittypi.conf                 (new)
#   Nothing else. No systemd units, no schedule, no Witty Pi settings. The
#   sensor timer picks the new config up on its next tick.
#
# USAGE
#   ./orc_deploy_wittypi_sensor.sh [user@host]        # default pi@orc-sukabumi
#   ./orc_deploy_wittypi_sensor.sh --dry-run          # print, connect to nothing
#
# ROLLBACK
#   ssh pi@orc-sukabumi 'sudo cp /usr/local/lib/orc-sensors/sensors_logger.py.bak \
#                                /usr/local/lib/orc-sensors/sensors_logger.py \
#                        && sudo rm -f /etc/orc-sensors/wittypi.conf'

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SHARED="$HERE/../shared"
LOGGER="$SHARED/usr/local/lib/orc-sensors/sensors_logger.py"
CONF="$SHARED/etc/orc-sensors/wittypi.conf"

TARGET="pi@orc-sukabumi"
DRY=0
for a in "$@"; do
    case "$a" in
        --dry-run) DRY=1 ;;
        *) TARGET="$a" ;;
    esac
done

for f in "$LOGGER" "$CONF"; do
    [ -f "$f" ] || { echo "missing: $f" >&2; exit 1; }
done

# Validate locally first. Pushing a file that cannot compile wastes the window.
python3 -m py_compile "$LOGGER" || { echo "local py_compile failed" >&2; exit 1; }
grep -q '"wittypi": read_wittypi' "$LOGGER" || {
    echo "logger has no wittypi driver registered" >&2; exit 1; }

B64_LOGGER="$(base64 -w0 "$LOGGER")"
B64_CONF="$(base64 -w0 "$CONF")"

REMOTE=$(cat <<REMOTE_EOF
set -eu
LOGGER=/usr/local/lib/orc-sensors/sensors_logger.py
CONF=/etc/orc-sensors/wittypi.conf

# Stage beside the target, never over it, until it has compiled.
echo "$B64_LOGGER" | base64 -d > /tmp/sensors_logger.candidate
echo "$B64_CONF"   | base64 -d > /tmp/wittypi.conf.candidate

python3 -m py_compile /tmp/sensors_logger.candidate || {
    echo "REMOTE py_compile FAILED — nothing changed"; exit 1; }

sudo cp -a "\$LOGGER" "\$LOGGER.bak"
# Stage into the TARGET directory then rename. install(1) copies in place, and
# this station can lose power at any moment — a truncated sensors_logger.py
# would break sht40, rg15 and ds18b20 as well as the new sensor. rename(2) on
# the same filesystem is atomic, so the file is either the old one or the new
# one and never half of either.
sudo install -m 0755 /tmp/sensors_logger.candidate "\$LOGGER.new"
sudo mv -f "\$LOGGER.new" "\$LOGGER"
sudo install -m 0644 /tmp/wittypi.conf.candidate "\$CONF.new"
sudo mv -f "\$CONF.new" "\$CONF"

echo "--- test run (all sensors) ---"
if sudo /usr/local/bin/orc-sensors; then
    echo "orc-sensors OK"
else
    echo "orc-sensors FAILED — rolling back sensors_logger.py"
    sudo cp -a "\$LOGGER.bak" "\$LOGGER"
    sudo rm -f "\$CONF"
    exit 1
fi

echo "--- wittypi CSV ---"
tail -3 /var/log/orc/sensors/wittypi_\$(date +%F).csv 2>/dev/null || echo "(no wittypi CSV yet)"
echo "--- other sensors still writing ---"
for s in sht40 rg15 ds18b20; do
    printf '%-9s %s\n' "\$s" "\$(tail -1 /var/log/orc/sensors/\${s}_\$(date +%F).csv 2>/dev/null || echo MISSING)"
done

# Piggyback the long-wake question onto this connection. Extended wakes are the
# energy problem (25 min vs 2 min, ~12x), and there are two candidate causes:
# ORC-OS's "shutdown after task" got unset, or its task keeps failing before it
# reaches the shutdown step. These reads are ~1 s and settle the first outright.
echo "--- ORC-OS settings (shutdown_after_task is the one that matters) ---"
python3 - <<'PYEOF' 2>&1 || echo "(settings read failed)"
import sqlite3
c = sqlite3.connect("/home/pi/.ORC-OS/orc-os.db").cursor()
c.execute("SELECT * FROM settings")
cols = [d[0] for d in c.description]
for row in c.fetchall():
    for k, v in zip(cols, row):
        print(f"  {k} = {v}")
PYEOF

echo "--- did THIS wake finish its task? ---"
journalctl -b 0 -u orc-api --no-pager -n 25 2>&1 | tail -25
echo "--- orc-capture this boot ---"
journalctl -b 0 -u orc-capture --no-pager -n 15 2>&1 | tail -15
REMOTE_EOF
)

if [ "$DRY" = 1 ]; then
    echo "--- would run on $TARGET ---"
    echo "$REMOTE" | sed 's/^/  /'
    exit 0
fi

echo "deploying to $TARGET ..."
ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 "$TARGET" "bash -s" <<< "$REMOTE"
