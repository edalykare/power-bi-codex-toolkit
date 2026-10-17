---
name: performance-analysis
description: Investigate Power BI query or model performance using measured DAX timings, equivalent result checks and explicit cache/model context; compare normalized samples locally.
---

# Performance analysis

## Prerequisites and tools

A real model connection and DAX Studio, Performance Analyzer or an appropriate
Microsoft trace tool is required to capture measurements. Python 3.11+ can compare
normalized timing samples after capture. The helper does not collect traces.

## Workflow

1. Establish the slow interaction/query, storage mode, data volume, engine/model
   version, security context, concurrency and reproducible filter state.
2. Capture a baseline with explicit warm/cold-cache conditions. Separate visual,
   DAX, formula-engine, storage-engine and external source time when available.
3. Form one testable hypothesis and make a focused local candidate change. Compare
   result sets (including totals and BLANKs) before comparing timings.
4. Collect at least three samples per case and version under comparable conditions.
   Normalize to the documented JSON structure and run `compare-timings`.
5. Report medians and sample counts with provenance and variability concerns. A
   descriptive change percentage is not a statistical significance test or a capacity estimate.

## Validation and examples

```sh
python "<skill-dir>/scripts/pbi.py" compare-timings "<timings.json>"
```

Resolve the helper from this skill's path. Example prompt: `Use $performance-analysis
to compare these baseline and candidate measurements after checking result equivalence.
Separate warm and cold cache results and identify missing evidence.`

Return the hypothesis, measured outcomes and limitations. Never fabricate timings.

## References

Read [timing input and measurement design](references/timings.md) before normalizing data.
