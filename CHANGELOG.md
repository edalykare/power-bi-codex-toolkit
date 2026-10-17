# Changelog

## Unreleased

- Fix `doctor` launching an implicit system probe on Windows with Python 3.11.
  Read the OS identifier from interpreter metadata and retain the no-subprocess check.
- Add regression coverage for Windows, macOS and Linux platform reporting without OS probes.

## 0.1.0 — 2026-10-17

- Initial Codex-native alpha with nine modular skills and two optional custom agents.
- Dependency-free offline CLI: DAX lexical checks, TMDL inventory/model checks,
  PBIP/PBIR structure checks, Markdown documentation, timing comparison and Fabric proposals.
- Selective skill installer with bundled helper source and no-overwrite behavior.
- Synthetic retail PBIP/PBIR/TMDL demo, DAX engine queries and Fabric examples.
- Pinned Microsoft JSON schemas and offline schema verification.
- Automated regression tests, three-OS CI, pre-commit configuration and contributor docs.
- Live engine, Desktop rendering, BPA and Fabric deployment remain external checks.
