"""Tests for Stage-1 pose bootstrap.

Assertions are structural (shape, range, invariance under reruns) rather
than exact-value — the bootstrap's numbers are sensitive to the focal
length default and world-frame conventions, which are free to change.
"""

from __future__ import annotations

import numpy as np

from auto_fit import bootstrap as bs


def _synthetic_gcps() -> list:
    """6 UTM points spanning a ~5×5 m footprint centred near our site."""
    base_x = 714120.0
    base_y = 9234410.0
    base_z = 620.0
    rows = [
        ("G1", base_x + 0.0, base_y + 0.0, base_z + 0.0),
        ("G2", base_x + 5.0, base_y + 0.0, base_z + 0.5),
        ("G3", base_x + 0.0, base_y + 5.0, base_z + 0.3),
        ("G4", base_x + 5.0, base_y + 5.0, base_z + 0.8),
        ("G5", base_x + 2.5, base_y + 2.5, base_z + 0.4),
        ("G6", base_x + 2.5, base_y + 0.0, base_z + 0.2),
    ]
    return [(gid, np.array([x, y, z])) for gid, x, y, z in rows]


def _synthetic_camera_position() -> np.ndarray:
    # ~5 m south of the cluster, 4 m above
    return np.array([714120.0 + 2.5, 9234410.0 - 5.0, 620.0 + 4.0])


def test_intrinsics_shape_and_focal() -> None:
    K = bs.build_intrinsics(1920, 1080, focal_px=1500.0)
    assert K.shape == (3, 3)
    assert K[0, 0] == 1500.0
    assert K[1, 1] == 1500.0
    assert K[0, 2] == 960.0   # principal point at image centre
    assert K[1, 2] == 540.0
    assert K[2, 2] == 1.0


def test_bootstrap_returns_valid_rvec_tvec() -> None:
    result = bs.bootstrap_pose(
        gcps=_synthetic_gcps(),
        camera_position=_synthetic_camera_position(),
        frame_size=(1920, 1080),
    )
    assert result.rvec.shape == (3, 1)
    assert result.tvec.shape == (3, 1)
    assert np.all(np.isfinite(result.rvec))
    assert np.all(np.isfinite(result.tvec))
    assert result.dist_coeffs.shape == (5,)


def test_bootstrap_is_deterministic() -> None:
    """Same inputs -> identical outputs. Guards against stochastic drift."""
    gcps = _synthetic_gcps()
    cam = _synthetic_camera_position()
    a = bs.bootstrap_pose(gcps, cam, (1920, 1080))
    b = bs.bootstrap_pose(gcps, cam, (1920, 1080))
    np.testing.assert_array_equal(a.rvec, b.rvec)
    np.testing.assert_array_equal(a.tvec, b.tvec)
    np.testing.assert_array_equal(a.K, b.K)


def test_project_points_gives_finite_pixels_near_image_centre() -> None:
    """GCP centroid should project near the principal point under a
    look-at bootstrap (since the look-at target IS the centroid)."""
    gcps = _synthetic_gcps()
    cam = _synthetic_camera_position()
    result = bs.bootstrap_pose(gcps, cam, (1920, 1080))

    centroid = np.array([p for _, p in gcps]).mean(axis=0).reshape(1, 3)
    projected = bs.project_points(
        centroid, result.K, result.dist_coeffs, result.rvec, result.tvec
    )
    assert projected.shape == (1, 2)
    x, y = projected[0]
    # principal point is (960, 540); look-at should land centroid there
    # (up to a few px in practice); allow generous tolerance.
    assert abs(x - 960.0) < 50.0
    assert abs(y - 540.0) < 50.0
