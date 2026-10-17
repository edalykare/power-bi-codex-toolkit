---
name: semantic-model
description: Design and change Power BI semantic model tables, columns, measures, relationships and metadata in local TMDL projects; inspect security and storage-mode implications.
---

# Semantic model

## Prerequisites and tools

Use a local TMDL definition or an explicitly authorized model connection. Python
3.11+ supports the inventory and static checks. Engine evaluation requires Microsoft
tools. Inspect storage mode before proposing Import, DirectQuery or Direct Lake changes.

## Workflow

1. Inventory the relevant model with `inventory`. For a multi-model repository,
   select one .SemanticModel/definition directory for inventory and documentation.
2. Establish fact grain, dimension keys, expected cardinality and filter direction.
   Preserve lineage tags, source mappings and existing security definitions.
3. Make the smallest local change. Keep business measures readable, documented and
   formatted. Treat display folders and descriptions as team conventions, not TMDL syntax.
4. Check endpoints and data types. A metadata-only check cannot establish one-side
   uniqueness, referential integrity, actual cardinality or absence of filter ambiguity.
5. Run `check --strict`, inspect the diff and prepare result queries. With an engine,
   validate key uniqueness, unmatched foreign keys, totals and relevant RLS/OLS roles.

## Validation and examples

Resolve the helper relative to this skill, replacing placeholders:

```sh
python "<skill-dir>/scripts/pbi.py" inventory "<model-definition-dir>"
python "<skill-dir>/scripts/pbi.py" check "<project-dir>" --strict
```

Example prompt: `Use $semantic-model to review the Sales-Product relationship and
add a documented Profit measure. Keep existing security and report bindings.`

Return the intended model behavior, local changes, static findings and outstanding
engine checks. Do not change a remote model or refresh it without explicit approval.

## References

Read [model validation boundaries](references/model-checks.md) for metadata findings
and data-quality queries to run with an authorized engine.
