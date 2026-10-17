# Normalized timing input

The helper accepts a toolkit-specific interchange format, not native Performance
Analyzer or DAX Studio exports:

```json
{"version":1,"cases":[{"name":"Warm cache, category totals","baselineMs":[120,125,122],"candidateMs":[100,101,99]}]}
```

Record capture-tool version, model commit, query text/hash, cache state, role,
connection mode and machine/capacity alongside it. Use separate cases for different
cache states and workloads. Do not mix warm and cold samples in one median.
`changePercent = (candidate median / baseline median - 1) * 100`; negative is faster.
Synthetic example values are demonstrations, not performance evidence.

- [Performance Analyzer](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-performance-analyzer)
- [DAX Studio server timings](https://daxstudio.org/docs/features/traces/server-timings-trace/)
