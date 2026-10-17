# Optional integrations

The offline CLI starts no servers, signs into no account and executes no remote
operation. The examples below are setup instructions reviewed against upstream
documentation, not evidence of a live connection. Configuration is never merged
automatically. See [sources](sources.md) for the review date and exact pages.

## Documentation MCP

Codex CLI and IDE share MCP configuration. Select only the servers needed, for example:

```sh
codex mcp add microsoftLearn --url https://learn.microsoft.com/api/mcp
codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp
codex mcp list
```

These change your local Codex configuration; run them intentionally. Microsoft
Learn serves public documentation, not tenant data. The
[official OpenAI setup](https://developers.openai.com/learn/docs-mcp) documents
its read-only docs endpoint. Review [native MCP configuration](https://learn.chatgpt.com/docs/extend/mcp)
before merging selected sections of [mcp.example.toml](../config/mcp.example.toml).
Trusted project configuration and organization requirements may affect availability.

## Power BI Authoring MCP

Microsoft's [Authoring MCP](https://learn.microsoft.com/en-us/power-bi/developer/mcp/power-bi-authoring-mcp)
provides live model authoring and DAX tools. The local server accesses Desktop or
local PBIP files; the hosted service cannot read your local files. The local server
does not support macOS. Select a supported Windows environment for Desktop work.

The documented local launcher uses the npm package `@microsoft/powerbi-modeling-mcp`
with `--start`. The disabled configuration template deliberately uses
`@REVIEWED_VERSION`: resolve a real version, review its publisher/release and package
requirements, replace that marker, then enable it. Do not silently execute `@latest`
as a reproducibility policy. First verify the server starts, discover its tools and
list the intended model's tables. This toolkit does not invent tool names or assume
the server's tool inventory is fixed.

Do not auto-accept a Microsoft EULA. If the installed release requires acceptance,
the user must review and explicitly authorize it. Verify Build/Write permissions,
XMLA/capacity and tenant settings for your chosen endpoint. Model authoring tools
are not report-page/visual editing tools.

The hosted authoring endpoint is documented as
`https://api.fabric.microsoft.com/v1/mcp/powerbi/authoring`. It requires Entra OAuth;
some clients' dynamic OAuth registration assumptions are incompatible. A copied URL
does not establish a working Codex sign-in. Follow Microsoft's external-client app
registration guidance and your organization's policies; hosted authentication and
session persistence were not integration-tested here.

## Fabric CLI

Install in a separate environment if desired:

```sh
python -m pip install ms-fabric-cli
fab --help
fab auth status
fab auth login
fab ls
fab api workspaces -X get
```

The package name, login and read-only API syntax follow
[Fabric CLI documentation](https://microsoft.github.io/fabric-cli/). Check your
installed help and record its version before using further commands. Review
authentication, target workspace identity and permissions before making changes.
Use the official workload-specific import/deployment APIs rather than assuming
arbitrary SQL/Python files can be uploaded as Fabric item definitions.

`fabric-plan` is an offline proposal only. It hashes supported local text files,
does not resolve all dependencies, and has no execute/apply command. The manifest's
workspace is a review target, not a verified ID. Use explicit authorization for
deployment, refreshes, jobs or destructive operations; prepare actual payloads first.

## Fabric local MCP

Microsoft [documents](https://learn.microsoft.com/en-us/rest/api/fabric/articles/mcp-servers/pro-dev-local/get-started-local)
the `@microsoft/fabric-mcp` launcher with `server start --mode all`. The corresponding
TOML example is disabled until a reviewed version is inserted. Discover its current
tools and auth requirements in the target environment. Tenant connectivity and
individual workload operations were not tested by this project.

## Tabular Editor and BPA

Tabular Editor is optional. CLI syntax, licensing and supported model formats differ
between TE2, TE3 and the newer `te` CLI. Consult the installed tool's help and
[vendor documentation](https://docs.tabulareditor.com/te2/Command-line-Options.html).
The [model-audit reference](../.agents/skills/model-audit/references/bpa.md) gives a
TE2 BIM analysis example. Two original rules are supplied, but were not evaluated
by a live BPA engine. No full BPA engine or community rule pack is vendored.

## Acceptance record

Before marking an adapter operational, retain sanitized evidence of tool/package
version, OS, target type, authentication method, read-only smoke query, intended
mutation test on a disposable target, verification and rollback. The current release
has only the local validations listed in [validation.md](validation.md).
