#!/usr/bin/env python3
"""Resolve the checkout or the self-contained installed toolkit bundle."""
import sys
from pathlib import Path

skill = Path(__file__).resolve().parents[1]
bundle = skill / ".toolkit"
source = Path(__file__).resolve().parents[4] / "src"
if (bundle / "pbi_codex").is_dir():
    sys.path.insert(0, str(bundle))
elif (source / "pbi_codex").is_dir():
    sys.path.insert(0, str(source))

from pbi_codex.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
