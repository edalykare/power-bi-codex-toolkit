---
name: dax-expert
description: Author, debug and review Power BI DAX measures or queries using model context and explicit result checks; use performance-analysis for measured timing comparisons.
---

# DAX expert

## Prerequisites and tools

Read the relevant model tables, relationships, storage modes, and existing measure
conventions. Python 3.11+ runs the bundled lexical checker. A connected Microsoft
Power BI Authoring MCP, Power BI Desktop, or DAX Studio is required to evaluate DAX.

## Workflow

1. Establish the business grain, expected totals, filters, BLANK/zero behavior and
   existing authorization to access the target model. Use the smallest relevant inventory.
2. Inspect dependent measures and relationships. Explain row context, filter context
   and context transition where they affect the answer. Check RLS assumptions.
3. Make the requested local change. Prefer qualified column references and clear
   variables; preserve useful existing naming and formatting. Use DIVIDE when the
   denominator can be zero or BLANK. A constant denominator can use `/`.
4. Run the helper's `dax` command for a .dax file, or `check` for a TMDL project.
   Review warnings; do not blindly replace operators or iterators to silence them.
5. If an authorized engine is available, evaluate baseline and candidate against
   totals, detail rows, empty selections, zero denominators and relevant security roles.
   Compare results before timing. Otherwise supply runnable EVALUATE queries and
   state that engine correctness and performance remain unverified.

## Validation and examples

Resolve this skill's directory from the loaded SKILL.md path. Run its helper by
absolute path, replacing the example placeholders before executing:

```sh
python "<skill-dir>/scripts/pbi.py" dax "<query.dax>" --strict
python "<skill-dir>/scripts/pbi.py" check "<project-dir>" --format json
```

Example prompt: `Use $dax-expert to fix Profit Margin for empty selections.
Preserve the current total semantics and provide engine test queries.`

Deliver the expression, assumptions, changed files, observed results and checks
not run. The lexer cannot validate function signatures, unqualified references,
filter behavior or query results. Never present a rewrite as faster without timings.

## References

Read [DAX checks and test design](references/dax-checks.md) when choosing test cases
or interpreting lint results. It links to Microsoft function and optimization docs.
