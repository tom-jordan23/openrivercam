"""Tests for the day-1/day-2 pair classifier.

This is the logic that saved us from the GCP1/GCP1.2 mislabel trap —
same-marker drift (legitimate RTK quality signal) vs different-marker
mislabel (just different points that got paired under `.2` suffix).
"""

from __future__ import annotations

import numpy as np

import sys
from pathlib import Path

_SURVEY_DIR = Path(__file__).resolve().parent.parent
if str(_SURVEY_DIR) not in sys.path:
    sys.path.insert(0, str(_SURVEY_DIR))

# orc_auto_fit is the driver module; classify_pairs is defined there
import orc_auto_fit as driver  # noqa: E402


def test_same_marker_pair_when_clicks_colocated() -> None:
    """Pair with clicks within 15 px threshold -> same_marker_drift."""
    world = {
        "A": np.array([714120.0, 9234410.0, 620.0]),
        "A.2": np.array([714120.3, 9234410.0, 620.0]),  # 30 cm UTM apart
    }
    pixels = {
        "A": (1000.0, 500.0),
        "A.2": (1002.0, 502.0),   # 2.8 px apart -> same marker
    }
    result = driver.classify_pairs(world, pixel_by_id=pixels)
    assert result["A"]["classification"] == "same_marker_drift"
    assert result["A.2"]["classification"] == "same_marker_drift"
    assert abs(result["A"]["utm_distance_m"] - 0.3) < 1e-6


def test_different_marker_pair_when_clicks_far_apart() -> None:
    """Pair with clicks > 15 px threshold -> different_markers.
    This is the GCP1 / GCP1.2 case we caught on the real data."""
    world = {
        "A": np.array([714120.0, 9234410.0, 620.0]),
        "A.2": np.array([714122.0, 9234410.0, 620.0]),  # 2 m UTM apart
    }
    pixels = {
        "A": (1240.0, 945.0),
        "A.2": (497.0, 341.0),    # 958 px apart -> different markers
    }
    result = driver.classify_pairs(world, pixel_by_id=pixels)
    assert result["A"]["classification"] == "different_markers"
    assert result["A.2"]["classification"] == "different_markers"


def test_unknown_classification_when_clicks_missing() -> None:
    """No click info -> classification is 'unknown' (not misclassified
    as same or different)."""
    world = {
        "A": np.array([714120.0, 9234410.0, 620.0]),
        "A.2": np.array([714120.1, 9234410.0, 620.0]),
    }
    result = driver.classify_pairs(world, pixel_by_id=None)
    assert result["A"]["classification"] == "unknown"
    assert result["A.2"]["classification"] == "unknown"


def test_orphan_pair_returns_nothing() -> None:
    """`.2` label with no day-1 partner -> not in the classification result."""
    world = {
        "Orphan.2": np.array([714120.0, 9234410.0, 620.0]),
    }
    result = driver.classify_pairs(world, pixel_by_id={"Orphan.2": (100.0, 100.0)})
    assert "Orphan.2" not in result


def test_non_pair_keys_ignored() -> None:
    """Day-1 GCP without a day-2 re-shoot -> not in the classification."""
    world = {
        "GCP_solo": np.array([714120.0, 9234410.0, 620.0]),
        "Other": np.array([714121.0, 9234410.0, 620.0]),
    }
    result = driver.classify_pairs(world, pixel_by_id={})
    assert "GCP_solo" not in result
    assert "Other" not in result
