"""Per-clip lighting metrics for the S/N-vs-exposure check (test B2).

Runs inside the orc-os-v060-orcapi container. Read-only on /media.

For each clip, averages over 8 evenly spaced frames:
  whole frame   mean, std, clipped (>=250) %, crushed (<=5) %
  near-bank ROI the waterline region the WL detector reads — crop 900x560 at
                (560,180) in the 1920x1080 frame, the same crop inspected by eye
                in the 2421 / 2430 / 2417 comparison
    mean, std, clipped %, crushed %, bright-low-saturation % (washed out),
    dark % (<40), bright % (>200), and sun_shade = min(dark%, bright%) — high
    only when the ROI holds both deep shadow and hard sun at once
    colour = mean saturation (near 0 means the IR/mono night image)

Usage: python3 frame_metrics.py /work/day0703.json /work/out_day/metrics.jsonl
"""
import json
import sys

import cv2
import numpy as np

ROI = (560, 180, 900, 560)  # x, y, w, h


def metrics(path, n=8):
    cap = cv2.VideoCapture(path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 64
    acc = []
    for idx in np.linspace(0, total - 1, n).astype(int):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
        ok, im = cap.read()
        if not ok:
            continue
        g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        x, y, w, h = ROI
        r = im[y:y + h, x:x + w]
        rg = g[y:y + h, x:x + w]
        hsv = cv2.cvtColor(r, cv2.COLOR_BGR2HSV)
        dark = (rg < 40).mean() * 100
        bright = (rg > 200).mean() * 100
        acc.append({
            "f_mean": g.mean(), "f_std": g.std(),
            "f_clip": (g >= 250).mean() * 100, "f_crush": (g <= 5).mean() * 100,
            "r_mean": rg.mean(), "r_std": rg.std(),
            "r_clip": (rg >= 250).mean() * 100, "r_crush": (rg <= 5).mean() * 100,
            "r_washed": ((hsv[..., 2] > 230) & (hsv[..., 1] < 40)).mean() * 100,
            "r_dark": dark, "r_bright": bright, "r_sun_shade": min(dark, bright),
            "r_sat": hsv[..., 1].mean(),
        })
    cap.release()
    if not acc:
        return {"error": "no frames read"}
    return {k: round(float(np.mean([a[k] for a in acc])), 2) for k in acc[0]}


def main():
    jobs = json.load(open(sys.argv[1]))
    with open(sys.argv[2], "w") as fo:
        for j in jobs:
            rec = {"id": j["id"], "wib": j.get("wib"), **metrics(j["clip"])}
            fo.write(json.dumps(rec) + "\n")
            fo.flush()
    print(f"wrote {len(jobs)} records")


if __name__ == "__main__":
    main()
