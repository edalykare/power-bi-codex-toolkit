# Technical limits

This is an alpha toolkit with tested local automation. Its domain skills guide
Codex; a skill's presence is not proof that an external tool or tenant is available.

## DAX and TMDL

The lexer is not a DAX grammar or evaluator. It does not resolve unqualified names,
function signatures, query scopes, context transition, UDFs or security behavior.
Qualified member checks apply only to extracted measure expressions and a supplied
complete model inventory. New syntax may require the Microsoft engine.

The TMDL reader handles common named declarations and scalar properties. It is not
a lossless serializer or compiler. Advanced partial declarations, multiline property
values, calculation groups, dynamic formats, roles, OLS/RLS, translations and nested
expression forms need Microsoft serializer/engine review. Legitimate partial
declarations and dynamic formatting can produce local duplicate/metadata warnings.
The reader never modifies source files to make them fit its inventory.

Relationship checks verify endpoint existence, scalar type differences and filter
direction metadata only. They cannot prove actual one-side uniqueness, unmatched
keys, relationship ambiguity, cardinality, storage compatibility or RLS propagation.
No performance improvement is established by a linter warning or a DAX rewrite.

## PBIP and PBIR

The local checker covers selected structural invariants, not the entire schema.
The separate JSON Schema script covers the demo's pinned versions, not arbitrary
future versions. It validates only documents declaring a vendored `$schema`.
Visual queries, bookmarks, theme resources, all identity references and report-level
measure dependencies are not exhaustively resolved. Desktop rendering and manual
interaction/accessibility checks remain required.

PBIX/PBIT files are not unpacked. Remote byConnection bindings are explicitly
unresolved. Paths leaving the chosen validation root are rejected even if legitimate
in a larger repository; rerun against the common containing directory. Cache folders
and discovered symlinks are skipped. Individual files over 10 MiB are rejected.

## Installation and packaging

Skills require Python 3.11+ to run helpers. The installer supports repository/user
scope but no automatic upgrades or global MCP configuration. Existing skill folders
are preserved. It preflights/stages the entire selection, then renames folders one
by one; interruption/concurrent modification can leave a subset installed. Inspect
the destination and rerun only missing skills in that situation.

The wheel installs CLI code only. Skill installation, schemas and examples use the
checkout or full source distribution. `doctor` discovers executable paths; it does
not establish version compatibility, successful login or service availability.

## External environments

Live DAX/TMDL compilation, Desktop opening/rendering, full BPA evaluation, Spark,
SQL endpoint execution, MCP authentication and Fabric remote operations were not
tested in this macOS environment. CI is configured for Windows/macOS/Linux; its
hosted runs have not occurred merely because local tests passed. No remote operation
is part of ordinary CI, no OpenAI model invocation is needed, and no cost estimate
is inferred from synthetic timings.

Paginated reports, Deneb/Python/R/SVG/custom visual generators, live query listeners,
Databricks/data-app panes, tenant/capacity administration and full deployment adapters
from the reference are deferred. See [reference analysis](reference-analysis.md).
