# Codex Instructions

Repository: `agent-ready`

## Operating Mode

- Work as a careful coding agent.
- Preserve user changes.
- Prefer targeted edits over rewrites.
- Run practical verification before final response.

## Detected Stack

- Languages: `Python`
- Frameworks: not detected
- Package managers: `Python/pyproject`

## Commands

Test:
```bash
python -m unittest discover -s tests -v
```

Build:
```bash
python -m build --sdist --wheel
```
```bash
make
```

Lint:
```bash
python -m ruff check .
```

## Files To Inspect First

- `.github/workflows/ci.yml`
- `Makefile`
- `README.md`
- `pyproject.toml`
