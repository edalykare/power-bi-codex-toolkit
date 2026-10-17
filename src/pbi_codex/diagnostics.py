"""Stable machine-readable diagnostics and bounded local file discovery."""

from dataclasses import asdict, dataclass
from pathlib import Path

MAX_FILE_BYTES = 10 * 1024 * 1024
IGNORED = {".git", ".pbi", ".venv", "node_modules", "__pycache__", "artifacts"}


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: str
    path: str
    line: int
    message: str

    def to_dict(self) -> dict:
        return asdict(self)


def files_under(root: Path, suffixes: set[str]) -> list[Path]:
    """Do not follow symlinks, caches, or paths outside the requested tree."""
    if root.is_symlink():
        raise ValueError(f"Symlink input is not supported: {root}")
    if not root.exists():
        raise ValueError(f"Input does not exist: {root}")
    if root.is_file():
        if root.suffix.lower() not in suffixes:
            raise ValueError(f"Unsupported file extension: {root.suffix}")
        return [root]
    import os

    found = []
    for base, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED and not (Path(base) / d).is_symlink())
        for name in sorted(names):
            p = Path(base) / name
            if p.suffix.lower() in suffixes and not p.is_symlink():
                found.append(p)
    return sorted(found)


def read_text(path: Path) -> str:
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError(f"File exceeds {MAX_FILE_BYTES} byte limit: {path}")
    return path.read_text(encoding="utf-8-sig")


def blocked(diagnostics: list[Diagnostic], strict: bool = False) -> bool:
    return any(d.severity == "error" or (strict and d.severity == "warning") for d in diagnostics)
