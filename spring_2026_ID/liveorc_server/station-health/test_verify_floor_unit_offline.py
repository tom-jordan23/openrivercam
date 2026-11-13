#!/usr/bin/env python3
"""Test verify_floor_unit_offline.py: it must pass a benign neighbourhood and FAIL on a real ordering cycle. No station."""
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"   <-- {detail}"))


def dump(wp5d_after=""):
    return f"""=== UNITS DUMP ===
@@@ UNIT wp5d.service
# /etc/systemd/system/wp5d.service
[Unit]
Description=wp5d
After=remote-fs.target {wp5d_after}
[Service]
Type=simple
ExecStart=/usr/bin/wp5d
[Install]
WantedBy=multi-user.target
@@@ SHOW wp5d.service
After=remote-fs.target
@@@ UNIT chrony.service
# /usr/lib/systemd/system/chrony.service
[Unit]
Description=chrony
After=network.target
[Service]
Type=forking
ExecStart=/usr/sbin/chronyd
[Install]
WantedBy=multi-user.target
@@@ UNIT orc-api.service
# /etc/systemd/system/orc-api.service
[Unit]
Description=orc api
Before=nginx.service
After=network.target wp5d.service
[Service]
ExecStart=/home/pi/venv/orc-os/bin/uvicorn main:app
[Install]
WantedBy=multi-user.target
@@@ UNIT orc-sensors.timer
# /etc/systemd/system/orc-sensors.timer
[Unit]
Description=sensors timer
[Timer]
OnBootSec=1min
[Install]
WantedBy=timers.target
@@@ UNIT orc-sensors.service
# /etc/systemd/system/orc-sensors.service
[Unit]
After=local-fs.target
[Service]
Type=oneshot
ExecStart=/usr/local/bin/orc-sensors
=== END ===
"""


def run(text):
    d = Path(tempfile.mkdtemp(prefix="vt_")); (d / "dump.txt").write_text(text)
    return subprocess.run([sys.executable, "-I", str(HERE / "verify_floor_unit_offline.py"), str(d / "dump.txt")], capture_output=True, text=True)


def main():
    r = run(dump())
    check("V1 reconstructs the units and passes a benign neighbourhood", r.returncode == 0 and "no ordering cycle" in r.stdout and "orc-api.service" in r.stdout, r.stdout[-400:] + r.stderr[-200:])
    r = run(dump(wp5d_after="orc-clock-floor.service"))        # wp5d ordered after our unit, our unit after wp5d: a cycle
    check("V2 a real ordering cycle through our unit is reported and fails", r.returncode == 1 and "PROBLEM" in r.stdout, r.stdout[-500:] + r.stderr[-200:])
    r = run("=== UNITS DUMP ===\n=== END ===\n")
    check("V3 an empty dump is refused, not passed", r.returncode != 0, r.stdout[-200:])
    bad = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(bad)}/{len(results)} passed" + (f"; FAILED: {bad}" if bad else "")); sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
