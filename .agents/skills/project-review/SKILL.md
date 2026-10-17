---
name: project-review
description: Review a Power BI or Fabric project diff, run relevant local checks and coordinate scoped specialist reviews when delegation is explicitly requested.
---

# Project review

## Prerequisites and tools

Use a Git worktree and Python 3.11+. Confirm the requested comparison base with
`git status --short` and `git diff`. External engine and Fabric checks are optional
and must be reported as unverified when unavailable.

## Workflow

1. Establish change scope and read the diff. Inspect the affected model/report and
   workload contracts; do not scan customer data or unrelated configuration.
2. Run the helper's `check` for PBIP/TMDL, `dax` for queries, and `fabric-plan` when
   a local Fabric manifest is present. Inspect both exit codes and diagnostics.
3. Review renamed object dependencies, RLS/OLS, report bindings, notebook/SQL side
   effects and compatibility changes. Static checks do not settle semantic questions.
4. If the user explicitly requests delegation and this environment exposes subagents,
   assign independent model/report reviews with bounded paths and read-only intent.
   Wait for their findings, reconcile conflicts and rerun checks after any fixes.
   Otherwise perform these reviews sequentially. Agent instructions do not enforce
   a read-only sandbox; all agents inherit the parent permissions.
5. Return actionable findings by severity with file/line, evidence and remediation.
   Distinguish blockers, suggestions and checks not run. Prepare a PR description
   when requested; do not push or publish without authorization.

## Validation and examples

```sh
python "<skill-dir>/scripts/pbi.py" check "<project-dir>" --strict --format json
```

Resolve the helper from this skill's path and replace placeholders.
Example prompt: `Use $project-review to review this branch against main. Do not
modify files. Include engine validation gaps and a draft PR description.`

## References

- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Review handoff](references/review.md)
