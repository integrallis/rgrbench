# RGRBench

**RGRBench** (Red–Green–Refactor Bench) is a Python TDD kata corpus built to serve as a
**benchmark oracle for agentic coding systems** — and the first such dataset that ships with
its own measured error bars.

Each of the **89 kata packages** pairs a reference implementation with a verified test
suite; **3 FastAPI applications** add integration-first examples. A system under evaluation
receives a package's **requirements document** (user-story level, derived from the tests
alone) and is graded by the package's **test suite** — an oracle it never sees.

## The numbers

| | |
|---|---|
| Kata packages | 89 (three difficulty tiers) |
| Kata tests | 1,580 — plus 27 FastAPI integration tests |
| Mutation score | **kill rate 0.981** over 4,824 mutants |
| Surviving mutants | 92, **every one classified** (91 proven behaviorally equivalent, 1 documented harness artifact) — 100% of killable mutants killed |
| Requirements | 92 documents, 351 user stories, 1,283 acceptance criteria |
| Traceability | **1,607/1,607 tests** mapped to acceptance criteria, machine-checked |
| Suite runtime | < 1 s (katas); order-independent; network-blocked; 10 s/test cap |

Per-package scores, tiers, sources, and provenance labels live in
[`dataset.json`](dataset.json) — the machine-readable dataset card.

## Layout

```
src/<package>/            reference implementation (one kata per package)
tests/test_<package>.py   the verified test suite — the oracle
requirements/<package>.md user-story requirements derived from the tests only
requirements/PROTOCOL.md  the derivation contract (enforced by gates)
requirements/apps/        requirements for the FastAPI applications
fastapi-tdd-examples/     three integration-first web applications
instrument/               what makes this a lab instrument:
  test_gates.py             corpus gates (gold validation, order independence,
                            hermeticity, runtime caps, structure, leak hygiene,
                            mutation-score ratchet)
  test_requirements_gates.py  requirements gates (traceability, leakage, structure)
  mutation_scores.json      per-package mutation measurements
  mutation_floors.json      ratchet floors — regressions fail the gates
  equivalent_mutants.md     per-mutant equivalence register with justifications
  AUDIT.md                  the audit record: criteria, measurements, findings
dataset.json              machine-readable dataset card
```

## Quickstart

```bash
uv sync --group dev        # or: make sync
make test                  # kata corpus (1,580 tests, < 1 s)
make gates                 # instrument gates (~5 s, no network needed)
```

FastAPI apps (each is its own uv project):

```bash
cd fastapi-tdd-examples/todo_app && uv sync --extra test && .venv/bin/python -m pytest -q
```

Regenerating measurements after changing code or tests:

```bash
make mutation              # minutes; then update floors deliberately
make manifest              # refresh dataset.json
```

## Using the dataset to evaluate a system

1. Give the system `requirements/<package>.md` (never the tests or the reference).
2. Let it build an implementation.
3. Run the package's test suite against the produced code (an adapter may map interfaces,
   but must never repair the implementation).
4. Report results alongside the package's `mutation_kill_rate` from `dataset.json` — the
   oracle's own measured blind-spot rate.

Provenance matters for study design: `dataset.json` labels each package either
`translated-human-tests` (35 packages — suites hand-written upstream, machine-translated,
then translation-repaired and mutation-hardened) or `machine-from-human-spec` (54 packages —
authored from human-written kata specifications). Stratify or subset accordingly.

## Determinism guarantees

No test or implementation touches the network, the filesystem, the system clock, or
unseeded randomness: time-dependent katas take injected clocks/dates, randomness is
injected or seeded, and the gates enforce hermeticity by blocking sockets during the run.

## Provenance and licensing

Original code and documents are MIT (see `LICENSE`). Kata concepts are long-standing
community material; verified upstream sources are credited in
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) and per-file docstrings, and documented
divergences from upstream (reference-defect repairs) are recorded in
`instrument/AUDIT.md`.
