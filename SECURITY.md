# Security

Do not post credentials, access tokens, connection strings or customer records in
issues. For a vulnerability, use the repository's private GitHub security reporting
feature if enabled. Otherwise contact a maintainer privately through their GitHub
profile before disclosing sensitive details; no private mailbox is advertised here.

The CLI reads local files and writes requested outputs. It does not execute DAX, M,
SQL, Python notebook cells, shell text from projects, or Fabric operations. Files
over 10 MiB are rejected by the ordinary input readers; discovered symlinks and
cache directories are skipped. Local project references cannot escape the chosen
root. These are guardrails, not an operating-system security sandbox.

Schema validation uses vendored, hashed schemas and never follows arbitrary remote
schema URLs. Review dependencies and external tools before installing them. MCP
servers run with their own account permissions; instruction-only reviewer agents
do not enforce a read-only tool capability. Use appropriate parent-session policies.

Model inventory JSON may include sensitive expressions/properties and local paths.
Review outputs before sharing. Keep secrets in approved credential stores and use
workload identities where your environment supports them. Never commit .pbi caches,
real PBIX files or tokens. The toolkit does not provide a comprehensive secret scanner.
