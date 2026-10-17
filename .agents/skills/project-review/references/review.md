# Review handoff

Give each reviewer the comparison base, changed file list, relevant project root,
intended behavior and known unverified checks. Ask for concrete findings and a short
summary instead of raw logs. Keep parallel reviewers away from overlapping edits.

An end-to-end local change combines model inventory, DAX/TMDL edits, report dependency
review, static checks and documentation. Engine/result/render checks follow when the
required environment is available. Deployment is a separate, explicitly authorized step.

This collection uses official SKILL.md discovery and optional standalone TOML agents.
It does not define slash commands, event hooks or hidden orchestration APIs.
