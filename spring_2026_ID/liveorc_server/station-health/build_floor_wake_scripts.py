#!/usr/bin/env python3
"""Build the clock-floor wake scripts for Sukabumi (ISS-FIELD-015).

    python3 -I build_floor_wake_scripts.py OUTDIR

Writes OUTDIR/iss015_floor_wake_a.sh (read-only checks + stage) and iss015_floor_wake_b.sh
(install), each with the exact tested files embedded (base64) and their sha256 sums. Run the
result through todo119_wake_runner.py, one script per wake. NOTHING here touches the station;
running the output does, and every station step needs Tom's explicit approval first.

Refuses to build unless: the three payload files have no uncommitted changes, the clock-floor
test suite passes, and the mutant check catches every broken copy. What is deployed is what was
tested and what is in git.

Plan: ISS-FIELD-015_FLOOR_DEPLOY_PLAN_2026-11-12.md. Never deploy via pi/deploy.sh (it writes
the Pi clock into the Witty Pi RTC unconditionally).
"""
import base64
import hashlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPRING = HERE.parents[1]                      # .../spring_2026_ID
REPO = SPRING.parent
PI = SPRING / "pi"
FILES = {                                     # name -> (repo file, station path)
    "FLOOR": (PI / "sukabumi/usr/local/bin/orc-clock-floor", "/usr/local/bin/orc-clock-floor"),
    "UNIT": (PI / "sukabumi/etc/systemd/system/orc-clock-floor.service", "/etc/systemd/system/orc-clock-floor.service"),
    "LOGGER": (PI / "shared/usr/local/lib/orc-sensors/sensors_logger.py", "/usr/local/lib/orc-sensors/sensors_logger.py"),
}
STATION_CHECKOUT = "eb7c7b0"                  # the station's git checkout; installed overlay files equal it (11-12)
DEPLOYED_LOGGER_COMMITS = ["eb7c7b0", "62608e4"]   # sensors_logger.py versions that have run on the station (original; wake-B build of 11-13)


def sh(*a, **k):
    return subprocess.run(a, capture_output=True, text=True, **k)


def die(msg):
    print("REFUSED: " + msg, file=sys.stderr)
    sys.exit(2)


def main():
    if len(sys.argv) != 2:
        die("usage: build_floor_wake_scripts.py OUTDIR")
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)

    for name, (p, _) in FILES.items():
        r = sh("git", "-C", str(REPO), "status", "--porcelain", "--", str(p))
        if r.stdout.strip():
            die(f"{p.name} has uncommitted changes; commit first so the deployed file is the committed file")
    t = sh(sys.executable, "-I", str(PI / "tests/clock_floor/test_clock_floor.py"))
    if t.returncode != 0:
        die("clock-floor tests fail:\n" + "\n".join(l for l in t.stdout.splitlines() if l.startswith("FAIL")))
    m = sh(sys.executable, "-I", str(PI / "tests/clock_floor/run_mutants.py"))
    if m.returncode != 0:
        die("mutant check failed:\n" + m.stdout[-600:])

    old = sh("git", "-C", str(REPO), "show", f"{STATION_CHECKOUT}:spring_2026_ID/pi/shared/usr/local/lib/orc-sensors/sensors_logger.py")
    if old.returncode != 0:
        die(f"cannot read sensors_logger.py at {STATION_CHECKOUT}")
    commit = sh("git", "-C", str(REPO), "rev-parse", "--short", "HEAD").stdout.strip()

    deployed = []
    for c in DEPLOYED_LOGGER_COMMITS:
        g = sh("git", "-C", str(REPO), "show", f"{c}:spring_2026_ID/pi/shared/usr/local/lib/orc-sensors/sensors_logger.py")
        if g.returncode != 0:
            die(f"cannot read sensors_logger.py at {c}")
        deployed.append(hashlib.sha256(g.stdout.encode()).hexdigest())

    def make_payload(names):
        lines = [f"BUILD_COMMIT='{commit}'", f"EXPECT_OLD_LOGGER_SHA='{hashlib.sha256(old.stdout.encode()).hexdigest()}'",
                 f"EXPECT_DEPLOYED_LOGGER_SHAS='{' '.join(deployed)}'"]
        for name in names:
            p, dest = FILES[name]
            data = p.read_bytes()
            lines.append(f"EXPECT_{name}_SHA='{hashlib.sha256(data).hexdigest()}'")
            lines.append(f"DEST_{name}='{dest}'")
            lines.append(f"B64_{name}='{base64.b64encode(data).decode()}'")
        return "\n".join(lines)

    for tmpl, dest, names in (("iss015_floor_wake_a.sh.in", "iss015_floor_wake_a.sh", list(FILES)),
                              ("iss015_floor_wake_b.sh.in", "iss015_floor_wake_b.sh", list(FILES)),
                              ("iss015_logger_update_wake.sh.in", "iss015_logger_update_wake.sh", ["LOGGER"])):
        payload = make_payload(names)
        text = (HERE / tmpl).read_text()
        if text.count("@@PAYLOAD@@") != 1:
            die(f"{tmpl} must contain @@PAYLOAD@@ exactly once")
        (out / dest).write_text(text.replace("@@PAYLOAD@@", payload))
        (out / dest).chmod(0o644)
        print(f"wrote {out / dest}  ({(out / dest).stat().st_size} bytes, build {commit})")
    print("tests pass; mutants caught; payload files are committed.")


if __name__ == "__main__":
    main()
