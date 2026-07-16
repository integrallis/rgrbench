# Instrument audit — TDD dataset as a lab instrument

The dataset's intended role: the hand-written, test-first suites become the *oracle* for
evaluating agentic coding systems — requirements are derived from the tests (abstraction
raised to use-case/user-story level, never a reading of the code), a system under test
builds from those requirements, and the original TDD suites grade the result. An oracle is
only as good as its blind spots are small, so this audit measures the dataset the way failed
benchmarks taught the field to: validate the gold, measure the oracle, block the leaks.

## Criteria (each traced to a documented benchmark failure)

| # | Criterion | Field lesson |
|---|---|---|
| C1 | Gold validation: every suite passes against its reference implementation | SWE-bench audits found >60% of flagged tasks unsolvable as written |
| C2 | Determinism: outcomes identical across runs and test orders | flaky oracles misattribute failures to systems under test |
| C3 | Hermeticity: no network, no unseeded randomness, no environment coupling | irreproducible harnesses; results that vary by machine |
| C4 | Oracle strength: mutation kill rate per package | EvalPlus: weak tests silently overestimate every graded system |
| C5 | Runtime bounds: whole corpus in seconds | hung suites poison batch evaluation |
| C6 | Structure: 1:1 package↔tests mapping, standard layout, standard tooling | harnesses nobody else can run don't get reproduced |
| C7 | Leak hygiene: no benchmark identifiers, no absolute paths, no redistributable third-party content | contamination fingerprints; datasets pulled for licensing |

`instrument/test_gates.py` makes C1–C7 executable (`make gates`, ~2 s);
`make mutation` regenerates the C4 measurements.

## Measurements (2026-07-14)

- Kata corpus (2026-07, post-ingestion): **89 packages, 1,580 tests**, all passing in
  under a second; identical outcomes under randomized orders; passes with all network
  calls blocked; per-test 10 s timeout (D-5).
- FastAPI apps: 3 apps, 27 tests, all passing (after D-1).
- **Mutation testing (mutmut, 4,824 mutants): overall kill rate 0.981.** 4,731 caught; the
  92 survivors are all accounted for in `equivalent_mutants.md` (46 legacy + 45 ingestion
  equivalents with per-mutant justification, 1 harness artifact) — **100% of killable
  mutants are killed**. Per-package scores in `mutation_scores.json`; ratchet floors (89
  packages) in `mutation_floors.json`; provenance-labeled dataset card in `dataset.json`.
- Growth history: 35 packages / 334 tests / kill rate 0.842 at first audit → reference
  repairs and translation-repair campaign (0.966) → tddbuddy ingestion of 54 packages
  authored from paraphrased human specs, 314 fresh survivors triaged (268 killed, 45
  equivalent, 1 harness artifact) → 0.981.
- Two mutmut limitations discovered and handled: warm module-level lru_cache masking
  (kata_potter, documented) and unmutated decorated members/module data — the latter made
  two packages' oracles invisible until their logic was restructured into measurable pure
  functions (public APIs unchanged; the missing-score gate caught it).
- Line-coverage caveat (legacy audit): the original "100%" was partly pragma-masked —
  `Board.rotate_left` was blanketed in `# pragma: no cover` instead of tested (see D-9).
  Pragmas stripped, method tested; the two remaining uncovered lines are defensive guards
  unreachable from the public API, documented in the equivalence register.

## Requirements layer (2026-07)

The dataset carries a prompt-side artifact per package: `requirements/<pkg>.md`, user-story
level requirements **derived from the test suite only** (authors never open src/), under the
protocol in `requirements/PROTOCOL.md`, with five machine-checked gates
(`test_requirements_gates.py`): existence, full test-traceability (every test maps to a
defined acceptance criterion — 1,607/1,607 tests mapped), leakage (no code, paths, private
or implementation-only identifiers), structure, and hygiene. Corpus: 92 documents (89 kata
+ 3 FastAPI apps), 351 user stories, 1,283 acceptance criteria. Derivation judgment calls
are recorded per document batch; two worth knowing: poker_hands states the standard
nine-category ranking where tests evidence only two orderings (declared as the single
domain-knowledge fill), and lcd_digits' requirements expose that its suite only specifies
digits 0 and 1 — the requirements layer doubles as a spec-coverage audit of the tests
themselves.

## Findings register

| ID | Finding | Status |
|----|---------|--------|
| D-1 | `todo_app` missing pytest path config — suite could not collect | FIXED (pyproject section added; 11 tests pass) |
| D-2 | Unseeded `random` in `calculator_tdd_ebook`'s `Any` utility — nondeterministic oracle risk | FIXED (per-test deterministic seeding in tests/conftest.py; consider seedable `Any` later) |
| D-3 | Corpus packaged as a literal top-level package named `src` (`from src.kata import …`) — breaks standard tooling (mutmut), leaks `src.` into interfaces | FIXED (standard src layout; imports rewritten; 334 tests green) |
| D-4 | Oracle strength uneven: 10 packages < 0.80 kill rate; `decorator_examples` 0.00, `stack` 0.46, `password_verifier` 0.53 | FIXED — strengthening campaign (2026-07): 151 survivors killed by new behavior tests, 48 classified equivalent with per-mutant verification (`equivalent_mutants.md`); overall 0.842 → 0.953; floors ratcheted. Provenance: suites were hand-written in the katas' original languages and machine-translated in 2025, so this was translation repair — restoring assertions the translation dropped (return values, exact messages, boundaries) — not machine authorship of a human oracle |
| D-5 | 10 mutants only caught by timeout — suites had no per-test time guards | FIXED — pytest-timeout wired at 10 s per test in addopts |
| D-6 | Repo hygiene: 439 MB `alpha/` (AoC content not redistributable), run archives, legacy `evaluator/`/`vanilla/`/`scripts/`, planning docs | FIXED — moved to the private archive (`private-archive/tdd-dataset-py-legacy/`); repo now contains the dataset, the apps, and this instrument |
| D-7 | `benchmark/` (9 tasks) was a v0 whose oracles were LLM-generated — the self-grading weakness the research measures | FIXED — retired to the private archive with its generation scripts; the successor design uses the hand-written suites as oracles |
| D-8 | Toolchain drift: root is poetry (py >=3.10,<3.14), FastAPI apps are uv (py >=3.13), one app uses dependency groups vs two using extras | FIXED — uv everywhere, requires-python >=3.12, extras style unified, explicit pytest config per app |
| D-9 | 16 mutants reported neither killed nor survived by mutmut despite "100%" line coverage | FIXED — all 16 were `Board.rotate_left`, which had zero tests and was hidden from coverage with `# pragma: no cover` blankets (a 2025 green-checkmark artifact); pragmas stripped, method tested (3 tests), all 16 mutants now killed |
| D-10 | `word_wrap` reference implementation hardcoded literal return values for the two exact inputs its tests used — the 2025 translation overfitted the implementation to the test cases (the ugly-mirror pattern inside the dataset itself) | FIXED — rewritten against the canonical kata spec (break at last space within width; longer words split at width; newlines preserved); overfitted tests re-pinned. Provenance resolved (2026-07): the upstream C# original (garora/TDD-Katas, MIT) breaks exactly once — its counter never resets — so its quirky expected values were self-consistent; the 2025 translation added a counter reset, matched neither the original nor the canonical kata, and papered over the difference with hardcoded returns. This corpus deliberately follows the canonical kata, not the upstream quirk (recorded in THIRD_PARTY_NOTICES.md) |
| D-11 | `find_min`/`find_max` `get_*_with_one_or_more_arguments(x)` crash on exactly one argument, contradicting name and docstring | FIXED — `min((first, *args))`; single-argument behavior test-pinned |
| D-12 | `leap_year` implemented the wrong Gregorian rule: 1900 came out leap; the `% 100 != 0` conjunct was lost in translation | FIXED — canonical rule implemented; century years pinned both ways (1900/2100 not leap, 1600/2000 leap); package now kills 14/14 mutants |
| D-13 | Smaller reference/spec conflicts: darts double-out rules; calculator leading zero; money silent 1:1 conversion | FIXED — darts busts on non-double checkout to 0 and on reaching 1 regardless of darts left; calculator replaces a leading-zero display on the next digit; money raises KeyError on unregistered rate pairs; all pinned by tests, blocked equivalence entries resolved |
| D-14 | Cosmetic reference quirks pinned by tests, revisit if refs change: tetris 3-wide pieces sit one column right of center on odd-width boards; tennis displays winner's score as "0" post-win; odd_even classifies 0/negative evens as neither, `is_prime(2)` False masked by API | RECORDED |

## What the numbers mean for the research

A kill rate is the oracle's blind-spot measure: every surviving mutant is a way a wrong
generated implementation would be certified correct. After D-4 remediation the oracle's
numbers are: 0.953 raw kill rate, 98.8% of killable
mutants killed, and a per-package score + equivalence register shipping as dataset
metadata — any study using this oracle can report its measured blind-spot rate. That is the
difference between this instrument and the benchmarks it learns from: the oracle arrives
with its error bars. With D-10..D-13 repaired against the kata specs, D-9's coverage gaming removed, and the
corpus re-measured, no known defect remains open in the findings register.
