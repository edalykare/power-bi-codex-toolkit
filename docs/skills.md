# Skill catalog

Each skill contains prerequisites, a focused workflow, helper usage, validation
boundaries, examples and task-specific sources. Invoke explicitly with `$name`,
or let Codex select a matching installed skill.

| Skill | Primary use | Local helper |
| --- | --- | --- |
| [dax-expert](../.agents/skills/dax-expert/SKILL.md) | Measures, queries, filter context, correctness tests | `dax`, `check` |
| [semantic-model](../.agents/skills/semantic-model/SKILL.md) | Grain, relationships, metadata and security impact | `inventory`, `check` |
| [tmdl-development](../.agents/skills/tmdl-development/SKILL.md) | Focused definition edits and rename impact | `check`, `inventory` |
| [pbip-report](../.agents/skills/pbip-report/SKILL.md) | Report bindings, pages, visuals and schema-aware changes | `check` |
| [model-audit](../.agents/skills/model-audit/SKILL.md) | Prioritized static/BPA review | `check` |
| [performance-analysis](../.agents/skills/performance-analysis/SKILL.md) | Measured hypotheses and comparable samples | `compare-timings` |
| [model-documentation](../.agents/skills/model-documentation/SKILL.md) | Markdown and JSON inventories | `docs`, `inventory` |
| [fabric-development](../.agents/skills/fabric-development/SKILL.md) | Local workload artifacts and reviewed live operations | `fabric-plan`, `doctor` |
| [project-review](../.agents/skills/project-review/SKILL.md) | Diff review and optional explicit delegation | Relevant checks |

The helpers are generic entry points to the same small package. The selective
installer bundles that package inside each skill. Installing `dax-expert` does not
require installing `semantic-model`; needed workflow context is described locally.
Advanced reference files are linked and loaded only for the active task.

The repository enforces a 150-line SKILL.md budget as a local quality rule, not an
OpenAI format requirement. UI metadata is optional and is not needed for these
skills. No Claude `tools:`/`model:` frontmatter or implicit shell hooks are reused.
