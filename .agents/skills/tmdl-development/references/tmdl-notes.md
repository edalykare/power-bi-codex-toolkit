# TMDL editing notes

The toolkit inventories common table, column, measure, partition and relationship
objects. Other recognized declarations are inventory-only. It reads simple property
lines and descriptions and preserves expression text in memory. It never serializes
or rewrites a file. Mixed indentation and unclosed expression fences are diagnostics.

It is not a complete grammar. Partial declarations, advanced multiline properties,
calculation groups, UDFs, cultures, roles and perspectives require Microsoft's
serializer and engine. Do not use a clean local result as a compilation certificate.

Example (tab indentation in an existing table):

```tmdl
    /// Margin at the current filter context.
    measure 'Profit Margin' = DIVIDE([Profit], [Revenue])
        formatString: 0.0%
        displayFolder: Sales
```

The indentation above illustrates nesting; match the actual file's tab/space style.
Multiple consecutive `///` lines may form a multiline description; do not collapse
or reject them merely because there is more than one line.

- [TMDL specification and serializer](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview)
- [PBIP semantic model folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset)
