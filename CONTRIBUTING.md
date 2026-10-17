# Contributing

Start with a focused issue or pull request describing the observed behavior, desired
result and relevant Power BI/Fabric versions. Use synthetic fixtures, not tenant data.

1. Use Python 3.11+ and create a virtual environment.
2. Install development tooling: `python -m pip install -e ".[dev]"`.
3. Run the checks in the README before proposing a change.
4. Add regression tests for new parser/check behavior and failure cases. Do not
   expand a heuristic into an undocumented language parser.
5. Update the capability matrix, CLI docs and changelog when behavior changes.

Keep skills narrowly triggered, independently installable and concise. Put detailed
mode-specific guidance in linked references. Do not add required global settings,
model pins, hidden hooks, auto-installers or unconditional cloud operations.

Preserve unsupported TMDL properties and describe engine validation requirements.
Use the exact schema version a report declares. To refresh vendored schemas, clone
Microsoft's source separately, review its commit/license, run
`python scripts/update_schemas.py /path/to/json-schemas`, inspect the diff, then run
schema checks and tests. Remove obsolete schema files only after reviewing callers.

The source reference inventory is historical evidence, not an auto-sync mechanism.
Attribute all imported/adapted material and confirm license compatibility. Your
contributions are distributed under this repository's GPL-3.0-only license, except
third-party material retaining its documented upstream terms.

Do not claim live Power BI/Fabric support based only on offline tests. Include exact
tool versions, sanitized evidence and the environment when reporting integration
validation. Do not accept an EULA or publish/deploy on behalf of another person.
