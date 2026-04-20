#!/usr/bin/env python3
"""Build a pyorc CameraConfig from a scene video and a surveyed GCP set.

Inputs
------
  * GCPs in the target CRS as CSV with columns: id,x,y,z  (e.g. UTM Zone 48S / EPSG:32748)
  * Water-level CSV with columns: x,y,z  (single row; z is used as z_0)
    OR pass --z0 to override.
  * Scene video (a single frame is pulled for pixel clicks).

Assumptions
-----------
  * No staff gauge: h_ref is left unset, which pyorc treats as 0.0.
  * z_0 is the water-surface elevation at the time the GCPs were measured,
    in the same vertical reference as the GCPs (typically ellipsoidal).

Outputs
-------
  * pyorc CameraConfig JSON (via CameraConfig.to_file).
  * Saved pixel-click file (optional, for re-running without the UI).
  * Per-GCP residual table printed to stdout, sorted worst-first.

Usage
-----
Interactive (first run at a site):

    python orc_build_camera_config.py \\
        --video spring_2026_ID/survey_data/source_data/20260420T034813.mp4 \\
        --gcps spring_2026_ID/survey_data/output/gcps.csv \\
        --water-level spring_2026_ID/survey_data/output/water_level.csv \\
        --crs 32748 \\
        --output spring_2026_ID/survey_data/output/sukabumi_camera_config.json \\
        --save-clicks spring_2026_ID/survey_data/output/sukabumi_clicks.json

Replay saved clicks (no UI):

    python orc_build_camera_config.py \\
        --video ... --gcps ... --water-level ... \\
        --clicks spring_2026_ID/survey_data/output/sukabumi_clicks.json \\
        --output spring_2026_ID/survey_data/output/sukabumi_camera_config.json

Dry-run (validate inputs, skip pyorc and skip clicks):

    python orc_build_camera_config.py --dry-run \\
        --video ... --gcps ... --water-level ...

Install
-------
The OpenRiverCam package is distributed on PyPI as *pyopenrivercam* but imports
as ``pyorc``. Note: a different unrelated package also named ``pyorc`` on PyPI
reads Apache ORC files — do not install that one.

    python3 -m venv .venv
    source .venv/bin/activate
    pip install pyopenrivercam opencv-python matplotlib requests

Or use the pyorc source checkout at /Users/tjordan/code/git/pyorc with its
environment.yml:

    conda env create -f /Users/tjordan/code/git/pyorc/environment.yml
    conda activate pyorc
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path


def load_gcps(csv_path: str) -> list[dict]:
    """Load GCPs from CSV with columns id,x,y,z in the target CRS."""
    rows = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(
                {
                    "id": r["id"].strip(),
                    "x": float(r["x"]),
                    "y": float(r["y"]),
                    "z": float(r["z"]),
                }
            )
    if len(rows) < 6:
        raise ValueError(
            f"pyorc needs at least 6 GCPs for 3D fit; only {len(rows)} found in {csv_path}"
        )
    return rows


def load_water_level(csv_path: str) -> float:
    """Load z_0 from a water-level CSV with columns x,y,z.

    If multiple rows, return the mean z.
    """
    zs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            zs.append(float(r["z"]))
    if not zs:
        raise ValueError(f"no rows found in {csv_path}")
    return sum(zs) / len(zs)


def probe_video(video_path: str, frame_idx: int = 0):
    """Return (width, height, frame_bgr) from a video at a given frame index."""
    import cv2  # local import so --help works without cv2

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"cannot open video: {video_path}")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    nframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_idx >= nframes:
        cap.release()
        raise RuntimeError(f"frame {frame_idx} out of range (video has {nframes})")
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ok, frame = cap.read()
    cap.release()
    if not ok:
        raise RuntimeError(f"failed to read frame {frame_idx} from {video_path}")
    return width, height, frame


def click_gcps(frame_bgr, gcp_ids: list[str]) -> list[list[float]]:
    """Open a matplotlib window and collect one pixel click per GCP.

    Displays the GCP id being requested in the window title. Press 'u' to
    undo the last click, 'q' to abort.
    """
    import cv2  # noqa: F401 (for colormap compatibility)
    import matplotlib.pyplot as plt

    frame_rgb = frame_bgr[:, :, ::-1]
    clicks: list[list[float]] = []
    state = {"idx": 0, "abort": False}

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.imshow(frame_rgb)
    ax.set_title(f"Click pixel for {gcp_ids[0]}  (u=undo, q=quit)")

    def refresh_title():
        if state["idx"] < len(gcp_ids):
            ax.set_title(
                f"Click pixel for {gcp_ids[state['idx']]}  "
                f"({state['idx']}/{len(gcp_ids)} done, u=undo, q=quit)"
            )
        else:
            ax.set_title("All GCPs clicked. Close the window to continue.")
        fig.canvas.draw_idle()

    def on_click(event):
        if event.inaxes != ax or event.xdata is None:
            return
        if state["idx"] >= len(gcp_ids):
            return
        clicks.append([float(event.xdata), float(event.ydata)])
        ax.plot(event.xdata, event.ydata, "r+", markersize=12, mew=2)
        ax.annotate(
            gcp_ids[state["idx"]],
            (event.xdata, event.ydata),
            color="yellow",
            fontsize=9,
            xytext=(6, 6),
            textcoords="offset points",
        )
        state["idx"] += 1
        refresh_title()

    def on_key(event):
        if event.key == "u" and clicks:
            clicks.pop()
            ax.lines[-1].remove()
            ax.texts[-1].remove()
            state["idx"] -= 1
            refresh_title()
        elif event.key == "q":
            state["abort"] = True
            plt.close(fig)

    fig.canvas.mpl_connect("button_press_event", on_click)
    fig.canvas.mpl_connect("key_press_event", on_key)
    plt.show()

    if state["abort"]:
        raise SystemExit("aborted by user")
    if len(clicks) != len(gcp_ids):
        raise SystemExit(
            f"only {len(clicks)}/{len(gcp_ids)} GCPs clicked; rerun to finish"
        )
    return clicks


def compute_residuals(
    src_px: list[list[float]],
    dst_world: list[list[float]],
    width: int,
    height: int,
    camera_matrix=None,
    dist_coeffs=None,
):
    """Solve the pose with cv2.solvePnP and return per-GCP pixel residuals.

    If camera_matrix/dist_coeffs are not provided, a nominal pinhole model
    is used with focal length = max(width, height) and zero distortion.
    Residuals under this model are indicative only; use the real lens
    calibration for publication-quality numbers.
    """
    import cv2
    import numpy as np

    src = np.array(src_px, dtype=np.float64)
    dst = np.array(dst_world, dtype=np.float64)

    # centre the world coords to keep solvePnP numerically well-conditioned
    dst_mean = dst.mean(axis=0)
    dst_c = dst - dst_mean

    if camera_matrix is None:
        f = float(max(width, height))
        camera_matrix = np.array(
            [[f, 0, width / 2.0], [0, f, height / 2.0], [0, 0, 1.0]],
            dtype=np.float64,
        )
    else:
        camera_matrix = np.asarray(camera_matrix, dtype=np.float64)

    if dist_coeffs is None:
        dist_coeffs = np.zeros(5, dtype=np.float64)
    else:
        dist_coeffs = np.asarray(dist_coeffs, dtype=np.float64).reshape(-1)

    ok, rvec, tvec = cv2.solvePnP(
        dst_c,
        src,
        camera_matrix,
        dist_coeffs,
        flags=cv2.SOLVEPNP_ITERATIVE,
    )
    if not ok:
        raise RuntimeError("cv2.solvePnP failed")

    projected, _ = cv2.projectPoints(dst_c, rvec, tvec, camera_matrix, dist_coeffs)
    projected = projected.reshape(-1, 2)
    residuals_px = np.linalg.norm(src - projected, axis=1)
    return residuals_px, rvec, tvec


def print_residual_table(gcps: list[dict], residuals_px):
    import numpy as np

    rms = float(np.sqrt(np.mean(residuals_px ** 2)))
    order = np.argsort(-residuals_px)
    print()
    print(f"{'rank':>4}  {'id':<10}  {'residual [px]':>14}")
    print("-" * 36)
    for rank, i in enumerate(order, start=1):
        print(f"{rank:>4}  {gcps[i]['id']:<10}  {residuals_px[i]:>14.2f}")
    print("-" * 36)
    print(f"{'RMSE [px]':>32}: {rms:.2f}")
    print(f"{'n GCPs':>32}: {len(gcps)}")
    print()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--video", required=True, help="scene video path")
    p.add_argument("--gcps", required=True, help="gcps.csv (id,x,y,z in target CRS)")
    p.add_argument(
        "--water-level",
        help="water_level.csv (x,y,z); z mean used as z_0",
    )
    p.add_argument("--z0", type=float, help="override z_0 in metres")
    p.add_argument("--crs", type=int, default=32748, help="target CRS EPSG (default 32748)")
    p.add_argument("--frame", type=int, default=0, help="video frame index for clicks")
    p.add_argument("--output", help="output camera_config.json path")
    p.add_argument("--clicks", help="load pre-saved pixel clicks JSON (skips UI)")
    p.add_argument("--save-clicks", help="write pixel clicks to this JSON after UI")
    p.add_argument(
        "--calibration-video",
        help="charuco video for lens calibration (passed to CameraConfig.set_lens_calibration)",
    )
    p.add_argument(
        "--lens-position",
        help="camera lens position 'x,y,z' in the target CRS",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="validate inputs, probe video, skip clicks and pyorc (for CI/testing)",
    )
    p.add_argument(
        "--pyorc-path",
        default=None,
        help="optional path to local pyorc checkout, prepended to sys.path (only needed if pyorc is not installed in the active env)",
    )
    args = p.parse_args(argv)

    # --- load GCPs ---
    gcps = load_gcps(args.gcps)
    gcp_ids = [g["id"] for g in gcps]
    print(f"loaded {len(gcps)} GCPs from {args.gcps}: {', '.join(gcp_ids)}")

    # --- z_0 ---
    if args.z0 is not None:
        z_0 = args.z0
        z_src = "--z0 flag"
    elif args.water_level:
        z_0 = load_water_level(args.water_level)
        z_src = args.water_level
    else:
        raise SystemExit("provide either --water-level CSV or --z0 FLOAT")
    print(f"z_0 = {z_0:.3f} m  (from {z_src})")

    # --- video probe + frame extract ---
    width, height, frame = probe_video(args.video, args.frame)
    print(f"video: {args.video}  {width}x{height}  frame {args.frame}")

    # --- pixel clicks ---
    if args.clicks:
        with open(args.clicks) as f:
            saved = json.load(f)
        if set(saved) != set(gcp_ids):
            raise SystemExit(
                "saved clicks do not match GCP ids: "
                f"got {sorted(saved)} vs {sorted(gcp_ids)}"
            )
        src_px = [saved[i] for i in gcp_ids]
        print(f"loaded clicks for {len(src_px)} GCPs from {args.clicks}")
    elif args.dry_run:
        cx, cy = width / 2.0, height / 2.0
        step = min(width, height) / (len(gcps) + 1)
        src_px = [[cx + (i - len(gcps) / 2) * step, cy] for i in range(len(gcps))]
        print(f"dry-run: synthesised {len(src_px)} dummy clicks along horizontal midline")
    else:
        src_px = click_gcps(frame, gcp_ids)
        if args.save_clicks:
            payload = {gid: pt for gid, pt in zip(gcp_ids, src_px)}
            Path(args.save_clicks).parent.mkdir(parents=True, exist_ok=True)
            with open(args.save_clicks, "w") as f:
                json.dump(payload, f, indent=2)
            print(f"saved clicks to {args.save_clicks}")

    dst_world = [[g["x"], g["y"], g["z"]] for g in gcps]

    # --- quick residual preview with a nominal lens model ---
    res_px, rvec, tvec = compute_residuals(src_px, dst_world, width, height)
    print("\nnominal-lens residual preview (no distortion correction yet):")
    print_residual_table(gcps, res_px)

    if args.dry_run:
        print("dry-run: skipping pyorc CameraConfig construction and JSON write.")
        return 0

    # --- pyorc CameraConfig build ---
    if args.pyorc_path and args.pyorc_path not in sys.path:
        sys.path.insert(0, args.pyorc_path)
    import pyorc

    cfg_kwargs = dict(
        height=height,
        width=width,
        crs=args.crs,
    )
    if args.calibration_video:
        cfg_kwargs["calibration_video"] = args.calibration_video
    cfg = pyorc.CameraConfig(**cfg_kwargs)

    cfg.set_gcps(
        src=[list(p) for p in src_px],
        dst=dst_world,
        z_0=z_0,
        # h_ref intentionally omitted: no staff gauge
    )

    if args.lens_position:
        lx, ly, lz = (float(v) for v in args.lens_position.split(","))
        cfg.set_lens_position(lx, ly, lz)

    # residuals with the solved/calibrated lens
    cm = getattr(cfg, "camera_matrix", None)
    dc = getattr(cfg, "dist_coeffs", None)
    res_px_real, _, _ = compute_residuals(src_px, dst_world, width, height, cm, dc)
    print("residuals with pyorc lens model:")
    print_residual_table(gcps, res_px_real)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        cfg.to_file(args.output)
        print(f"wrote camera config: {args.output}")
    else:
        print("no --output path given; config not written")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
