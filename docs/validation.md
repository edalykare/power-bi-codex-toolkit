# Validation record

Local validation date: **2026-10-17**. Host: macOS arm64, Python 3.12.6.
The available Codex executable reported `0.162.0-alpha.17.2`; no paid model invocation
or live MCP connection was used to validate this toolkit.

## Executed locally

| Check | Result |
| --- | --- |
| `python -m unittest discover -s tests -v` with dev extras | 71 tests passed, including schema and YAML tests |
| `python scripts/pbi.py check examples/retail --strict` | 0 errors, 0 warnings |
| `python scripts/pbi.py dax examples/dax --strict` | 0 errors, 0 warnings |
| `python scripts/validate_schemas.py` | 8 demo files, 0 schema errors, offline resolution |
| Individual installed skill helper smoke tests | All 9 skill bundles ran from paths outside checkout |
| Single-skill isolated Python smoke test | Passed without PYTHONPATH or a global CLI package dependency |
| Editable CLI package install | Passed in a local virtualenv |
| `python scripts/check_repo.py` | Skills, local links, agent TOML and schema hashes passed |
| `python -m ruff check .` and format checks | Passed |
| OpenAI skill-creator `quick_validate.py` | All 9 skills passed |
| `python -S -m unittest discover -s tests -v` | 67 tests passed; 4 schema/YAML tests skipped without dev extras |
| `python -m build` | Source distribution and platform-independent wheel built successfully |
| `python scripts/smoke_distribution.py` | Source archive contents, independent skill install, fresh wheel install, executable/module CLI passed without network |
| Documentation/inventory/Fabric/timing commands | Generated local review artifacts successfully |

Tests exercise lexical quote/comment/delimiter behavior, escaped names, metadata
and relationship failures, JSON duplicate keys, model namespace separation, path
escapes, Windows-style paths, invalid dimensions, strict exit codes, no-overwrite
output/installation, unknown schemas and valid/invalid timing samples.

The initial dependency install and isolated build encountered the sandbox's network
restriction. Both succeeded after explicitly approved network retries. No global
Python environment, Codex user configuration or remote repository was changed.

## Hosted CI follow-up

The initial hosted Windows/Python 3.11 test run exposed an implicit subprocess in
`platform.system()`. `doctor` now reads the OS identifier from `sys.platform`, retaining
the existing Windows/Darwin/Linux output names. A regression test covers all three
identifiers while rejecting OS probes and subprocess calls. It failed before the fix
and passes afterward. The original no-subprocess test remains enabled.

Hosted matrix results are available in the repository's GitHub Actions runs; local
test results alone do not establish success on another operating system.

## External checks not executed locally

- TMDL deserialization or DAX evaluation using a Microsoft engine.
- Desktop opening, M refresh, report rendering/interactions and RLS/OLS identities.
- Tabular Editor BPA rule evaluation or real performance trace capture.
- Fabric CLI authentication, MCP startup/OAuth, remote deployment, refresh or jobs.

The demo's expected totals and timing examples are synthetic fixtures, not results
observed from Power BI. These limits are also stated in the skills and README.
