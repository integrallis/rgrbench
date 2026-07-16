# Evaluation harness protocol

How a system under evaluation is graded against a package's oracle suite.

## Roles

- **Candidate**: the implementation the system built from `requirements/<pkg>.md`. It has
  its own API — the requirements deliberately specify behavior, not signatures.
- **Adapter**: a thin mapping layer that exposes the candidate under the names and
  signatures the oracle tests import. It may rename, re-export, reorder or forward
  arguments, and wrap or construct the candidate's own types. It must never compute,
  decide, or store domain state: the candidate must be the only source of behavior.
- **Oracle**: the package's verified test suite, run unmodified against the adapted
  candidate.

## The no-cheating property, enforced two ways

1. **Static constraints** (`adapter_check.py`): adapter modules may contain imports,
   assignments of aliases, class definitions whose methods only delegate, and functions
   whose bodies are a single return/delegation. Control flow (`if`/`for`/`while`/`try`),
   arithmetic and comparison operators, and comprehensions are forbidden. Size is capped.
   Violations fail the evaluation before anything runs.
2. **Candidate-execution check**: coverage measurement during the oracle run must show
   candidate code executing whenever tests pass. Passing tests that execute zero candidate
   lines mean the adapter is supplying behavior — the evaluation is rejected outright.
3. **Transparency by screened fault injection**: the harness injects single faults
   (operator flips, constant nudges) into a copy of the candidate, targeting only lines
   the passing tests execute. Each fault is first SCREENED for behavioral effect at the
   candidate boundary: the oracle run is traced (every call into and return out of
   candidate code, per test), and a fault whose boundary trace is identical to baseline on
   the passing tests is behaviorally neutral — it carries no signal about the adapter and
   is discarded, with replacement sampling until enough behavior-changing faults are
   found. Transparency = detected / behavior-changing faults. A fault that demonstrably
   changes candidate behavior without changing any oracle outcome is the opacity evidence
   that counts. If no behavior-changing fault can be found, the result carries an
   "insufficient transparency signal" note instead of an accusation. Evaluations below
   the threshold are rejected, not scored. The trace comparison happens beneath the
   adapter, so an adapter cannot influence its own screening.

## Grading

`evaluate.py` assembles a workspace (candidate package + adapter modules + the oracle test
file), runs pytest, and emits machine-readable results: per-test pass/fail, pass fraction,
the static-check verdict, and the transparency score. A package's result is only
comparable when reported alongside the oracle's own measured blind-spot rate
(`mutation_kill_rate` in `dataset.json`).
