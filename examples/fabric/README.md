# Local Fabric examples

`manifest.json` is a **toolkit-specific proposal format**, not a Microsoft item
definition or deployable manifest:

```json
{
  "version": 1,
  "workspace": "Retail Development.Workspace",
  "items": [{"name": "Retail", "type": "Notebook", "source": "notebooks/retail-quality.py"}]
}
```

```sh
python scripts/pbi.py fabric-plan examples/fabric/manifest.json
```

The output hashes supported local files, lists the proposed target and identifies
unverified live prerequisites. Sources must remain under the manifest directory.
Allowed type labels: Lakehouse, Warehouse, Notebook, DataPipeline, Dataflow,
SemanticModel and Report. Type recognition is not API/import validation.
There is no apply command, network access, authentication or remote mutation.

`notebooks/retail-quality.py` is a PySpark cell/function example requiring an attached
lakehouse and a Sales table. `warehouse/retail-quality.sql` is a read-only T-SQL query
requiring an existing dbo.Sales table. These standalone source files are not full
Fabric item definitions. Python syntax compilation was checked; Spark/SQL execution
was not. Resolve actual schemas, permissions, connections, environment and capacity
in the target workspace before preparing an authorized job or deployment.

For pipelines/dataflows, inspect their current item definitions and connection
bindings using supported Microsoft tools. The skill covers their review workflow;
this release does not fabricate untested item JSON or execute their jobs.
