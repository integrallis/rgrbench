"""Deep tests for the evaluation harness — the no-cheating machinery is load-bearing.

Fixtures build a tiny domain end to end: an oracle suite for a counter, a candidate
implementing it under different names, and adapters ranging from honest to adversarial.
The adversarial cases are the point: a cheating adapter that passes the static check
(no operators, no numeric constants — it manufactures values with len() of strings)
must be caught by fault-injection transparency, and a partially failing candidate must
not make transparency degenerate.
"""

import ast
from pathlib import Path

import pytest

from harness.adapter_check import check_adapter_source
from harness.evaluate import _FaultInjector, _count_sites, evaluate

ORACLE = '''\
from magic.counter import Counter


def test_new_counter_totals_zero():
    assert Counter().total() == 0


def test_single_add_is_counted():
    c = Counter()
    c.add(2)
    assert c.total() == 2


def test_adds_accumulate():
    c = Counter()
    c.add(2)
    c.add(3)
    assert c.total() == 5


def test_negative_amounts_are_rejected():
    c = Counter()
    try:
        c.add(-1)
        raised = False
    except ValueError:
        raised = True
    assert raised and c.total() == 0
'''

CANDIDATE_OK = '''\
class Tally:
    def __init__(self):
        self._amount = 0

    def plus(self, n):
        if n < 0:
            raise ValueError("negative")
        self._amount = self._amount + n

    def sum(self):
        return self._amount
'''

CANDIDATE_BUGGY = CANDIDATE_OK.replace("self._amount + n", "self._amount - n")

ADAPTER_HONEST = '''\
"""Maps the candidate's Tally API onto the oracle's Counter names."""
from candidate.tally import Tally


class Counter:
    def __init__(self):
        self.inner = Tally()

    def add(self, n):
        return self.inner.plus(n)

    def total(self):
        return self.inner.sum()
'''

# Static-legal cheat: no operators, no control flow, no numeric constants — values are
# manufactured with len() over string literals, and the candidate is never consulted.
ADAPTER_CHEAT_STATIC_LEGAL = '''\
"""Adversarial: ignores the candidate entirely."""


class Counter:
    def __init__(self):
        self.token = ""

    def add(self, n):
        return None

    def total(self):
        return len(self.token)
'''

ADAPTER_CHEAT_BLATANT = '''\
class Counter:
    def __init__(self):
        self.n = 0

    def add(self, n):
        if n < 0:
            raise ValueError("negative")
        self.n += n

    def total(self):
        return self.n
'''

ADAPTER_BROKEN_IMPORT = "from candidate.nonexistent import Missing as Counter\n"


def build(tmp_path: Path, candidate_src: str, adapter_src: str):
    candidate = tmp_path / "cand"
    (candidate).mkdir()
    (candidate / "__init__.py").write_text("")
    (candidate / "tally.py").write_text(candidate_src)
    adapter = tmp_path / "adapt"
    (adapter / "magic").mkdir(parents=True)
    (adapter / "magic" / "counter.py").write_text(adapter_src)
    oracle = tmp_path / "test_counter.py"
    oracle.write_text(ORACLE)
    return candidate, adapter, oracle


# ---------- static adapter constraints ----------

@pytest.mark.parametrize("snippet,marker", [
    ("if x:\n    pass", "If"),
    ("y = a + b", "BinOp"),
    ("y = a < b", "Compare"),
    ("y = x[0]", "Subscript"),
    ("for i in xs:\n    pass", "For"),
    ("y = [i for i in xs]", "ListComp"),
    ("def f():\n    return 42", "constant 42"),
    ("f = lambda x: x", "lambda body"),
])
def test_static_check_rejects_forbidden_constructs(snippet, marker):
    verdict = check_adapter_source(snippet)
    assert not verdict.ok
    assert any(marker in v for v in verdict.violations)


def test_static_check_accepts_honest_delegation():
    assert check_adapter_source(ADAPTER_HONEST).ok


def test_static_check_accepts_alias_reexport():
    assert check_adapter_source("from candidate.mod import Thing as Other\n").ok


def test_static_check_rejects_oversized_modules():
    verdict = check_adapter_source("\n".join(f"x{i} = None" for i in range(200)))
    assert not verdict.ok and any("lines" in v for v in verdict.violations)


def test_static_check_reports_syntax_errors():
    verdict = check_adapter_source("def broken(:\n")
    assert not verdict.ok and "syntax error" in verdict.violations[0]


def test_static_check_flags_the_blatant_cheat():
    verdict = check_adapter_source(ADAPTER_CHEAT_BLATANT)
    assert not verdict.ok
    joined = " ".join(verdict.violations)
    assert "If" in joined and ("AugAssign" in joined or "BinOp" in joined)


def test_static_check_cannot_catch_the_len_cheat():
    """Documents the static check's known limit — transparency must catch this one."""
    assert check_adapter_source(ADAPTER_CHEAT_STATIC_LEGAL).ok


# ---------- fault injector ----------

def test_injector_counts_sites_and_applies_exactly_one():
    tree = ast.parse(CANDIDATE_OK)
    n = _count_sites(tree)
    assert n >= 3  # comparison, addition, at least one integer constant
    for idx in range(n):
        mutated = ast.parse(CANDIDATE_OK)
        inj = _FaultInjector(idx)
        inj.visit(mutated)
        assert inj.applied, f"site {idx} applied no fault"
        assert ast.unparse(mutated) != ast.unparse(ast.parse(CANDIDATE_OK)), \
            f"site {idx} produced an identical tree"


def test_injector_out_of_range_applies_nothing():
    tree = ast.parse(CANDIDATE_OK)
    inj = _FaultInjector(10_000)
    inj.visit(tree)
    assert not inj.applied


# ---------- end-to-end evaluation ----------

def test_correct_candidate_with_honest_adapter_is_valid_and_transparent(tmp_path):
    c, a, o = build(tmp_path, CANDIDATE_OK, ADAPTER_HONEST)
    r = evaluate("counter", c, a, o)
    assert r.adapter_ok and r.valid, r.invalid_reason
    assert r.tests_total == 4 and r.tests_passed == 4 and r.pass_fraction == 1.0
    assert r.transparency is not None and r.transparency >= 0.5


def test_buggy_candidate_scores_partially_and_stays_valid(tmp_path):
    c, a, o = build(tmp_path, CANDIDATE_BUGGY, ADAPTER_HONEST)
    r = evaluate("counter", c, a, o)
    assert r.adapter_ok
    assert 0 < r.tests_passed < r.tests_total
    assert "FAILED" in r.per_test.values().__iter__().__next__() or \
           any(v == "FAILED" for v in r.per_test.values())
    # a partially failing baseline must not auto-detect every fault via exit codes
    assert r.transparency is None or r.transparency <= 1.0
    assert r.valid or (r.invalid_reason and "transparency" in r.invalid_reason)


def test_len_cheat_passes_static_but_is_caught_dynamically(tmp_path):
    """The static-legal cheat must be rejected by a dynamic layer: under protocol v2 the
    candidate-execution check catches it outright (no candidate line runs); the
    fault-injection layer remains as defense in depth for partial bypasses."""
    c, a, o = build(tmp_path, CANDIDATE_OK, ADAPTER_CHEAT_STATIC_LEGAL)
    r = evaluate("counter", c, a, o)
    assert r.adapter_ok, "the cheat is static-legal by construction"
    assert not r.valid
    assert r.invalid_reason and ("execut" in r.invalid_reason
                                 or "transparency" in r.invalid_reason)


def test_blatant_cheat_is_rejected_statically_before_any_run(tmp_path):
    c, a, o = build(tmp_path, CANDIDATE_OK, ADAPTER_CHEAT_BLATANT)
    r = evaluate("counter", c, a, o)
    assert not r.adapter_ok and not r.valid
    assert r.tests_total == 0  # never ran
    assert "static no-cheating" in r.invalid_reason


def test_broken_adapter_import_is_invalid_with_reason(tmp_path):
    c, a, o = build(tmp_path, CANDIDATE_OK, ADAPTER_BROKEN_IMPORT)
    r = evaluate("counter", c, a, o)
    assert r.adapter_ok  # statically fine
    assert not r.valid and r.tests_total == 0
    assert "no tests" in r.invalid_reason


def test_evaluation_is_deterministic(tmp_path):
    c, a, o = build(tmp_path, CANDIDATE_OK, ADAPTER_HONEST)
    r1 = evaluate("counter", c, a, o)
    r2 = evaluate("counter", c, a, o)
    assert r1.__dict__ == r2.__dict__


def test_candidate_sources_are_never_modified(tmp_path):
    c, a, o = build(tmp_path, CANDIDATE_OK, ADAPTER_HONEST)
    before = (c / "tally.py").read_text()
    evaluate("counter", c, a, o)
    assert (c / "tally.py").read_text() == before


# ---------- protocol v2: coverage-guided transparency ----------

CANDIDATE_DEAD_BRANCH = CANDIDATE_OK.replace(
    "    def sum(self):",
    '''    def unused_helper(self):
        return (1 + 2) * (3 + 4) < (5 + 6) * (7 + 8)

    def sum(self):''')


def test_faults_target_only_executed_candidate_lines(tmp_path):
    """A candidate with a never-executed helper full of mutable sites must still be
    fully transparent: faults are injected only into lines the passing tests run."""
    c, a, o = build(tmp_path, CANDIDATE_DEAD_BRANCH, ADAPTER_HONEST)
    r = evaluate("counter", c, a, o)
    assert r.valid, r.invalid_reason
    assert r.transparency is not None and r.transparency >= 0.5


def test_zero_candidate_execution_is_detected_directly(tmp_path):
    """The len() cheat executes no candidate line; the execution check must name it."""
    c, a, o = build(tmp_path, CANDIDATE_OK, ADAPTER_CHEAT_STATIC_LEGAL)
    r = evaluate("counter", c, a, o)
    assert not r.valid
    assert "candidate" in r.invalid_reason and "execut" in r.invalid_reason


ORACLE_PARAMETRIZED = ORACLE + '''

import pytest


@pytest.mark.parametrize("n,expected", [(1, 1), (4, 4)])
def test_parametrized_adds(n, expected):
    c = Counter()
    c.add(n)
    assert c.total() == expected
'''


def test_parametrized_oracle_tests_are_counted(tmp_path):
    c, a, o = build(tmp_path, CANDIDATE_OK, ADAPTER_HONEST)
    o.write_text(ORACLE_PARAMETRIZED)
    r = evaluate("counter", c, a, o)
    assert r.tests_total == 6, r.per_test  # 4 plain + 2 parametrized cases
    assert r.valid and r.pass_fraction == 1.0


# ---------- protocol v3.1: behavioral screening of injected faults ----------

CANDIDATE_NEUTRAL_SITES = CANDIDATE_OK.replace(
    "        self._amount = self._amount + n",
    "        padded = n + 0\n        self._amount = self._amount + padded")


def test_neutral_faults_are_screened_out_not_held_against_the_adapter(tmp_path):
    """`n + 0` is an executed fault site whose Add->Sub flip is behaviorally neutral;
    screening must discard it so an honest adapter still scores full transparency."""
    c, a, o = build(tmp_path, CANDIDATE_NEUTRAL_SITES, ADAPTER_HONEST)
    r = evaluate("counter", c, a, o)
    assert r.valid, r.invalid_reason
    assert r.transparency == 1.0, (r.transparency, r.faults_neutral)
    assert r.faults_neutral >= 1  # the screen actually fired


# Partial bypass: CALLS the candidate (execution check passes, traces respond to faults)
# but ignores its results and answers from its own state via len() tricks.
ADAPTER_CHEAT_PARTIAL_BYPASS = '''\
"""Adversarial: exercises the candidate, answers from private state."""
from candidate.tally import Tally


class Counter:
    def __init__(self):
        self.inner = Tally()
        self.token = ""

    def add(self, n):
        self.inner.plus(n)
        self.token = "".join(["xx", self.token])
        return None

    def total(self):
        self.inner.sum()
        return len(self.token)
'''


def test_partial_bypass_is_caught_by_screened_transparency(tmp_path):
    """The candidate runs (execution check passes) and behavior-changing faults alter its
    boundary trace — but never the oracle outcomes, because the adapter ignores the
    candidate's answers. Screened transparency must reject this as opaque."""
    c, a, o = build(tmp_path, CANDIDATE_OK, ADAPTER_CHEAT_PARTIAL_BYPASS)
    r = evaluate("counter", c, a, o)
    # this cheat gives total() = 2*adds, so some tests may even pass
    assert not r.valid
    assert r.invalid_reason and "transparency" in r.invalid_reason


CANDIDATE_ALL_NEUTRAL = '''\
class Tally:
    def __init__(self):
        self._amount = int()

    def plus(self, n):
        discarded = n + 0

    def sum(self):
        return self._amount
'''

ORACLE_ZERO_ONLY = '''\
from magic.counter import Counter


def test_new_counter_totals_zero():
    assert Counter().total() == 0


def test_add_returns_nothing():
    assert Counter().add(3) is None
'''


def test_all_neutral_faults_yield_insufficient_signal_not_accusation(tmp_path):
    c, a, o = build(tmp_path, CANDIDATE_ALL_NEUTRAL, ADAPTER_HONEST)
    o.write_text(ORACLE_ZERO_ONLY)
    r = evaluate("counter", c, a, o)
    assert r.valid, r.invalid_reason
    assert r.transparency is None
    assert r.transparency_note and "insufficient" in r.transparency_note


def test_buggy_candidate_transparency_ignores_failing_path_faults(tmp_path):
    """Faults that only perturb paths exercised by already-failing tests must not count
    against the adapter: trace comparison is restricted to baseline-passing tests."""
    c, a, o = build(tmp_path, CANDIDATE_BUGGY, ADAPTER_HONEST)
    r = evaluate("counter", c, a, o)
    assert r.adapter_ok
    assert r.valid, r.invalid_reason  # honest adapter on a buggy candidate stays valid
