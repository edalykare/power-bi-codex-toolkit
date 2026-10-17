"""Tests use only the standard library; schema tests additionally use dev extras."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
