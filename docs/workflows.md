# End-to-end workflows

## Change a measure safely

1. Use semantic-model to inventory affected objects and establish grain/filter behavior.
2. Use dax-expert and tmdl-development to edit the measure and prepare result queries.
3. Use pbip-report to inspect dependent visual queries, filters and conditional formats.
4. Run `check` on the containing project and `dax` on the prepared queries.
5. Run result queries in an authorized engine, then inspect report rendering in Desktop.
6. Use model-documentation and project-review to update documentation and prepare a PR.

When the engine/Desktop is unavailable, complete local work and attach explicit
pending acceptance checks. Local checks do not prove unchanged totals or valid visuals.

## Investigate a slow report

Start with a reproducible interaction and exported query. Use performance-analysis
to capture a baseline and control cache state. Use dax-expert or semantic-model to
form one candidate, verify results, repeat timings, and summarize comparable samples.
Keep measurements by storage mode, role and workload. Do not infer CU savings from
a desktop timing percentage.

## Prepare a Fabric release

Use fabric-development to inspect item definitions, local SQL/notebook changes,
connection dependencies and target workspace. Generate a local hashed proposal
with `fabric-plan`. Resolve the current CLI/API support and prepare exact remote
payloads plus rollback. Request approval for that concrete action/target unless
already explicitly authorized. Execute only in an available authorized environment,
record operation IDs, and separate deployment from refresh/job execution.

## Optional parallel review

The two agents in `.codex/agents/` are project-scoped standalone TOML agents under
the [current Codex convention](https://learn.chatgpt.com/docs/agent-configuration/subagents).
They are available only in clients supporting that format. No API/framework dependency
is needed. User scope is `~/.codex/agents/`; do not overwrite a preexisting agent.

Example prompt:

```text
Use $project-review. Delegate independent reviews to model-reviewer and
report-reviewer for the changes against main. Keep both reviews free of edits,
wait for both findings, and combine them with local check results.
Do not modify remote state or publish a PR.
```

Give each reviewer bounded files, base revision and expected behavior. The main
agent owns integration and any approved edits. All agents inherit parent permissions;
instructions asking for no edits are behavioral guidance, not a separate sandbox.
If subagents are unavailable, execute the same reviews sequentially and say so.
