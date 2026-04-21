"""Annotated-frame visualization for auto-fit runs.

Writes `annotated.png` to the run directory showing, per GCP:
  - GT click (blue cross) if ground truth supplied
  - Bootstrap projection (red dot, small)
  - Final projection under refined pose (magenta dot, small)
  - Detected pixel (green circle for inlier, orange X for outlier/rejected)
  - Line from final projection to detected pixel

This is the single most useful diagnostic for iterating on detector/bootstrap
parameters — you can see at a glance which windows went right, which snapped
to the wrong feature, and whether the pose refinement is plausible.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


COLOR_GT = (255, 0, 0)          # blue
COLOR_BOOTSTRAP = (0, 0, 255)   # red
COLOR_FINAL_PROJ = (255, 0, 255)  # magenta
COLOR_INLIER = (0, 255, 0)      # green
COLOR_OUTLIER = (0, 165, 255)   # orange
COLOR_NOT_DETECTED = (128, 128, 128)  # gray


def draw_cross(img, xy, color, size=10, thickness=2):
    x, y = int(round(xy[0])), int(round(xy[1]))
    cv2.line(img, (x - size, y), (x + size, y), color, thickness)
    cv2.line(img, (x, y - size), (x, y + size), color, thickness)


def draw_x(img, xy, color, size=8, thickness=2):
    x, y = int(round(xy[0])), int(round(xy[1]))
    cv2.line(img, (x - size, y - size), (x + size, y + size), color, thickness)
    cv2.line(img, (x - size, y + size), (x + size, y - size), color, thickness)


def annotate_run(
    frame_bgr: np.ndarray,
    gcp_ids: list[str],
    bootstrap_proj: dict[str, tuple[float, float]],
    final_proj: dict[str, tuple[float, float]] | None,
    detections: dict[str, tuple[float, float]],
    inlier_set: set[str],
    gt_clicks: dict[str, list[float]] | None,
    output_path: Path,
) -> None:
    img = frame_bgr.copy()

    for gid in gcp_ids:
        boot = bootstrap_proj.get(gid)
        fin = final_proj.get(gid) if final_proj else None
        det = detections.get(gid)
        gt = gt_clicks.get(gid) if gt_clicks else None

        if gt is not None:
            draw_cross(img, gt, COLOR_GT, size=12, thickness=2)
            cv2.putText(
                img, gid,
                (int(gt[0]) + 14, int(gt[1]) - 4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_GT, 1,
            )

        if boot is not None:
            cv2.circle(img, (int(boot[0]), int(boot[1])), 4,
                       COLOR_BOOTSTRAP, -1)
        if fin is not None:
            cv2.circle(img, (int(fin[0]), int(fin[1])), 4,
                       COLOR_FINAL_PROJ, -1)
        if det is not None:
            colour = COLOR_INLIER if gid in inlier_set else COLOR_OUTLIER
            if gid in inlier_set:
                cv2.circle(img, (int(det[0]), int(det[1])), 10,
                           colour, 2)
            else:
                draw_x(img, det, colour, size=8, thickness=2)
            if fin is not None:
                cv2.line(img,
                         (int(fin[0]), int(fin[1])),
                         (int(det[0]), int(det[1])),
                         colour, 1)

        if det is None and boot is not None:
            # mark "not detected" with a gray small-cross on the bootstrap loc
            cv2.putText(
                img, gid,
                (int(boot[0]) + 6, int(boot[1]) + 14),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_NOT_DETECTED, 1,
            )

    # Legend block top-left
    legend = [
        ("GT click (+)", COLOR_GT),
        ("bootstrap proj", COLOR_BOOTSTRAP),
        ("final proj", COLOR_FINAL_PROJ),
        ("inlier detection (O)", COLOR_INLIER),
        ("outlier detection (X)", COLOR_OUTLIER),
    ]
    y = 24
    for text, colour in legend:
        cv2.putText(img, text, (14, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour, 1)
        y += 18

    cv2.imwrite(str(output_path), img)
