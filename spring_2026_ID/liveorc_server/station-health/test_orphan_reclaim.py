#!/usr/bin/env python3
"""Fixture test for the orphaned-plot reclaim script (TODO-119). No station.   python3 -I test_orphan_reclaim.py

Builds the script from a small allow-list and runs it against a fake videos tree and DB. Covers every skip reason, the
all-or-nothing abort rule, dry-run vs apply, and that nothing outside the allow-list (mp4s, other files, directories, other plots)
is ever touched.
"""
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"   <-- {detail}"))


def mk(p, size, age_s=10 * 86400):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"x" * size)
    t = time.time() - age_s; os.utime(p, (t, t))


def snap(root):
    return sorted((str(p.relative_to(root)), p.lstat().st_size) for p in root.rglob("*") if p.is_symlink() or p.is_file())


def setup(tmp):
    V = tmp / "videos"
    good = [(101, "20260703", 300), (102, "20260703", 400), (103, "20260704", 500), (104, "20260801", 600)]
    for i, d, n in good: mk(V / d / str(i) / "output/plot_quiver.jpg", n); mk(V / d / str(i) / "output/other.nc", 50)
    # failure cases, each also on the allow-list
    mk(V / "20260710/201/output/plot_quiver.jpg", 100); mk(V / "20260710/201/video.mp4", 999)             # has an mp4
    mk(V / "20260710/202/output/plot_quiver.jpg", 111)                                                    # size differs (list says 100)
    mk(V / "20260710/203/output/plot_quiver.jpg", 100)                                                    # DB row FAILED
    mk(V / "20260710/205/output/plot_quiver.jpg", 100, age_s=3600)                                        # modified an hour ago
    mk(V / "20260710/209/output/real.bin", 100)                                                           # a file of exactly the listed size ...
    (V / "20260710/206/output").mkdir(parents=True); (V / "20260710/206/output/plot_quiver.jpg").symlink_to(V / "20260710/209/output/real.bin")   # ... behind a symlink
    _t = time.time() - 10 * 86400; os.utime(V / "20260710/206/output/plot_quiver.jpg", (_t, _t), follow_symlinks=False)   # old link, so only the symlink rule stops it
    # 204: on the list but already gone
    mk(V / "20260710/300/output/plot_quiver.jpg", 77); mk(V / "20260710/300/note.mp4", 5)                 # NOT on the list; must survive
    db = tmp / "orc.db"; c = sqlite3.connect(db); c.execute("CREATE TABLE video (id INTEGER PRIMARY KEY, sync_status TEXT)")
    for i in (101, 102, 103, 104, 201, 202, 204, 205, 206): c.execute("INSERT INTO video VALUES (?,'SYNCED')", (i,))
    c.execute("INSERT INTO video VALUES (203,'FAILED')"); c.commit(); c.close()
    shim = tmp / "bin"; shim.mkdir()
    (shim / "sqlite3").write_text("#!/usr/bin/env python3\nimport sqlite3, sys\na = sys.argv[1:]\nsep = '|'\nif a and a[0] == '-separator': sep = a[1]; a = a[2:]\n"
                                  "c = sqlite3.connect(a[0], uri=True)\nfor r in c.execute(a[1]): print(sep.join('' if x is None else str(x) for x in r))\n")
    (shim / "sqlite3").chmod(0o755)
    return V, db, shim


def build(tmp, lines):
    # entry 206 is a symlink: stat() without -L reports the link's OWN size, so list that size; then only the "not a regular file" rule can stop it
    link = tmp / "videos/20260710/206/output/plot_quiver.jpg"
    if link.is_symlink(): lines = [l.replace("206|20260710|100", f"206|20260710|{os.lstat(link).st_size}") for l in lines]
    al = tmp / "allow.txt"; al.write_text("\n".join(lines) + "\n")
    r = subprocess.run([sys.executable, "-I", str(HERE / "build_orphan_reclaim.py"), str(al), str(tmp / "out")], capture_output=True, text=True)
    return r


def run(tmp, V, db, shim, name, **env):
    e = dict(os.environ, PATH=f"{shim}:{os.environ['PATH']}", ISS_V=str(V), ISS_DB=str(db), ISS_MANIFEST_DIR=str(tmp), ISS_MAX_UPTIME_S="999999999", **env)
    return subprocess.run(["bash", str(tmp / "out" / name)], env=e, capture_output=True, text=True, timeout=120)


def main():
    good = ["101|20260703|300", "102|20260703|400", "103|20260704|500", "104|20260801|600"]
    bad = ["201|20260710|100", "202|20260710|100", "203|20260710|100", "204|20260710|100", "205|20260710|100", "206|20260710|100"]

    # the builder refuses bad input
    t0 = Path(tempfile.mkdtemp(prefix="rc0_"))
    check("R1 builder refuses a malformed line", build(t0, ["1|2026|5"]).returncode == 2)
    check("R2 builder refuses a duplicate id", build(t0, ["1|20260101|5", "1|20260102|6"]).returncode == 2)
    check("R3 builder refuses an empty list", build(t0, []).returncode == 2)

    # 1. all-good list: dry run deletes nothing, apply deletes exactly the list
    tmp = Path(tempfile.mkdtemp(prefix="rc1_")); V, db, shim = setup(tmp)
    b = build(tmp, good); check("R4 builder accepts a good list (template is committed)", b.returncode == 0, b.stderr)
    before = snap(V)
    r = run(tmp, V, db, shim, "todo119_orphan_plot_reclaim_dry.sh")
    check("R5 dry run: preflight ok for all 4, deletes nothing", "preflight: 4 checked, 4 ok" in r.stdout and "DRY RUN" in r.stdout and snap(V) == before, r.stdout[-300:])
    r = run(tmp, V, db, shim, "todo119_orphan_plot_reclaim_apply.sh")
    after = snap(V); gone = sorted(set(x for x, _ in before) - set(x for x, _ in after))
    check("R6 apply deletes exactly the 4 listed plots and nothing else",
          gone == sorted(f"{d}/{i}/output/plot_quiver.jpg" for i, d in ((101, "20260703"), (102, "20260703"), (103, "20260704"), (104, "20260801"))), gone)
    check("R7 directories, other files, mp4s and unlisted plots survive",
          (V / "20260703/101/output/other.nc").exists() and (V / "20260703/101/output").is_dir() and (V / "20260710/300/output/plot_quiver.jpg").exists() and (V / "20260710/300/note.mp4").exists())
    check("R8 reports the deletion and a manifest", "deleted 4 files (1800 bytes" in r.stdout and any((tmp).glob("orphan-plot-reclaim-*.manifest")), r.stdout[-400:])
    man = next(tmp.glob("orphan-plot-reclaim-*.manifest"), None)
    check("R9 manifest lists each deletion", man is not None and man.read_text().count("|deleted") == 4, man and man.read_text())

    # 2. every skip reason; override the abort threshold so the run proceeds past the skips
    tmp = Path(tempfile.mkdtemp(prefix="rc2_")); V, db, shim = setup(tmp)
    build(tmp, good + bad); before = snap(V)
    r = run(tmp, V, db, shim, "todo119_orphan_plot_reclaim_apply.sh", ISS_ABORT_PCT="100")
    for why in ("video dir has an mp4", "size differs", "DB row not SYNCED", "already gone", "modified in the last 24 h", "not a regular file"):
        check(f"R10 skips: {why}", f"skipped for '{why}': 1" in r.stdout, r.stdout[-600:])
    after = snap(V); gone = set(x for x, _ in before) - set(x for x, _ in after)
    check("R11 with the skips, still deletes only the 4 good plots", len(gone) == 4 and all("/output/plot_quiver.jpg" in g for g in gone) and not any("/2026071" in g for g in gone), gone)
    check("R12 the symlink entry was skipped, not followed: link and target both still exist, and nothing 'failed'",
          os.path.islink(V / "20260710/206/output/plot_quiver.jpg") and (V / "20260710/209/output/real.bin").exists() and " 0 failed" in r.stdout, r.stdout[-300:])

    # 3. the default abort rule: 6 of 10 entries fail -> nothing is deleted
    tmp = Path(tempfile.mkdtemp(prefix="rc3_")); V, db, shim = setup(tmp)
    build(tmp, good + bad); before = snap(V)
    r = run(tmp, V, db, shim, "todo119_orphan_plot_reclaim_apply.sh")
    check("R13 default abort threshold: too many skips -> ABORT and NOTHING deleted", "ABORT" in r.stdout and snap(V) == before, r.stdout[-300:])

    # 4. refusals
    tmp = Path(tempfile.mkdtemp(prefix="rc4_")); V, db, shim = setup(tmp); build(tmp, good); before = snap(V)
    r = subprocess.run(["bash", str(tmp / "out/todo119_orphan_plot_reclaim_apply.sh")], env=dict(os.environ, PATH=f"{shim}:{os.environ['PATH']}", ISS_V=str(V), ISS_DB=str(db), ISS_MANIFEST_DIR=str(tmp), ISS_MAX_UPTIME_S="1"), capture_output=True, text=True)
    check("R14 refuses an old wake and deletes nothing", "REFUSED: wake is" in r.stdout and snap(V) == before, r.stdout[-200:])
    r = run(tmp, V, tmp / "missing.db", shim, "todo119_orphan_plot_reclaim_apply.sh")
    check("R15 refuses an unreadable DB and deletes nothing", "REFUSED" in r.stdout and snap(V) == before, r.stdout[-200:])
    r = run(tmp, V, db, shim, "todo119_orphan_plot_reclaim_apply.sh", ISS_MIN_AGE_S="99999999")
    check("R16 a plot newer than the age floor is never deleted", "ABORT" in r.stdout and snap(V) == before, r.stdout[-300:])
    r = run(tmp, V, db, shim, "todo119_orphan_plot_reclaim_apply.sh", ISS_BUDGET_S="0")
    check("R17 a spent time budget stops cleanly with nothing deleted past it", "time budget reached" in r.stdout and snap(V) == before, r.stdout[-300:])

    bad_ = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(bad_)}/{len(results)} passed" + (f"; FAILED: {bad_}" if bad_ else "")); sys.exit(1 if bad_ else 0)


if __name__ == "__main__":
    main()
