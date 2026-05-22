# Release v0.1.0

## Summary

`agent-ready` makes repositories easier and safer for AI coding agents by generating durable onboarding context and CI drift checks.

## Highlights

- Generate `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `.agent/context.json`, and `.agent/checklist.md`.
- Run `agent-ready . --check` in CI to detect stale agent context.
- Run `agent-ready . --score` to measure agent-readiness.
- Use the included GitHub Action to add agent-readiness checks to any repository.

## Proof

```bash
agent-ready . --score
# agent-readiness: 100/100 (A)

agent-ready . --check
# agent-ready files are current
```

## Suggested GitHub Release Title

`v0.1.0 - CI for AI coding context`
