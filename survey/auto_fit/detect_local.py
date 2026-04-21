"""Stage 2a — local checker-score marker detector.

Given a grayscale video frame and a predicted pixel location for a GCP,
find the best checkerboard/X-pattern marker inside a window centred on
that prediction.

Approach (per AUTO_FIT_DESIGN.md v0.2 §5.2):
  1. Extract a window of ±half_window px around the predicted centre.
  2. Run Shi-Tomasi corner detection inside the window.
  3. For each corner candidate, compute a "checker-ness" score by
     comparing the four quadrants around it: a genuine 2×2 checker has
     two diagonal-matching high-contrast pairs.
  4. Apply non-maximum suppression and return the top candidate if its
     score exceeds a threshold.

The detector is deliberately simple. The global-detection spike
(/tmp/auto_fit_spike/detection/) produced 108 candidates with only
~10 real markers in a whole frame — a 10 % precision. Restricting to
±50 px windows eliminates that noise because real cobbles and wall
edges are unlikely to coincide with our projected GCP locations.
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class Detection:
    x: float         # pixel x in the full frame
    y: float         # pixel y in the full frame
    score: float     # checker score (higher = more marker-like)
    scale: int       # half-size of the winning quadrant test
    n_candidates: int  # raw corner count the detector evaluated in the window
    accepted: bool   # whether the detection passed the score threshold


DEFAULT_SCALES = (6, 10, 14, 20)
DEFAULT_SCORE_THRESHOLD = 25.0
DEFAULT_MAX_CORNERS = 60
DEFAULT_QUALITY = 0.005
DEFAULT_MIN_DISTANCE = 8


def _checker_score(gray: np.ndarray, cx: int, cy: int, half: int) -> float:
    """Score how "checker-like" the local patch is at scale `half` px.

    A 2×2 checker has opposite quadrants of similar intensity and
    adjacent quadrants of different intensity. We return (adj_diff_sum -
    diag_diff_sum), which is large-positive for a genuine checker and
    near-zero or negative for smooth/edge/random texture.
    """
    h, w = gray.shape
    if cx - half < 0 or cy - half < 0 or cx + half >= w or cy + half >= h:
        return -np.inf
    tl = gray[cy - half:cy, cx - half:cx].mean()
    tr = gray[cy - half:cy, cx:cx + half].mean()
    bl = gray[cy:cy + half, cx - half:cx].mean()
    br = gray[cy:cy + half, cx:cx + half].mean()
    # High positive when adjacent pairs differ sharply and diagonal
    # pairs are similar -> classic checker signature
    adj = abs(tl - tr) + abs(bl - br) + abs(tl - bl) + abs(tr - br)
    diag = abs(tl - br) + abs(tr - bl)
    return float(adj / 2.0 - diag / 2.0)


def detect_in_window(
    gray: np.ndarray,
    predicted_xy: tuple[float, float],
    half_window: int,
    scales: tuple[int, ...] = DEFAULT_SCALES,
    score_threshold: float = DEFAULT_SCORE_THRESHOLD,
    max_corners: int = DEFAULT_MAX_CORNERS,
    quality: float = DEFAULT_QUALITY,
    min_distance: int = DEFAULT_MIN_DISTANCE,
) -> Detection:
    """Detect the best marker candidate in a window around a predicted pixel.

    Parameters
    ----------
    gray : HxW uint8 grayscale frame.
    predicted_xy : (x, y) in full-frame pixel coordinates.
    half_window : size of the search window in each direction.

    Returns
    -------
    Detection whose `accepted` flag indicates whether the top candidate
    cleared the score threshold. Even rejected detections carry (x, y,
    score) for diagnostic purposes.
    """
    H, W = gray.shape
    px, py = predicted_xy
    x0 = max(0, int(round(px - half_window)))
    y0 = max(0, int(round(py - half_window)))
    x1 = min(W, int(round(px + half_window)))
    y1 = min(H, int(round(py + half_window)))
    if x1 - x0 < 4 * scales[0] or y1 - y0 < 4 * scales[0]:
        return Detection(x=float(px), y=float(py), score=-np.inf, scale=0,
                         n_candidates=0, accepted=False)

    sub = gray[y0:y1, x0:x1]
    # Shi-Tomasi corners in the window
    corners = cv2.goodFeaturesToTrack(
        sub,
        maxCorners=max_corners,
        qualityLevel=quality,
        minDistance=min_distance,
        blockSize=7,
    )
    if corners is None or len(corners) == 0:
        return Detection(x=float(px), y=float(py), score=-np.inf, scale=0,
                         n_candidates=0, accepted=False)

    best: Detection | None = None
    for c in corners.reshape(-1, 2):
        # back to full-frame coords
        fx = int(round(c[0])) + x0
        fy = int(round(c[1])) + y0
        best_score_for_c = -np.inf
        best_scale_for_c = 0
        for s in scales:
            sc = _checker_score(gray, fx, fy, half=s)
            if sc > best_score_for_c:
                best_score_for_c = sc
                best_scale_for_c = s
        if best is None or best_score_for_c > best.score:
            best = Detection(
                x=float(fx),
                y=float(fy),
                score=float(best_score_for_c),
                scale=int(best_scale_for_c),
                n_candidates=len(corners),
                accepted=False,
            )

    if best is None:
        return Detection(x=float(px), y=float(py), score=-np.inf, scale=0,
                         n_candidates=0, accepted=False)

    best.accepted = bool(best.score >= score_threshold)
    return best


def refine_subpixel(gray: np.ndarray, xy: tuple[float, float],
                    window: int = 5) -> tuple[float, float]:
    """Polish a detected pixel to sub-pixel accuracy via cv2.cornerSubPix."""
    p = np.array([[xy]], dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.001)
    cv2.cornerSubPix(gray, p, (window, window), (-1, -1), criteria)
    return float(p[0, 0, 0]), float(p[0, 0, 1])
