# CLI reference

Run `python scripts/pbi.py --help` from a checkout, or install the package and use
`pbi-codex`. `python -m pbi_codex` works after installation too. Runtime: Python
3.11+, standard library only. The schema validator is a separate development script.

| Command | Input | Output |
| --- | --- | --- |
| `check PATH` | Containing PBIP/PBIR/TMDL tree or individual file | Local diagnostics |
| `dax PATH` | .dax file or directory | Lexical diagnostics |
| `inventory PATH` | One TMDL model directory | JSON counts, objects, expressions and reader diagnostics |
| `docs PATH` | One TMDL model directory | Markdown table/column/measure/relationship inventory |
| `doctor` | None | Executable locations, Python version, platform; launches nothing |
| `fabric-plan PATH` | Local manifest JSON | Hashed definition inventory and unverified remote prerequisites |
| `compare-timings PATH` | Normalized timing JSON | Median samples and descriptive percentage changes |

All path commands accept `--output FILE` and `--force`. Parent output directories
are created; overwrites require `--force`. `check` and `dax` also accept
`--format text|json` and `--strict`. `--version` is a top-level option.

`0`: no blocking findings / successful inventory. `1`: diagnostic errors, or warnings
with `--strict`. `2`: invalid inputs, missing dependencies or I/O failures. An empty
input tree is not success. Inventory/documentation are reader operations, not a
complete semantic audit; run `check` separately.

JSON diagnostics have `code`, `severity`, `path`, `line` and `message`. Paths are
local source locations. Lines are 1-based; JSON structure findings currently point
to line 1, while common TMDL and DAX findings point to their declaration/expression.
Summaries explicitly mark engine and schema validation as not run by `check`.

## Finding families

| IDs | Meaning |
| --- | --- |
| `DAX000–002` | Empty input and lexical delimiter/quote/comment problems |
| `DAX101–102` | Division review and FORMAT-as-text advisory |
| `DAX201` | Unknown qualified table/member in an inventoried measure |
| `TMDL000–002`, `TMDL101` | Missing input, obvious nesting/fence issues, mixed indentation |
| `MODEL001`, `MODEL900` | Duplicate common declarations; inventory-only object kinds |
| `META101–103` | Missing measure metadata or explicit source-column type |
| `REL001–003`, `REL101` | Endpoints, differing types and bidirectional-filter review |
| `JSON001–002`, `JSON101` | Invalid/duplicate-key JSON, wrong top-level shape, schema URL advisory |
| `PATH001–003` | Missing targets/files or nonportable/out-of-root references |
| `PBIP001–002` | Missing/malformed report artifacts |
| `PBIR001–009`, `PBIR106` | Binding, page-order, identity and dimension checks |
| `PBIR900–901` | Remote binding unresolved or enhanced PBIR absent |

Metadata policies are intentionally advisory. A dynamic format string or intentional
bidirectional relationship can warrant keeping a warning. Strict mode is suitable
for controlled fixtures; teams should review warnings before adopting it universally.

## Schemas

```sh
python scripts/validate_schemas.py examples/retail
```

Requires `jsonschema` from `.[dev]`. Checks schema-bearing JSON only, verifies pinned
hashes and resolves only vendored schemas. An unknown schema URI fails without a
network request. Vendor new versions through `scripts/update_schemas.py` using a
separately reviewed local clone. This never downloads a URL supplied by a project.

## Fabric manifests and timing samples

See [Fabric examples](../examples/fabric/README.md) and
[timing examples](../examples/performance/README.md) for exact formats. These are
toolkit-specific local formats, not Microsoft deployment/trace-export standards.
