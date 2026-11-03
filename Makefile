# TxnVigil v2 — developer entry points (P0-T03; spec §22, ADR-0005).
# Tools run through uv by default. To use globally installed tools instead:
#   make lint RUN=
#   make lint RUN= PYRIGHT_ARGS="--pythonpath $$(which python3)"   # point pyright at an interpreter
# CI is the authoritative test runner (CP-0 D-E).

RUN ?= uv run
PY ?= python
PYRIGHT_ARGS ?=

.DEFAULT_GOAL := help
.PHONY: help sync lint fmt test test-unit trace up down clean

help: ## List targets
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-10s %s\n", $$1, $$2}'

sync: ## Create .venv with the dev dependency group (uv sync --group dev)
	uv sync --group dev

lint: ## ruff check, ruff format --check, pyright (strict on core/)
	$(RUN) ruff check .
	$(RUN) ruff format --check .
	$(RUN) pyright $(PYRIGHT_ARGS)

fmt: ## Auto-fix lint issues and format
	$(RUN) ruff check --fix .
	$(RUN) ruff format .

test: ## All tests with coverage (gate: 80% on core/, NFR-08)
	$(RUN) pytest --cov --cov-report=term-missing --cov-report=xml

test-unit: ## Unit tests only, no coverage
	$(RUN) pytest tests/unit

trace: ## Traceability check of docs/traceability.csv (warn mode; --strict from P2, T04)
	$(RUN) python scripts/check_traceability.py

up: ## Start the local stack (not yet available)
	@echo "compose arrives in P0-T05 (DLV-3)"

down: ## Stop the local stack (not yet available)
	@echo "compose arrives in P0-T05 (DLV-3)"

clean: ## Remove caches and coverage output
	$(PY) -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for n in ('__pycache__', '.pytest_cache', '.ruff_cache', 'htmlcov') for p in pathlib.Path('.').rglob(n) if '.venv' not in p.parts and 'node_modules' not in p.parts]; [p.unlink() for p in map(pathlib.Path, ('.coverage', 'coverage.xml')) if p.exists()]"
