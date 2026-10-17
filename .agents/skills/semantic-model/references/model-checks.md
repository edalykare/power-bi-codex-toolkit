# Model checks

The helper checks duplicate table/column/measure names (case insensitive), qualified
measure-expression references, missing measure format/folder/description, relationship
endpoints and type mismatches. Bidirectional filtering is a review warning, not a
universal error. Dynamic format strings and partial declarations need engine review.

TMDL supports declarations across files; an advanced partial-definition model can
produce duplicate-name findings in this lightweight inventory. Inspect those findings
with Microsoft's serializer rather than deleting legal declarations.

With an engine, inspect duplicate dimension keys and blank/unmatched fact keys using
COUNTROWS, DISTINCTCOUNT and EXCEPT in a bounded diagnostic query. RLS tests must use
the effective role/identity; an unrestricted query does not validate role behavior.

- [Star schema guidance](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)
- [Model relationships](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand)
- [RLS](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security)
- [Direct Lake](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview)
