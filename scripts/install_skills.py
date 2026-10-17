#!/usr/bin/env python3
"""Install selected self-contained skills; never alter existing skill folders."""

import argparse
import json
import shutil
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
INSTALLED_LAUNCHER = '''#!/usr/bin/env python3
"""Use the helper source bundled with this installed skill."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".toolkit"))
from pbi_codex.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
'''


def install(names: list[str], destination: Path) -> list[Path]:
    available = {p.name for p in SKILLS.iterdir() if (p / "SKILL.md").is_file()}
    if not names or len(names) != len(set(names)) or set(names) - available:
        raise ValueError("Select unique skill names from --list, or use --all.")
    if any(p.is_symlink() for p in [destination, *destination.parents]):
        raise ValueError("Installation destination must not contain symlink components.")
    destination = destination.resolve()
    if destination == SKILLS.resolve() or destination.is_relative_to(SKILLS.resolve()):
        raise ValueError("Use skills in place when working in this toolkit checkout.")
    for name in names:
        if (destination / name).exists() or (destination / name).is_symlink():
            raise FileExistsError(f"Skill already exists (not overwritten): {destination / name}")
        source = SKILLS / name
        if source.is_symlink() or any(p.is_symlink() for p in source.rglob("*")):
            raise ValueError(f"Symlink in skill source: {name}")
    destination.mkdir(parents=True, exist_ok=True)
    installed = []
    with tempfile.TemporaryDirectory(prefix=".pbi-codex-install-", dir=destination) as temporary:
        stage = Path(temporary)
        for name in names:
            source = SKILLS / name
            target = stage / name
            shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            package = target / ".toolkit" / "pbi_codex"
            shutil.copytree(
                ROOT / "src" / "pbi_codex",
                package,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            (target / "scripts" / "pbi.py").write_text(INSTALLED_LAUNCHER, encoding="utf-8")
            for notice in ("LICENSE", "ATTRIBUTIONS.md"):
                shutil.copy2(ROOT / notice, target / notice)
            (target / ".toolkit" / "installation.json").write_text(
                json.dumps(
                    {
                        "toolkitVersion": tomllib.loads(
                            (ROOT / "pyproject.toml").read_text(encoding="utf-8")
                        )["project"]["version"],
                        "skill": name,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        # Stage the complete selection before making any installed skill visible.
        for name in names:
            target = destination / name
            if target.exists() or target.is_symlink():
                raise FileExistsError(f"Destination appeared during install: {target}")
            (stage / name).rename(target)
            installed.append(target)
    return installed


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("skills", nargs="*")
    p.add_argument("--list", action="store_true")
    p.add_argument("--all", action="store_true")
    scope = p.add_mutually_exclusive_group()
    scope.add_argument(
        "--project", type=Path, help="Target project root; installs into .agents/skills"
    )
    scope.add_argument("--user", action="store_true", help="Install into ~/.agents/skills")
    scope.add_argument("--dest", type=Path, help="Explicit skill parent directory")
    args = p.parse_args(argv)
    available = sorted(p.name for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())
    if args.list:
        print("\n".join(available))
        return 0
    if args.all and args.skills:
        p.error("Choose --all or specific skill names.")
    if not (args.project or args.user or args.dest):
        p.error("Choose --project PATH, --user, or --dest PATH.")
    destination = (
        args.project / ".agents" / "skills"
        if args.project
        else Path.home() / ".agents" / "skills"
        if args.user
        else args.dest
    )
    try:
        for target in install(available if args.all else args.skills, destination):
            print(f"Installed {target}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"Installation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
