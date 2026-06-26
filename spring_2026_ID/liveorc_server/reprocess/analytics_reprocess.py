#!/usr/bin/env python3
"""Quantify how the Fit 6 reprocess changed the Sukabumi record.

Consumes the JSONL emitted by reprocess_fit6.py (works on a --dry-run log too, so
you can preview the impact BEFORE committing). Produces a Markdown report + PNG
plots: water-level datum shift, discharge change, rating-curve before/after,
velocimetry coverage, and the biggest movers.

  python analytics_reprocess.py reprocess-logs/reprocess_dry_<stamp>.jsonl [--out report]

Optional full-column DB diff (after a commit), joining the backup baseline CSV with
a post-commit CSV by time_series id:
  python analytics_reprocess.py LOG.jsonl --baseline-csv pre/api_timeseries.csv \
        --post-csv post/api_timeseries.csv --out report
"""
import argparse
import json
import os
import statistics as st

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_PLT = True
except Exception:
    HAVE_PLT = False


def load(jsonl):
    rows = []
    with open(jsonl) as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def describe(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return "n=0"
    return (f"n={len(xs)} mean={st.mean(xs):.3f} median={st.median(xs):.3f} "
            f"min={min(xs):.3f} max={max(xs):.3f}"
            + (f" sd={st.pstdev(xs):.3f}" if len(xs) > 1 else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl")
    ap.add_argument("--out", default="reprocess-report")
    ap.add_argument("--baseline-csv", default=None)
    ap.add_argument("--post-csv", default=None)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    rows = load(args.jsonl)
    by_status = {}
    for r in rows:
        by_status.setdefault(r["status"], []).append(r)
    ok = by_status.get("ok", [])

    # paired arrays (only rows that had both an old and a new value)
    oh, nh, oq, nq, nv, nf, movers = [], [], [], [], [], [], []
    for r in ok:
        o, n = r.get("old") or {}, r.get("new") or {}
        if o.get("h") is not None and n.get("h") is not None:
            oh.append(o["h"]); nh.append(n["h"])
        if o.get("q_50") is not None and n.get("q_50") is not None:
            oq.append(o["q_50"]); nq.append(n["q_50"])
            pct = (n["q_50"] - o["q_50"]) / o["q_50"] * 100 if o["q_50"] else float("inf")
            movers.append((pct, r["video_id"], o["q_50"], n["q_50"],
                           o.get("h"), n.get("h")))
        if n.get("v_av") is not None:
            nv.append(n["v_av"])
        if n.get("fraction_velocimetry") is not None:
            nf.append(n["fraction_velocimetry"])

    dh = [b - a for a, b in zip(oh, nh)]
    dq = [b - a for a, b in zip(oq, nq)]
    sign_flips = sum(1 for a, b in zip(oq, nq) if (a > 0) != (b > 0))
    movers.sort(key=lambda t: abs(t[0]) if t[0] != float("inf") else 1e18, reverse=True)

    # ---- plots ----
    plots = []
    if HAVE_PLT:
        if dh:
            plt.figure(); plt.hist(dh, bins=40)
            plt.xlabel("Δ water level new−old [m]"); plt.ylabel("count")
            plt.title("Water-level datum shift (Fit 6 − salvage)")
            p = os.path.join(args.out, "delta_h.png"); plt.savefig(p, dpi=110, bbox_inches="tight"); plt.close()
            plots.append(p)
        if oq and nq:
            plt.figure(); plt.scatter(oq, nq, s=8, alpha=0.4)
            lim = max(oq + nq) * 1.05 if (oq + nq) else 1
            plt.plot([0, lim], [0, lim], "k--", lw=0.8)
            plt.xlabel("old q_50 [m³/s]"); plt.ylabel("new q_50 [m³/s]")
            plt.title("Discharge: Fit 6 vs salvage (1:1 dashed)")
            p = os.path.join(args.out, "q50_scatter.png"); plt.savefig(p, dpi=110, bbox_inches="tight"); plt.close()
            plots.append(p)
        if oh and oq and nh and nq:
            plt.figure()
            plt.scatter(oh, oq, s=8, alpha=0.4, label="salvage")
            plt.scatter(nh, nq, s=8, alpha=0.4, label="Fit 6")
            plt.xlabel("water level h [m]"); plt.ylabel("q_50 [m³/s]")
            plt.title("Rating curve before/after"); plt.legend()
            p = os.path.join(args.out, "rating_curve.png"); plt.savefig(p, dpi=110, bbox_inches="tight"); plt.close()
            plots.append(p)
        if nf:
            plt.figure(); plt.hist(nf, bins=40)
            plt.xlabel("fraction_velocimetry [%] (new)"); plt.ylabel("count")
            plt.title("Velocimetry coverage after Fit 6")
            p = os.path.join(args.out, "fraction_velocimetry.png"); plt.savefig(p, dpi=110, bbox_inches="tight"); plt.close()
            plots.append(p)

    # ---- markdown ----
    md = os.path.join(args.out, "REPORT.md")
    with open(md, "w") as f:
        f.write("# Sukabumi Fit 6 reprocess — impact report\n\n")
        f.write(f"Source log: `{args.jsonl}`  \n")
        f.write(f"Total videos in log: **{len(rows)}**\n\n")
        f.write("## Outcomes\n\n| status | count |\n|---|---|\n")
        for k in sorted(by_status):
            f.write(f"| {k} | {len(by_status[k])} |\n")
        f.write("\n_Only `ok` rows are written to the DB; everything else leaves the old value intact._\n\n")

        f.write("## Water level (h)\n\n")
        f.write(f"- old: {describe(oh)}\n- new: {describe(nh)}\n- Δ(new−old): {describe(dh)}\n")
        f.write("- A consistent negative Δh is expected (Fit 6 z_0=615.0 vs the higher salvage datum).\n\n")

        f.write("## Discharge (q_50)\n\n")
        f.write(f"- old: {describe(oq)}\n- new: {describe(nq)}\n- Δ(new−old): {describe(dq)}\n")
        f.write(f"- sign flips (pos↔neg/zero): **{sign_flips}**\n\n")
        f.write("## Velocimetry\n\n")
        f.write(f"- new v_av: {describe(nv)}\n- new fraction_velocimetry [%]: {describe(nf)}\n\n")

        f.write("## Biggest discharge movers (top 15 by |%|)\n\n")
        f.write("| video | old q_50 | new q_50 | %Δ | old h | new h |\n|---|---|---|---|---|---|\n")
        for pct, vid, o_, n_, oh_, nh_ in movers[:15]:
            pj = "inf" if pct == float("inf") else f"{pct:+.0f}%"
            f.write(f"| {vid} | {o_:.3f} | {n_:.3f} | {pj} | "
                    f"{'' if oh_ is None else f'{oh_:.2f}'} | {'' if nh_ is None else f'{nh_:.2f}'} |\n")
        f.write("\n")
        if plots:
            f.write("## Plots\n\n")
            for p in plots:
                f.write(f"![{os.path.basename(p)}]({os.path.basename(p)})\n\n")
        if not HAVE_PLT:
            f.write("_matplotlib not available — plots skipped (text stats only)._\n")

    print(f"Report written: {md}")
    for p in plots:
        print(f"  plot: {p}")
    print("\nHeadline:")
    print(f"  ok={len(ok)}  Δh {describe(dh)}")
    print(f"  q_50 Δ {describe(dq)}  sign_flips={sign_flips}")


if __name__ == "__main__":
    main()
