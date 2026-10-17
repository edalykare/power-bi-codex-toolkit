"""Read common TMDL declarations without rewriting or executing expressions.

This is an inventory reader for tables, columns, measures, and relationships.
Other declarations are retained as nodes, not semantically validated.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

from .diagnostics import Diagnostic, files_under, read_text

NAME = r"(?:'(?:[^']|'')*'|[^\s=]+)"
DECLARATION = re.compile(
    rf"^(?P<kind>table|column|measure|relationship|model|database|partition|hierarchy|level|"
    rf"calculationGroup|calculationItem|role|tablePermission|columnPermission|perspective|"
    rf"perspectiveTable|perspectiveColumn|perspectiveMeasure|perspectiveHierarchy|cultureInfo|"
    rf"dataSource|expression|function|queryGroup)\s+(?P<name>{NAME})(?P<tail>.*)$"
)
PROPERTY = re.compile(r"^([A-Za-z][A-Za-z0-9]*):\s*(.*)$")
FLAGS = {
    "isHidden",
    "isKey",
    "isNameInferred",
    "isDataTypeInferred",
    "isDefaultLabel",
    "isDefaultImage",
    "isAvailableInMdx",
    "isPrivate",
}


def unquote(name: str) -> str:
    return name[1:-1].replace("''", "'") if name.startswith("'") and name.endswith("'") else name


@dataclass
class Object:
    kind: str
    name: str
    path: str
    line: int
    indent: int
    parent: "Object | None" = field(default=None, repr=False)
    properties: dict[str, str] = field(default_factory=dict)
    description: str = ""
    expression: str = ""
    expression_line: int = 0

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "name": self.name,
            "table": self.table_name,
            "path": self.path,
            "line": self.line,
            "properties": self.properties,
            "description": self.description,
            "expression": self.expression,
        }

    @property
    def table_name(self) -> str | None:
        parent = self.parent
        while parent:
            if parent.kind == "table":
                return parent.name
            parent = parent.parent
        return None


def parse_file(path: Path) -> tuple[list[Object], list[Diagnostic]]:
    objects: list[Object] = []
    issues: list[Diagnostic] = []
    stack: list[Object] = []
    descriptions: list[str] = []
    expression_owner: Object | None = None
    fence = False
    indent_modes: set[str] = set()
    lines = read_text(path).splitlines()
    for number, raw in enumerate(lines, 1):
        stripped = raw.lstrip(" \t")
        prefix = raw[: len(raw) - len(stripped)]
        indent = len(prefix.expandtabs(4))
        if fence:
            if stripped == "```":
                fence = False
                expression_owner = None
            elif expression_owner:
                expression_owner.expression += raw + "\n"
            continue
        if not stripped:
            # Whitespace inside an expression is preserved; blank lines break descriptions.
            if expression_owner:
                expression_owner.expression += raw + "\n"
            descriptions = []
            continue
        if stripped.startswith("///"):
            if expression_owner and indent > expression_owner.indent:
                expression_owner.expression += raw + "\n"
                continue
            descriptions.append(stripped[3:].strip())
            continue
        if stripped.startswith("//"):
            if expression_owner and indent > expression_owner.indent:
                expression_owner.expression += raw + "\n"
            continue
        if prefix:
            indent_modes.add("tabs" if "\t" in prefix else "spaces")
            if " " in prefix and "\t" in prefix:
                indent_modes.update({"tabs", "spaces"})
        # Fenced expressions may start after '=' on the declaration or on their own line.
        if stripped == "```":
            fence = True
            continue
        prop = PROPERTY.match(stripped)
        match = DECLARATION.match(stripped)
        # Expression text is deeper than its object's ordinary property level.
        if expression_owner and indent > expression_owner.indent and not prop:
            # Named child declarations should still be inventoried (e.g. table -> column).
            if not match or expression_owner.kind in {
                "measure",
                "column",
                "calculationItem",
                "expression",
                "function",
            }:
                expression_owner.expression += raw + "\n"
                continue
        while stack and stack[-1].indent >= indent:
            stack.pop()
        if match:
            kind, name, tail = match.group("kind", "name", "tail")
            node = Object(
                kind,
                unquote(name),
                str(path),
                number,
                indent,
                stack[-1] if stack else None,
                description="\n".join(descriptions),
            )
            objects.append(node)
            stack.append(node)
            descriptions = []
            expression_owner = None
            if "=" in tail and kind in {
                "measure",
                "column",
                "calculationItem",
                "expression",
                "function",
            }:
                expr = tail.split("=", 1)[1].strip()
                node.expression_line = number if expr and expr != "```" else number + 1
                if expr == "```":
                    fence = True
                else:
                    node.expression = expr + "\n" if expr else ""
                expression_owner = node
            if kind in {"column", "measure", "partition", "hierarchy", "calculationGroup"}:
                if not node.parent or node.parent.kind != "table":
                    issues.append(
                        Diagnostic(
                            "TMDL001",
                            "error",
                            str(path),
                            number,
                            f"{kind} {node.name!r} must be nested under a table.",
                        )
                    )
            continue
        descriptions = []
        if stack and prop:
            node = stack[-1]
            key, value = prop.groups()
            node.properties[key] = value
            expression_owner = None
        elif stack and stripped in FLAGS:
            stack[-1].properties[stripped] = "true"
            expression_owner = None
        elif stack and stripped.startswith(("annotation ", "extendedProperty ", "ref ")):
            expression_owner = None
    if fence:
        issues.append(
            Diagnostic("TMDL002", "error", str(path), len(lines), "Unclosed TMDL expression fence.")
        )
    if len(indent_modes) > 1:
        issues.append(
            Diagnostic(
                "TMDL101",
                "warning",
                str(path),
                1,
                "Mixed tab and space indentation; verify with the Microsoft serializer.",
            )
        )
    return objects, issues


def load_model(root: Path) -> tuple[list[Object], list[Diagnostic]]:
    paths = files_under(root, {".tmdl"})
    if not paths:
        return [], [Diagnostic("TMDL000", "error", str(root), 1, "No TMDL files found.")]
    objects, issues = [], []
    for path in paths:
        nodes, diagnostics = parse_file(path)
        objects.extend(nodes)
        issues.extend(diagnostics)
    return objects, issues
