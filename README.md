# Power BI Codex Toolkit

[![CI](https://github.com/edalykare/power-bi-codex-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/edalykare/power-bi-codex-toolkit/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange)](CHANGELOG.md)

Build and review Power BI and Microsoft Fabric projects with **OpenAI Codex**.
Nine focused skills, local project checks, a synthetic PBIP demo, and optional
Microsoft integrations. The offline CLI has **no runtime dependencies**.

Inspired by [Kurt Buhler's Power BI Agentic Development](https://github.com/data-goblin/power-bi-agentic-development).
Reimplemented around Codex conventions. See [analysis](docs/reference-analysis.md)
and [attributions](ATTRIBUTIONS.md). Independent community project; not affiliated
with or endorsed by OpenAI, Microsoft, or Data Goblins.

## Start in two minutes

Prerequisites: Git, Python **3.11+**, and [Codex CLI or IDE](https://learn.chatgpt.com/docs/codex/cli).
On Windows, use `py -3` instead of `python` if needed.

```sh
git clone https://github.com/edalykare/power-bi-codex-toolkit.git
cd power-bi-codex-toolkit
python scripts/pbi.py doctor
python scripts/pbi.py check examples/retail --strict
python scripts/pbi.py dax examples/dax --strict
codex
```

Then ask Codex:

```text
Use $semantic-model and $dax-expert to review examples/retail.
Explain Profit Margin at the total and category levels. Add engine test
queries for zero revenue and empty selections. Do not change remote state.
```

Repository skills are discovered from `.agents/skills/`; no plugin marketplace,
API key, or MCP connection is needed for local file work. Model usage requires
your own Codex access. See the [quickstart](docs/quickstart.md).

## Install only the skills you need

From this checkout, install selected skills into another project:

```sh
python scripts/install_skills.py --list
python scripts/install_skills.py dax-expert semantic-model tmdl-development --project ../my-power-bi-project
```

Or use `--user` for `~/.agents/skills`, or `--all` for the complete collection.
Existing folders are never overwritten. Each installed skill includes its helper
code and license notices, so the checkout can move afterward. Restart Codex if
new skills do not appear. No global configuration or MCP server is installed.

For a conventional executable, optionally install the Python CLI:

```sh
python -m venv .venv
# macOS/Linux
. .venv/bin/activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -e .
pbi-codex check examples/retail --strict
```

## Capabilities and evidence

| Area | Included | Validation boundary |
| --- | --- | --- |
| DAX | Authoring/review skill, lexical checks, qualified references in model measures, test queries | No local DAX evaluator or full parser |
| Semantic models | Inventory, duplicate names, measure metadata, relationship endpoints/types | Key uniqueness, RLS/OLS and cardinality require an engine |
| TMDL | Common declaration reader, descriptions, multiline measures, structural findings | Microsoft serializer remains authoritative |
| PBIP/PBIR | Artifact and binding checks, page order, identifiers, basic dimensions | Visual query semantics and rendering require Power BI |
| JSON schemas | 15 pinned Microsoft schema files with hashes; offline validation script | Covers the demo's selected versions |
| BPA | Audit skill and two original Tabular Editor rule examples | Full BPA engine is an optional external dependency |
| Performance | Measured-test workflow; median comparison of normalized samples | No trace capture; shipped timings are synthetic |
| Documentation | Markdown model inventory and JSON object export | Business meaning and sensitive content need review |
| Fabric | Workload guidance, CLI/MCP setup, local SQL/PySpark examples, hashed proposal | No built-in deploy, refresh, remote execution or remote diff |
| Reviews | Scoped workflows, two optional Codex custom agents, pre-commit and CI | Agent behavior depends on client capabilities and access |

The CI badge reflects GitHub runs **after publication**. Local results and checks
that could not run are recorded in [validation](docs/validation.md).

## Architecture

```text
.agents/skills/       Nine independent SKILL.md entry points and references
.codex/agents/       Optional model-reviewer and report-reviewer TOML agents
src/pbi_codex/       Standard-library-only CLI and static checks
scripts/            Checkout launcher, installer, repository/schema checks
examples/           Synthetic PBIP/TMDL/PBIR, DAX, Fabric and BPA examples
vendor/             Pinned Microsoft JSON schemas and MIT notice
config/             Opt-in MCP configuration example
docs/               Architecture, integrations, workflows and limitations
.github/            CI, Dependabot, issue and pull request templates
```

Skills load supporting references only when relevant. Helpers read local files;
they never execute model expressions or launch third-party tools. Codex's native
MCP configuration stays under user control. See [architecture](docs/architecture.md),
[skill catalog](docs/skills.md) and [end-to-end workflows](docs/workflows.md).

## Useful commands

```sh
python scripts/pbi.py inventory examples/retail/Retail.SemanticModel/definition
python scripts/pbi.py docs examples/retail/Retail.SemanticModel/definition --output artifacts/model.md
python scripts/pbi.py check examples/retail --format json --output artifacts/checks.json
python scripts/pbi.py fabric-plan examples/fabric/manifest.json
python scripts/pbi.py compare-timings examples/performance/timings.json
```

Exit codes: `0` completed without blocking findings; `1` errors (or warnings with
`--strict`); `2` invalid input, missing dependencies, or I/O failure. An output
file is not overwritten unless `--force` is specified. Full [CLI reference](docs/cli.md).

## Microsoft and Codex integration

Use the [integration guide](docs/integrations.md) for Fabric CLI, Microsoft Learn
MCP, Power BI Authoring MCP and Tabular Editor. The local Power BI Authoring MCP
does not support macOS; a hosted connection also needs compatible Entra OAuth setup.
MCP examples are disabled where local paths or reviewed package versions are required.

Codex custom agents follow the [current standalone TOML format](https://learn.chatgpt.com/docs/agent-configuration/subagents).
Request delegation explicitly; workflows work sequentially too. Custom agent
instructions do not create an independent read-only sandbox.

## Development

```sh
python -m pip install -e ".[dev]"
python scripts/check_repo.py
python -m unittest discover -s tests -v
python -m ruff check .
python scripts/validate_schemas.py
python -m build
python scripts/smoke_distribution.py
```

CI runs on Linux, Windows and macOS with Python 3.11 and 3.13. It requires no
tenant, secrets, paid API calls or Power BI Desktop. Optional pre-commit setup:
install `pre-commit`, then run `pre-commit install` after reviewing
[the configuration](.pre-commit-config.yaml).

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md),
[technical limits](docs/limitations.md), [sources](docs/sources.md) and
[CHANGELOG.md](CHANGELOG.md). Licensed under [GPL-3.0-only](LICENSE);
vendored Microsoft schemas retain their MIT license.
