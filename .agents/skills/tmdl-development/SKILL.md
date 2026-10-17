---
name: tmdl-development
description: Author or repair local .tmdl model definitions, preserve object identity and expressions, and distinguish structural checks from Microsoft serializer validation.
---

# TMDL development

## Prerequisites and tools

Read the existing definition folder and its compatibility level. Python 3.11+ runs
local checks. Microsoft TmdlSerializer, Power BI Desktop or the local Power BI
Authoring MCP is needed for authoritative deserialization and engine validation.

## Workflow

1. Inventory affected declarations and their references before editing. Preserve
   unknown properties, lineage tags, roles, translations and source expressions.
2. Match existing indentation. Quote names containing whitespace/special characters;
   escape a single quote by doubling it. TMDL references use Table.Column, while
   DAX uses 'Table'[Column]. Descriptions precede declarations with `///`.
3. Keep multiline DAX and M indentation intact; preserve expression fences if used.
   A source expression is code to inspect, never code to run during a static check.
4. For renames, review relationships, DAX, sort-by columns, hierarchies, roles,
   perspectives, translations and report queries. A textual replacement is insufficient.
5. Run the helper over the containing project, review the diff, then deserialize with
   a Microsoft tool when available. Reopen the project after external edits if Desktop
   already holds an older in-memory copy. Do not claim a successful Desktop load untested.

## Validation and examples

```sh
python "<skill-dir>/scripts/pbi.py" check "<project-dir>" --strict
python "<skill-dir>/scripts/pbi.py" inventory "<model-definition-dir>"
```

Replace placeholders using this skill's loaded file path and the requested project.
Example prompt: `Use $tmdl-development to add a multiline measure without changing
lineage tags. Review the rename impact and identify required engine validation.`

Deliver a focused diff, static diagnostic results and remaining engine checks.

## References

Read [TMDL editing notes](references/tmdl-notes.md) for supported syntax and limits.
