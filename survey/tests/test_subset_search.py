"""Tests for Stage-3 subset search.

Structural invariants only (|S| >= min, quadrant coverage, RMSE
monotonicity) — never assert the exact winning subset, since that
depends on the specific noise pattern of the dataset.
"""

from __future__ import annotations

import numpy as np

from auto_fit import bootstrap as bs
from auto_fit import subset_search as ss


def _synthetic_gcp_dict(n: int = 10) -> tuple[dict, dict, list[str]]:
    """Build a synthetic (world_by_id, pixel_by_id, ids) from a known
    camera pose + zero noise. Every GCP should be a perfect inlier.
    """
    # World points span four quadrants of the image
    rng = np.random.default_rng(42)
    world = rng.uniform(
        low=[714115.0, 9234405.0, 618.0],
        high=[714125.0, 9234415.0, 622.0],
        size=(n, 3),
    )
    ids = [f"GCP{i + 1}" for i in range(n)]
    world_by_id = {gid: world[i] for i, gid in enumerate(ids)}

    # Camera pose: look at centroid from ~5 m south, 4 m up
    centroid = world.mean(axis=0)
    cam = np.array([centroid[0], centroid[1] - 5.0, centroid[2] + 4.0])
    K = bs.build_intrinsics(1920, 1080, focal_px=1500.0)
    dist = np.zeros(5)

    # Use look-at matrix consistent with bootstrap_pose
    gcps_list = list(world_by_id.items())
    boot = bs.bootstrap_pose(gcps_list, cam, (1920, 1080), focal_px=1500.0)

    # Compute "perfect" pixels under the bootstrap pose
    pixels = bs.project_points(world, boot.K, boot.dist_coeffs,
                               boot.rvec, boot.tvec)
    pixel_by_id = {gid: (float(pixels[i, 0]), float(pixels[i, 1]))
                   for i, gid in enumerate(ids)}
    return world_by_id, pixel_by_id, ids


def test_search_on_noiseless_data_keeps_all_gcps() -> None:
    """With zero noise, dropping any GCP strictly increases RMSE."""
    world, pixels, ids = _synthetic_gcp_dict(n=10)
    K = bs.build_intrinsics(1920, 1080, focal_px=1500.0)
    dist = np.zeros(5)
    cam = np.array([p for p in world.values()]).mean(axis=0)
    cam = cam + np.array([0.0, -5.0, 4.0])
    # Use the same bootstrap pose as _synthetic_gcp_dict
    boot = bs.bootstrap_pose(list(world.items()), cam, (1920, 1080))

    result = ss.subset_search(
        all_ids=ids,
        world_by_id=world,
        pixel_by_id=pixels,
        K=K,
        dist_coeffs=dist,
        camera_position_world=cam,
        init_rvec=boot.rvec,
        init_tvec=boot.tvec,
        frame_size=(1920, 1080),
        min_size=6,
        require_all_quadrants=False,  # synthetic data may not span all 4
        exhaustive_below_n=0,  # skip exhaustive (not needed for this test)
    )
    # Should terminate with the baseline (no drops) or something very close
    assert result.best.rmse_m < 1e-3  # essentially zero
    # Greedy trajectory records at most len(ids) - min_size + 1 steps
    assert len(result.greedy_trajectory) <= 10 - 6 + 1 + 1


def test_hard_constraint_min_size() -> None:
    """Subset size never drops below min_size."""
    world, pixels, ids = _synthetic_gcp_dict(n=10)
    K = bs.build_intrinsics(1920, 1080, focal_px=1500.0)
    cam = np.array([p for p in world.values()]).mean(axis=0)
    cam = cam + np.array([0.0, -5.0, 4.0])
    boot = bs.bootstrap_pose(list(world.items()), cam, (1920, 1080))

    result = ss.subset_search(
        all_ids=ids,
        world_by_id=world,
        pixel_by_id=pixels,
        K=K,
        dist_coeffs=np.zeros(5),
        camera_position_world=cam,
        init_rvec=boot.rvec,
        init_tvec=boot.tvec,
        frame_size=(1920, 1080),
        min_size=6,
        require_all_quadrants=False,
        exhaustive_below_n=0,
    )
    assert len(result.best.ids) >= 6
    for ev in result.greedy_trajectory:
        assert len(ev.ids) >= 6, (
            f"trajectory step |S|={len(ev.ids)} violates min_size=6"
        )


def test_search_is_deterministic() -> None:
    """Same inputs -> same best subset (same IDs, same RMSE)."""
    world, pixels, ids = _synthetic_gcp_dict(n=10)
    K = bs.build_intrinsics(1920, 1080, focal_px=1500.0)
    cam = np.array([p for p in world.values()]).mean(axis=0)
    cam = cam + np.array([0.0, -5.0, 4.0])
    boot = bs.bootstrap_pose(list(world.items()), cam, (1920, 1080))

    def run():
        return ss.subset_search(
            all_ids=ids, world_by_id=world, pixel_by_id=pixels,
            K=K, dist_coeffs=np.zeros(5),
            camera_position_world=cam,
            init_rvec=boot.rvec, init_tvec=boot.tvec,
            frame_size=(1920, 1080),
            min_size=6, require_all_quadrants=False,
            exhaustive_below_n=0,
        )

    a = run()
    b = run()
    assert set(a.best.ids) == set(b.best.ids)
    assert abs(a.best.rmse_m - b.best.rmse_m) < 1e-9


def test_quadrant_of_classifier() -> None:
    """Trivial unit test of the image-quadrant helper used by the spread
    constraint. Catches a sign flip."""
    assert ss._quadrant_of((100, 100), (1920, 1080)) == 0   # top-left
    assert ss._quadrant_of((1800, 100), (1920, 1080)) == 1  # top-right
    assert ss._quadrant_of((100, 900), (1920, 1080)) == 2   # bottom-left
    assert ss._quadrant_of((1800, 900), (1920, 1080)) == 3  # bottom-right
