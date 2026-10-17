# PBIR checks and authoring

Local checks parse JSON strictly (including duplicate keys), verify PBIP artifact
paths and byPath bindings, page ordering, folder/name identity and basic dimensions.
They do not validate visual query semantics, all resource paths, themes, bookmarks,
layout overlaps or Microsoft JSON schemas. byConnection is reported as unresolved.

Use a current Desktop-created PBIR visual as an editable baseline. Common visual
container fields include name, position and a visual object; nested properties vary
by schema version and visual type. Preserve IDs used by bookmarks/interactions.
Modeling MCP and report authoring are separate capabilities.

- [PBIP overview](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
- [Report folder and schemas](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report)
- [Microsoft schema source](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report)
- [Power BI accessibility](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports)
