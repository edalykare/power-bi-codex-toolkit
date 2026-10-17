"""Static checks of inventoried metadata and relationship endpoints."""

import re
from pathlib import Path

from .dax import lint_dax, qualified_references
from .diagnostics import Diagnostic
from .tmdl import NAME, Object, load_model, unquote

ENDPOINT = re.compile(rf"^({NAME})\.({NAME})$")
SUPPORTED = {"table", "column", "measure", "relationship", "model", "database", "partition"}


def endpoint(value: str) -> tuple[str, str] | None:
    match = ENDPOINT.fullmatch(value)
    return tuple(unquote(v).casefold() for v in match.groups()) if match else None


def validate_model(root: Path) -> tuple[list[Object], list[Diagnostic]]:
    nodes, issues = load_model(root)
    tables = {o.name.casefold(): o for o in nodes if o.kind == "table"}
    columns = {
        (o.table_name.casefold(), o.name.casefold()): o
        for o in nodes
        if o.kind == "column" and o.table_name
    }
    members = {
        (o.table_name.casefold(), o.name.casefold())
        for o in nodes
        if o.kind in {"column", "measure"} and o.table_name
    }
    seen: dict[tuple, Object] = {}

    def add(code: str, severity: str, obj: Object, message: str) -> None:
        issues.append(Diagnostic(code, severity, obj.path, obj.line, message))

    for o in nodes:
        # Measures have model-wide names; columns and measures share a table namespace.
        if o.kind == "measure":
            keys = [("measure", o.name.casefold()), ("member", o.table_name, o.name.casefold())]
        elif o.kind == "column":
            keys = [("member", o.table_name, o.name.casefold())]
        else:
            keys = [(o.kind, o.table_name, o.name.casefold())]
        for key in keys:
            normalized = tuple(v.casefold() if isinstance(v, str) else v for v in key)
            if normalized in seen:
                add("MODEL001", "error", o, f"Duplicate {o.kind} name: {o.name!r}.")
                break
            seen[normalized] = o
        if o.kind not in SUPPORTED:
            add(
                "MODEL900",
                "info",
                o,
                f"{o.kind} inventoried only; use engine validation for its semantics.",
            )
        if o.kind == "measure":
            for key in ("formatString", "displayFolder"):
                if not o.properties.get(key):
                    add("META101", "warning", o, f"Measure {o.name!r} has no {key}.")
            if not (o.description or o.properties.get("description")):
                add("META102", "warning", o, f"Measure {o.name!r} has no description.")
            issues.extend(lint_dax(o.expression, o.path, max(0, o.expression_line - 1)))
            for table, member, line in qualified_references(o.expression):
                key = (table.casefold(), member.casefold())
                if table.casefold() not in tables or key not in members:
                    issues.append(
                        Diagnostic(
                            "DAX201",
                            "error",
                            o.path,
                            o.expression_line + line - 1,
                            f"Unknown qualified reference {table!r}[{member}].",
                        )
                    )
        if o.kind == "column" and not o.properties.get("dataType"):
            # Calculated columns may have inferred types.
            if not o.expression and o.properties.get("isDataTypeInferred") != "true":
                add("META103", "warning", o, f"Column {o.name!r} has no explicit dataType.")
        if o.kind == "relationship":
            endpoints = []
            for prop in ("fromColumn", "toColumn"):
                value = endpoint(o.properties.get(prop, ""))
                if value is None:
                    add(
                        "REL001",
                        "error",
                        o,
                        f"Missing or unsupported {prop} (expected Table.Column).",
                    )
                elif value not in columns:
                    add("REL002", "error", o, f"Relationship {prop} points to a missing column.")
                else:
                    endpoints.append(columns[value])
            if len(endpoints) == 2:
                types = [c.properties.get("dataType") for c in endpoints]
                if all(types) and types[0].casefold() != types[1].casefold():
                    add(
                        "REL003",
                        "warning",
                        o,
                        f"Relationship types differ: {types[0]} vs {types[1]}.",
                    )
            if o.properties.get("crossFilteringBehavior", "").casefold() == "bothdirections":
                add(
                    "REL101",
                    "warning",
                    o,
                    "Bidirectional relationship: review ambiguity and RLS propagation.",
                )
    return nodes, issues
