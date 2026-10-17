#!/usr/bin/env python3
"""Check this repository's constrained skill frontmatter, local links and TOML."""

import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", ".venv", "vendor", "artifacts", "dist", "build", "__pycache__"}


def check(root: Path = ROOT) -> list[str]:
    failures = []
    skills = sorted((root / ".agents" / "skills").glob("*/SKILL.md"))
    if not skills:
        failures.append("No Codex skills found.")
    for path in skills:
        text = path.read_text(encoding="utf-8")
        # This repo deliberately uses single-line scalar name/description fields.
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not match:
            failures.append(f"{path}: missing YAML frontmatter")
            continue
        metadata = {}
        for line in match[1].splitlines():
            key, sep, value = line.partition(":")
            if not sep or key in metadata:
                failures.append(f"{path}: malformed/duplicate frontmatter key")
            metadata[key] = value.strip()
        if metadata.get("name") != path.parent.name or not re.fullmatch(
            r"[a-z0-9]+(?:-[a-z0-9]+)*", metadata.get("name", "")
        ):
            failures.append(f"{path}: name must match the lowercase skill directory")
        if len(metadata.get("name", "")) > 64 or not metadata.get("description"):
            failures.append(f"{path}: invalid name/description")
        if len(text.splitlines()) > 150:
            failures.append(f"{path}: entry point exceeds the repository's 150-line budget")
        for required in ("Prerequisites", "Validation", "References"):
            if required not in text:
                failures.append(f"{path}: missing {required} guidance")
        if not (path.parent / "scripts" / "pbi.py").is_file():
            failures.append(f"{path}: helper missing")
    for path in root.rglob("*"):
        if any(
            part in IGNORED or part.endswith(".egg-info") for part in path.relative_to(root).parts
        ):
            continue
        if path.suffix == ".toml" and path.is_file():
            try:
                data = tomllib.loads(path.read_text(encoding="utf-8"))
                if path.parent == root / ".codex" / "agents":
                    if not all(
                        isinstance(data.get(k), str) and data[k]
                        for k in ("name", "description", "developer_instructions")
                    ):
                        failures.append(f"{path}: incomplete standalone custom agent")
                    if any(k in data for k in ("sandbox_mode", "approval_policy", "mcp_servers")):
                        failures.append(
                            f"{path}: custom agent cannot override parent permissions/MCP"
                        )
            except (ValueError, OSError) as exc:
                failures.append(f"{path}: {exc}")
        if path.suffix != ".md" or not path.is_file():
            continue
        for target in re.findall(
            r"(?<!!)\[[^\]]+\]\(([^\s)]+)\)", path.read_text(encoding="utf-8")
        ):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            local = unquote(target.split("#", 1)[0]).strip("<>")
            if local and not (path.parent / local).exists():
                failures.append(f"{path.relative_to(root)}: broken local link {target}")
    manifest_path = root / "vendor" / "microsoft-json-schemas" / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        for entry in manifest["files"]:
            path = manifest_path.parent / entry["path"]
            if (
                not path.exists()
                or hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]
            ):
                failures.append(f"Schema missing or modified: {entry['path']}")
    return failures


if __name__ == "__main__":
    failures = check()
    print(
        "\n".join(failures)
        if failures
        else "Repository checks passed (skills, local links, TOML, schema hashes)."
    )
    sys.exit(bool(failures))
