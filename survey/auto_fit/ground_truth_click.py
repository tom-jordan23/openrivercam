#!/usr/bin/env python3
"""Phase 0 ground-truth clicker for the auto-fit design.

Produces a versioned JSON fixture (per AUTO_FIT_DESIGN.md v0.2 §9.1) by
prompting the operator to click each GCP on a single pinned frame of the
calibration video.

Usage:

    python3 survey/auto_fit/ground_truth_click.py \\
        --video spring_2026_ID/survey_data/source_data/20260420T034813.mp4 \\
        --gcps spring_2026_ID/survey_data/output/gcps.csv \\
        --camera-position spring_2026_ID/survey_data/output/camera_position.csv \\
        --site sukabumi \\
        --collected-by "Tom Jordan" \\
        -o survey/tests/fixtures/sukabumi_gt_clicks_v1.json

Controls:

    left-click    record pixel at cursor for the current GCP
    n / space     advance to the next GCP
    b             back to the previous GCP
    u             undo the click on the current GCP
    s             skip (mark GCP as not visible in this frame)
    scroll-wheel  zoom in (scroll up) / out (scroll down) centred on cursor
    q             save and exit
    close window  save and exit

Output JSON follows AUTO_FIT_DESIGN.md §9.1 exactly:
    - schema_version, site, video_source, frame_index
    - frame_sha256 (of the PNG-encoded frame), gcps_csv_sha256
    - collected_by, collected_date, method
    - clicks: {gcp_id: [x, y]} for every clicked GCP
    - skipped: sorted list of GCP IDs the operator marked not-visible
    - bank_assignment: auto-computed from UTM via PCA; edit the file
      by hand if the auto-assignment is wrong

The file is versioned by filename (not by schema_version). To create a
new ground-truth set (e.g. after a re-survey), save as _v2 — never
overwrite _v1.
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
    """Hash the PNG-encoded bytes of the frame so the SHA is reproducible
    independent of the video-decoder path."""
    ok, buf = cv2.imencode(".png", cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR))
    if not ok:
        raise RuntimeError("failed to PNG-encode frame for SHA-256")
    return hashlib.sha256(buf.tobytes()).hexdigest()


def load_frame(video_path: Path, frame_idx: int) -> np.ndarray:
    cap = cv2.VideoCapture(str(video_path))
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_idx < 0 or frame_idx >= n:
        cap.release()
        raise SystemExit(
            f"frame_index {frame_idx} out of range (video has {n} frames)"
        )
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ok, frame_bgr = cap.read()
    cap.release()
    if not ok:
        raise SystemExit(f"could not read frame {frame_idx} from {video_path}")
    return cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)


def load_gcps(path: Path) -> list[tuple[str, float, float, float]]:
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(
                (row["id"], float(row["x"]), float(row["y"]), float(row["z"]))
            )
    return rows


def load_camera_xy(path: Path) -> tuple[float, float]:
    with open(path) as f:
        r = csv.DictReader(f)
        row = next(r)
        return (float(row["x"]), float(row["y"]))


def compute_bank_assignment(
    gcps: list[tuple[str, float, float, float]],
    camera_xy: tuple[float, float] | None,
) -> dict[str, str]:
    """Classify each GCP as 'near' or 'far' bank relative to the camera.

    Method: PCA across GCP UTM XY. The minor principal axis is the
    across-river direction (GCPs span both banks, so the minor axis has
    the smaller spread). Each GCP and the camera get projected onto that
    axis. GCPs with the same sign as the camera's projection are 'near';
    opposite sign is 'far'.

    If camera_xy is None, every GCP is labelled 'unknown' and the user
    is expected to fill in by hand.
    """
    if camera_xy is None:
        return {g[0]: "unknown" for g in gcps}
    xy = np.array([[g[1], g[2]] for g in gcps], dtype=float)
    centroid = xy.mean(axis=0)
    centered = xy - centroid
    # SVD gives principal directions in V-transpose
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    minor_axis = vt[-1]  # smallest singular value direction
    gcp_proj = centered @ minor_axis
    cam_proj = (np.array(camera_xy) - centroid) @ minor_axis
    cam_side = 1.0 if cam_proj >= 0 else -1.0
    return {
        g[0]: ("near" if (np.sign(p) if p != 0 else cam_side) == cam_side else "far")
        for g, p in zip(gcps, gcp_proj)
    }


class ClickerApp:
    def __init__(self, frame_rgb: np.ndarray, gcps: list, meta: dict):
        self.frame = frame_rgb
        self.gcps = gcps
        self.meta = meta
        self.clicks: dict[str, tuple[float, float]] = {}
        self.skipped: set[str] = set()
        self.idx = 0
        self.height, self.width = frame_rgb.shape[:2]

        self.fig, self.ax = plt.subplots(figsize=(15, 8.5))
        self.ax.imshow(frame_rgb)
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(self.height, 0)
        self.artists: list = []

        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.fig.canvas.mpl_connect("key_press_event", self.on_key)
        self.fig.canvas.mpl_connect("scroll_event", self.on_scroll)
        self.update_title()
        print(
            "ground-truth clicker: "
            "left-click=record, n=next, b=back, u=undo, s=skip, q=save+quit, "
            "scroll=zoom. Use matplotlib toolbar for pan if needed."
        )

    @property
    def current(self) -> tuple | None:
        return self.gcps[self.idx] if self.idx < len(self.gcps) else None

    def update_title(self) -> None:
        cur = self.current
        if cur is None:
            self.ax.set_title(
                f"All {len(self.gcps)} GCP(s) visited — press q to save and exit"
            )
        else:
            gid = cur[0]
            if gid in self.clicks:
                x, y = self.clicks[gid]
                state = f"clicked at ({x:.1f}, {y:.1f})"
            elif gid in self.skipped:
                state = "SKIPPED (not visible)"
            else:
                state = "unclicked"
            clicked_n = len(self.clicks)
            skipped_n = len(self.skipped)
            self.ax.set_title(
                f"[{self.idx + 1}/{len(self.gcps)}] GCP {gid}  —  {state}  "
                f"(clicked: {clicked_n}, skipped: {skipped_n})\n"
                "left-click=record   n=next   b=back   u=undo   s=skip   q=save+quit"
            )
        self.fig.canvas.draw_idle()

    def redraw_markers(self) -> None:
        for a in self.artists:
            a.remove()
        self.artists = []
        cur_gid = self.current[0] if self.current else None
        for gid, (x, y) in self.clicks.items():
            highlight = gid == cur_gid
            colour = "yellow" if highlight else "lime"
            radius = 10 if highlight else 6
            circ = mpatches.Circle(
                (x, y), radius, fill=False, linewidth=2, edgecolor=colour
            )
            self.ax.add_patch(circ)
            txt = self.ax.text(
                x + radius + 2,
                y - radius - 2,
                gid,
                color=colour,
                fontsize=9,
                weight="bold",
            )
            self.artists.append(circ)
            self.artists.append(txt)

    def on_click(self, event) -> None:
        if event.inaxes is not self.ax or event.button != 1:
            return
        tb = self.fig.canvas.toolbar
        if tb is not None and tb.mode != "":
            return  # zoom/pan is active; don't record a stray click
        cur = self.current
        if cur is None:
            return
        gid = cur[0]
        if event.xdata is None or event.ydata is None:
            return
        self.clicks[gid] = (float(event.xdata), float(event.ydata))
        self.skipped.discard(gid)
        self.redraw_markers()
        self.update_title()

    def on_key(self, event) -> None:
        k = event.key
        if k in ("n", " ", "right"):
            self.advance(+1)
        elif k in ("b", "left"):
            self.advance(-1)
        elif k == "u":
            cur = self.current
            if cur and cur[0] in self.clicks:
                del self.clicks[cur[0]]
                self.redraw_markers()
                self.update_title()
        elif k == "s":
            cur = self.current
            if cur:
                gid = cur[0]
                self.skipped.add(gid)
                self.clicks.pop(gid, None)
                self.redraw_markers()
                self.advance(+1)
        elif k == "q":
            plt.close(self.fig)

    def advance(self, delta: int) -> None:
        self.idx = max(0, min(len(self.gcps), self.idx + delta))
        self.redraw_markers()
        self.update_title()

    def on_scroll(self, event) -> None:
        if event.inaxes is not self.ax or event.xdata is None:
            return
        scale = 0.8 if event.button == "up" else 1.25
        x, y = event.xdata, event.ydata
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        new_halfw = (xlim[1] - xlim[0]) * scale / 2
        new_halfh = (ylim[0] - ylim[1]) * scale / 2  # imshow y is inverted
        self.ax.set_xlim(x - new_halfw, x + new_halfw)
        self.ax.set_ylim(y + new_halfh, y - new_halfh)
        self.fig.canvas.draw_idle()

    def run(self) -> None:
        plt.show()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Ground-truth clicker — Phase 0 of the auto-fit design.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--video", type=Path, required=True, help="Calibration video")
    ap.add_argument(
        "--gcps", type=Path, required=True, help="gcps.csv (ORC-OS format)"
    )
    ap.add_argument(
        "--camera-position",
        type=Path,
        help="camera_position.csv — used to auto-compute bank_assignment",
    )
    ap.add_argument(
        "--frame-index", type=int, default=0, help="Frame to click on (default 0)"
    )
    ap.add_argument("--site", required=True, help="Site name (e.g. sukabumi)")
    ap.add_argument("--collected-by", required=True, help="Operator name")
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output JSON path (versioned filename, e.g. sukabumi_gt_clicks_v1.json)",
    )
    ap.add_argument(
        "--force", action="store_true", help="Overwrite output if it exists"
    )
    args = ap.parse_args(argv)

    if args.output.exists() and not args.force:
        raise SystemExit(
            f"{args.output} exists — refusing to overwrite. "
            "Use --force, or save to a new versioned filename (…_v2.json)."
        )

    frame = load_frame(args.video, args.frame_index)
    gcps = load_gcps(args.gcps)
    camera_xy = (
        load_camera_xy(args.camera_position) if args.camera_position else None
    )
    bank_assignment = compute_bank_assignment(gcps, camera_xy)

    meta = {
        "schema_version": 1,
        "site": args.site,
        "video_source": str(args.video),
        "frame_index": args.frame_index,
        "frame_sha256": frame_sha256(frame),
        "gcps_csv_sha256": sha256_file(args.gcps),
        "collected_by": args.collected_by,
        "collected_date": str(date.today()),
        "method": "manual-click via survey/auto_fit/ground_truth_click.py",
    }

    app = ClickerApp(frame, gcps, meta)
    app.run()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        **meta,
        "clicks": {gid: [round(x, 2), round(y, 2)] for gid, (x, y) in app.clicks.items()},
        "skipped": sorted(app.skipped),
        "bank_assignment": bank_assignment,
    }
    with open(args.output, "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")

    print(
        f"\nsaved {len(app.clicks)} click(s), {len(app.skipped)} skipped "
        f"→ {args.output}"
    )
    total = len(gcps)
    unclicked = total - len(app.clicks) - len(app.skipped)
    if unclicked:
        unclicked_ids = [
            g[0] for g in gcps if g[0] not in app.clicks and g[0] not in app.skipped
        ]
        print(
            f"WARNING: {unclicked} GCP(s) were neither clicked nor skipped: "
            f"{unclicked_ids}. Re-run to finish."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
