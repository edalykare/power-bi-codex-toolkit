# Example prompts

## DAX correctness

```text
Use $dax-expert to fix the Profit Margin measure in this PBIP project.
It should return BLANK for zero revenue, preserve category filters and compute
a ratio of totals at the grand total. Add queries for each edge case and tell
me which results you actually evaluated.
```

## Model and TMDL changes

```text
Use $semantic-model and $tmdl-development to review the Product relationship.
Inspect key types, cardinality assumptions, filter direction and RLS impact.
Make only the requested local metadata fixes, preserve lineage tags, then run
the structural checks. Identify any data-quality checks needing an engine.
```

## Report editing

```text
Use $pbip-report to change the overview page title and add Revenue by Category
using the existing report's visual patterns and schema versions. Preserve IDs
used by bookmarks. Validate the local files and list Desktop acceptance checks.
```

## Audit and documentation

```text
Use $model-audit and $model-documentation for this one semantic model. Produce
a prioritized findings list and artifacts/model.md. Separate static metadata
findings, actual BPA output and unverified engine/security behavior.
```

## Fabric proposal

```text
Use $fabric-development to review the local Notebook and Warehouse examples.
Generate a hashed proposal for Retail Development and explain dependency order,
connection bindings and rollback. Prepare exact commands only after checking
the installed CLI help. Do not deploy, refresh or run a remote job.
```

## Performance evidence

```text
Use $performance-analysis to investigate this query with the supplied server
timings. Verify result equivalence, compare warm-cache medians, and distinguish
measured improvements from hypotheses. Do not fabricate missing samples.
```

## Diff review

```text
Use $project-review to review this branch against main without edits. Report
concrete regressions with file locations and describe which checks ran. Draft
a PR description, but do not push or publish it.
```
