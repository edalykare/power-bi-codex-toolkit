# Timing comparison format

`timings.json` contains **synthetic samples**, not actual Power BI measurements.

```sh
python scripts/pbi.py compare-timings examples/performance/timings.json
```

The toolkit format uses `version: 1` and a nonempty `cases` array. Each case has a
unique nonempty `name`, plus `baselineMs` and `candidateMs` arrays of at least three
positive finite numbers. The helper reports sample counts, medians and
`(candidate median / baseline median - 1) * 100` as changePercent. Negative means
lower median duration. This is a descriptive summary, not a significance test.

Normalize captured samples yourself. This is not a native DAX Studio or Performance
Analyzer export parser. Keep cache state, query, model commit, role, data volume,
capture-tool version, connection mode and concurrency with the data. Use separate
cases for different cache states; verify result equivalence before timing a rewrite.
