"""Join the 07-03 lighting metrics with the harness results (test B2).

Usage: python3 analyse_day.py out_day/metrics.jsonl out_day/runs/results_serial.jsonl
"""
import json
import statistics as st
import sys
from collections import defaultdict

metrics = {r["id"]: r for r in map(json.loads, open(sys.argv[1]))}
runs = [json.loads(l) for l in open(sys.argv[2])]


def ok(r):
    return r.get("h") is not None and r.get("rc") == 0


def sn(r):
    """Accepted S/N if the run passed, else the best rejected S/N."""
    if r["accepted"]:
        return r["accepted"][-1][1]
    if r["rejected"]:
        return max(x[1] for x in r["rejected"])
    return None


def is_day(wib):
    h = int(wib[:2])
    return 6 <= h < 18


def rank(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    rk = [0.0] * len(xs)
    for pos, i in enumerate(order):
        rk[i] = float(pos)
    return rk


def spearman(a, b):
    if len(a) < 4:
        return float("nan")
    ra, rb = rank(a), rank(b)
    ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den if den else float("nan")


for r in runs:
    r["wib"] = metrics[r["id"]]["wib"]

print("## 1. pass rate and median S/N, by method × arrangement × day/night")
print(f"{'arr':8} {'method':9} | {'day ok':>8} {'day med S/N':>11} | {'night ok':>8} {'night med S/N':>13}")
for arr in ("live", "up_both"):
    for m in ("grayscale", "hue", "sat", "val"):
        rs = [r for r in runs if r["arr"] == arr and r["method"] == m]
        d = [r for r in rs if is_day(r["wib"])]
        n = [r for r in rs if not is_day(r["wib"])]
        fmt = lambda g: (f"{sum(map(ok, g))}/{len(g)}", f"{st.median([s for s in map(sn, g) if s is not None]):.2f}" if g else "-")
        dk, ds = fmt(d)
        nk, ns = fmt(n)
        print(f"{arr:8} {m:9} | {dk:>8} {ds:>11} | {nk:>8} {ns:>13}")

print("\n## 2. live arrangement, per clip: S/N by method beside the lighting metrics")
by = defaultdict(dict)
for r in runs:
    if r["arr"] == "live":
        by[r["id"]][r["method"]] = r
print(f"{'id':5} {'WIB':5} | {'gray':>6} {'hue':>6} {'sat':>6} {'val':>6} | {'sun_shade':>9} {'clip%':>6} {'washed%':>7} {'roi std':>7} {'sat':>5}")
for vid in sorted(by, key=lambda v: metrics[v]["wib"]):
    mm = metrics[vid]
    cells = []
    for m in ("grayscale", "hue", "sat", "val"):
        r = by[vid].get(m)
        s = sn(r) if r else None
        cells.append(("-" if s is None else f"{s:.2f}") + ("*" if r and ok(r) else " "))
    print(f"{vid:5} {mm['wib']:5} | {cells[0]:>6} {cells[1]:>6} {cells[2]:>6} {cells[3]:>6} | "
          f"{mm['r_sun_shade']:9.2f} {mm['r_clip']:6.2f} {mm['r_washed']:7.2f} {mm['r_std']:7.1f} {mm['r_sat']:5.1f}")
print("  (* = passed the 2.0 gate)")

print("\n## 3. daytime only, live arrangement: Spearman rank correlation of S/N with each metric")
for m in ("grayscale", "hue", "sat", "val"):
    rows = [(sn(by[v][m]), metrics[v]) for v in by if m in by[v] and is_day(metrics[v]["wib"]) and sn(by[v][m]) is not None]
    s = [x[0] for x in rows]
    line = [f"{k}={spearman(s, [x[1][k] for x in rows]):+.2f}" for k in ("r_sun_shade", "r_clip", "r_washed", "r_std", "r_mean", "f_clip")]
    print(f"  {m:9} n={len(rows):2}  " + "  ".join(line))
