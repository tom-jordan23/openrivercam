"""Tests for CameraConfig emission + pyorc round-trip + cert sidecar."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import sys
_SURVEY_DIR = Path(__file__).resolve().parent.parent
if str(_SURVEY_DIR) not in sys.path:
    sys.path.insert(0, str(_SURVEY_DIR))

import orc_auto_fit as driver  # noqa: E402
from auto_fit import bootstrap as bs  # noqa: E402


def _minimal_fit_inputs():
    """6 GCPs spanning 4 image quadrants, with pixels computed from a
    known pose so the fit is exactly satisfiable."""
    world_by_id = {
        "G1": np.array([714115.0, 9234415.0, 620.0]),
        "G2": np.array([714125.0, 9234415.0, 620.0]),
        "G3": np.array([714115.0, 9234405.0, 620.0]),
        "G4": np.array([714125.0, 9234405.0, 620.0]),
        "G5": np.array([714120.0, 9234410.0, 620.0]),
        "G6": np.array([714118.0, 9234412.0, 620.0]),
    }
    centroid = np.array(list(world_by_id.values())).mean(axis=0)
    camera_xyz = centroid + np.array([0.0, -5.0, 4.0])

    K = bs.build_intrinsics(1920, 1080, focal_px=1500.0)
    dist = np.zeros(5)
    boot = bs.bootstrap_pose(
        list(world_by_id.items()), camera_xyz, (1920, 1080)
    )
    world = np.array([world_by_id[g] for g in world_by_id])
    projected = bs.project_points(world, boot.K, boot.dist_coeffs,
                                  boot.rvec, boot.tvec)
    pixel_by_id = {
        gid: (float(projected[i, 0]), float(projected[i, 1]))
        for i, gid in enumerate(world_by_id)
    }
    return world_by_id, pixel_by_id, K, dist, camera_xyz


def test_emit_produces_valid_pyorc_json(tmp_path: Path) -> None:
    world, pixels, K, dist, cam = _minimal_fit_inputs()
    out = tmp_path / "test_auto_fit.json"
    info = driver.emit_camera_config(
        output_path=out,
        subset_ids=list(world.keys()),
        pixel_by_id=pixels,
        world_by_id=world,
        K=K,
        dist_coeffs=dist,
        camera_xyz=cam,
        z_0=617.0,
        frame_width=1920,
        frame_height=1080,
        crs="EPSG:32748",
        certification_status="ok",
    )
    assert out.exists()
    assert info["roundtrip_ok"], f"roundtrip failed: {info['roundtrip_mismatches']}"
    # Main JSON should be pure pyorc-loadable — no certification metadata
    # at top level (that lives in the sidecar, see test_emit_creates_cert_sidecar)
    data = json.loads(out.read_text())
    assert data["height"] == 1080
    assert data["width"] == 1920
    assert data["gcps"]["z_0"] == 617.0
    assert len(data["gcps"]["src"]) == 6
    assert "certification_status" not in data, (
        "certification_status must NOT be in the main pyorc JSON — "
        "pyorc.load_camera_config rejects unknown top-level kwargs. "
        "Use the _cert.json sidecar instead."
    )
    assert "resolvability_note" not in data


def test_emit_creates_cert_sidecar(tmp_path: Path) -> None:
    world, pixels, K, dist, cam = _minimal_fit_inputs()
    out = tmp_path / "test_auto_fit.json"
    driver.emit_camera_config(
        output_path=out,
        subset_ids=list(world.keys()),
        pixel_by_id=pixels, world_by_id=world,
        K=K, dist_coeffs=dist, camera_xyz=cam,
        z_0=617.0, frame_width=1920, frame_height=1080,
        crs="EPSG:32748",
        certification_status="ok",
    )
    cert_path = out.parent / (out.stem + "_cert.json")
    assert cert_path.exists()
    cert = json.loads(cert_path.read_text())
    assert cert["certification_status"] == "ok"
    assert cert["camera_config_file"] == out.name


def test_emit_demo_mode_records_resolvability_note(tmp_path: Path) -> None:
    world, pixels, K, dist, cam = _minimal_fit_inputs()
    out = tmp_path / "test_auto_fit_DEMO_UNCERTIFIED.json"
    note = "unit test — pretending the fit failed the quality gate"
    driver.emit_camera_config(
        output_path=out,
        subset_ids=list(world.keys()),
        pixel_by_id=pixels, world_by_id=world,
        K=K, dist_coeffs=dist, camera_xyz=cam,
        z_0=617.0, frame_width=1920, frame_height=1080,
        crs="EPSG:32748",
        certification_status="demo-only",
        resolvability_note=note,
    )
    # Main JSON stays pyorc-pure; certification_status + note live in the sidecar
    data = json.loads(out.read_text())
    assert "certification_status" not in data
    assert "resolvability_note" not in data

    cert_path = out.parent / (out.stem + "_cert.json")
    cert = json.loads(cert_path.read_text())
    assert cert["certification_status"] == "demo-only"
    assert cert["resolvability_note"] == note


def test_dist_coeffs_shape_is_5_by_1_for_orc_os(tmp_path: Path) -> None:
    """Regression test: ORC-OS's pydantic schema indexes dist_coeffs[i][0].
    Emitting as 1×5 row makes ORC-OS crash with IndexError. We emit 5×1.
    """
    world, pixels, K, dist, cam = _minimal_fit_inputs()
    out = tmp_path / "shape_check.json"
    driver.emit_camera_config(
        output_path=out,
        subset_ids=list(world.keys()),
        pixel_by_id=pixels, world_by_id=world,
        K=K, dist_coeffs=dist, camera_xyz=cam,
        z_0=617.0, frame_width=1920, frame_height=1080,
        crs="EPSG:32748",
    )
    data = json.loads(out.read_text())
    dc = data["dist_coeffs"]
    # Must be 5 rows, each a single-element list
    assert len(dc) == 5, f"expected 5 rows, got {len(dc)}"
    for row in dc:
        assert isinstance(row, list) and len(row) == 1
