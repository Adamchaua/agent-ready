.PHONY: install test lint build check score refresh clean

PYTHON ?= python
AGENT_READY ?= agent-ready

install:
	$(PYTHON) -m pip install -e '.[dev]'

test:
	$(PYTHON) -m unittest discover -s tests -v

lint:
	$(PYTHON) -m ruff check .

build:
	$(PYTHON) -m build --sdist --wheel

check:
	$(AGENT_READY) . --check

score:
	$(AGENT_READY) . --score

refresh:
	$(AGENT_READY) . --write --force

clean:
	rm -rf build dist *.egg-info
