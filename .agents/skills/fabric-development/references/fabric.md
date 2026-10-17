# Fabric tools and workloads

Install Fabric CLI in a separate environment with `python -m pip install ms-fabric-cli`,
then inspect `fab --help`. User login is `fab auth login`; read-only discovery examples
are `fab auth status`, `fab ls` and `fab api workspaces -X get`. Verify identity and
workspace IDs before requesting a mutation. Do not embed credentials in arguments,
tracked files or generated plans. Use the organization's approved authentication flow.

The offline manifest uses version: 1, workspace and items. Each item has name, type
and a local source under the manifest directory. Supported type labels are Lakehouse,
Warehouse, Notebook, DataPipeline, Dataflow, SemanticModel and Report. A recognized
label does not prove an item is importable or its API is enabled. Only supported text
files are hashed, not a complete deployment dependency closure. No command is executed.

Workload checks:
- Lakehouse: Spark schema, Delta compatibility, OneLake access, key quality and attachment.
- Warehouse: supported T-SQL, schema names, grants, transaction behavior and endpoint.
- Notebook: attachment, environment/packages, parameter contracts and job cost.
- Pipeline: activity dependencies, connections, parameters, retry/idempotency and secrets.
- Dataflow: destination, gateway, connection bindings, M transformations and refresh support.

Use item-specific APIs for definitions; validate base64 payloads and the current
supported item type. Separate import/deployment from job execution. For long-running
operations, honor the documented operation URL and Retry-After; cap polling and report
operation IDs without secrets. Do not estimate capacity cost from wall time alone.

- [Fabric CLI](https://microsoft.github.io/fabric-cli/)
- [Fabric REST APIs](https://learn.microsoft.com/en-us/rest/api/fabric/articles/)
- [Local Fabric MCP](https://learn.microsoft.com/en-us/rest/api/fabric/articles/mcp-servers/pro-dev-local/get-started-local)
- [Lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview)
- [Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing)
- [Data Factory](https://learn.microsoft.com/en-us/fabric/data-factory/data-factory-overview)
