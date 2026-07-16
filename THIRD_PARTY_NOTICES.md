# Attributions

The kata corpus ports classic, community-standard TDD exercises — material replicated in
essentially every programming language. Verified upstream sources:

- **garora/TDD-Katas** (github.com/garora/TDD-Katas, MIT) — the C# collection most of the
  kata suites were translated from: Bowling Game, FizzBuzz, LCD Digits, Mine Fields,
  Odd/Even, Password Verifier, String Calculator, String Sum, Calc Stats, Leap Year,
  Natural String Sorting, Prime Factor, Recently Used List, Word Wrap (per-file docstrings
  name the original .cs files; verified via the shared test fixtures, typos included).
- **danidemi/tutorial-java-tdd** (github.com/danidemi/tutorial-java-tdd) — the Java darts
  (301, double-out) kata this corpus's darts package ports.
- **Esko Luontola** — TDD Tetris tutorial (github.com/luontola/tdd-tetris-tutorial).
- **Kent Beck** — Money and xUnit, reimplemented from *Test-Driven Development: By Example*
  (ports from the book's spec, in the long tradition of such reimplementations).
- Remaining katas trace to community repositories credited in each file's docstring
  (An4ik, in28minutes, giorgiosironi, among others).

Documented divergences from upstream: this corpus repairs upstream reference defects rather
than reproducing them, and records each repair in `instrument/AUDIT.md`. Notably, the
upstream C# Word Wrap inserts a single line break after the first `width` non-whitespace
characters and never wraps again; this corpus implements the canonical word-wrap kata
(break at word boundaries within the width; long words split at the width) and re-pins the
affected tests. The upstream leap-year kata's missing century rule and the darts double-out
edge cases are likewise repaired and documented (AUDIT D-10..D-13).

Original material in this repository is MIT (see `LICENSE`).
