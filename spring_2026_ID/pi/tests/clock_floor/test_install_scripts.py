#!/usr/bin/env python3
"""Sandbox tests for the clock-floor install scripts (ISS-FIELD-015). No station, no root.

    python3 -I pi/tests/clock_floor/test_install_scripts.py

Builds wake A / wake B with build_floor_wake_scripts.py, then runs them (and the rollback) against a
fake station root: ISS015_TEST_ROOT prefixes every station path, `sudo` and `systemctl` are stubs.
Proves the install order, idempotence, the refusals, and that a rollback restores the OLD logger.
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPRING = HERE.parents[2]
PI = SPRING / "pi"
SH = SPRING / "liveorc_server/station-health"
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"   <-- {detail}"))


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    d = Path(tempfile.mkdtemp(prefix="inst_"))
    b = subprocess.run([sys.executable, "-I", str(SH / "build_floor_wake_scripts.py"), str(d / "build")], capture_output=True, text=True)
    if b.returncode != 0:
        print("build refused (commit the payload files first):", b.stderr[-400:]); sys.exit(2)
    A, B = d / "build/iss015_floor_wake_a.sh", d / "build/iss015_floor_wake_b.sh"
    RB = SH / "iss015_floor_rollback.sh"

    root = d / "root"; stage = d / "stage"
    for sub in ("usr/local/bin", "usr/local/lib/orc-sensors", "etc/systemd/system", "var/lib"):
        (root / sub).mkdir(parents=True)
    old = subprocess.run(["git", "-C", str(SPRING.parent), "show", "eb7c7b0:spring_2026_ID/pi/shared/usr/local/lib/orc-sensors/sensors_logger.py"],
                         capture_output=True, text=True).stdout
    logger = root / "usr/local/lib/orc-sensors/sensors_logger.py"
    logger.write_text(old); logger.chmod(0o644)
    new_logger = PI / "shared/usr/local/lib/orc-sensors/sensors_logger.py"
    bindir = d / "bin"; bindir.mkdir()
    (bindir / "sudo").write_text('#!/bin/bash\n[ "$1" = "-n" ] && shift\nexec "$@"\n')
    (bindir / "systemctl").write_text(
        '#!/bin/bash\ncase "$1" in\n list-jobs) exit 0;;\n daemon-reload) echo reload >> "$T/sysctl.log";;\n'
        ' enable) echo enable >> "$T/sysctl.log"; touch "$T/enabled"; echo "Created symlink";;\n'
        ' disable) echo disable >> "$T/sysctl.log"; rm -f "$T/enabled";;\n'
        ' is-enabled) [ -e "$T/enabled" ] && echo enabled || { echo disabled; exit 1; };;\n is-active) echo inactive; exit 3;;\n *) exit 0;;\nesac\n')
    (bindir / "chronyc").write_text('#!/bin/bash\nprintf "Reference ID    : CB591F0D (x)\\nStratum         : 4\\nLeap status     : Normal\\n"\n')
    for n in ("sudo", "systemctl", "chronyc"): (bindir / n).chmod(0o755)
    env = dict(os.environ, T=str(d), PATH=f"{bindir}:{os.environ['PATH']}", ISS015_STAGE=str(stage), ISS015_TEST_ROOT=str(root),
               ISS015_MAX_UPTIME_S="999999999")

    def run(script, **extra):
        return subprocess.run(["bash", str(script)], env=dict(env, **extra), capture_output=True, text=True, timeout=120)

    # ── wake A ────────────────────────────────────────────────────────
    a = run(A)
    check("A1 wake A stages and verifies, installs nothing",
          "RESULT: staged and verified" in a.stdout and not (root / "usr/local/bin/orc-clock-floor").exists(), a.stdout[-300:])
    check("A2 staged files are byte-identical to the repo",
          sha(stage / "orc-clock-floor") == sha(PI / "sukabumi/usr/local/bin/orc-clock-floor") and sha(stage / "sensors_logger.py") == sha(new_logger))
    check("A3 wake A refuses a wake older than its limit", "REFUSED: wake is" in run(A, ISS015_MAX_UPTIME_S="1").stdout)

    # ── wake B refusals (nothing may change) ──────────────────────────
    r = run(B, ISS015_MAX_UPTIME_S="1")
    check("B1 refuses when the wake is too old; nothing installed", "REFUSED: wake is" in r.stdout and not (root / "usr/local/bin/orc-clock-floor").exists(), r.stdout[-200:])
    shutil.rmtree(stage, ignore_errors=True)                  # B must not need wake A's staging directory (a reboot can wipe /tmp)
    bad = d / "build/b_tampered.sh"; txt = B.read_text()
    i = txt.index("B64_FLOOR='") + len("B64_FLOOR='"); bad.write_text(txt[:i] + ("A" if txt[i] != "A" else "B") + txt[i + 1:])
    r = run(bad)
    check("B2 a corrupted embedded payload is refused before anything is installed", "REFUSED: payload FLOOR" in r.stdout and not (root / "usr/local/bin/orc-clock-floor").exists(), r.stdout[-200:])
    logger.write_text(old + "\n# local edit\n")
    r = run(B)
    check("B3 refuses when the installed logger is neither old nor new", "REFUSED: installed sensors_logger.py" in r.stdout and sha(logger) != sha(new_logger), r.stdout[-200:])
    logger.write_text(old)

    # ── wake B install (the staging directory was removed above: B stages itself) ──
    r = run(B)
    fl = root / "usr/local/bin/orc-clock-floor"
    check("B4 install completes", "RESULT: INSTALLED" in r.stdout, r.stdout[-400:] + r.stderr[-200:])
    check("B5 floor script, unit and logger are the tested bytes",
          sha(fl) == sha(PI / "sukabumi/usr/local/bin/orc-clock-floor") and os.access(fl, os.X_OK)
          and sha(root / "etc/systemd/system/orc-clock-floor.service") == sha(PI / "sukabumi/etc/systemd/system/orc-clock-floor.service")
          and sha(logger) == sha(new_logger))
    bks = sorted((root / "var/lib/orc-clock-floor-backup").glob("sensors_logger.py.*"))
    check("B6 exactly one backup, and it is the OLD logger", len(bks) == 1 and bks[0].read_text() == old, bks)
    log = (d / "sysctl.log").read_text().split()
    check("B7 daemon-reload happens before enable; unit enabled but never started",
          log.index("reload") < log.index("enable") and (d / "enabled").exists() and "start" not in log, log)
    check("B8 floor seeded (chrony stub synced) with a plausible time", (root / "var/lib/orc-clock-floor/floor").exists() and int((root / "var/lib/orc-clock-floor/floor").read_text()) > 1793491200,
          (root / "var/lib/orc-clock-floor").exists())
    check("B9 no stray .new files left behind", not list(root.rglob("*.new")), list(root.rglob("*.new")))

    r = run(B)
    bks = sorted((root / "var/lib/orc-clock-floor-backup").glob("sensors_logger.py.*"))
    check("B10 second run is idempotent: still installed, STILL one backup (the old one)", "RESULT: INSTALLED" in r.stdout and len(bks) == 1 and bks[0].read_text() == old, (len(bks), r.stdout[-200:]))

    # ── rollback ──────────────────────────────────────────────────────
    r = run(RB)
    check("RB1 rollback restores the OLD logger byte for byte", "RESULT: rolled back" in r.stdout and logger.read_text() == old, r.stdout[-300:])
    check("RB2 rollback removes the script and unit and disables the service",
          not fl.exists() and not (root / "etc/systemd/system/orc-clock-floor.service").exists() and not (d / "enabled").exists())
    (root / "var/lib/orc-clock-floor-backup/sensors_logger.py.zzz").write_text("def broken(:\n")
    os.utime(root / "var/lib/orc-clock-floor-backup/sensors_logger.py.zzz", (2000000000, 2000000000))
    r = run(RB)
    check("RB3 rollback refuses a backup that does not compile; logger untouched", "REFUSED: backup does not compile" in r.stdout and logger.read_text() == old, r.stdout[-200:])

    bad = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(bad)}/{len(results)} passed" + (f"; FAILED: {bad}" if bad else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
