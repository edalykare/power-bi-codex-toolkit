---
name: fabric-development
description: Develop local Microsoft Fabric lakehouse, warehouse, notebook, pipeline or dataflow artifacts and prepare workspace deployment reviews with Fabric CLI or MCP when available.
---

# Microsoft Fabric development

## Prerequisites and tools

Python 3.11+ runs the offline plan helper. Live operations require an installed
Fabric CLI (`ms-fabric-cli`, executable `fab`) or configured official Microsoft MCP,
Entra authentication, the right workspace permissions and workload capacity.

## Workflow

1. Identify workload, workspace and item; inspect local definitions and dependencies.
   Choose the relevant section of the Fabric reference rather than loading all docs.
2. Make requested local SQL, PySpark, notebook or item-definition changes. Validate
   syntax using the appropriate tooling; static Python compilation does not run Spark.
3. For live discovery, inspect `fab --help`, `fab auth status` and relevant command
   help. List only the scoped metadata needed. Do not print access tokens or data rows.
4. Prepare an offline `fabric-plan` from a manifest. It hashes supported local files
   for review; it is not an importable item definition, remote diff or executable plan.
5. Before a deployment, refresh, notebook/pipeline run or destructive operation,
   resolve the exact remote target and present the actual command/API payload,
   dependencies, expected effects and rollback. Obtain explicit authorization unless
   already granted for that action and target. Stop on denied permissions.
6. After an authorized operation, follow documented long-running-operation headers,
   bounded polling and failure details. Do not retry a non-idempotent create blindly.

## Validation and examples

```sh
python "<skill-dir>/scripts/pbi.py" fabric-plan "<manifest.json>"
python "<skill-dir>/scripts/pbi.py" doctor
```

Resolve the helper from this skill's path and replace placeholders.
Example prompt: `Use $fabric-development to review the local Warehouse SQL and
prepare a deployment proposal for Retail Development. Do not execute remote jobs.`

Deliver local validation results, dependency order, target proposal and unverified
live prerequisites. Dataflows and pipelines are covered as reviewed definitions;
no remote deployment or execution adapter is bundled.

## References

Read [Fabric tools and workload choices](references/fabric.md) for the selected workload.
