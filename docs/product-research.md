# Product Research: agent-ready

## Market Signal

AI coding agents are moving from novelty to everyday engineering workflow. Teams now maintain `AGENTS.md`, `CLAUDE.md`, Cursor rules, Copilot instructions, and other tool-specific context files by hand. The demand is not simply for another template generator; it is for a reliable way to keep repo-agent instructions accurate as code changes.

Examples of adjacent demand signals include popular repositories and tools around `AGENTS.md`, repo-to-prompt packing, repo ingestion, Claude/Cursor rule templates, and AI-native onboarding docs.

## User Pain

- Agent instructions drift after package, CI, or architecture changes.
- Every coding agent expects slightly different context files.
- New agents waste time rediscovering build/test commands and repo boundaries.
- Teams need guardrails around secrets, generated files, migrations, deployments, and high-risk code.
- Human READMEs describe the product, but agents need operational instructions.

## Positioning

**agent-ready is CI for AI coding context.**

It scans a repository, extracts evidence-backed commands and risk areas, then generates durable onboarding files for coding agents.

## Wedge

Start with a CLI that generates and checks `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, and `.agent/context.json`. Grow into a GitHub Action or app that comments on PRs when agent instructions drift.

## Differentiators

- Multi-agent output, not one vendor file.
- Evidence-based scanner, not generic templates.
- Drift check via `agent-ready --check`.
- Safety-first defaults for secrets, generated files, vendor folders, and deployment surfaces.
