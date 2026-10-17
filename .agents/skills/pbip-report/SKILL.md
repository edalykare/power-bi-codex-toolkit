---
name: pbip-report
description: Inspect, create or modify local PBIP/PBIR reports, pages, visuals and model bindings while preserving schemas and object identifiers.
---

# PBIP and report development

## Prerequisites and tools

Use a PBIP/PBIR project, Python 3.11+ and the matching Microsoft JSON schemas.
Power BI Desktop on Windows is required for a visual acceptance check. A PBIX is a
binary artifact: request or create a PBIP export through a supported Microsoft tool.

## Workflow

1. Inspect definition.pbir and the semantic model binding. Distinguish byPath from
   remote byConnection and legacy report.json from enhanced PBIR definition files.
2. Read the changed files' schema versions. Reuse an existing compatible visual
   shape or Microsoft's schema; do not invent query bindings or visual properties.
3. Implement the requested local report change. Keep identifiers, pageOrder and
   activePageName consistent. Review changed measures/columns in visual queries,
   filters, bookmarks, tooltips and conditional formatting after a model rename.
4. Run `check` at the containing project root, so ../Model bindings stay in scope.
   Validate changed JSON against its exact schema using trusted local schemas if
   available; never fetch arbitrary project-provided schema URLs without review.
5. Open in Desktop to verify rendering, interactions, accessible labels, contrast,
   keyboard navigation and totals. Report engine/render checks not performed.

## Validation and examples

```sh
python "<skill-dir>/scripts/pbi.py" check "<project-dir>" --strict --format json
```

Resolve the skill helper from its loaded path and replace placeholders.
Example prompt: `Use $pbip-report to add a revenue-by-category visual to the local
report. Preserve page IDs and verify its measure binding and schema version.`

No report renderer or visual authoring MCP is bundled. The modeling MCP edits
semantic models; do not assume it edits pages or visuals. Never publish implicitly.

## References

Read [PBIR file checks](references/pbir-checks.md) before changing report JSON.
