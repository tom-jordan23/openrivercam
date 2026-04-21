"""Stage 2b — pose refinement via MAGSAC PnP.

Given (UTM, pixel) correspondences and frozen intrinsics, fit the camera
pose and report per-GCP reprojection residuals in world-metres.

We use cv2.solvePnPRansac with the USAC_MAGSAC flag when available
(MAGSAC++ — Barath et al., CVPR 2020; the soft-weighted RANSAC variant
recommended by the research review). If the flag is unsupported by the
installed OpenCV wheel we fall back to plain cv2.RANSAC.

For numerical stability, world coordinates are recentred on the GCP
centroid before being handed to solvePnP; the final tvec is shifted back
to the raw UTM frame before being returned to the caller.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import cv2
import numpy as np


def _select_pnp_flags() -> int:
    """Prefer MAGSAC++ if the installed OpenCV supports it."""
    return getattr(cv2, "USAC_MAGSAC", cv2.RANSAC)


@dataclass
class RefineResult:
    rvec: np.ndarray                    # Rodrigues rotation, world -> camera
    tvec: np.ndarray                    # translation, world -> camera (3x1)
    inlier_ids: list[str]               # GCP IDs that MAGSAC accepted
    outlier_ids: list[str]              # GCP IDs MAGSAC rejected
    per_gcp_residual_px: dict[str, float]     # reprojection error in pixels
    per_gcp_residual_m: dict[str, float]      # reprojection error in world metres
    rmse_px: float                      # over inliers only
    rmse_m: float                       # over inliers only
    pnp_flags: int                      # which RANSAC variant was used
    reprojection_threshold_px: float    # RANSAC threshold used
    extra: dict = field(default_factory=dict)


def _pixels_to_world_metres(
    residual_px: float, approx_range_m: float, focal_px: float
) -> float:
    """Convert a pixel residual into an approximate world-metres residual
    using the simple pinhole conversion at the given camera range."""
    return residual_px * approx_range_m / focal_px


def refine_pose_magsac(
    gcp_ids: list[str],
    world_points: np.ndarray,           # N x 3, raw UTM
    image_points: np.ndarray,           # N x 2
    K: np.ndarray,
    dist_coeffs: np.ndarray,
    camera_position_world: np.ndarray,  # for metres-conversion of residuals
    reprojection_threshold_px: float = 8.0,
    confidence: float = 0.9999,
    max_iters: int = 10000,
    rng_seed: int = 0,
) -> Optional[RefineResult]:
    """Fit (rvec, tvec) with MAGSAC PnP and return per-GCP residuals.

    Returns None if PnP failed (insufficient points, degenerate geometry).
    """
    assert len(gcp_ids) == len(world_points) == len(image_points)
    n = len(gcp_ids)
    if n < 4:
        return None

    # Recentre on GCP centroid for numerical stability
    centroid = world_points.mean(axis=0)
    wp_centred = (world_points - centroid).astype(np.float64).reshape(-1, 1, 3)
    ip = image_points.astype(np.float64).reshape(-1, 1, 2)

    cv2.setRNGSeed(int(rng_seed))
    flags = _select_pnp_flags()
    try:
        ok, rvec, tvec_local, inliers = cv2.solvePnPRansac(
            wp_centred,
            ip,
            K,
            dist_coeffs,
            iterationsCount=max_iters,
            reprojectionError=float(reprojection_threshold_px),
            confidence=float(confidence),
            flags=flags,
        )
    except cv2.error:
        # Retry with plain RANSAC if MAGSAC flag caused trouble
        flags = cv2.RANSAC
        ok, rvec, tvec_local, inliers = cv2.solvePnPRansac(
            wp_centred,
            ip,
            K,
            dist_coeffs,
            iterationsCount=max_iters,
            reprojectionError=float(reprojection_threshold_px),
            confidence=float(confidence),
            flags=flags,
        )
    if not ok or inliers is None or len(inliers) < 4:
        return None

    inlier_idx = set(int(i) for i in inliers.flatten())

    # Shift tvec back to raw-UTM frame.
    # With world = centred + centroid, the projection equation is
    #   x_cam = R_wc @ (X_world - centroid) + tvec_local
    #         = R_wc @ X_world + (tvec_local - R_wc @ centroid)
    # so the UTM-frame tvec is tvec_local - R_wc @ centroid.
    R_wc, _ = cv2.Rodrigues(rvec)
    tvec_world = tvec_local.flatten() - R_wc @ centroid
    tvec_world = tvec_world.reshape(3, 1)

    # Residuals: reproject every GCP (not just inliers) and measure
    projected, _ = cv2.projectPoints(
        world_points.astype(np.float64).reshape(-1, 1, 3),
        rvec,
        tvec_world,
        K,
        dist_coeffs,
    )
    projected = projected.reshape(-1, 2)
    residuals_px_vec = image_points - projected
    residuals_px = np.linalg.norm(residuals_px_vec, axis=1)

    # Approximate per-GCP camera range for pixel->metres conversion.
    # This uses the true camera position so the conversion is accurate
    # even when the pose is imperfect.
    ranges_m = np.linalg.norm(world_points - camera_position_world, axis=1)
    focal_px = float(0.5 * (K[0, 0] + K[1, 1]))
    residuals_m = residuals_px * ranges_m / focal_px

    per_gcp_px = {gid: float(r) for gid, r in zip(gcp_ids, residuals_px)}
    per_gcp_m = {gid: float(r) for gid, r in zip(gcp_ids, residuals_m)}

    inlier_ids = [gcp_ids[i] for i in range(n) if i in inlier_idx]
    outlier_ids = [gcp_ids[i] for i in range(n) if i not in inlier_idx]

    inlier_res_px = np.array([per_gcp_px[g] for g in inlier_ids])
    inlier_res_m = np.array([per_gcp_m[g] for g in inlier_ids])
    rmse_px = float(np.sqrt(np.mean(inlier_res_px ** 2))) if len(inlier_res_px) else float("nan")
    rmse_m = float(np.sqrt(np.mean(inlier_res_m ** 2))) if len(inlier_res_m) else float("nan")

    return RefineResult(
        rvec=rvec.astype(np.float64),
        tvec=tvec_world.astype(np.float64),
        inlier_ids=inlier_ids,
        outlier_ids=outlier_ids,
        per_gcp_residual_px=per_gcp_px,
        per_gcp_residual_m=per_gcp_m,
        rmse_px=rmse_px,
        rmse_m=rmse_m,
        pnp_flags=int(flags),
        reprojection_threshold_px=float(reprojection_threshold_px),
    )
