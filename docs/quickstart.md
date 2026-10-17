# Quickstart

## Work in this repository

Install Python 3.11+ and Codex following the
[official CLI guide](https://learn.chatgpt.com/docs/codex/cli). If using npm, the
official package is `@openai/codex`; authenticate through your supported Codex flow.
No OpenAI SDK dependency or API key is required by this toolkit's scripts.

```sh
python scripts/pbi.py doctor
python scripts/pbi.py check examples/retail --strict
python scripts/pbi.py inventory examples/retail/Retail.SemanticModel/definition
codex
```

The repository's `AGENTS.md` and `.agents/skills/` are available when Codex runs
inside the checkout. In the IDE, open the checkout as your workspace, use its Codex
chat and invoke a skill by name, such as `$dax-expert`.

Try the [prompt examples](prompts.md), then inspect the diff and run the local
checks again. A clean check means only that the implemented static rules passed.

## Use skills in another project

```sh
python scripts/install_skills.py dax-expert semantic-model tmdl-development --project ../sales-analysis
```

This creates `.agents/skills/<selected-name>` in the target. Each folder contains
SKILL.md, its reference, a helper launcher, bundled Python source and license
notices. No other skill, root AGENTS.md, custom agent, MCP server or Git hook is
installed. The small helper bundle is duplicated intentionally to keep each skill
portable. Record version 0.1.0 in your project dependency/change records.

For personal skills, substitute `--user`. The current official discovery path is
`~/.agents/skills`; `CODEX_HOME` is not used by this installer. Older clients may
need an update. Restart Codex if the skills do not appear, and ask it to summarize
available skills. No model call was run by the installer itself.

Use `--list` before selecting names. The installer rejects unknown names, duplicate
selections, symlink destinations and existing target folders. To update, first back
up and review your existing skill, then remove/move it yourself and install the new
version. To uninstall, remove only the installed skill folders you selected.

## Windows and Power BI Desktop

PowerShell examples:

```powershell
py -3 --version
py -3 scripts/pbi.py check examples/retail --strict
py -3 scripts/install_skills.py dax-expert --project 'C:\Projects\Sales Analysis'
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe scripts/validate_schemas.py
```

Using the venv executable directly avoids changing PowerShell execution policy.
Use the actual interpreter path if `py -3` selects Python older than 3.11.
Paths containing spaces must be quoted. Helpers accept Windows relative paths in
PBIP/PBIR bindings, but do not accept absolute or escaping references.

Open `examples/retail/Retail.pbip` in a compatible Power BI Desktop with PBIP, TMDL
and enhanced PBIR support enabled as required by your build. Refresh the synthetic
M tables locally, inspect the revenue chart, and run the DAX queries. Desktop is
Windows-only; a WSL/cloud session cannot directly attach to Windows localhost merely
because Desktop is open. Choose a supported client/server network arrangement.

The demo's schema and static checks ran on macOS. Desktop opening, M refresh and
chart rendering still require Windows acceptance; see [demo instructions](../examples/retail/README.md).

## Optional tooling

Use [integrations](integrations.md) for live models, Fabric CLI and MCP. Keep that
setup separate from skill installation. For toolkit development, install `.[dev]`
and run the commands in the root README. A three-OS CI matrix is provided; local
execution does not mean those remote jobs have run yet.
