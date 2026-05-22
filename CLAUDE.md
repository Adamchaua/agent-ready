# Claude Code Instructions

Repository: `agent-ready`

Use this as the first context file when working in Claude Code.

## What To Know

- Main languages: `Python`
- Frameworks: not detected
- Key directories: `agent_ready`, `docs`, `.github`, `assets`, `tests`
- Risk areas: `deployment`

## Verification Commands

Test:
```bash
python -m unittest discover -s tests -v
```

Build:
```text
not detected
```

Lint:
```text
not detected
```

## Claude-Specific Rules

- Do not run destructive shell commands without explicit user approval.
- Before editing, locate the relevant tests or examples.
- Keep changes minimal and explain verification clearly.
- Avoid broad refactors unless the task explicitly asks for them.
