#!/usr/bin/env python3
"""Build the orphaned-plot reclaim script from an allow-list (TODO-119).

    python3 -I build_orphan_reclaim.py ALLOWLIST.txt OUTDIR

Writes OUTDIR/todo119_orphan_plot_reclaim_dry.sh (APPLY=0) and OUTDIR/todo119_orphan_plot_reclaim_apply.sh (APPLY=1). The allow-list
is produced by match_orphans_to_server.py (`id|date|bytes` per line). Refuses on a malformed or duplicated entry, or if the template
has uncommitted changes. Building touches nothing on the station.
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TMPL = HERE / "todo119_orphan_plot_reclaim.sh.in"


def die(m):
    print("REFUSED: " + m, file=sys.stderr); sys.exit(2)


def main():
    if len(sys.argv) != 3: die("usage: build_orphan_reclaim.py ALLOWLIST.txt OUTDIR")
    lines = [l.strip() for l in Path(sys.argv[1]).read_text().splitlines() if l.strip()]
    if not lines: die("empty allow-list")
    seen, total = set(), 0
    for l in lines:
        m = re.fullmatch(r"(\d+)\|(\d{8})\|(\d+)", l)
        if not m: die(f"malformed allow-list line: {l!r}")
        if m.group(1) in seen: die(f"duplicate id {m.group(1)}")
        seen.add(m.group(1)); total += int(m.group(3))
    st = subprocess.run(["git", "-C", str(HERE), "status", "--porcelain", "--", str(TMPL)], capture_output=True, text=True)
    if st.stdout.strip(): die("the template has uncommitted changes; commit first")
    commit = subprocess.run(["git", "-C", str(HERE), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    text = TMPL.read_text()
    if text.count("@@PAYLOAD@@") != 1 or text.count("@@ALLOWLIST@@") != 1: die("template placeholders wrong")
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    for mode, name in ((0, "dry"), (1, "apply")):
        payload = f"BUILD_COMMIT='{commit}'\nEXPECT_N={len(lines)}\nEXPECT_BYTES={total}\nAPPLY={mode}"
        p = out / f"todo119_orphan_plot_reclaim_{name}.sh"
        p.write_text(text.replace("@@PAYLOAD@@", payload).replace("@@ALLOWLIST@@", "\n".join(sorted(lines, key=lambda s: int(s.split('|')[0])))))
        print(f"wrote {p}  ({len(lines)} entries, {total} bytes = {total / 2**30:.3f} GiB, build {commit})")


if __name__ == "__main__":
    main()
