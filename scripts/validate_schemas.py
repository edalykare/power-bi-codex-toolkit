#!/usr/bin/env python3
"""Validate PBIP/PBIR JSON using pinned local schemas. Never fetch remote schemas."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pbi_codex.diagnostics import files_under  # noqa: E402
from pbi_codex.project import JSON_SUFFIXES, load_json  # noqa: E402


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("path", nargs="?", type=Path, default=ROOT / "examples" / "retail")
    args = p.parse_args(argv)
    try:
        from jsonschema.validators import validator_for
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT7
    except ImportError:
        print(
            'Install development dependencies: python -m pip install -e ".[dev]"', file=sys.stderr
        )
        return 2
    try:
        base = ROOT / "vendor" / "microsoft-json-schemas"
        manifest = load_json(base / "manifest.json")
        resources, schemas = [], {}
        for entry in manifest["files"]:
            raw = (base / entry["path"]).read_bytes()
            if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
                raise ValueError(f"Schema integrity mismatch: {entry['path']}")
            data = json.loads(raw)
            schemas[entry["uri"]] = data
            resources.append(
                (entry["uri"], Resource.from_contents(data, default_specification=DRAFT7))
            )
        registry = Registry().with_resources(resources)
        failures, checked = [], 0
        for path in files_under(args.path, JSON_SUFFIXES):
            data = load_json(path)
            if not isinstance(data, dict) or "$schema" not in data:
                continue
            uri = data["$schema"]
            if uri not in schemas:
                raise ValueError(f"Schema is not vendored (no network request made): {uri}")
            schema = schemas[uri]
            cls = validator_for(schema)
            cls.check_schema(schema)
            validator = cls(schema, registry=registry)
            for error in validator.iter_errors(data):
                location = "/".join(str(v) for v in error.absolute_path) or "<root>"
                failures.append(f"{path}:{location}: {error.message}")
            checked += 1
        if not checked:
            raise ValueError("No schema-bearing JSON files found.")
        print(
            "\n".join(failures)
            if failures
            else f"Microsoft JSON Schema validation: {checked} file(s), 0 errors; network disabled."
        )
        return int(bool(failures))
    except (OSError, ValueError) as exc:
        print(f"Schema validation error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
