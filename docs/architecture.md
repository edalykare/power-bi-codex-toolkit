# Architecture

The core is a Python 3.11+ standard-library package plus Codex-native instructions.
No LLM framework, API client, tenant or Power BI installation is needed for local
checks. The Python wheel installs the CLI; use a Git checkout/source distribution
to install skills or access the demonstration and pinned schemas.

## Codex surfaces

- `AGENTS.md` supplies short repository-wide working instructions. It does not
  contain the entire Power BI manual or force unrelated skills into context.
- `.agents/skills/<name>/SKILL.md` provides discovery metadata and task guidance.
  Each skill has a linked reference and helper entry point. Installer bundles are
  self-contained source copies with license notices, not cross-skill symlinks.
- `.codex/agents/*.toml` defines two optional custom agents using the current
  standalone `name`, `description`, `developer_instructions` schema. They inherit
  the parent model and permissions. No model pin or invented tool API is required.
- MCP uses native Codex TOML configuration. Examples are opt-in and local package
  versions must be reviewed before enabling them. No MCP server is bundled.

These choices follow the [skills](https://learn.chatgpt.com/docs/build-skills),
[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[subagent](https://learn.chatgpt.com/docs/agent-configuration/subagents) and
[MCP](https://learn.chatgpt.com/docs/extend/mcp) documentation reviewed on 2026-10-17.

## Python boundaries

| Module | Responsibility |
| --- | --- |
| `diagnostics` | Findings, UTF-8 reads, bounded file discovery and exclusions |
| `dax` | Tokenization, delimiters, lexical advisories and qualified reference extraction |
| `tmdl` | Common declarations, descriptions, properties and expressions in memory |
| `model` | Metadata/name checks and relationship endpoint checks |
| `project` | Strict JSON parsing, PBIP paths, PBIR bindings and page/visual structure |
| `operations` | Markdown/JSON inventory, executable discovery, local proposals and timing medians |
| `cli` | Arguments, reports, output handling and stable exit codes |

The reader never writes TMDL/PBIR or executes project expressions. Codex uses its
normal file editing tools for requested changes. This avoids making a partial
parser responsible for a lossless serialization it cannot guarantee.

`check` scopes declarations by enclosing `definition/` folder so independent models
can share names. `inventory` and `docs` should be scoped to one model. A standalone
TMDL file can be checked, but references to omitted files are naturally unresolved.

## Validation layers

1. Local lexical/structural checks: fast, deterministic, offline.
2. Microsoft JSON schemas: pinned transitive closure for the demo's selected versions;
   separate optional `jsonschema` dependency, no network resolution.
3. Microsoft serializer / semantic engine: authoritative TMDL load and DAX behavior.
4. Desktop report rendering, interactions, security identities and Fabric operations:
   environment-dependent acceptance checks, not inferred from layers 1–2.

GitHub Actions and optional pre-commit run explicit commands. We deliberately avoid
translating reference-project Claude/Copilot hook payloads into invented Codex events.
This is a portability decision; it is not a claim that Codex lacks hook capabilities.

## Evolution

The first release prioritizes dax-expert, semantic-model and tmdl-development.
The extensions add report/audit/documentation/review/performance guidance and local
Fabric proposals. Future adapters should wrap maintained Microsoft tools, retain
the same read-only defaults, and add real integration evidence before advertising
execution support. Plugin packaging can be added separately; direct repository and
user skill installation currently keeps the collection selective and inspectable.
