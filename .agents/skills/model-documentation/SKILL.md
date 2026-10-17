---
name: model-documentation
description: Generate and review a local Markdown or JSON inventory of Power BI TMDL tables, columns, measures and relationships without exposing source credentials or evaluating code.
---

# Model documentation

## Prerequisites and tools

Use a local TMDL model definition and Python 3.11+. No model connection is needed.
Inventory output contains expressions and properties; inspect it for customer data
or credentials before sharing. Prefer the Markdown output when expressions are unnecessary.

## Workflow

1. Select the requested model definition, not every model in a mono-repository.
2. Run `inventory` for machine-readable metadata or `docs` for a Markdown object list.
3. Review business descriptions, relationship direction and missing metadata. Preserve
   source descriptions and label newly inferred business meaning as an assumption.
4. Check generated output against source objects, review sensitive content and share
   only the requested scope. The generator does not document all RLS/OLS semantics,
   M lineage, visual dependencies or data values.

## Validation and examples

```sh
python "<skill-dir>/scripts/pbi.py" docs "<model-definition-dir>" --output "<inventory.md>"
python "<skill-dir>/scripts/pbi.py" inventory "<model-definition-dir>"
```

Resolve this skill's helper and replace placeholders. Output files are not overwritten
unless `--force` is explicitly passed. Example prompt: `Use $model-documentation to
write an inventory for the Retail model and flag descriptions needing business review.`

Return the artifact path, object counts and documentation gaps.

## References

- [TMDL object metadata](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview)
- [Inventory limits](references/documentation.md)
