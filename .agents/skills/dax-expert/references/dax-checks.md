# DAX checks and test design

The helper checks empty input, unclosed strings/comments/identifiers and unmatched
parentheses/braces. It emits a division warning and FORMAT advisory. It accepts
expressions and queries; it does not distinguish a valid measure from a valid query.
Qualified references are checked only when running a complete TMDL model check.
Bare [Name] can denote a measure or a row-context column, so it is not resolved.

Write a result matrix for total, each relevant group, a filtered subset, an empty
subset, BLANK inputs, and zero denominators. Test non-additive ratios at the total
level. For time intelligence, verify the date table, date relationships and calendar.
For CALCULATE rewrites, consider overwrite versus intersection (KEEPFILTERS).
Boolean filter arguments have restrictions; FILTER can be necessary.

Authoritative references:
- [CALCULATE](https://learn.microsoft.com/en-us/dax/calculate-function-dax)
- [DIVIDE versus /](https://learn.microsoft.com/en-us/dax/best-practices/dax-divide-function-operator)
- [Filter arguments](https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-avoid-filter-as-filter-argument)
- [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries)
