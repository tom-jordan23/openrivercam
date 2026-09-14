"""Re-extract results from existing run outputs, serially (libhdf5 is not
thread-safe). No reprocessing. Reports the water level pyorc ACCEPTED, not the
highest S/N seen. Usage: python3 extract_serial.py /work/out_full"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, "/work")
from run_swap import extract  # noqa: E402

root = sys.argv[1]
recs = {}
for line in open(os.path.join(root, "results.jsonl")):
    r = json.loads(line)
    recs[(r["id"], r["arr"], r.get("method"))] = r

out = []
for (vid, arr, method), r in sorted(recs.items(), key=lambda kv: (kv[0][0], kv[0][1], str(kv[0][2]))):
    d = os.path.join(root, f"{vid}_{arr}" if method is None else f"{vid}_{arr}_{method}")
    text = ""
    for f in ("stdout.txt", "stderr.txt"):
        p = os.path.join(d, f)
        if os.path.exists(p):
            text += open(p, errors="replace").read()
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)
    acc = re.findall(r"Found significant water level at h: ([\d.]+) m with signal-to-noise: ([\d.]+)", text)
    rej = re.findall(r"Found water level at h: ([\d.]+) m with too low signal-to-noise: ([\d.]+)", text)
    rec = {"id": vid, "arr": arr, "method": method, "cls": r["cls"], "rc": r.get("returncode"),
           "accepted": [(float(h), float(s)) for h, s in acc],
           "rejected": [(float(h), float(s)) for h, s in rej],
           "wl_failed": "could not be estimated" in text.lower()}
    nc = os.path.join(d, "output", "transect_transect_1.nc")
    if os.path.exists(nc):
        try:
            rec.update(extract(nc))
        except Exception as e:  # noqa: BLE001
            rec["extract_error"] = repr(e)[:200]
    else:
        rec["no_transect_nc"] = True
    out.append(rec)

with open(os.path.join(root, "results_serial.jsonl"), "w") as fo:
    for rec in out:
        fo.write(json.dumps(rec) + "\n")
print(f"wrote {len(out)} records")
