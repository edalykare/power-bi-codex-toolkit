"""Documentation, environment discovery, timing summaries, and offline Fabric plans."""

import hashlib
import math
import platform
import shutil
import statistics
import sys
from collections import Counter
from pathlib import Path

from .diagnostics import files_under, read_text
from .project import load_json, local_target
from .tmdl import Object


def markdown_cell(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace("|", "&#124;")
        .replace("\n", "<br>")
    )


def model_documentation(objects: list[Object]) -> str:
    lines = [
        "# Semantic model inventory",
        "",
        "Generated from local TMDL metadata. Expressions were not executed.",
        "",
        "| Kind | Table | Name | Description | Format |",
        "| --- | --- | --- | --- | --- |",
    ]
    for o in sorted(objects, key=lambda x: (x.table_name or "", x.kind, x.name)):
        if o.kind not in {"table", "column", "measure", "relationship"}:
            continue
        values = [
            o.kind,
            o.table_name or "",
            o.name,
            o.description or o.properties.get("description", ""),
            o.properties.get("formatString", ""),
        ]
        lines.append("| " + " | ".join(markdown_cell(v) for v in values) + " |")
    lines.extend(["", "## Relationships", ""])
    for o in objects:
        if o.kind == "relationship":
            lines.append(
                f"- {markdown_cell(o.name)}: {markdown_cell(o.properties.get('fromColumn', '?'))} → "
                f"{markdown_cell(o.properties.get('toColumn', '?'))}; "
                f"filter={markdown_cell(o.properties.get('crossFilteringBehavior', 'oneDirection (default)'))}."
            )
    return "\n".join(lines) + "\n"


def inventory(objects: list[Object]) -> dict:
    return {
        "counts": dict(sorted(Counter(o.kind for o in objects).items())),
        "objects": [o.to_dict() for o in objects],
        "validationLevel": "static-inventory-only",
    }


def doctor() -> dict:
    # Existence checks only: never launch third-party tools or trigger login.
    # platform.system() can spawn a shell on Windows/Python 3.11; use interpreter metadata.
    system = {"win32": "Windows", "darwin": "Darwin", "linux": "Linux"}.get(
        sys.platform, sys.platform
    )
    return {
        "python": platform.python_version(),
        "platform": system,
        "tools": {
            name: shutil.which(name)
            for name in ("git", "codex", "fab", "node", "npx", "dotnet", "TabularEditor")
        },
        "checks": "Executable discovery only; no authentication, server startup, or engine validation.",
    }


def fabric_plan(manifest: Path) -> dict:
    data = load_json(manifest)
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("Fabric manifest must be an object with version: 1.")
    workspace = data.get("workspace")
    if (
        not isinstance(workspace, str)
        or not workspace.strip()
        or any(c in workspace for c in "/\\\r\n")
    ):
        raise ValueError(
            "workspace must be a nonempty workspace name or ID without path separators."
        )
    items = data.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("items must be a nonempty array.")
    actions, seen = [], set()
    supported = {
        "Lakehouse",
        "Warehouse",
        "Notebook",
        "DataPipeline",
        "Dataflow",
        "SemanticModel",
        "Report",
    }
    for item in items:
        if not isinstance(item, dict) or item.get("type") not in supported:
            raise ValueError(f"Item type must be one of: {', '.join(sorted(supported))}")
        name = item.get("name")
        if not isinstance(name, str) or not name.strip() or any(c in name for c in "/\\\r\n"):
            raise ValueError("Each item needs a name without path separators.")
        key = (name.casefold(), item["type"])
        if key in seen:
            raise ValueError(f"Duplicate Fabric target: {name}.{item['type']}")
        seen.add(key)
        source = local_target(manifest.parent, item.get("source"), manifest.parent)
        paths = files_under(
            source, {".json", ".tmdl", ".py", ".sql", ".ipynb", ".pbir", ".pbism", ".csv"}
        )
        if not paths:
            raise ValueError(f"No supported local definition files found: {source}")
        digests = []
        for path in paths:
            # Use the same size and encoding checks as other commands before hashing bytes.
            read_text(path)
            digests.append(
                {
                    "path": str(path.relative_to(manifest.parent.resolve())),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
            )
        actions.append(
            {
                "operation": "review-item-definition",
                "name": name,
                "type": item["type"],
                "source": str(source.relative_to(manifest.parent.resolve())),
                "files": digests,
            }
        )
    return {
        "version": 1,
        "status": "proposed",
        "workspace": workspace,
        "actions": actions,
        "remoteOperationsExecuted": False,
        "requiresExplicitAuthorization": True,
        "unverified": [
            "Workspace identity and permissions",
            "Item-specific import API and definition format",
            "Dependencies, connection bindings, capacity and licensing",
            "Remote diff and rollback",
        ],
    }


def compare_timings(path: Path) -> dict:
    data = load_json(path)
    if (
        not isinstance(data, dict)
        or data.get("version") != 1
        or not isinstance(data.get("cases"), list)
        or not data["cases"]
    ):
        raise ValueError(
            "Expected version: 1 and a nonempty cases array (see examples/performance)."
        )
    output, names = [], set()
    for case in data["cases"]:
        if (
            not isinstance(case, dict)
            or not isinstance(case.get("name"), str)
            or not case["name"].strip()
        ):
            raise ValueError("Each timing case needs a nonempty name.")
        if case["name"] in names:
            raise ValueError("Timing case names must be unique.")
        names.add(case["name"])
        medians = {}
        for key in ("baselineMs", "candidateMs"):
            values = case.get(key)
            if (
                not isinstance(values, list)
                or len(values) < 3
                or any(
                    not isinstance(x, (int, float))
                    or isinstance(x, bool)
                    or not math.isfinite(x)
                    or x <= 0
                    for x in values
                )
            ):
                raise ValueError(f"{key} needs at least three positive finite numeric samples.")
            medians[key] = statistics.median(values)
        base, candidate = medians["baselineMs"], medians["candidateMs"]
        output.append(
            {
                "name": case["name"],
                "baselineMedianMs": base,
                "candidateMedianMs": candidate,
                "changePercent": round((candidate / base - 1) * 100, 2),
                "baselineSamples": len(case["baselineMs"]),
                "candidateSamples": len(case["candidateMs"]),
            }
        )
    return {
        "cases": output,
        "interpretation": "Descriptive medians only. Correctness, cache state, model version and workload equivalence must be verified separately.",
    }
