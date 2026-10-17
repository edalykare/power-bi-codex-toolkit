"""Small DAX lexer for conservative linting, not parsing or evaluation."""

from dataclasses import dataclass

from .diagnostics import Diagnostic


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    line: int


def tokenize(text: str, path: str = "<expression>") -> tuple[list[Token], list[Diagnostic]]:
    tokens: list[Token] = []
    issues: list[Diagnostic] = []
    i, line = 0, 1
    while i < len(text):
        c = text[i]
        if c.isspace():
            line += c == "\n"
            i += 1
            continue
        if text.startswith(("//", "--"), i):
            end = text.find("\n", i)
            i = len(text) if end < 0 else end
            continue
        if text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end < 0:
                issues.append(Diagnostic("DAX002", "error", path, line, "Unclosed block comment."))
                break
            line += text[i : end + 2].count("\n")
            i = end + 2
            continue
        if c in "\"'[":
            close = "]" if c == "[" else c
            kind = {'"': "string", "'": "identifier", "[": "reference"}[c]
            start_line = line
            value: list[str] = []
            i += 1
            closed = False
            while i < len(text):
                if text[i] == close:
                    if i + 1 < len(text) and text[i + 1] == close:
                        value.append(close)
                        i += 2
                        continue
                    i += 1
                    closed = True
                    break
                line += text[i] == "\n"
                value.append(text[i])
                i += 1
            if not closed:
                issues.append(Diagnostic("DAX002", "error", path, start_line, f"Unclosed {kind}."))
            tokens.append(Token(kind, "".join(value), start_line))
            continue
        if c.isalpha() or c == "_":
            end = i + 1
            while end < len(text) and (text[end].isalnum() or text[end] == "_"):
                end += 1
            tokens.append(Token("word", text[i:end], line))
            i = end
        else:
            tokens.append(Token("symbol", c, line))
            i += 1
    return tokens, issues


def lint_dax(text: str, path: str = "<expression>", line_offset: int = 0) -> list[Diagnostic]:
    tokens, issues = tokenize(text, path)
    if not tokens:
        issues.append(Diagnostic("DAX000", "error", path, 1, "Empty DAX expression or query."))
    stack: list[Token] = []
    for index, t in enumerate(tokens):
        if t.kind == "symbol":
            if t.value in ("(", "{"):
                stack.append(t)
            elif t.value in (")", "}"):
                expected = {")": "(", "}": "{"}[t.value]
                if not stack or stack[-1].value != expected:
                    issues.append(
                        Diagnostic("DAX001", "error", path, t.line, f"Unmatched {t.value}.")
                    )
                else:
                    stack.pop()
            elif t.value == "/":
                issues.append(
                    Diagnostic(
                        "DAX101",
                        "warning",
                        path,
                        t.line,
                        "Review division: use DIVIDE for a possibly zero/BLANK denominator; constants can use /.",
                    )
                )
        if (
            t.kind == "word"
            and t.value.upper() == "FORMAT"
            and index + 1 < len(tokens)
            and tokens[index + 1].value == "("
        ):
            issues.append(
                Diagnostic(
                    "DAX102",
                    "info",
                    path,
                    t.line,
                    "FORMAT returns text; consider model format strings for numeric measures.",
                )
            )
    for t in stack:
        issues.append(Diagnostic("DAX001", "error", path, t.line, f"Unclosed {t.value}."))
    return [Diagnostic(d.code, d.severity, d.path, d.line + line_offset, d.message) for d in issues]


def qualified_references(text: str) -> list[tuple[str, str, int]]:
    tokens, _ = tokenize(text)
    keywords = {
        "RETURN",
        "EVALUATE",
        "VAR",
        "DEFINE",
        "MEASURE",
        "COLUMN",
        "TABLE",
        "ORDER",
        "BY",
        "ASC",
        "DESC",
        "IN",
        "NOT",
        "AND",
        "OR",
    }
    return [
        (a.value, b.value, b.line)
        for a, b in zip(tokens, tokens[1:], strict=False)
        if (a.kind == "identifier" or (a.kind == "word" and a.value.upper() not in keywords))
        and b.kind == "reference"
    ]
