"""Workspace assembly, oracle grading, and fault-injection transparency.

evaluate(candidate_dir, adapter_dir, oracle_test_file) -> EvaluationResult:
1. static-check every adapter module (adapter_check);
2. assemble an isolated workspace: candidate/ package, adapter modules at the top level
   (they provide the import names the oracle expects), the oracle test file;
3. run pytest -> per-test outcomes;
4. transparency: for N seeded single-fault variants of the candidate, re-run the oracle;
   report the fraction of faults detected (suite fails). Low transparency means the
   adapter, not the candidate, is producing behavior — the evaluation is invalid.
"""

from __future__ import annotations

import ast
import copy
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from harness.adapter_check import check_adapter_source

TRANSPARENCY_FAULTS = 8       # behavior-changing faults to collect (screened denominator)
MAX_FAULT_SAMPLES = 24        # total injection attempts before giving up the search
TRANSPARENCY_THRESHOLD = 0.5  # at least half the BEHAVIOR-CHANGING faults must be detected

_CONFTEST = '''\
import json
import os
import re
import sys

_TRACE = os.environ.get("BOUNDARY_TRACE")
if _TRACE:
    _log = open(_TRACE, "a")
    _ADDR = re.compile(r" at 0x[0-9a-f]+")
    _SEP = os.sep + "candidate" + os.sep

    def _norm(v):
        try:
            r = repr(v)
        except Exception:
            r = "<unrepr>"
        return _ADDR.sub("", r)[:200]

    def _prof(frame, event, arg):
        if event not in ("call", "return"):
            return
        if _SEP not in frame.f_code.co_filename:
            return
        kind = "C" if event == "call" else "R"
        payload = _norm(dict(frame.f_locals)) if event == "call" else _norm(arg)
        _log.write(json.dumps([kind, frame.f_code.co_qualname, payload]) + "\\n")
        _log.flush()

    def pytest_runtest_setup(item):
        _log.write(json.dumps(["T", item.name]) + "\\n")
        _log.flush()
        sys.setprofile(_prof)

    def pytest_runtest_teardown(item):
        sys.setprofile(None)
'''


def _parse_trace(path: Path) -> dict[str, tuple]:
    """Per-test candidate-boundary trace segments: {test name: (records...)}."""
    segments: dict[str, list] = {}
    current: list | None = None
    if not path.is_file():
        return {}
    for line in path.read_text().splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec[0] == "T":
            current = segments.setdefault(rec[1], [])
        elif current is not None:
            current.append(tuple(rec))
    return {t: tuple(rs) for t, rs in segments.items()}
_SEED = 20260714  # fixed harness seed; runs are reproducible


@dataclass
class EvaluationResult:
    package: str
    adapter_ok: bool
    adapter_violations: list[str]
    tests_total: int = 0
    tests_passed: int = 0
    pass_fraction: float = 0.0
    transparency_faults: int = 0
    transparency_detected: int = 0
    transparency: float | None = None
    faults_sampled: int = 0
    faults_neutral: int = 0
    transparency_note: str | None = None
    valid: bool = False
    invalid_reason: str | None = None
    per_test: dict[str, str] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=2)


class _FaultInjector(ast.NodeTransformer):
    """Applies exactly one behavioral mutation, chosen by index over candidate sites."""

    SWAPS = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Add,
             ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt,
             ast.Eq: ast.NotEq, ast.NotEq: ast.Eq}

    def __init__(self, target_index: int):
        self.target_index = target_index
        self.seen = 0
        self.applied = False
        self.site_lines: list[int] = []
        self._current_line = 0

    def _hit(self) -> bool:
        self.site_lines.append(self._current_line)
        self.seen += 1
        if self.seen - 1 == self.target_index and not self.applied:
            self.applied = True
            return True
        return False

    def visit_BinOp(self, node: ast.BinOp):
        self._current_line = getattr(node, "lineno", 0)
        self.generic_visit(node)
        if type(node.op) in self.SWAPS and self._hit():
            node.op = self.SWAPS[type(node.op)]()
        return node

    def visit_Compare(self, node: ast.Compare):
        self._current_line = getattr(node, "lineno", 0)
        self.generic_visit(node)
        if len(node.ops) == 1 and type(node.ops[0]) in self.SWAPS and self._hit():
            node.ops[0] = self.SWAPS[type(node.ops[0])]()
        return node

    def visit_Constant(self, node: ast.Constant):
        self._current_line = getattr(node, "lineno", 0)
        if isinstance(node.value, int) and not isinstance(node.value, bool):
            if self._hit():
                node.value = node.value + 1
        return node


def _count_sites(tree: ast.AST) -> int:
    probe = _FaultInjector(target_index=-1)
    probe.visit(copy.deepcopy(tree))
    return probe.seen


def _run_pytest(workspace: Path,
                trace: Path | None = None) -> tuple[int, dict[str, str]]:
    env = {"PYTHONPATH": str(workspace), "PATH": "/usr/bin:/bin",
           "PYTHONDONTWRITEBYTECODE": "1"}
    if trace is not None:
        trace.unlink(missing_ok=True)
        env["BOUNDARY_TRACE"] = str(trace)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", "-v", "--timeout=10", "-p", "no:randomly",
         "-o", "addopts="],
        capture_output=True, text=True, timeout=300, cwd=workspace, env=env,
    )
    per_test: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        m = re.match(r"tests/\S+::(\w+(?:\[[^\]]*\])?)\s+(PASSED|FAILED|ERROR)", line)
        if m:
            per_test[m.group(1)] = m.group(2)
    _run_pytest.last_tail = (proc.stdout + proc.stderr)[-1200:]
    return proc.returncode, per_test


def _covered_candidate_lines(workspace: Path) -> dict[str, set[int]]:
    """Lines of candidate/ executed while running the oracle (coverage-measured)."""
    env = {"PYTHONPATH": str(workspace), "PATH": "/usr/bin:/bin",
           "PYTHONDONTWRITEBYTECODE": "1"}
    subprocess.run(
        [sys.executable, "-m", "coverage", "run", "--include=candidate/*",
         "-m", "pytest", "tests", "-q", "--timeout=10", "-p", "no:randomly",
         "-o", "addopts="],
        capture_output=True, text=True, timeout=300, cwd=workspace, env=env,
    )
    out = subprocess.run(
        [sys.executable, "-m", "coverage", "json", "-o", "-"],
        capture_output=True, text=True, timeout=60, cwd=workspace, env=env,
    )
    covered: dict[str, set[int]] = {}
    try:
        data = json.loads(out.stdout[out.stdout.index("{"):])
        for fname, fdata in data.get("files", {}).items():
            covered[Path(fname).name] = set(fdata.get("executed_lines", []))
    except (ValueError, KeyError):
        pass
    return covered


def _assemble(workspace: Path, candidate_dir: Path, adapter_dir: Path,
              oracle_test_file: Path) -> None:
    shutil.copytree(candidate_dir, workspace / "candidate")
    for f in adapter_dir.rglob("*.py"):
        dest = workspace / f.relative_to(adapter_dir)
        dest.parent.mkdir(parents=True, exist_ok=True)
        for parent in dest.relative_to(workspace).parents:
            init = workspace / parent / "__init__.py"
            if parent.name and not init.exists():
                init.write_text("")
        shutil.copy(f, dest)
    tests = workspace / "tests"
    tests.mkdir(exist_ok=True)
    (tests / "__init__.py").write_text("")
    shutil.copy(oracle_test_file, tests / oracle_test_file.name)
    (workspace / "conftest.py").write_text(_CONFTEST)


def evaluate(package: str, candidate_dir: Path, adapter_dir: Path,
             oracle_test_file: Path) -> EvaluationResult:
    candidate_dir = Path(candidate_dir)
    adapter_dir = Path(adapter_dir)
    oracle_test_file = Path(oracle_test_file)

    violations: list[str] = []
    for f in sorted(adapter_dir.rglob("*.py")):
        verdict = check_adapter_source(f.read_text(), str(f.relative_to(adapter_dir)))
        violations.extend(verdict.violations)
    result = EvaluationResult(package=package, adapter_ok=not violations,
                              adapter_violations=violations)
    if violations:
        result.invalid_reason = "adapter failed static no-cheating constraints"
        return result

    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "ws"
        workspace.mkdir()
        _assemble(workspace, candidate_dir, adapter_dir, oracle_test_file)

        # verbose per-test grading run, boundary-traced for fault screening
        baseline_trace_file = Path(tmp) / "baseline.trace"
        rc, per = _run_pytest(workspace, trace=baseline_trace_file)
        result.per_test = per
        result.tests_total = len(result.per_test)
        result.tests_passed = sum(1 for v in result.per_test.values() if v == "PASSED")
        result.pass_fraction = (result.tests_passed / result.tests_total
                                if result.tests_total else 0.0)
        if result.tests_total == 0:
            tail = proc_tail if (proc_tail := getattr(_run_pytest, "last_tail", "")) else ""
            result.invalid_reason = ("oracle collected no tests (adapter import failure "
                                     f"or environment error): {tail[-400:]}")
            return result

        # transparency: only meaningful when the un-faulted run passes everything the
        # candidate can pass; we inject into whichever tests currently pass.
        baseline_pass_set = {t for t, v in result.per_test.items() if v == "PASSED"}
        covered = _covered_candidate_lines(workspace)
        if baseline_pass_set and not any(covered.values()):
            result.invalid_reason = (
                "passing tests execute no candidate code — the adapter is supplying "
                "behavior (candidate-execution check)")
            return result

        sources = {f: f.read_text() for f in (workspace / "candidate").rglob("*.py")
                   if f.name != "__init__.py"}
        sites = []
        for f, src in sources.items():
            try:
                probe = _FaultInjector(target_index=-1)
                probe.visit(ast.parse(src))
            except SyntaxError:
                continue
            file_cov = covered.get(f.name, set())
            sites.extend((f, i) for i, line in enumerate(probe.site_lines)
                         if line in file_cov)
        if not sites:
            # execution check already passed; nothing coverable to mutate
            result.valid = True
            return result

        baseline_trace = _parse_trace(baseline_trace_file)
        baseline_pass = baseline_pass_set
        rng = random.Random(_SEED)
        rng.shuffle(sites)
        fault_trace_file = Path(tmp) / "fault.trace"
        behavior_changing = detected = neutral = sampled = 0
        for f, idx in sites:
            if behavior_changing >= TRANSPARENCY_FAULTS or sampled >= MAX_FAULT_SAMPLES:
                break
            sampled += 1
            tree = ast.parse(sources[f])
            injector = _FaultInjector(idx)
            injector.visit(tree)
            f.write_text(ast.unparse(tree))
            _, per = _run_pytest(workspace, trace=fault_trace_file)
            f.write_text(sources[f])  # restore
            fault_trace = _parse_trace(fault_trace_file)
            # neutrality is judged at the candidate boundary, restricted to the tests
            # that pass at baseline: a fault that changes nothing an honest adapter
            # could transmit carries no signal about opacity
            changed = any(baseline_trace.get(t) != fault_trace.get(t)
                          for t in baseline_pass)
            if not changed:
                neutral += 1
                continue
            behavior_changing += 1
            now_pass = {t for t, v in per.items() if v == "PASSED"} if per else set()
            if not baseline_pass.issubset(now_pass):
                detected += 1
        result.faults_sampled = sampled
        result.faults_neutral = neutral
        result.transparency_faults = behavior_changing
        result.transparency_detected = detected
        if behavior_changing == 0:
            if baseline_pass:
                result.transparency_note = (
                    "insufficient transparency signal: all sampled faults were "
                    "behaviorally neutral for the exercised workload")
            result.valid = True
            return result
        result.transparency = detected / behavior_changing
        if result.transparency < TRANSPARENCY_THRESHOLD and baseline_pass:
            result.invalid_reason = (
                f"transparency {result.transparency:.2f} below threshold "
                f"{TRANSPARENCY_THRESHOLD}: oracle outcomes are insensitive to "
                f"behavior-changing candidate faults — the adapter may be supplying "
                f"behavior")
            return result

    result.valid = True
    return result
