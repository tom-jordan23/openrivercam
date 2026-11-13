#!/usr/bin/env python3
"""Fixture test for todo119_plot_orphan_grab.sh (TODO-119). No station.

    python3 -I test_plot_orphan_grab.py

Builds a fake uploads/videos tree (sparse files with known apparent sizes), a fake ORC-OS DB and a fake orc_api
package, runs the grab against them (a `sqlite3` shim stands in for the CLI), and checks the numbers it prints against
answers worked out by hand. Also proves the grab is read-only: the tree's file list and sizes are identical afterwards.
"""
import os
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "todo119_plot_orphan_grab.sh"
GIB = 1 << 30
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"   <-- {detail}"))


def sparse(p, size):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "wb") as f:
        f.truncate(size)


def snapshot(root):
    return sorted((str(p.relative_to(root)), p.stat().st_size, p.stat().st_mtime_ns) for p in root.rglob("*") if p.is_file())


def main():
    d = Path(tempfile.mkdtemp(prefix="orph_"))
    V = d / "uploads/videos"
    #            dir            mp4  plot  other-jpg  nc    DB sync_status (None = no DB row)
    cases = [("20261001/100", 1, 2, 0, 1, "SYNCED"),     # mp4 present, plot present
             ("20260901/50",  0, 3, 0, 1, "SYNCED"),     # orphan, synced
             ("20260902/51",  0, 1, 0, 0, "FAILED"),     # orphan, never synced
             ("20260111/7",   0, 2, 0, 0, None),         # orphan, January dir, no DB row
             ("20260903/52",  0, 0, 1, 0, "SYNCED"),     # no mp4, no plot, other jpg only
             ("20261002/101", 1, 1, 0, 0, "LOCAL")]      # mp4 present, plot present
    for rel, mp4, plot, jpg, nc, _ in cases:
        if mp4: sparse(V / rel / "video.mp4", mp4 * GIB)
        if plot: sparse(V / rel / "output/plot_quiver.jpg", plot * GIB)
        if jpg: sparse(V / rel / "output/frame.jpg", jpg * GIB)
        if nc: sparse(V / rel / "output/transect_1.nc", nc * GIB)
    (V / "readme.txt").write_text("loose")

    db = d / "orc-os.db"
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE video (id INTEGER PRIMARY KEY, timestamp TEXT, status TEXT, file TEXT, image TEXT, thumbnail TEXT, sync_status TEXT)")
    c.execute("CREATE TABLE disk_management (id INTEGER PRIMARY KEY, min_free_space REAL)")
    c.execute("INSERT INTO disk_management VALUES (1, 5.0)")
    for rel, mp4, *_rest, ss in cases:
        if ss is not None:
            vid = int(rel.split("/")[1])
            c.execute("INSERT INTO video VALUES (?,?,?,?,?,?,?)", (vid, "2026-10-01", "DONE", f"videos/{rel}/video.mp4", f"videos/{rel}/img.jpg", f"videos/{rel}/t.jpg", ss))
    c.commit(); c.close()

    pkg = d / "orc_api"; (pkg / "utils").mkdir(parents=True)
    (pkg / "utils/disk_management.py").write_text("def get_free_space(home):\n    return shutil.disk_usage(home).free / 1024**3\n\ndef delete_file(p, logger=None):\n    os.remove(p)\n")
    (pkg / "utils/queue.py").write_text("files = {'file': open(video.file, 'rb')}\n")
    shim = d / "bin"; shim.mkdir()
    (shim / "sqlite3").write_text(
        "#!/usr/bin/env python3\nimport sqlite3, sys\na = sys.argv[1:]\nsep = '|'\n"
        "if a and a[0] == '-separator': sep = a[1]; a = a[2:]\n"
        "uri, sql = a[0], a[1]\nc = sqlite3.connect(uri, uri=True)\n"
        "for r in c.execute(sql): print(sep.join('' if x is None else str(x) for x in r))\n")
    (shim / "sqlite3").chmod(0o755)

    before = snapshot(d / "uploads")
    env = dict(os.environ, PATH=f"{shim}:{os.environ['PATH']}", ISS_V=str(V), ISS_DB=str(db), ISS_PKG=str(pkg),
               ISS_WEB=str(d / "www"), ISS_SKIP_JOURNAL="1")
    r = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True, timeout=120)
    out = r.stdout
    print(out[-3500:] if os.environ.get("ORPH_VERBOSE") else "")

    check("O1 the script runs to its END marker", r.returncode == 0 and "=== END ===" in out, (r.returncode, r.stderr[-300:], out[-300:]))
    check("O2 the grab changed nothing (file list, sizes and mtimes identical)", snapshot(d / "uploads") == before)
    check("O3 6 video dirs: 2 with mp4, 4 without; 1 loose file",
          "video dirs: 6  (with mp4: 2, without mp4: 4)" in out and "files not under a video dir: 1" in out, [l for l in out.splitlines() if "video dirs" in l])
    check("O4 orphaned plots: 3 files, 6.00 GiB", "ORPHANED (no mp4):     3 files    6.00 GiB" in out, [l for l in out.splitlines() if "ORPHANED" in l])
    check("O5 plots with an mp4: 2 files, 3.00 GiB", "WITH mp4 present :     2 files    3.00 GiB" in out, [l for l in out.splitlines() if "WITH mp4" in l])
    check("O6 bytes in dirs without an mp4 = 3+1+1 (nc)+... = 8 GiB (plots 6 + nc 1 + other jpg 1)", "dirs WITHOUT an mp4 (plots, nc, hash, yml...): 8.00 GiB" in out, [l for l in out.splitlines() if "WITHOUT" in l])
    check("O7 orphans by month: 202609 -> 2 files 4 GiB, 202601 -> 1 file 2 GiB",
          "202609     2   4.000" in out and "202601     1   2.000" in out, [l for l in out.splitlines() if l.strip().startswith("2026")])
    for label, cnt, gib in (("NOMP4 / SYNCED", 1, 3), ("NOMP4 / FAILED", 1, 1), ("NOMP4 / NO_DB_ROW", 1, 2), ("mp4 / SYNCED", 1, 2), ("mp4 / LOCAL", 1, 1)):
        line = next((l for l in out.splitlines() if l.strip().startswith(label)), "")
        check(f"O8 join row '{label}': {cnt} plot, {gib}.000 GiB", f"{cnt} plots" in line and f"{gib}.000 GiB" in line, line)
    check("O9 the disk manager's free-space function and configured minimum are printed",
          "disk_usage(home).free / 1024**3" in out and "configured min_free_space: 5.0" in out)
    check("O10 DB column probe lists the video file/image/thumbnail columns", all(f"video|{col}" in out for col in ("file", "image", "thumbnail")))

    check("O12 a grep that finds nothing is not reported as a timeout", "(stopped:" not in out and "TIMED OUT" not in out, [l for l in out.splitlines() if "stopped" in l or "TIMED" in l])
    check("O13 the layout samples come from date directories, not the loose readme.txt", "readme.txt" not in out.split("layout samples")[1].split("reading every file")[0], out.split("layout samples")[1][:200])

    # an unreadable DB must refuse, not guess
    r2 = subprocess.run(["bash", str(SCRIPT)], env=dict(env, ISS_DB=str(d / "missing.db")), capture_output=True, text=True, timeout=60)
    check("O11 unreadable DB: refuses and reads no files", "REFUSED" in r2.stdout and "=== END ===" not in r2.stdout, r2.stdout[-200:])

    bad = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(bad)}/{len(results)} passed" + (f"; FAILED: {bad}" if bad else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
