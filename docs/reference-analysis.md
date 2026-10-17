# Reference analysis and adaptation decisions

Reference: [data-goblin/power-bi-agentic-development](https://github.com/data-goblin/power-bi-agentic-development),
cloned and reviewed at `2ad33e597e965ee2c208f06b766f869c2c060a44` on 2026-10-17.
The snapshot has **13 plugins, 33 skills and 8 agent definitions**. A machine-readable
[inventory](reference-inventory.json) records every skill entry point, agent, hook,
command and MCP configuration with source paths, byte counts and SHA-256 hashes.

## Organization and execution model

The root Claude marketplace enumerates independently versioned domain plugins.
Plugin manifests describe identity, tools and, in some cases, pane settings/types.
Skills use supporting references, scripts and examples. Most of the reference
content is conditional guidance; loading it all would waste context.

Claude/Copilot-specific PreToolUse/PostToolUse hooks validate file/model changes;
several newer plugins use TypeScript/TSX hook modules to register live UI panes.
PBIP hooks include prebuilt platform binaries for lightweight TMDL validation,
PBIR checks and binding checks. Desktop hooks inspect shell/TOM activity to check
measure metadata/references, refresh snapshots and inspect compatibility or integrity.
Paginated-report hooks inspect RDL. Shell/PowerShell bridges handle platform differences.

The source's `scripts/validate-plugins.sh` invokes Claude's plugin validator. Its
GitHub workflow installs Claude and gates execution on `ENABLE_PLUGIN_CI`. Its
release-bump script updates lockstep manifest/skill versions. The Tabular Editor
sync script pulls another upstream skill, reapplies local augmentations and can
install a post-merge hook; it retains the existing copy when network sync fails.
These are useful maintenance patterns, but are not Codex installation APIs.

## Plugin-by-plugin mapping

| Reference plugin and all skill names | Useful concepts | Codex decision in 0.1.0 |
| --- | --- | --- |
| semantic-models: dax, lineage-analysis, organize-semantic-model, power-query, refresh-semantic-model, semantic-model | Context-aware DAX, object lifecycle, metadata, lineage and refresh diagnostics | dax-expert, semantic-model, model-documentation; M inspected, refresh remains external |
| pbip: pbip, pbir-format, tmdl | Project boundaries, exact schemas, identity-preserving edits, cascading renames | tmdl-development, pbip-report, Python structure checks and separate official schema validation |
| pbi-desktop: connect-pbid | TOM/ADOMD, query capture, traces, model snapshots | Official Authoring MCP setup; no vendored TOM binaries, port discovery or live query listener |
| tabular-editor: bpa-rules, c-sharp-scripting, te-cli, te-docs, te2-cli | BPA, compatibility/version differences and CLI automation | model-audit and two original sample rules; C# macros/new CLI execution deferred |
| reports: create-pbi-report, modifying-theme-json, pbi-report-design, pbir-cli, review-report | Design brief, interactivity, schemas and review | pbip-report, one demo chart, report reviewer; live CLI/pane and theme renderer deferred |
| fabric-cli: fabric-cli | Workspaces/items, auth, CLI discovery, REST audiences and long-running operations | fabric-development, verified documented command examples and offline proposal |
| etl: executing-spark, using-duckdb | Lakehouse query modes, Livy lifecycle, local/remote data access | Local PySpark/SQL examples and workload checks; no Spark/Livy/DuckDB execution adapter |
| fabric-admin: audit-tenant-settings, fabric-capacity | Governance scoping, permissions and capacity context | Prerequisite guidance only; tenant/capacity administration deferred |
| custom-visuals: deneb-visuals, powerbi-custom-visuals, python-visuals, r-visuals, svg-visuals | Visual-specific contracts, schema/design review and custom visuals MCP | Deferred; no untested generator or imported asset catalog |
| paginated-reports: paginated-report | RDL layout, validation and print acceptance | Deferred; no claim of RDL support |
| goblin-mode: help-me-get-started, improve-my-agent-setup | Onboarding and setup diagnostics | Focused quickstart, doctor and prompt examples |
| databricks-cli: no SKILL.md entries | CLI-driven live Databricks pane | Deferred; separate product and host UI APIs |
| fabric-data-app: no SKILL.md entries | CLI-driven app discovery/deployment pane | Deferred; no data-app hosting integration |

## Agents, hooks and MCP

The eight reference agents are semantic-model-auditor, pbip-validator,
query-listener, bpa-expression-helper, deneb-reviewer, python-reviewer, r-reviewer
and svg-reviewer. Their review questions inform the model/report reviewer scopes.
Claude model/tool/color frontmatter is not copied. Current Codex standalone TOML
agents are supplied, with inherited model/permissions and explicitly requested delegation.
The workflow also works without subagents.

Metadata/referential integrity hook concepts become explicit local checks or documented
engine tests. Source hook payloads, matcher strings, lifecycle events and pane modules
are not mechanically translated. Git hooks are opt-in through pre-commit; CI directly
invokes the same scripts and does not depend on a paid agent session or repository variable.

The reference's custom-visuals MCP configuration is specific to pbiviz tooling. We
instead document optional official Microsoft documentation/Authoring/Fabric servers.
Remote tool availability and names are discovered at runtime. Read-only offline
validation is always available without a server.

## Reuse, adaptation and redesign

Reusable ideas: modular domain routing, progressive references, schema-aware file
editing, object identity preservation, metadata policies and evidence-based review.
Adapted: domain workflows, authoring prompts and audit categories, written afresh
for Codex. Redesigned: installation, helper packaging, cross-platform validation,
agents, hook replacement, CI and remote-operation authorization boundaries.

We do not adopt blanket force flags, automatic package/binary upgrades, compatibility
upgrades or implicit remote mutation. Local findings are never described as engine
validation. Documentation and tested adapters take priority over feature parity.

The GPL v3 source license and upstream contributor attributions were inspected.
No source hooks, executables, assets or bundled skill bodies were copied. GPL-3.0-only
was selected for the new toolkit; Microsoft schema snapshots separately retain MIT.
See [ATTRIBUTIONS.md](../ATTRIBUTIONS.md) for provenance.
