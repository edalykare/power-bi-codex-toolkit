"""Offline PBIP/PBIR structure checks, deliberately not JSON Schema validation."""

import json
import re
from pathlib import Path, PureWindowsPath

from .diagnostics import Diagnostic, files_under, read_text

JSON_SUFFIXES = {".json", ".pbip", ".pbir", ".pbism"}


def load_json(path: Path):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError(f"Duplicate JSON key {key!r} in {path}")
            obj[key] = value
        return obj

    def invalid(value):
        raise ValueError(f"Invalid JSON constant {value!r} in {path}")

    return json.loads(read_text(path), object_pairs_hook=unique, parse_constant=invalid)


def local_target(base: Path, value: str, boundary: Path) -> Path:
    """Resolve portable local references, rejecting absolute and escaping paths."""
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ValueError("Expected a nonempty local path.")
    windows = PureWindowsPath(value)
    normalized = value.replace("\\", "/")
    if windows.drive or normalized.startswith("/"):
        raise ValueError("Absolute paths are not portable project references.")
    target = (base / normalized).resolve()
    if not target.is_relative_to(boundary.resolve()):
        raise ValueError(
            "Reference escapes the validation root; select the containing project directory."
        )
    # Reject symlink references even if their resolved destination is inside the root.
    candidate = base / normalized
    if any(p.is_symlink() for p in [candidate, *candidate.parents] if p != boundary.parent):
        raise ValueError("Symlink project references are not supported.")
    return target


def validate_project(root: Path) -> list[Diagnostic]:
    paths = files_under(root, JSON_SUFFIXES)
    boundary = root.parent if root.is_file() else root
    issues: list[Diagnostic] = []
    objects: dict[Path, dict] = {}

    def add(code: str, severity: str, p: Path, message: str) -> None:
        issues.append(Diagnostic(code, severity, str(p), 1, message))

    for path in paths:
        try:
            data = load_json(path)
            if not isinstance(data, dict):
                if path.suffix != ".json" or path.name in {
                    "visual.json",
                    "page.json",
                    "report.json",
                    "pages.json",
                    "version.json",
                }:
                    add("JSON002", "error", path, "Expected a JSON object.")
                continue
            objects[path.resolve()] = data
        except (ValueError, UnicodeError, OSError) as exc:
            add("JSON001", "error", path, str(exc))

    def reference(p: Path, value, required_file: str | None = None) -> None:
        try:
            target = local_target(p.parent, value, boundary)
            if not target.is_dir():
                add("PATH001", "error", p, f"Referenced directory does not exist: {value}")
            elif required_file and not (target / required_file).is_file():
                add("PATH002", "error", p, f"Referenced directory lacks {required_file}: {value}")
        except ValueError as exc:
            add("PATH003", "error", p, str(exc))

    for p, data in objects.items():
        if "$schema" in data:
            if not isinstance(data["$schema"], str) or not data["$schema"].startswith("https://"):
                add(
                    "JSON101",
                    "warning",
                    p,
                    "$schema should be an HTTPS URL; schemas are not fetched by this checker.",
                )
        if p.suffix == ".pbip":
            artifacts = data.get("artifacts")
            if not isinstance(artifacts, list) or not artifacts:
                add("PBIP001", "error", p, "PBIP must contain a nonempty artifacts array.")
            else:
                for artifact in artifacts:
                    report = artifact.get("report") if isinstance(artifact, dict) else None
                    if not isinstance(report, dict):
                        add("PBIP002", "error", p, "Expected an artifact.report object.")
                    else:
                        reference(p, report.get("path"), "definition.pbir")
        if p.name == "definition.pbir":
            binding = data.get("datasetReference")
            if not isinstance(binding, dict) or len(set(binding) & {"byPath", "byConnection"}) != 1:
                add(
                    "PBIR001",
                    "error",
                    p,
                    "Expected exactly one datasetReference.byPath or byConnection.",
                )
            elif "byPath" in binding:
                by_path = binding["byPath"]
                reference(
                    p,
                    by_path.get("path") if isinstance(by_path, dict) else None,
                    "definition.pbism",
                )
            else:
                add(
                    "PBIR900",
                    "info",
                    p,
                    "Remote byConnection binding was not authenticated or resolved.",
                )
            if not (p.parent / "definition").is_dir():
                add(
                    "PBIR901",
                    "info",
                    p,
                    "Enhanced PBIR definition absent; legacy report content is not inspected.",
                )
        if p.name == "pages.json" and p.parent.name == "pages":
            order = data.get("pageOrder")
            if not isinstance(order, list) or any(not isinstance(v, str) for v in order):
                add("PBIR002", "error", p, "pageOrder must be an array of page identifiers.")
            elif len(order) != len(set(order)):
                add("PBIR003", "error", p, "Duplicate page identifier in pageOrder.")
            else:
                for page in order:
                    if (
                        not re.fullmatch(r"[A-Za-z0-9_-]+", page)
                        or not (p.parent / page / "page.json").is_file()
                    ):
                        add("PBIR004", "error", p, f"Missing or invalid page: {page!r}.")
                active = data.get("activePageName")
                if active is not None and active not in order:
                    add("PBIR005", "error", p, "activePageName is not in pageOrder.")
                actual = {x.parent.name for x in p.parent.glob("*/page.json") if not x.is_symlink()}
                if actual - set(order):
                    add("PBIR106", "warning", p, "Some page folders are absent from pageOrder.")
        if p.name in {"page.json", "visual.json"}:
            if data.get("name") != p.parent.name:
                add("PBIR006", "error", p, "name must match the containing folder identifier.")
        if p.name == "page.json":
            for key in ("width", "height"):
                if (
                    not isinstance(data.get(key), (int, float))
                    or isinstance(data.get(key), bool)
                    or data[key] <= 0
                ):
                    add("PBIR007", "error", p, f"Page {key} must be positive.")
        if p.name == "visual.json":
            pos = data.get("position", {})
            if not isinstance(pos, dict) or any(
                not isinstance(pos.get(k), (int, float)) or isinstance(pos.get(k), bool)
                for k in ("x", "y", "z", "width", "height")
            ):
                add(
                    "PBIR008",
                    "error",
                    p,
                    "Visual position needs numeric x, y, z, width and height.",
                )
            elif pos["width"] <= 0 or pos["height"] <= 0:
                add("PBIR009", "error", p, "Visual dimensions must be positive.")
    return issues
