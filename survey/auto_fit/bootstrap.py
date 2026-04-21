"""Stage 1 — pose bootstrap for the auto-fit pipeline.

Produces an initial (K, rvec, tvec, dist_coeffs) quadruple that is accurate
enough for Stage 2's windowed marker detection. The quality bar is "each
GCP projects within ~±50 px of its true pixel location" — that is what
defines the first-pass detection window.

Inputs: surveyed camera position (CAM) and the set of GCP UTM coordinates.
Output: a world-to-camera (rvec, tvec) using the standard OpenCV
convention (rvec in Rodrigues form, tvec in camera coordinates), plus
frozen intrinsics K and (zero) distortion.

Coordinate system: world points are UTM in metres (EPSG:32748 at Sukabumi).
Internally we subtract a reference offset to keep the PnP objective
numerically well-conditioned, but the returned pose is expressed relative
to the raw (unshifted) world frame.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


DEFAULT_FOCAL_PX = 1500.0
DEFAULT_PRINCIPAL_POINT = None  # resolved from frame size at call time


@dataclass
class BootstrapResult:
    K: np.ndarray               # 3x3 intrinsics
    dist_coeffs: np.ndarray     # 5-vector (zeros by default)
    rvec: np.ndarray            # Rodrigues rotation, world -> camera
    tvec: np.ndarray            # translation, world -> camera
    camera_center_world: np.ndarray  # world-frame camera position (for reporting)
    gcp_centroid_world: np.ndarray   # world-frame GCP centroid (look-at target)
    frame_size: tuple           # (width, height)


def load_gcps(path: Path) -> list[tuple[str, np.ndarray]]:
    """Return [(id, np.array([x, y, z])), ...] from an ORC-OS gcps.csv."""
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(
                (
                    row["id"],
                    np.array([float(row["x"]), float(row["y"]), float(row["z"])]),
                )
            )
    return rows


def load_camera_position(path: Path) -> np.ndarray:
    with open(path) as f:
        r = csv.DictReader(f)
        row = next(r)
        return np.array([float(row["x"]), float(row["y"]), float(row["z"])])


def build_intrinsics(frame_width: int, frame_height: int,
                     focal_px: float = DEFAULT_FOCAL_PX) -> np.ndarray:
    """Default intrinsics: square pixels, focal=focal_px, principal point
    at image centre, zero skew."""
    return np.array(
        [
            [focal_px, 0.0, frame_width / 2.0],
            [0.0, focal_px, frame_height / 2.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=np.float64,
    )


def _look_at_matrix(eye: np.ndarray, target: np.ndarray,
                    world_up: np.ndarray) -> np.ndarray:
    """Build a 3x3 world-to-camera rotation matrix.

    OpenCV camera convention: +Z points into the scene, +Y points down in
    the image, +X points right. We construct the orthonormal basis from
    the look-at direction and a world-up hint.
    """
    forward = target - eye
    forward = forward / np.linalg.norm(forward)

    # right = forward x world_up; but the image-down axis must project to
    # something physically sensible (roughly "down" in the world).
    # Build "image right" = normalize(cross(forward, world_up))
    right = np.cross(forward, world_up)
    rn = np.linalg.norm(right)
    if rn < 1e-6:
        # forward is parallel to world_up; pick any orthogonal direction
        right = np.cross(forward, np.array([1.0, 0.0, 0.0]))
        rn = np.linalg.norm(right)
    right = right / rn

    # image down = cross(forward, right); this is +Y_cam in OpenCV convention
    down = np.cross(forward, right)
    down = down / np.linalg.norm(down)

    # world -> camera: rows are camera basis in world frame
    R_wc = np.array([right, down, forward])
    return R_wc


def bootstrap_pose(
    gcps: list[tuple[str, np.ndarray]],
    camera_position: np.ndarray,
    frame_size: tuple[int, int],
    focal_px: float = DEFAULT_FOCAL_PX,
) -> BootstrapResult:
    """Construct initial K, rvec, tvec from CAM + GCP centroid look-at.

    This is deterministic and parameter-free apart from focal length.
    """
    width, height = frame_size
    gcp_points = np.array([p for _, p in gcps])
    centroid = gcp_points.mean(axis=0)

    # Look-at rotation, assuming world-up is +Z (UTM ellipsoidal height)
    R_wc = _look_at_matrix(
        eye=camera_position,
        target=centroid,
        world_up=np.array([0.0, 0.0, 1.0]),
    )

    # tvec = -R_wc @ camera_position (standard camera-extrinsic identity:
    # a world point X projects to R_wc @ X + tvec in camera coords; when
    # X = camera_position, camera coord must be [0,0,0], hence
    # tvec = -R_wc @ camera_position)
    tvec = -R_wc @ camera_position
    rvec, _ = cv2.Rodrigues(R_wc)

    K = build_intrinsics(width, height, focal_px=focal_px)
    dist_coeffs = np.zeros(5, dtype=np.float64)

    return BootstrapResult(
        K=K,
        dist_coeffs=dist_coeffs,
        rvec=rvec.astype(np.float64),
        tvec=tvec.reshape(3, 1).astype(np.float64),
        camera_center_world=camera_position.copy(),
        gcp_centroid_world=centroid,
        frame_size=frame_size,
    )


def project_points(
    world_points: np.ndarray,
    K: np.ndarray,
    dist_coeffs: np.ndarray,
    rvec: np.ndarray,
    tvec: np.ndarray,
) -> np.ndarray:
    """Project Nx3 world points to Nx2 image pixels."""
    if world_points.size == 0:
        return np.zeros((0, 2), dtype=np.float64)
    pts = world_points.reshape(-1, 1, 3).astype(np.float64)
    projected, _ = cv2.projectPoints(pts, rvec, tvec, K, dist_coeffs)
    return projected.reshape(-1, 2)
