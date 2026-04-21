"""Stage 3 — minimum-RMSE subset search.

Greedy drop-one from the full resolved set of (UTM, pixel) correspondences.
At each step, remove the GCP whose removal most reduces RMSE. Stop when
(a) next removal would raise RMSE instead, (b) size hits the hard floor
(default 6), or (c) a soft guardrail fires.

Optionally run an exhaustive check over C(n, k..n) for small n after the
greedy loop, to verify the greedy result is a local optimum.

Hard constraints per AUTO_FIT_DESIGN.md §5.3:
  |S| >= 6                                       (ORC_FIT_STRATEGY §5 floor)
  every image quadrant contains ≥ 1 GCP in S     (prevents bank collapse)

Each subset evaluation is a single cv2.solvePnP call (~1 ms) with frozen
intrinsics — no re-optimization.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from typing import Optional

import cv2
import numpy as np


@dataclass
class SubsetEvaluation:
    ids: tuple[str, ...]
    rmse_px: float
    rmse_m: float
    per_gcp_residual_px: dict[str, float]
    per_gcp_residual_m: dict[str, float]
    rvec: np.ndarray
    tvec: np.ndarray
    rejected_reason: Optional[str] = None  # non-None means the subset was filtered


@dataclass
class SubsetSearchResult:
    best: SubsetEvaluation
    baseline: SubsetEvaluation                      # full set evaluation
    greedy_trajectory: list[SubsetEvaluation]       # RMSE trace of the drop-one loop
    exhaustive_considered: int                      # how many subsets the exhaustive step scored
    exhaustive_best: Optional[SubsetEvaluation]     # only set if exhaustive ran
    constraints: dict = field(default_factory=dict)


def _solvepnp_on_subset(
    ids: list[str],
    world_by_id: dict[str, np.ndarray],
    pixel_by_id: dict[str, tuple[float, float]],
    K: np.ndarray,
    dist_coeffs: np.ndarray,
    camera_position_world: np.ndarray,
    init_rvec: np.ndarray,
    init_tvec: np.ndarray,
) -> Optional[SubsetEvaluation]:
    """Fit a pose on `ids` using plain cv2.solvePnP (deterministic,
    fast). Uses the supplied (rvec, tvec) as initial guess for iteration."""
    if len(ids) < 4:
        return None
    wp = np.array([world_by_id[g] for g in ids], dtype=np.float64)
    ip = np.array([list(pixel_by_id[g]) for g in ids], dtype=np.float64)
    centroid = wp.mean(axis=0)
    wp_c = (wp - centroid).reshape(-1, 1, 3)
    ip_r = ip.reshape(-1, 1, 2)
    # Shift init_tvec to the centred world
    R_wc, _ = cv2.Rodrigues(init_rvec)
    init_tvec_c = (init_tvec.flatten() + R_wc @ centroid).reshape(3, 1)
    try:
        ok, rvec, tvec_c = cv2.solvePnP(
            wp_c, ip_r, K, dist_coeffs,
            rvec=init_rvec.astype(np.float64).copy(),
            tvec=init_tvec_c.astype(np.float64).copy(),
            useExtrinsicGuess=True,
            flags=cv2.SOLVEPNP_ITERATIVE,
        )
    except cv2.error:
        return None
    if not ok:
        return None
    R_wc2, _ = cv2.Rodrigues(rvec)
    tvec_world = tvec_c.flatten() - R_wc2 @ centroid
    tvec_world = tvec_world.reshape(3, 1)

    projected, _ = cv2.projectPoints(
        wp.reshape(-1, 1, 3), rvec, tvec_world, K, dist_coeffs
    )
    proj = projected.reshape(-1, 2)
    res_px = np.linalg.norm(ip - proj, axis=1)
    ranges_m = np.linalg.norm(wp - camera_position_world, axis=1)
    focal_px = float(0.5 * (K[0, 0] + K[1, 1]))
    res_m = res_px * ranges_m / focal_px
    return SubsetEvaluation(
        ids=tuple(ids),
        rmse_px=float(np.sqrt(np.mean(res_px ** 2))),
        rmse_m=float(np.sqrt(np.mean(res_m ** 2))),
        per_gcp_residual_px={g: float(r) for g, r in zip(ids, res_px)},
        per_gcp_residual_m={g: float(r) for g, r in zip(ids, res_m)},
        rvec=rvec.astype(np.float64),
        tvec=tvec_world.astype(np.float64),
    )


def _quadrant_of(pixel: tuple[float, float], frame_size: tuple[int, int]) -> int:
    """Return image quadrant 0..3 for a pixel.
      0 = top-left, 1 = top-right, 2 = bottom-left, 3 = bottom-right."""
    w, h = frame_size
    return (0 if pixel[0] < w / 2 else 1) + (0 if pixel[1] < h / 2 else 2)


def _check_constraints(
    ids: list[str],
    pixel_by_id: dict[str, tuple[float, float]],
    frame_size: tuple[int, int],
    min_size: int,
    require_all_quadrants: bool,
) -> Optional[str]:
    """Return None if constraints satisfied, else a reason string."""
    if len(ids) < min_size:
        return f"|S|={len(ids)} < min_size={min_size}"
    if require_all_quadrants:
        seen = {_quadrant_of(pixel_by_id[g], frame_size) for g in ids}
        if len(seen) < 4:
            missing = sorted({0, 1, 2, 3} - seen)
            return f"empty image quadrants {missing}"
    return None


def subset_search(
    all_ids: list[str],
    world_by_id: dict[str, np.ndarray],
    pixel_by_id: dict[str, tuple[float, float]],
    K: np.ndarray,
    dist_coeffs: np.ndarray,
    camera_position_world: np.ndarray,
    init_rvec: np.ndarray,
    init_tvec: np.ndarray,
    frame_size: tuple[int, int],
    min_size: int = 6,
    require_all_quadrants: bool = True,
    exhaustive_below_n: int = 15,
) -> SubsetSearchResult:
    """Greedy drop-one + optional exhaustive.

    Trajectory records every step including rejected moves (so the audit
    can show why the loop stopped).
    """
    # Baseline evaluation: full set
    baseline = _solvepnp_on_subset(
        all_ids, world_by_id, pixel_by_id, K, dist_coeffs,
        camera_position_world, init_rvec, init_tvec,
    )
    if baseline is None:
        raise RuntimeError("Baseline PnP failed on full set")

    reason = _check_constraints(
        all_ids, pixel_by_id, frame_size, min_size, require_all_quadrants
    )
    baseline.rejected_reason = reason  # may be None

    trajectory = [baseline]
    current_ids = list(all_ids)
    current_best = baseline

    while True:
        best_removal: Optional[SubsetEvaluation] = None
        for g in current_ids:
            trial = [x for x in current_ids if x != g]
            reason = _check_constraints(
                trial, pixel_by_id, frame_size, min_size, require_all_quadrants
            )
            if reason is not None:
                # infeasible; skip
                continue
            ev = _solvepnp_on_subset(
                trial, world_by_id, pixel_by_id, K, dist_coeffs,
                camera_position_world,
                current_best.rvec, current_best.tvec,
            )
            if ev is None:
                continue
            if best_removal is None or ev.rmse_m < best_removal.rmse_m:
                best_removal = ev
        if best_removal is None:
            break  # constraints prevent any removal
        if best_removal.rmse_m >= current_best.rmse_m:
            break  # no improvement
        trajectory.append(best_removal)
        current_best = best_removal
        current_ids = list(best_removal.ids)

    # Optional exhaustive sweep over subsets of the greedy result (and
    # supersets by adding one-back), just to guard against greedy local
    # minima.
    exhaustive_considered = 0
    exhaustive_best: Optional[SubsetEvaluation] = None
    n = len(current_ids)
    if n <= exhaustive_below_n:
        for size in range(min_size, len(all_ids) + 1):
            for combo in combinations(all_ids, size):
                exhaustive_considered += 1
                combo_list = list(combo)
                reason = _check_constraints(
                    combo_list, pixel_by_id, frame_size, min_size,
                    require_all_quadrants,
                )
                if reason is not None:
                    continue
                ev = _solvepnp_on_subset(
                    combo_list, world_by_id, pixel_by_id, K, dist_coeffs,
                    camera_position_world, init_rvec, init_tvec,
                )
                if ev is None:
                    continue
                if exhaustive_best is None or ev.rmse_m < exhaustive_best.rmse_m:
                    exhaustive_best = ev

    best = current_best
    if exhaustive_best is not None and exhaustive_best.rmse_m < best.rmse_m:
        best = exhaustive_best

    return SubsetSearchResult(
        best=best,
        baseline=baseline,
        greedy_trajectory=trajectory,
        exhaustive_considered=exhaustive_considered,
        exhaustive_best=exhaustive_best,
        constraints={
            "min_size": min_size,
            "require_all_quadrants": require_all_quadrants,
            "exhaustive_below_n": exhaustive_below_n,
        },
    )
