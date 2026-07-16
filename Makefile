# tdd-dataset-py — dataset and instrument targets (uv-based)

.PHONY: help sync test test-apps gates mutation manifest format lint all

help:
	@echo "  sync       - create/refresh the venv (uv sync --group dev)"
	@echo "  test       - run the kata corpus test suite"
	@echo "  test-apps  - run the FastAPI app suites (needs per-app venvs; see README)"
	@echo "  gates      - run the instrument quality gates (structure, hermeticity,"
	@echo "               order independence, oracle ratchet, requirements + harness)"
	@echo "  mutation   - full mutation run + score export (minutes; ratchet floors"
	@echo "               deliberately afterwards)"
	@echo "  manifest   - regenerate dataset.json from scores and requirements"
	@echo "  format     - black + isort"
	@echo "  lint       - ruff + mypy"
	@echo "  all        - test + gates"

sync:
	uv sync --group dev

test:
	.venv/bin/python -m pytest tests/ -q

test-apps:
	@for app in fastapi-tdd-examples/*/; do \
		( cd $$app && .venv/bin/python -m pytest tests/ -q ) || exit 1; \
	done

gates:
	.venv/bin/python -m pytest instrument/ harness/tests -q

mutation:
	rm -rf mutants && .venv/bin/mutmut run && .venv/bin/python instrument/export_scores.py

manifest:
	.venv/bin/python instrument/make_manifest.py

format:
	.venv/bin/black src tests instrument && .venv/bin/isort src tests instrument

lint:
	.venv/bin/ruff check src tests instrument && .venv/bin/mypy src

all: test gates
