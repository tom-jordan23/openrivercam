#!/usr/bin/env python3
"""Broken-copy check for test_clock_floor.py (ISS-FIELD-015).

    python3 -I pi/tests/clock_floor/run_mutants.py

Each mutant is a copy of orc-clock-floor or sensors_logger.py with ONE rule deliberately broken.
The test suite must FAIL on every one. A mutant that passes means a rule has no test behind it.
Mutants cover the rules added on 2026-11-13: the watermark cap, --dry-run, the pre-station-file guard in rotation, the early-boot clock guard.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PI = HERE.parents[1]
FLOOR = PI / "sukabumi/usr/local/bin/orc-clock-floor"
LOGGER = PI / "shared/usr/local/lib/orc-sensors/sensors_logger.py"
TEST = HERE / "test_clock_floor.py"

FLOOR_MUTANTS = {
    "watermark cap removed": ('&& [ "$wm" -le $(( floor + MAX_WM_AHEAD )) ]', ''),
    "dry-run restore still sets the clock": ('WOULD set it to $eff (nothing changed)"', 'WOULD set it to $eff (nothing changed)"; $SET_CMD "@$eff" >/dev/null 2>&1'),
    "dry-run restore waits for wp5d": ('[ "$DRY" = 1 ] && MAX_WAIT=0', ':'),
    "dry-run restore writes the state file": ('    [ "$DRY" = 1 ] && return 0\n    mkdir -p "$RUN_DIR"', '    mkdir -p "$RUN_DIR"'),
    "dry-run save writes the floor": ('if [ "$DRY" = 1 ]; then log "WOULD save floor $sys (was $floor); nothing written"; return 0; fi', ':'),
    "unknown flag accepted": ('elif [ -n "${2:-}" ]; then echo "usage: $0 restore|save [--dry-run] | status" >&2; exit 2; fi', 'fi'),
    "dry-run flag sticky": ('if [ "${2:-}" = "--dry-run" ]; then DRY=1;', 'DRY=1; if [ "${2:-}" = "--dry-run" ]; then DRY=1;'),
}
LOGGER_MUTANTS = {
    "rotation never deletes (rotation disabled)": ('            os.remove(path)', '            pass'),
    "rotation deletes pre-station (January) files": ('if file_date < MIN_PLAUSIBLE_DATE:\n            continue', 'if False:\n            continue'),
    "guard removed (never defers)": ('    if clock_untrusted():\n        log(', '    if False:\n        log('),
    "guard ignores whether the floor set the clock": ('    if not _floor_set_clock():\n        return False\n', ''),
    "guard defers forever (no uptime window)": ('    if up is None or up >= CLOCK_DEFER_UNTIL_S:', '    if up is None:'),
    "guard window boundary off by one": ('up >= CLOCK_DEFER_UNTIL_S', 'up > CLOCK_DEFER_UNTIL_S'),
    "guard fails closed on unreadable uptime": ('    if up is None or up >= CLOCK_DEFER_UNTIL_S:', '    if up is not None and up >= CLOCK_DEFER_UNTIL_S:'),
    "guard ignores chrony (always untrusted)": ('    return not _chrony_synced()', '    return True'),
    "local reference counts as synced": ('    if re.search(r"^Reference ID\\s*:\\s*(00000000|7F7F0101)", out, re.M):\n        return False\n', ''),
    "any stratum counts as synced": ('    return bool(m) and 1 <= int(m.group(1)) <= 9', '    return bool(m)'),
}


def run_suite(env_extra):
    env = dict(os.environ, **env_extra)
    r = subprocess.run([sys.executable, "-I", str(TEST)], env=env, capture_output=True, text=True, timeout=300)
    failed = [l for l in r.stdout.splitlines() if l.startswith("FAIL")]
    return r.returncode, failed


def main():
    base_rc, base_fail = run_suite({})
    if base_rc != 0:
        print("baseline suite FAILS; fix that first:", base_fail)
        return 2
    tmp = Path(tempfile.mkdtemp(prefix="mut_"))
    survivors = []
    jobs = [("floor", n, FLOOR, m, "ORC_CF_TEST_SCRIPT") for n, m in FLOOR_MUTANTS.items()] + \
           [("logger", n, LOGGER, m, "ORC_CF_TEST_LOGGER") for n, m in LOGGER_MUTANTS.items()]
    for kind, name, src, (old, new), var in jobs:
        text = src.read_text()
        if text.count(old) != 1:
            print(f"BROKEN MUTANT (pattern found {text.count(old)}x, need 1): {name}")
            survivors.append(name)
            continue
        p = tmp / f"{kind}_{len(list(tmp.iterdir()))}{src.suffix}"
        p.write_text(text.replace(old, new)); p.chmod(0o755)
        rc, failed = run_suite({var: str(p)})
        caught = rc != 0
        print(("CAUGHT   " if caught else "SURVIVED ") + f"{kind}: {name}" + (f"   ({failed[0][5:60]}...)" if caught and failed else ""))
        if not caught:
            survivors.append(name)
    print(f"\n{len(jobs) - len(survivors)}/{len(jobs)} mutants caught" + (f"; SURVIVORS: {survivors}" if survivors else ""))
    return 1 if survivors else 0


if __name__ == "__main__":
    sys.exit(main())
