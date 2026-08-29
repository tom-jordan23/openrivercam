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
#   Also ships the Witty Pi BOOT CONTEXT (ISS-FIELD-010): power-on reason,
#   previous shutdown reason, and downtime_s measured by the station's own
#   clock, folded into the wittypi row so they ride the sensor upload instead of
#   waiting for an SSH window Tailscale has repeatedly failed to provide.
#
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
#   /etc/orc-sensors/orccapture.conf              (new)
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
CAPCONF="$SHARED/etc/orc-sensors/orccapture.conf"

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

# py_compile only proves the file parses. TODO-117 shipped a driver that parsed
# perfectly and paired voltage with a current from a different sample, which was
# not visible until a day of uploaded rows turned out to be unfittable. This
# exercises the sampling logic against synthetic wp5 output and checks the
# emitted keys against CSV_HEADER, in-process, before the window opens.
"$HERE/test_wittypi_pairing.py" >/dev/null 2>&1 || {
    echo "wittypi pairing test FAILED — run test_wittypi_pairing.py" >&2; exit 1; }
# The capture driver classifies which fault a wake hit. A misclassification is
# worse than no data — it would send a site visit after the wrong component.
"$HERE/test_orccapture.py" >/dev/null 2>&1 || {
    echo "orccapture test FAILED — run test_orccapture.py" >&2; exit 1; }

B64_LOGGER="$(base64 -w0 "$LOGGER")"
B64_CONF="$(base64 -w0 "$CONF")"
B64_CAPCONF="$(base64 -w0 "$CAPCONF")"

REMOTE=$(cat <<REMOTE_EOF
set -eu
LOGGER=/usr/local/lib/orc-sensors/sensors_logger.py
CONF=/etc/orc-sensors/wittypi.conf
CAPCONF=/etc/orc-sensors/orccapture.conf

# ── Diagnostics FIRST ────────────────────────────────────────────────
# These are read-only and cost about a second. They run before anything can
# abort so the wake window always yields them, even if the deploy backs out.
# The question they answer: extended wakes are the energy problem (25 min
# against 2 min, ~12x), and either ORC-OS's shutdown-after-task got unset, or
# its task keeps failing before reaching the shutdown step.
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

echo "--- orc-api, this boot ---"
journalctl -b 0 -u orc-api --no-pager -n 20 2>&1 | tail -20
echo "--- orc-capture, this boot ---"
journalctl -b 0 -u orc-capture --no-pager -n 12 2>&1 | tail -12

# ── Pre-flight the wp5 read ──────────────────────────────────────────
# The previous attempt installed the sensor, found wp5 returned nothing, and
# rolled back — a whole wake window spent to learn one fact. Prove the exact
# read works BEFORE touching anything, so a bad read costs nothing.
echo "--- wp5 read pre-flight ---"
PROBE="\$(printf '14\\n' | timeout 10 wp5 2>&1 | grep -m1 -i 'V-IN' || true)"
if [ -z "\$PROBE" ]; then
    echo "PRE-FLIGHT FAILED: no V-IN line from wp5. Nothing installed, nothing changed."
    exit 1
fi
echo "  \$PROBE"

# ── Install ──────────────────────────────────────────────────────────
echo "$B64_LOGGER" | base64 -d > /tmp/sensors_logger.candidate
echo "$B64_CONF"   | base64 -d > /tmp/wittypi.conf.candidate
echo "$B64_CAPCONF" | base64 -d > /tmp/orccapture.conf.candidate

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
sudo install -m 0644 /tmp/orccapture.conf.candidate "\$CAPCONF.new"
sudo mv -f "\$CAPCONF.new" "\$CAPCONF"
sudo mv -f "\$CONF.new" "\$CONF"

# Test AS THE SERVICE USER, never as root. orc-sensors.service is User=pi, and
# running the test with sudo does two kinds of damage: it validates a path that
# never executes in production, and it creates the day's CSV owned by root so
# every subsequent timer run fails with EACCES. That is exactly what happened on
# 2026-08-27 — the sensor logged once, from this test, and never again.
echo "--- test run (all sensors, as the service user) ---"
if sudo -u pi /usr/local/bin/orc-sensors; then
    echo "orc-sensors OK"
else
    echo "orc-sensors FAILED — rolling back sensors_logger.py"
    sudo cp -a "\$LOGGER.bak" "\$LOGGER"
    sudo rm -f "\$CONF"
    exit 1
fi

# Belt and braces: whatever created today's CSVs, make sure the service user
# owns them before we walk away.
sudo chown -R pi:pi /var/log/orc/sensors 2>/dev/null || true

# ISS-FIELD-010: the boot context is read from /var/log/wp5d.log by the SERVICE
# USER, and nothing has ever verified that pi can read it. The 2026-08-27
# capture proves only that ROOT could — the collector ran under sudo. If pi
# cannot, the feature degrades quietly to power_on_reason_code = -2 and we would
# not find out until a week of rows came back empty, which is the whole failure
# pattern this deploy script exists to break.
echo "--- wp5d.log readability (as the service user) ---"
ls -l /var/log/wp5d.log 2>/dev/null || echo "(wp5d.log missing)"
if sudo -u pi test -r /var/log/wp5d.log; then
    echo "wp5d.log readable by pi — boot context will populate"
else
    echo "wp5d.log NOT readable by pi — boot context would emit -2 (unreadable)"
    # A read bit on a daemon log is harmless and reversible, and the
    # alternative is waiting another week for a window to fix it by hand.
    sudo chmod o+r /var/log/wp5d.log 2>/dev/null || true
    if sudo -u pi test -r /var/log/wp5d.log; then
        echo "  -> granted o+r; NOTE this may not survive wp5d rotating its log,"
        echo "     so check power_on_reason_code in the uploaded rows stays > -2"
    else
        echo "  -> STILL unreadable; boot context will not populate"
    fi
fi

# Same class of risk as wp5d.log: the capture driver reads the journal AS THE
# SERVICE USER, and journalctl needs adm or systemd-journal group membership.
# Nothing has ever verified pi has it, and if it does not the driver degrades
# quietly to capture_result_code = -2.
echo "--- journal readability (as the service user) ---"
if sudo -u pi journalctl -u orc-capture.service -n 1 --no-pager >/dev/null 2>&1 \
   || sudo -u pi journalctl -t orc-capture -n 1 --no-pager >/dev/null 2>&1; then
    echo "journal readable by pi — capture outcome will populate"
else
    echo "journal NOT readable by pi — capture_result_code would be -2"
    sudo usermod -aG systemd-journal pi 2>/dev/null || true
    echo "  -> added pi to systemd-journal; takes effect on the NEXT boot,"
    echo "     so expect -2 for one cycle and a real code after that"
fi

echo "--- orccapture CSV ---"
tail -2 /var/log/orc/sensors/orccapture_\$(date +%F).csv 2>/dev/null || echo "(no orccapture CSV yet)"

echo "--- wittypi CSV ---"
tail -3 /var/log/orc/sensors/wittypi_\$(date +%F).csv 2>/dev/null || echo "(no wittypi CSV yet)"
echo "--- other sensors still writing ---"
for s in sht40 rg15 ds18b20; do
    printf '%-9s %s\n' "\$s" "\$(tail -1 /var/log/orc/sensors/\${s}_\$(date +%F).csv 2>/dev/null || echo MISSING)"
done
REMOTE_EOF
)

if [ "$DRY" = 1 ]; then
    echo "--- would run on $TARGET ---"
    echo "$REMOTE" | sed 's/^/  /'
    exit 0
fi

echo "deploying to $TARGET ..."
ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 "$TARGET" "bash -s" <<< "$REMOTE"
