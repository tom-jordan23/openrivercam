#!/usr/bin/env python3
"""Fixture test for todo119_swap_orphan_verify_grab.sh and match_orphans_to_server.py (TODO-119). No station.

    python3 -I test_swap_orphan_verify.py
"""
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GRAB, MATCH = HERE / "todo119_swap_orphan_verify_grab.sh", HERE / "match_orphans_to_server.py"
GIB = 1 << 30
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"   <-- {detail}"))


def sparse(p, size):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "wb") as f: f.truncate(size)


def snap(root):
    return sorted((str(p.relative_to(root)), p.stat().st_size, p.stat().st_mtime_ns) for p in root.rglob("*") if p.is_file())


def main():
    d = Path(tempfile.mkdtemp(prefix="vf_")); V = d / "uploads/videos"
    #  id  date      mp4  plot  status   station ts
    cases = [(10, "20260703", 0, 3, "SYNCED", "2026-07-03 01:00:00.000000"),   # orphan, on server with image   -> SAFE
             (11, "20260703", 0, 1, "SYNCED", "2026-07-03 01:30:00.000000"),   # orphan, on server WITHOUT image -> SERVER_NO_IMAGE
             (12, "20260704", 0, 2, "SYNCED", "2026-07-04 02:00:00.000000"),   # orphan, no server record, older than listing end -> NO_SERVER_RECORD
             (13, "20260705", 0, 1, "FAILED", "2026-07-05 03:00:00.000000"),   # orphan, never synced -> NOT_SYNCED
             (14, "20261110", 0, 1, "SYNCED", "2026-11-10 04:00:00.000000"),   # orphan newer than the listing -> NEWER_THAN_LISTING
             (15, "20260706", 1, 2, "SYNCED", "2026-07-06 05:00:00.000000")]   # has an mp4: not an orphan
    for i, dt, mp4, plot, st, ts in cases:
        if mp4: sparse(V / dt / str(i) / "video.mp4", GIB)
        sparse(V / dt / str(i) / "output/plot_quiver.jpg", plot * GIB)
    db = d / "orc-os.db"; c = sqlite3.connect(db)
    c.execute("CREATE TABLE video (id INTEGER PRIMARY KEY, timestamp TEXT, sync_status TEXT)")
    for i, dt, mp4, plot, st, ts in cases: c.execute("INSERT INTO video VALUES (?,?,?)", (i, ts, st))
    c.commit(); c.close()
    shim = d / "bin"; shim.mkdir()
    (shim / "sqlite3").write_text("#!/usr/bin/env python3\nimport sqlite3, sys\na = sys.argv[1:]\nsep = '|'\nif a and a[0] == '-separator': sep = a[1]; a = a[2:]\n"
                                  "c = sqlite3.connect(a[0], uri=True)\nfor r in c.execute(a[1]): print(sep.join('' if x is None else str(x) for x in r))\n")
    (shim / "sqlite3").chmod(0o755)
    swap = d / "swapfile"; sparse(swap, 2 * GIB)
    before = snap(d / "uploads"); swap_before = (swap.stat().st_size, swap.stat().st_mtime_ns)
    env = dict(os.environ, PATH=f"{shim}:{os.environ['PATH']}", ISS_V=str(V), ISS_DB=str(db), ISS_SWAP=str(swap))
    r = subprocess.run(["bash", str(GRAB)], env=env, capture_output=True, text=True, timeout=180)
    out = r.stdout; (d / "grab.txt").write_text(out)
    orph = sorted(l for l in out.splitlines() if l.startswith("ORPHAN|"))
    check("V1 runs to END", r.returncode == 0 and "=== END ===" in out, (r.returncode, r.stderr[-300:]))
    check("V2 read-only: video tree and the swap file unchanged", snap(d / "uploads") == before and (swap.stat().st_size, swap.stat().st_mtime_ns) == swap_before)
    check("V3 exactly the 5 orphans are listed (not id 15, which has an mp4)", [l.split("|")[1] for l in orph] == ["10", "11", "12", "13", "14"], orph)
    check("V4 orphan line carries date, bytes, status and the DB timestamp",
          "ORPHAN|10|20260703|3221225472|SYNCED|2026-07-03 01:00:00.000000" in orph, orph[:1])
    check("V5 part A prints the swap file's allocation and the kernel swap list", "allocated bytes (du)" in out and "/proc/swaps" not in out.split("A2.")[0] and "=== A2." in out)
    check("V6 part A names units/configs it searched", "swap/zram unit files" in out and "files that mention /var/swap" in out)

    man = [{"id": 900, "timestamp": "2026-07-03T01:00:00Z", "image": "https://x/media/videos/4/20260703/a.jpg"},
           {"id": 901, "timestamp": "2026-07-03T01:30:00Z", "image": None},
           {"id": 902, "timestamp": "2026-09-16T00:00:00Z", "image": "https://x/m.jpg"}]
    (d / "man.json").write_text(json.dumps(man))
    al = d / "allow.txt"
    m = subprocess.run([sys.executable, "-I", str(MATCH), str(d / "grab.txt"), str(d / "man.json"), "--allowlist", str(al)], capture_output=True, text=True)
    mo = m.stdout
    def row(label): return next((l for l in mo.splitlines() if l.strip().startswith(label)), "")
    check("M1 SAFE = the one synced orphan whose server record has an image", " 1 " in row("SAFE") and "3.000" in row("SAFE"), row("SAFE"))
    check("M2 server record without an image is not safe", " 1 " in row("SERVER_NO_IMAGE"), row("SERVER_NO_IMAGE"))
    check("M3 no server record (older than the listing's end) is not safe", " 1 " in row("NO_SERVER_RECORD"), row("NO_SERVER_RECORD"))
    check("M4 a plot that never synced is not safe", " 1 " in row("NOT_SYNCED"), row("NOT_SYNCED"))
    check("M5 an orphan newer than the listing is reported separately", " 1 " in row("NEWER_THAN_LISTING"), row("NEWER_THAN_LISTING"))
    check("M6 the allow-list holds only the safe orphan", al.exists() and al.read_text().strip() == "10|20260703|3221225472", al.read_text() if al.exists() else None)
    shifted = [dict(x, timestamp=x["timestamp"].replace("T01:", "T08:").replace("T01:30", "T08:30")) for x in man]
    (d / "man2.json").write_text(json.dumps(shifted)); al2 = d / "allow2.txt"
    m2 = subprocess.run([sys.executable, "-I", str(MATCH), str(d / "grab.txt"), str(d / "man2.json"), "--allowlist", str(al2)], capture_output=True, text=True)
    check("M7 a +7 h zone mismatch is detected, warned about, and no allow-list is written", "WARNING" in m2.stdout and not al2.exists(), m2.stdout[-300:])
    bad = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(bad)}/{len(results)} passed" + (f"; FAILED: {bad}" if bad else "")); sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
