---
name: model-audit
description: Audit local Power BI model metadata and prepare or run an explicitly requested Tabular Editor Best Practice Analyzer review; report static and engine findings separately.
---

# Model audit and BPA

## Prerequisites and tools

Python 3.11+ supports static checks. Full BPA evaluation requires a compatible
Tabular Editor installation and reviewed rule files. Do not install or execute a
rule's fix expression automatically; it may mutate the model.

## Workflow

1. Scope the requested audit to one model and record storage mode and engine access.
2. Run `check` and `inventory`; classify observed errors, metadata warnings and
   unverified performance/security questions. Keep file and line references.
3. If BPA is requested and available, inspect the tool version, supported file format
   and CLI help. Use a read-only analysis command against a disposable/local model.
   TE2, TE3 and the newer `te` CLI have different syntax and format support.
4. Review rule scope, expression language, compatibility level and severity. Keep
   local metadata policies distinct from Microsoft's requirements and BPA findings.
5. Present prioritized fixes with evidence. Apply only the requested local changes;
   rerun the relevant checks. Engine integrity, RLS and cardinality remain separate tests.

## Validation and examples

```sh
python "<skill-dir>/scripts/pbi.py" check "<project-dir>" --format json
```

Resolve the helper from this skill's loaded directory and replace placeholders.
Example prompt: `Use $model-audit to audit metadata and relationship risks. Include
BPA only if an installed compatible engine is available; do not apply rule fixes.`

Return rule IDs, locations, severity, evidence, remediation and checks not run.

## References

Read [BPA integration](references/bpa.md) for the optional external engine workflow.
