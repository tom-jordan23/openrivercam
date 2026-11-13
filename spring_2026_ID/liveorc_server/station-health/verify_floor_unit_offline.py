#!/usr/bin/env python3
"""Check the clock-floor unit against the station's real neighbouring units for ordering cycles (ISS-FIELD-015). Workstation only.

    python3 -I verify_floor_unit_offline.py DUMP.txt [--floor-unit PATH]

DUMP is a capture of iss015_units_dump_grab.sh. Every `systemctl cat` block is split back into unit files and drop-ins in a temp tree; the
tree plus our orc-clock-floor.service is then given to `systemd-analyze verify` (which parses units and reports ordering cycles; it runs
nothing). Warnings about missing executables or unknown option names from the OTHER distribution's systemd are filtered and counted;
anything mentioning a cycle, or an error on our unit, is printed and makes the exit status non-zero.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
UNIT = HERE.parents[1] / "pi/sukabumi/etc/systemd/system/orc-clock-floor.service"


def split_dump(text, root):
    cur_unit, cur_file, n = None, None, 0
    for line in text.splitlines():
        m = re.match(r"@@@ UNIT (\S+)", line)
        if m: cur_unit, cur_file = m.group(1), None; continue
        if line.startswith("@@@"): cur_unit = None; cur_file = None; continue
        if cur_unit is None: continue
        h = re.match(r"# (/\S+\.(?:service|timer|conf|target|socket))$", line)
        if h:
            src = Path(h.group(1))
            dest = root / (src.name if src.suffix != ".conf" else f"{src.parent.name}/{src.name}")
            dest.parent.mkdir(parents=True, exist_ok=True); cur_file = dest.open("w"); n += 1; continue
        if cur_file: cur_file.write(line + "\n")
    return n


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("dump"); ap.add_argument("--floor-unit", default=str(UNIT)); a = ap.parse_args()
    text = Path(a.dump).read_text(errors="replace")
    root = Path(tempfile.mkdtemp(prefix="unitv_"))
    n = split_dump(text, root)
    present = sorted(p.name for p in root.iterdir() if p.is_file())
    print(f"units reconstructed from the dump: {n} files: {', '.join(present)}")
    if not present: sys.exit("no units found in the dump")
    (root / "orc-clock-floor.service").write_text(Path(a.floor_unit).read_text())
    env = dict(os.environ, SYSTEMD_UNIT_PATH=f"{root}:")
    r = subprocess.run(["systemd-analyze", "verify", "--no-pager", str(root / "orc-clock-floor.service")] +
                       [str(root / p) for p in present if p.endswith((".service", ".timer"))], env=env, capture_output=True, text=True)
    lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    noise = re.compile(r"is not executable|not found|Unknown (key|section)|CPUAccounting|MemoryAccounting|BlockIOAccounting|Support for option|Failed to open|No such file", re.I)
    kept = [l for l in lines if not noise.search(l)]
    print(f"systemd-analyze output: {len(lines)} lines, {len(lines) - len(kept)} filtered as missing-executable / foreign-systemd noise")
    cyc = [l for l in lines if re.search(r"cycle|ordering", l, re.I)]
    floor_err = [l for l in kept if "orc-clock-floor" in l]
    for l in kept[:25]: print("  " + l)
    if cyc or floor_err:
        print("\nRESULT: PROBLEM: " + ("ordering cycle reported" if cyc else "error on our unit")); sys.exit(1)
    print("\nRESULT: no ordering cycle and no error on orc-clock-floor.service against these neighbours")
    print("(verify parses units; it does not boot them. Real boot order is still confirmed on the station at the first wake after install.)")


if __name__ == "__main__":
    main()
