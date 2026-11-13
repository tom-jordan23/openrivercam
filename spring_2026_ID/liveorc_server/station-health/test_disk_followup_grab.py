#!/usr/bin/env python3
"""Fixture test for todo119_disk_followup_grab.sh (TODO-119). No station.   python3 -I test_disk_followup_grab.py

Fake uploads tree (sparse files, chosen mtimes), fake DB with a settings table, fake orc_api. The expected numbers are worked
out by hand in the comments. Also proves the grab is read-only.
"""
import calendar
import os
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "todo119_disk_followup_grab.sh"
GIB = 1 << 30
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"   <-- {detail}"))


def utc(y, m, d, hh=0, mm=0):
    return calendar.timegm((y, m, d, hh, mm, 0))


def mk(p, size, mtime):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "wb") as f: f.truncate(size)
    os.utime(p, (mtime, mtime))


def snapshot(root):
    return sorted((str(p.relative_to(root)), p.stat().st_size, p.stat().st_mtime_ns) for p in root.rglob("*") if p.is_file())


def main():
    d = Path(tempfile.mkdtemp(prefix="fu_")); V = d / "uploads/videos"
    #  7713: Jan 11, FAILED : mp4 2G (23:00) + plot 1G (23:05)           7714: Jan 12, SYNCED: mp4 2G
    #  3000: Jul 03, FAILED : mp4 1G                                       7792: Nov 13, SYNCED: mp4 1G + plot 1G
    #  7700: Nov 12, no DB row: mp4 1G
    mk(V / "20260111/7713/video.mp4", 2 * GIB, utc(2026, 1, 11, 23, 0)); mk(V / "20260111/7713/output/plot_quiver.jpg", GIB, utc(2026, 1, 11, 23, 5))
    mk(V / "20260112/7714/video.mp4", 2 * GIB, utc(2026, 1, 12, 8, 0))
    mk(V / "20260703/3000/video.mp4", GIB, utc(2026, 7, 3, 12, 0))
    mk(V / "20261113/7792/video.mp4", GIB, utc(2026, 11, 13, 14, 31)); mk(V / "20261113/7792/output/plot_quiver.jpg", GIB, utc(2026, 11, 13, 14, 35))
    mk(V / "20261112/7700/video.mp4", GIB, utc(2026, 11, 12, 9, 0))
    db = d / "orc-os.db"; c = sqlite3.connect(db)
    c.execute("CREATE TABLE video (id INTEGER PRIMARY KEY, sync_status TEXT)")
    c.execute("CREATE TABLE settings (id INTEGER PRIMARY KEY, sync_file INTEGER, sync_image INTEGER, video_file_fmt TEXT)")
    c.execute("INSERT INTO settings VALUES (1, 1, 0, '{%Y%m%d}/{id}/{%Y%m%dT%H%M%S}.mp4')")
    for i, s in ((7713, "FAILED"), (7714, "SYNCED"), (3000, "FAILED"), (7792, "SYNCED")): c.execute("INSERT INTO video VALUES (?,?)", (i, s))
    c.commit(); c.close()
    pkg = d / "orc_api"; (pkg / "routers").mkdir(parents=True); (pkg / "utils").mkdir()
    (pkg / "routers/video.py").write_text('@router.get("/{id}/image/", response_class=FileResponse)\ndef get_image(id):\n    if not os.path.exists(file_path):\n        raise HTTPException(404)\n    return FileResponse(file_path)\n')
    (pkg / "utils/sync_helper.py").write_text("if settings.sync_image:\n    files['image'] = open(video.image, 'rb')\n")
    (d / "dphys").write_text("# comment\nCONF_SWAPSIZE=2048\n")
    before = snapshot(d / "uploads")
    shim = d / "bin"; shim.mkdir()
    (shim / "sqlite3").write_text("#!/usr/bin/env python3\nimport sqlite3, sys\na = sys.argv[1:]\nsep = '|'\nif a and a[0] == '-separator': sep = a[1]; a = a[2:]\n"
                                  "c = sqlite3.connect(a[0], uri=True)\nfor r in c.execute(a[1]): print(sep.join('' if x is None else str(x) for x in r))\n")
    (shim / "sqlite3").chmod(0o755)
    env = dict(os.environ, PATH=f"{shim}:{os.environ['PATH']}", ISS_V=str(V), ISS_DB=str(db), ISS_PKG=str(pkg), ISS_SWAPCONF=str(d / "dphys"),
               ISS_SAMPLE="0", ISS_SKIP_JOURNAL="1", ISS_PURGE_BYTES=str(3 * GIB))
    r = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True, timeout=120)
    out = r.stdout
    if os.environ.get("FU_VERBOSE"): print(out); print(r.stderr)

    check("F1 runs to END with nothing on stderr", r.returncode == 0 and "=== END ===" in out and r.stderr.strip() == "", (r.returncode, r.stderr[-300:]))
    check("F2 read-only: tree unchanged", snapshot(d / "uploads") == before)
    check("F3 settings row printed (sync_image=0 shows the plot is NOT uploaded)", "sync_file=1  sync_image=0" in out, [l for l in out.splitlines() if "sync_" in l][:3])
    check("F4 the /image/ endpoint code and the sync_image reader are shown", 'raise HTTPException(404)' in out and "if settings.sync_image" in out)
    for label, cnt, gib in (("mp4 / FAILED", 2, 3), ("mp4 / SYNCED", 2, 3), ("mp4 / NO_DB_ROW", 1, 1), ("mp4 / TOTAL", 5, 7)):
        line = next((l for l in out.splitlines() if l.strip().startswith(label)), "")
        check(f"F5 {label}: {cnt} clips, {gib}.00 GiB", f"{cnt} clips" in line and f"{gib}.00 GiB" in line, line)
    for label, cnt, gib in (("Jan dirs / FAILED", 1, 3), ("Jan dirs / SYNCED", 1, 2)):
        line = next((l for l in out.splitlines() if l.strip().startswith(label)), "")
        check(f"F6 {label}: {cnt} video, {gib}.000 GiB", f"{cnt} videos" in line and f"{gib}.000 GiB" in line, line)
    pv = [l for l in out.splitlines() if l.startswith("    2026-")]
    check("F7 purge preview lists oldest first, with each video's sync status",
          len(pv) >= 3 and pv[0].split()[0:2] == ["2026-01-11", "23:00:00"] and "FAILED" in pv[0] and "20260111/7713/video.mp4" in pv[0] and pv[1].split()[1] == "23:05:00", pv[:3])
    sm = next((l for l in out.splitlines() if "files," in l and "videos by status" in l), "")
    check("F8 purge of 3 GiB removes 2 files = 3.000 GiB in 1 video, FAILED=1", "2 files, 3.000 GiB, in 1 videos by status: FAILED=1" in sm, sm)
    check("F9 swap config line printed", "CONF_SWAPSIZE=2048" in out)
    check("F10 no timeout message", "TIMED OUT" not in out)
    bad = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(bad)}/{len(results)} passed" + (f"; FAILED: {bad}" if bad else "")); sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
