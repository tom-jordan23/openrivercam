#!/usr/bin/env python3
"""IPB GCP clicker with predictive overlay.

Lets the operator click the 19 IPB GCP candidates (IDs 1-19) on a pinned
video frame. Once 6 or more clicks are recorded, the tool solves cv2.solvePnP
against the prior camera intrinsics (the SAME camera, same lens) to find the
camera pose in the IPB local frame, then projects every remaining GCP onto
the frame as a faint prediction so the rest of the clicks are guided.

Usage:

    python3 survey/ipb_gcp_click.py \\
        --video spring_2026_ID/survey_data/source_data/20260420T034813.mp4 \\
        --classified spring_2026_ID/survey_data/ipb_survey_1/classified.csv \\
        --intrinsics spring_2026_ID/sukabumi_bringup/data/camera_config.json \\
        -o spring_2026_ID/survey_data/ipb_survey_1/ipb_gcp_clicks.json

Controls:
    left-click   record pixel at cursor for the current GCP
    n / space    next GCP
    b            back
    u            undo current GCP's click
    s            mark current GCP as skipped (not visible)
    p            re-fit pose and refresh predictions
    q            save and exit
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

import cv2
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def frame_sha256(frame_rgb: np.ndarray) -> str:
    ok, buf = cv2.imencode(".png", cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR))
    if not ok:
        raise RuntimeError("failed to PNG-encode frame")
    return hashlib.sha256(buf.tobytes()).hexdigest()


def load_frame(video: Path, idx: int) -> np.ndarray:
    cap = cv2.VideoCapture(str(video))
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if idx < 0 or idx >= n:
        cap.release()
        raise SystemExit(f"frame_index {idx} out of range ({n} frames)")
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ok, bgr = cap.read()
    cap.release()
    if not ok:
        raise SystemExit(f"could not read frame {idx}")
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def load_gcp_candidates(classified_csv: Path, id_range=(1, 19)) -> list[dict]:
    """Return list of {id, x, y, z} for GCP candidates (IDs in id_range).

    Pulls from the structure-derived classified.csv. Falls back to whatever
    rows are labelled GCP_candidate if no numeric IDs are in id_range.
    """
    out: list[dict] = []
    with open(classified_csv) as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                i = int(row["id"])
            except ValueError:
                continue
            if id_range[0] <= i <= id_range[1]:
                out.append(
                    dict(
                        id=row["id"],
                        x=float(row["easting_ipb"]),
                        y=float(row["northing_ipb"]),
                        z=float(row["z_ipb"]),
                    )
                )
    out.sort(key=lambda r: int(r["id"]))
    return out


def load_intrinsics(camera_config_json: Path) -> tuple[np.ndarray, np.ndarray]:
    with open(camera_config_json) as f:
        cfg = json.load(f)
    K = np.asarray(cfg["camera_matrix"], dtype=np.float64)
    D = np.asarray(cfg["dist_coeffs"], dtype=np.float64).reshape(-1, 1)
    return K, D


class IPBClicker:
    def __init__(
        self,
        frame: np.ndarray,
        gcps: list[dict],
        K: np.ndarray,
        D: np.ndarray,
        meta: dict,
    ):
        self.frame = frame
        self.gcps = gcps
        self.K = K
        self.D = D
        self.meta = meta
        self.h, self.w = frame.shape[:2]
        self.clicks: dict[str, tuple[float, float]] = {}
        self.skipped: set[str] = set()
        self.idx = 0
        self.predictions: dict[str, tuple[float, float]] = {}
        self.rvec = None
        self.tvec = None
        self.pose_inliers: list[str] = []

        # Two-panel figure: frame on left, IPB plan view on right
        self.fig, (self.ax, self.ax_plan) = plt.subplots(
            1, 2, figsize=(18, 8.5), gridspec_kw={"width_ratios": [3, 1]}
        )
        self.ax.imshow(frame)
        self.ax.set_xlim(0, self.w)
        self.ax.set_ylim(self.h, 0)
        self.ax.set_title("video frame — left-click to record")

        # Reference plan view
        xs = [g["x"] for g in gcps]
        ys = [g["y"] for g in gcps]
        zs = [g["z"] for g in gcps]
        self.ax_plan.scatter(xs, ys, c=zs, cmap="viridis", s=80, edgecolor="k")
        for g in gcps:
            self.ax_plan.annotate(
                g["id"], (g["x"], g["y"]), fontsize=9, xytext=(4, 4),
                textcoords="offset points",
            )
        self.ax_plan.set_aspect("equal")
        self.ax_plan.set_title("IPB GCP plan view\n(reference)")
        self.ax_plan.grid(alpha=0.3)
        self.plan_highlight = None

        self.artists: list = []
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.fig.canvas.mpl_connect("key_press_event", self.on_key)
        self.fig.canvas.mpl_connect("scroll_event", self.on_scroll)
        self.update_title()
        self.redraw_markers()
        print(
            "IPB GCP clicker: left-click=record, n=next, b=back, u=undo, "
            "s=skip, p=re-predict, q=save+quit, scroll=zoom."
        )
        print(
            "Predictions appear automatically once 6 clicks are recorded; "
            "use --intrinsics from the prior salvage camera_config.json."
        )

    @property
    def current(self):
        return self.gcps[self.idx] if self.idx < len(self.gcps) else None

    def update_title(self):
        cur = self.current
        if cur is None:
            self.ax.set_title(f"all {len(self.gcps)} GCPs visited — q to save")
        else:
            gid = cur["id"]
            if gid in self.clicks:
                cx, cy = self.clicks[gid]
                state = f"clicked at ({cx:.0f}, {cy:.0f})"
            elif gid in self.skipped:
                state = "SKIPPED"
            elif gid in self.predictions:
                px, py = self.predictions[gid]
                state = f"predicted at ({px:.0f}, {py:.0f})"
            else:
                state = "unclicked, no prediction yet"
            self.ax.set_title(
                f"[{self.idx + 1}/{len(self.gcps)}] GCP {gid} "
                f"(IPB E={cur['x']:.2f} N={cur['y']:.2f} z={cur['z']:.2f})  —  {state}\n"
                f"clicked {len(self.clicks)}  skipped {len(self.skipped)}  "
                "n=next  b=back  u=undo  s=skip  p=re-predict  q=save"
            )
        self.fig.canvas.draw_idle()

    def refit_pose(self):
        if len(self.clicks) < 6:
            self.predictions = {}
            self.rvec = self.tvec = None
            return
        world = np.array(
            [[g["x"], g["y"], g["z"]] for g in self.gcps if g["id"] in self.clicks],
            dtype=np.float64,
        )
        pix = np.array(
            [self.clicks[g["id"]] for g in self.gcps if g["id"] in self.clicks],
            dtype=np.float64,
        )
        ok, rvec, tvec, inliers = cv2.solvePnPRansac(
            world, pix, self.K, self.D,
            reprojectionError=20.0, iterationsCount=2000,
            flags=cv2.SOLVEPNP_ITERATIVE,
        )
        if not ok:
            print("  solvePnPRansac failed")
            return
        self.rvec, self.tvec = rvec, tvec
        ids_with_clicks = [g["id"] for g in self.gcps if g["id"] in self.clicks]
        self.pose_inliers = (
            [ids_with_clicks[i] for i in inliers.flatten()] if inliers is not None else ids_with_clicks
        )

        # project every GCP
        full_world = np.array(
            [[g["x"], g["y"], g["z"]] for g in self.gcps], dtype=np.float64
        )
        proj, _ = cv2.projectPoints(full_world, rvec, tvec, self.K, self.D)
        proj = proj.reshape(-1, 2)
        self.predictions = {}
        for g, (u, v) in zip(self.gcps, proj):
            if 0 <= u < self.w and 0 <= v < self.h:
                self.predictions[g["id"]] = (float(u), float(v))

        # quick RMSE on clicks-vs-predictions for QA
        residuals = []
        for g in self.gcps:
            if g["id"] in self.clicks and g["id"] in self.predictions:
                cx, cy = self.clicks[g["id"]]
                px, py = self.predictions[g["id"]]
                residuals.append(np.hypot(cx - px, cy - py))
        if residuals:
            print(
                f"  pose fit: n_clicks={len(self.clicks)}, inliers={len(self.pose_inliers)}, "
                f"RMSE on clicks = {np.sqrt(np.mean(np.square(residuals))):.1f} px"
            )

    def redraw_markers(self):
        for a in self.artists:
            try:
                a.remove()
            except Exception:
                pass
        self.artists = []
        cur_gid = self.current["id"] if self.current else None

        # predictions (faint orange + ID)
        for gid, (x, y) in self.predictions.items():
            if gid in self.clicks:
                continue  # don't double-draw
            color = "yellow" if gid == cur_gid else "orange"
            ring = mpatches.Circle((x, y), 14, fill=False, lw=1.5, edgecolor=color, alpha=0.85)
            self.ax.add_patch(ring)
            cross = self.ax.plot(x, y, "+", color=color, ms=12, mew=1.5, alpha=0.85)[0]
            txt = self.ax.text(x + 16, y - 16, gid, color=color, fontsize=10, weight="bold", alpha=0.9)
            self.artists += [ring, cross, txt]

        # clicks (solid lime, current=cyan)
        for gid, (x, y) in self.clicks.items():
            color = "cyan" if gid == cur_gid else "lime"
            radius = 12 if gid == cur_gid else 8
            ring = mpatches.Circle((x, y), radius, fill=False, lw=2.5, edgecolor=color)
            self.ax.add_patch(ring)
            txt = self.ax.text(x + radius + 3, y - radius - 3, gid, color=color, fontsize=11, weight="bold")
            self.artists += [ring, txt]

        # plan-view highlight of current GCP
        if self.plan_highlight is not None:
            try:
                self.plan_highlight.remove()
            except Exception:
                pass
        if self.current is not None:
            cx, cy = self.current["x"], self.current["y"]
            self.plan_highlight = self.ax_plan.scatter(
                [cx], [cy], s=400, facecolors="none", edgecolors="red", linewidths=3, zorder=5
            )
        self.fig.canvas.draw_idle()

    def on_click(self, event):
        if event.inaxes is not self.ax:
            return
        if event.button != 1 or self.current is None:
            return
        gid = self.current["id"]
        self.clicks[gid] = (float(event.xdata), float(event.ydata))
        self.skipped.discard(gid)
        print(f"  GCP {gid} clicked at ({event.xdata:.1f}, {event.ydata:.1f})")
        self.refit_pose()
        self.redraw_markers()
        self.update_title()

    def on_key(self, event):
        if event.key in (" ", "n"):
            self.idx = min(self.idx + 1, len(self.gcps) - 1)
        elif event.key == "b":
            self.idx = max(self.idx - 1, 0)
        elif event.key == "u":
            if self.current is not None:
                self.clicks.pop(self.current["id"], None)
                self.refit_pose()
        elif event.key == "s":
            if self.current is not None:
                gid = self.current["id"]
                self.skipped.add(gid)
                self.clicks.pop(gid, None)
                self.refit_pose()
                self.idx = min(self.idx + 1, len(self.gcps) - 1)
        elif event.key == "p":
            self.refit_pose()
        elif event.key == "q":
            plt.close(self.fig)
            return
        self.redraw_markers()
        self.update_title()

    def on_scroll(self, event):
        if event.inaxes is not self.ax:
            return
        factor = 0.7 if event.button == "up" else 1.4
        cx, cy = event.xdata, event.ydata
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim(cx + (xlim[0] - cx) * factor, cx + (xlim[1] - cx) * factor)
        self.ax.set_ylim(cy + (ylim[0] - cy) * factor, cy + (ylim[1] - cy) * factor)
        self.fig.canvas.draw_idle()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True, type=Path)
    ap.add_argument("--classified", required=True, type=Path,
                    help="ipb_survey_1/classified.csv produced by the IPB analysis")
    ap.add_argument("--intrinsics", required=True, type=Path,
                    help="JSON with camera_matrix + dist_coeffs (prior camera_config.json)")
    ap.add_argument("--frame-index", type=int, default=0)
    ap.add_argument("--id-range", type=int, nargs=2, default=[1, 19],
                    help="inclusive IPB ID range to treat as GCPs (default 1-19)")
    ap.add_argument("-o", "--output", required=True, type=Path)
    ap.add_argument("--site", default="sukabumi")
    ap.add_argument("--collected-by", default="")
    args = ap.parse_args()

    frame = load_frame(args.video, args.frame_index)
    gcps = load_gcp_candidates(args.classified, tuple(args.id_range))
    if not gcps:
        sys.exit(f"no GCP candidates in {args.classified} for ID range {args.id_range}")
    K, D = load_intrinsics(args.intrinsics)
    print(f"loaded {len(gcps)} GCP candidates (IDs {gcps[0]['id']}..{gcps[-1]['id']})")
    print(f"frame {args.frame_index} of {args.video.name}")
    print(f"intrinsics: focal = ({K[0,0]:.0f}, {K[1,1]:.0f}), "
          f"principal = ({K[0,2]:.0f}, {K[1,2]:.0f})")

    meta = dict(
        schema_version="ipb-gcp-clicks/v1",
        site=args.site,
        video_source=str(args.video),
        frame_index=args.frame_index,
        frame_sha256=frame_sha256(frame),
        classified_csv=str(args.classified),
        classified_sha256=sha256_file(args.classified),
        intrinsics_source=str(args.intrinsics),
        collected_by=args.collected_by,
        collected_date=str(date.today()),
        method="click-with-pose-prediction",
    )

    app = IPBClicker(frame, gcps, K, D, meta)
    plt.show()

    out = dict(
        **meta,
        clicks={gid: list(xy) for gid, xy in sorted(app.clicks.items(), key=lambda kv: int(kv[0]))},
        skipped=sorted(app.skipped, key=int),
        pose=(
            dict(
                rvec=app.rvec.flatten().tolist(),
                tvec=app.tvec.flatten().tolist(),
                inliers=sorted(app.pose_inliers, key=int),
                world_frame="IPB local (NOT UTM)",
            ) if app.rvec is not None else None
        ),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nsaved {len(app.clicks)} clicks ({len(app.skipped)} skipped) to {args.output}")


if __name__ == "__main__":
    main()
