"""Command line entry point: deterministic local checks, no remote writes."""

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .dax import lint_dax
from .diagnostics import Diagnostic, blocked, files_under, read_text
from .model import validate_model
from .operations import compare_timings, doctor, fabric_plan, inventory, model_documentation
from .project import JSON_SUFFIXES, validate_project
from .tmdl import load_model


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Offline Power BI checks; no DAX/TMDL execution or remote actions."
    )
    p.add_argument("--version", action="version", version=__version__)
    subs = p.add_subparsers(dest="command", required=True)
    for name, help_text in {
        "check": "Check PBIP/PBIR JSON and common TMDL model metadata",
        "dax": "Lexically lint .dax expressions or queries",
        "inventory": "Export TMDL object inventory as JSON",
        "docs": "Generate a Markdown model inventory",
        "fabric-plan": "Inventory local Fabric definitions for a proposed deployment review",
        "compare-timings": "Compare normalized baseline/candidate timing samples",
    }.items():
        sub = subs.add_parser(name, help=help_text)
        sub.add_argument("path", type=Path)
        sub.add_argument(
            "--output", type=Path, help="Write a local file; refuses to overwrite without --force"
        )
        sub.add_argument("--force", action="store_true", help="Allow overwriting the output file")
        if name in {"check", "dax"}:
            sub.add_argument("--format", choices=("text", "json"), default="text")
            sub.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    subs.add_parser("doctor", help="Discover optional executables without starting them")
    return p


def check(root: Path) -> tuple[list[Diagnostic], dict]:
    sources = files_under(root, JSON_SUFFIXES | {".tmdl"})
    if not sources:
        raise ValueError("No Power BI JSON or TMDL sources found in the validation root.")
    diagnostics = validate_project(root)
    tmdl_paths = [p for p in sources if p.suffix.lower() == ".tmdl"]
    # Scope object names by semantic model, not by the entire mono-repository.
    groups: dict[Path, list[Path]] = {}
    for path in tmdl_paths:
        definition = next((parent for parent in path.parents if parent.name == "definition"), None)
        scope = definition if definition else (root.parent if root.is_file() else root)
        groups.setdefault(scope, []).append(path)
    for scope in sorted(groups):
        _, found = validate_model(root if root.is_file() else scope)
        diagnostics.extend(found)
    return diagnostics, {
        "files": len(sources),
        "models": len(groups),
        "validationLevel": "static-structural",
        "engineValidation": "not-run",
        "jsonSchemaValidation": "not-run",
    }


def render_diagnostics(diagnostics: list[Diagnostic], summary: dict, fmt: str) -> str:
    diagnostics = sorted(diagnostics, key=lambda d: (d.path, d.line, d.code, d.message))
    if fmt == "json":
        return (
            json.dumps(
                {"summary": summary, "diagnostics": [d.to_dict() for d in diagnostics]}, indent=2
            )
            + "\n"
        )
    lines = [f"{d.path}:{d.line}: {d.severity} {d.code}: {d.message}" for d in diagnostics]
    errors = sum(d.severity == "error" for d in diagnostics)
    warnings = sum(d.severity == "warning" for d in diagnostics)
    lines.append(
        f"Static checks: {errors} error(s), {warnings} warning(s). Engine and JSON Schema validation: not run."
    )
    return "\n".join(lines) + "\n"


def emit(text: str, output: Path | None, force: bool) -> None:
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w" if force else "x", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
    else:
        sys.stdout.write(text)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "doctor":
            print(json.dumps(doctor(), indent=2))
            return 0
        # Keep relative project references consistent regardless of the current shell.
        if args.path.is_symlink():
            raise ValueError("Symlink input is not supported.")
        root = args.path.resolve()
        if not root.exists():
            raise ValueError(f"Input does not exist: {args.path}")
        result = 0
        if args.command in {"check", "dax"}:
            if args.command == "check":
                diagnostics, summary = check(root)
            else:
                paths = files_under(root, {".dax"})
                if not paths:
                    raise ValueError("No .dax files found.")
                diagnostics = [d for path in paths for d in lint_dax(read_text(path), str(path))]
                summary = {
                    "files": len(paths),
                    "validationLevel": "lexical-only",
                    "engineValidation": "not-run",
                }
            text = render_diagnostics(diagnostics, summary, args.format)
            result = int(blocked(diagnostics, args.strict))
        elif args.command in {"inventory", "docs"}:
            nodes, diagnostics = load_model(root)
            if blocked(diagnostics):
                sys.stderr.write(render_diagnostics(diagnostics, {}, "text"))
                return 1
            text = (
                model_documentation(nodes)
                if args.command == "docs"
                else json.dumps(
                    {**inventory(nodes), "diagnostics": [d.to_dict() for d in diagnostics]},
                    indent=2,
                )
                + "\n"
            )
        elif args.command == "fabric-plan":
            text = json.dumps(fabric_plan(root), indent=2) + "\n"
        else:
            text = json.dumps(compare_timings(root), indent=2) + "\n"
        emit(text, args.output, args.force)
        return result
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"Input/output error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
