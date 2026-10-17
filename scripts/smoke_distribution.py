#!/usr/bin/env python3
"""Offline acceptance checks for a locally built source distribution and wheel."""

import argparse
import os
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(argv: list[str], cwd: Path) -> str:
    environment = {k: v for k, v in os.environ.items() if k not in {"PYTHONPATH", "PYTHONHOME"}}
    result = subprocess.run(argv, cwd=cwd, env=environment, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"Command failed: {argv}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=ROOT / "dist")
    args = parser.parse_args(argv)
    wheels = sorted(args.dist.glob("*.whl"))
    sources = sorted(args.dist.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sources) != 1:
        parser.error("Expected exactly one built wheel and one .tar.gz source distribution.")
    with tempfile.TemporaryDirectory(prefix="pbi-codex-distribution-") as temporary:
        base = Path(temporary).resolve()
        extracted = base / "source"
        extracted.mkdir()
        with tarfile.open(sources[0]) as archive:
            for member in archive.getmembers():
                target = (extracted / member.name).resolve()
                if not target.is_relative_to(extracted):
                    raise ValueError("Source archive contains an escaping path.")
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    stream = archive.extractfile(member)
                    if stream is None:
                        raise ValueError("Could not read source archive member.")
                    with stream:
                        target.write_bytes(stream.read())
                else:
                    raise ValueError("Source archive contains a nonregular file.")
        source = next(extracted.iterdir())
        if len(list((source / ".agents" / "skills").glob("*/SKILL.md"))) != 9:
            raise ValueError("Source distribution lacks the skill collection.")
        for path in (
            "LICENSE",
            "ATTRIBUTIONS.md",
            "vendor/microsoft-json-schemas/LICENSE",
            ".codex/agents/model-reviewer.toml",
            "scripts/install_skills.py",
        ):
            if not (source / path).is_file():
                raise ValueError(f"Source distribution lacks {path}.")
        run([sys.executable, "-S", str(source / "scripts" / "check_repo.py")], base)
        run(
            [
                sys.executable,
                "-S",
                str(source / "scripts" / "pbi.py"),
                "check",
                str(source / "examples" / "retail"),
                "--strict",
            ],
            base,
        )
        installed = base / "skills"
        run(
            [
                sys.executable,
                "-S",
                str(source / "scripts" / "install_skills.py"),
                "dax-expert",
                "--dest",
                str(installed),
            ],
            base,
        )
        run(
            [
                sys.executable,
                "-I",
                str(installed / "dax-expert" / "scripts" / "pbi.py"),
                "check",
                str(source / "examples" / "retail"),
                "--strict",
            ],
            base,
        )
        with zipfile.ZipFile(wheels[0]) as wheel:
            if not any(p.endswith("/licenses/LICENSE") for p in wheel.namelist()):
                raise ValueError("Wheel license is missing.")
        venv = base / "venv"
        run([sys.executable, "-m", "venv", str(venv)], base)
        bindir = venv / ("Scripts" if os.name == "nt" else "bin")
        python = bindir / ("python.exe" if os.name == "nt" else "python")
        cli = bindir / ("pbi-codex.exe" if os.name == "nt" else "pbi-codex")
        run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--no-index",
                "--no-deps",
                str(wheels[0].resolve()),
            ],
            base,
        )
        run([str(cli), "check", str(source / "examples" / "retail"), "--strict"], base)
        run(
            [str(python), "-m", "pbi_codex", "dax", str(source / "examples" / "dax"), "--strict"],
            base,
        )
    print(
        "Distribution smoke checks passed: source contents, independent skill, wheel install and CLI; no network used."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
