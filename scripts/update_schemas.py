#!/usr/bin/env python3
"""Vendor demo schema roots and their $ref closure from a reviewed local Microsoft clone.

No network access. This script changes vendor files only when explicitly invoked.
"""

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urldefrag, urljoin

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "https://developer.microsoft.com/json-schemas/"


def refs(value):
    if isinstance(value, dict):
        if isinstance(value.get("$ref"), str):
            yield value["$ref"]
        for child in value.values():
            yield from refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from refs(child)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("clone", type=Path, help="Local checkout of microsoft/json-schemas")
    args = p.parse_args()
    source = args.clone.resolve()
    commit = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
    ).stdout.strip()
    roots = set()
    for path in (ROOT / "examples" / "retail").rglob("*"):
        if path.is_file() and path.suffix in {".json", ".pbip", ".pbir", ".pbism"}:
            schema = json.loads(path.read_text()).get("$schema")
            if schema:
                roots.add(schema)
    todo, schemas = list(roots), {}
    while todo:
        uri = urldefrag(todo.pop())[0]
        if uri in schemas:
            continue
        if not uri.startswith(PREFIX):
            raise ValueError(f"Unsupported external schema reference: {uri}")
        relative = uri.removeprefix(PREFIX)
        path = (source / relative).resolve()
        if not path.is_relative_to(source):
            raise ValueError("Schema reference escaped the clone.")
        raw = path.read_bytes()
        data = json.loads(raw)
        schemas[uri] = (relative, raw)
        todo.extend(urljoin(uri, ref) for ref in refs(data) if not ref.startswith("#"))
    destination = ROOT / "vendor" / "microsoft-json-schemas"
    destination.mkdir(parents=True, exist_ok=True)
    files = []
    for uri, (relative, raw) in sorted(schemas.items()):
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        files.append({"uri": uri, "path": relative, "sha256": hashlib.sha256(raw).hexdigest()})
    shutil.copy2(source / "LICENSE", destination / "LICENSE")
    manifest = {
        "repository": "https://github.com/microsoft/json-schemas",
        "commit": commit,
        "roots": sorted(roots),
        "files": files,
    }
    (destination / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Vendored {len(files)} schema files from {commit}. Review the diff and remove obsolete files manually."
    )


if __name__ == "__main__":
    main()
