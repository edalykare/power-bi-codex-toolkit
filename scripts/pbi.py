#!/usr/bin/env python3
"""Run the toolkit directly from a checkout without installing dependencies."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pbi_codex.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
