# Synthetic retail project

Open `Retail.pbip` in a compatible Windows Power BI Desktop build supporting PBIP,
TMDL and enhanced PBIR. Refresh locally to materialize two tiny M `#table` sources;
no account, network data source, absolute file path or credentials are embedded.

The model has Product (2 rows), Sales (4 rows), a many-to-one single-direction
Sales.ProductKey → Product.ProductKey relationship, and four measures. Revenue
and Cost source columns use separate names (`RevenueAmount`, `CostAmount`) to
avoid collisions with the measure names. A revenue-by-category chart binds Product
Category to the axis and the Revenue measure to the value role.

```sh
python scripts/pbi.py check examples/retail --strict
python scripts/validate_schemas.py examples/retail
python scripts/pbi.py dax examples/dax --strict
```

The first/third commands require Python only. Schema validation requires dev extras.
Run them from the toolkit root. The schema snapshot covers the exact `$schema`
versions used by these files; no schema URL is fetched at validation time.

Expected arithmetic for engine acceptance (not yet observed in Desktop):

| Scope | Revenue | Cost | Profit | Profit Margin |
| --- | ---: | ---: | ---: | ---: |
| All rows | 1600 | 1090 | 510 | 0.31875 |
| Bikes | 1500 | 1050 | 450 | 0.30 |
| Accessories | 100 | 40 | 60 | 0.60 |
| RevenueAmount = 0 | 0 | 0 | 0 | BLANK |
| Category = Missing | BLANK | BLANK | BLANK | BLANK |

Use `examples/dax/revenue-by-category.dax` and `examples/dax/edge-cases.dax`
in a DAX engine. Confirm filter propagation and that the total is a ratio of totals,
not the average of category margins. Reopen Desktop after external metadata edits.
Verify chart rendering, category labels, totals and interactions manually.

Static checks and eight JSON Schema validations passed locally on macOS. No Desktop
load, Microsoft serializer, refresh or DAX engine result has been verified. This is
an authored demo project awaiting those Windows acceptance checks, not a shipped PBIX.
