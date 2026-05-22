# Changelog

## v0.1.0 - Initial Agent-Ready Release

### Added

- CLI scanner for local repositories.
- Generated agent context outputs: `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `.agent/context.json`, and `.agent/checklist.md`.
- `--check` drift gate for CI.
- `--score` agent-readiness score with JSON support.
- Python package, build, lint, test, CI, and Makefile workflow.
- GitHub Action metadata for marketplace usage.
- Product research, architecture diagram, hero image, and demo output asset.

### Verified

- `agent-ready . --score` returns `100/100 (A)` for this repo.
- Unit tests, Ruff lint, generated context check, and package build pass locally.
