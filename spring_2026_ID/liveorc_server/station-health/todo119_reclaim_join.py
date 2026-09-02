#!/usr/bin/env python3
"""TODO-119: join the station's file inventory against the verified mirror.

WHY THIS IS THE RIGHT COMPARISON
    Tom, 2026-09-02: verify first, before deleting anything. The question is
    which station-local clips are provably redundant. Asking the server's
    DATABASE is not evidence of bytes - that check would have passed on
    2026-08-09, the day before 26 GB of media was destroyed with every row
    intact (MEDIA_VOLUME_RUNBOOK.md).

    So the comparison is against bytes: the TODO-114 mirror at
    data/liveorc-mirror/4/media, 2630 mp4s pulled 2026-08-25 over two
    independent transports that agreed. It is also itself a second copy, so a
    clip verified here survives in two places even if the station's goes.

    Size-for-size, not name-for-name. The link tears connections down
    mid-transfer, so a truncated server copy marked SYNCED was a live
    possibility that only a size comparison could catch.

INPUTS   the newest orc-sukabumi-deletesafety119g-*.txt grab, and the mirror tree
OUTPUTS  findings/sukabumi_backlog_workplan.csv - the newest-first upload plan
         and a reclaim/hold verdict per clip. Reads only; deletes nothing.
"""
import collections, csv, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
art = sorted((REPO/"data/station-forensics").glob("orc-sukabumi-deletesafety119g-*.txt"))[-1]
mirror_dir = REPO/"data/liveorc-mirror/4/media"

lines = art.read_text().splitlines()
i0 = next(i for i,l in enumerate(lines) if l.startswith("=== INVENTORY"))
i1 = next(i for i,l in enumerate(lines) if l.startswith("=== END INVENTORY"))
rows = []
for l in lines[i0+1:i1]:
    p = l.split("|")
    if len(p) == 4 and p[3].isdigit():
        rows.append({"status": p[0], "remote_id": p[1], "name": p[2], "bytes": int(p[3])})

mir = {f.name: f.stat().st_size for f in mirror_dir.rglob("*.mp4")}
print(f"station extant mp4s {len(rows)}   mirror files {len(mir)}   source {art.name}")

out = REPO/"spring_2026_ID/findings/sukabumi_backlog_workplan.csv"
with out.open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["date","name","station_status","remote_id","station_bytes",
                "mirror_bytes","in_mirror","size_match","verdict"])
    counts = collections.Counter(); gb = collections.Counter()
    for r in sorted(rows, key=lambda r: r["name"], reverse=True):
        mb = mir.get(r["name"])
        inm = mb is not None
        same = inm and mb == r["bytes"]
        if r["status"] == "SYNCED":
            # RECLAIM only on independently verified bytes. A clip synced after
            # the 08-25 mirror is absent for an innocent reason, but absent is
            # absent - it has no second copy, so it is held, not deleted.
            v = "RECLAIM" if same else ("HOLD-mismatch" if inm else "HOLD-unverified")
        elif inm and same:
            # FAILED yet byte-identical on the server: the upload completed and
            # the acknowledgement did not survive. Nothing to re-drive.
            v = "ALREADY-ON-SERVER"
        else:
            v = "UPLOAD"
        counts[v] += 1; gb[v] += r["bytes"]
        w.writerow([f"{r['name'][:4]}-{r['name'][4:6]}-{r['name'][6:8]}", r["name"],
                    r["status"], r["remote_id"], r["bytes"], mb if inm else "",
                    inm, same, v])

print(f"\n{'verdict':20} {'files':>6} {'GB':>7}")
for v, n in counts.most_common():
    print(f"{v:20} {n:6d} {gb[v]/2**30:7.2f}")
print(f"\nwritten: {out.relative_to(REPO)}")
