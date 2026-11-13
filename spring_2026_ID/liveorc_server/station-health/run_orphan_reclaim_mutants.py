#!/usr/bin/env python3
"""Broken-copy check for the orphaned-plot reclaim script (TODO-119).   python3 -I run_orphan_reclaim_mutants.py

Each mutant removes ONE safety rule from the built script. Three invariants must catch it:
  I1 the dry run changes nothing; I2 with the skips present only the 4 good plots are deleted; I3 the default abort rule deletes nothing.
A mutant that survives means a rule has no test behind it.
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))   # -I drops the script dir from sys.path
import test_orphan_reclaim as T  # noqa: E402

MUTANTS = {
    "no mp4 check": ('elif [ -n "$(find "$d" -name \'*.mp4\' -print -quit 2>/dev/null)" ]; then r="video dir has an mp4"', 'elif false; then r="x"'),
    "no SYNCED check": ('elif ! printf \'%s\\n\' "$synced" | grep -qx "$id"; then r="DB row not SYNCED"', 'elif false; then r="x"'),
    "no size check": ('elif [ "$(stat -c %s "$p")" != "$bytes" ]; then r="size differs"', 'elif false; then r="x"'),
    "no regular-file/symlink check": ('elif [ -L "$p" ] || [ ! -f "$p" ]; then r="not a regular file"', 'elif false; then r="x"'),
    "no age check": ('elif [ $((now - $(stat -c %Y "$p"))) -lt "$MINAGE" ]; then r="modified in the last 24 h"', 'elif false; then r="x"'),
    "dry run deletes": ('if [ "$APPLY" != 1 ]; then echo "DRY RUN:', 'if false; then echo "DRY RUN:'),
    "abort rule removed": ('if [ "$n_skip" -gt "$limit" ]; then echo "ABORT', 'if false; then echo "ABORT'),
}


def scenarios(mutate):
    """Return a list of violated invariants for one (possibly mutated) build."""
    bad = []
    good = ["101|20260703|300", "102|20260703|400", "103|20260704|500", "104|20260801|600"]
    badl = ["201|20260710|100", "202|20260710|100", "203|20260710|100", "204|20260710|100", "205|20260710|100", "206|20260710|100"]
    def prep(lines):
        tmp = Path(tempfile.mkdtemp(prefix="mu_")); V, db, shim = T.setup(tmp); T.build(tmp, lines)
        for n in ("dry", "apply"):
            p = tmp / "out" / f"todo119_orphan_plot_reclaim_{n}.sh"; txt = p.read_text()
            if mutate:
                old, new = mutate
                if txt.count(old) != 1: return None
                p.write_text(txt.replace(old, new))
        return tmp, V, db, shim
    s = prep(good + badl)
    if s is None: return ["pattern not found"]
    tmp, V, db, shim = s; before = T.snap(V)
    T.run(tmp, V, db, shim, "todo119_orphan_plot_reclaim_dry.sh", ISS_ABORT_PCT="100")
    if T.snap(V) != before: bad.append("I1 dry run changed files")
    r = T.run(tmp, V, db, shim, "todo119_orphan_plot_reclaim_apply.sh", ISS_ABORT_PCT="100")
    gone = set(x for x, _ in before) - set(x for x, _ in T.snap(V))
    if len(gone) != 4 or any("/2026071" in g for g in gone): bad.append(f"I2 deleted the wrong set: {sorted(gone)}")
    elif " 0 failed" not in r.stdout: bad.append("I2b an entry that should have been skipped reached the delete loop (reported failed)")
    tmp, V, db, shim = prep(good + badl); before = T.snap(V)
    T.run(tmp, V, db, shim, "todo119_orphan_plot_reclaim_apply.sh")
    if T.snap(V) != before: bad.append("I3 default abort rule did not stop the deletion")
    return bad


def main():
    base = scenarios(None)
    if base: print("baseline violates invariants:", base); return 2
    surv = []
    for name, m in MUTANTS.items():
        v = scenarios(m)
        print(("CAUGHT   " if v else "SURVIVED ") + name + (f"   ({v[0][:70]})" if v else ""))
        if not v: surv.append(name)
    print(f"\n{len(MUTANTS) - len(surv)}/{len(MUTANTS)} broken copies caught" + (f"; SURVIVORS: {surv}" if surv else ""))
    return 1 if surv else 0


if __name__ == "__main__":
    sys.exit(main())
