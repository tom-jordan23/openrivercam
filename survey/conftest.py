"""Pytest conftest — makes `survey/` importable so tests can `from auto_fit import ...`.

Matches the path-setup pattern in `survey/orc_auto_fit.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SURVEY_DIR = Path(__file__).resolve().parent
if str(_SURVEY_DIR) not in sys.path:
    sys.path.insert(0, str(_SURVEY_DIR))
