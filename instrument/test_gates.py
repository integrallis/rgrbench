"""Instrument quality gates for the TDD dataset.

These meta-tests assert the properties that make the dataset usable as a lab instrument —
the lessons of failed SWE benchmarks, executable: the gold suites must pass (SWE-bench Pro
validates gold before anything), pass in any order (hidden cross-test state), pass with the
network blocked (hermeticity), finish fast (a hung suite poisons batch evaluation), keep a
1:1 structure between packages and their tests, and hold their measured oracle strength
(EvalPlus's lesson: weak tests silently overestimate every system they grade).

Run: `pytest instrument/ -q` from the repo root (uses the repo venv's pytest).
Regenerate mutation scores first when src/ or tests/ change: `make mutation`.
"""

import json
import re
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
TESTS = ROOT / "tests"
KATAS = sorted(p.name for p in SRC.iterdir() if p.is_dir() and p.name != "__pycache__")
FASTAPI_APPS = sorted(
    p for p in (ROOT / "fastapi-tdd-examples").iterdir() if (p / "pyproject.toml").is_file()
)
SUITE_TIME_CAP_S = 30.0
OVERALL_KILL_FLOOR = 0.98  # measured 2026-07 post-ingestion; may only ratchet up


def run_pytest(args, timeout=180):
    return subprocess.run(
        [sys.executable, "-m", "pytest", *args],
        capture_output=True, text=True, timeout=timeout, cwd=ROOT,
    )


# ---------- structure ----------

def test_every_kata_package_has_tests():
    untested = []
    test_text = "\n".join(f.read_text() for f in TESTS.glob("test_*.py"))
    for kata in KATAS:
        if not re.search(rf"\bfrom {kata}[.\s]|\bimport {kata}\b", test_text):
            untested.append(kata)
    assert not untested, f"src packages never imported by any test: {untested}"


def test_every_kata_package_is_importable():
    missing = [k for k in KATAS if not (SRC / k / "__init__.py").is_file()]
    assert not missing, f"packages without __init__.py: {missing}"


def test_no_src_prefixed_imports():
    offenders = [str(f) for f in list(TESTS.rglob("*.py")) + list(SRC.rglob("*.py"))
                 if re.search(r"\bfrom src\.|\bimport src\.", f.read_text())]
    assert not offenders, f"'src.' is a layout directory, not a package: {offenders}"


def test_tests_import_only_their_own_kata():
    cross = []
    for f in TESTS.glob("test_*.py"):
        imported = set(re.findall(r"^from (\w+)", f.read_text(), re.M))
        foreign = imported & set(KATAS)
        own = {k for k in foreign if k in f.stem or f.stem.replace("test_", "") in k}
        extra = foreign - own
        if extra and not own:
            # file naming doesn't match any package it imports — mapping is unclear
            cross.append((f.name, sorted(foreign)))
    assert not cross, f"test files whose kata mapping is ambiguous: {cross}"


def test_no_absolute_paths_or_benchmark_ids_in_tests():
    offenders = [f.name for f in TESTS.glob("test_*.py")
                 if re.search(r"/home/|HumanEval|LiveCodeBench", f.read_text())]
    assert not offenders, f"tests referencing absolute paths or benchmark ids: {offenders}"


# ---------- suite health ----------

def test_suite_passes_with_network_blocked():
    t0 = time.monotonic()
    proc = run_pytest(["tests/", "-q", "-p", "instrument.no_network"])
    wall = time.monotonic() - t0
    assert proc.returncode == 0, proc.stdout[-2000:]
    assert wall < SUITE_TIME_CAP_S, f"suite took {wall:.1f}s (cap {SUITE_TIME_CAP_S}s)"


@pytest.mark.parametrize("seed", ["101", "77143"])
def test_suite_order_independent(seed):
    proc = run_pytest(["tests/", "-q", f"--randomly-seed={seed}"])
    assert proc.returncode == 0, proc.stdout[-2000:]


# ---------- fastapi apps ----------

@pytest.mark.parametrize("app", FASTAPI_APPS, ids=lambda p: p.name)
def test_fastapi_app_suite_passes(app):
    py = app / ".venv" / "bin" / "python"
    if not py.is_file():
        pytest.skip(f"no venv — run: cd {app} && uv sync --extra test (or --all-groups)")
    proc = subprocess.run([str(py), "-m", "pytest", "tests/", "-q"],
                          capture_output=True, text=True, timeout=300, cwd=app)
    assert proc.returncode == 0, proc.stdout[-2000:]


# ---------- oracle strength (ratchet) ----------

def _scores():
    f = ROOT / "instrument" / "mutation_scores.json"
    assert f.is_file(), "run `make mutation` to generate instrument/mutation_scores.json"
    return json.loads(f.read_text())


def test_overall_mutation_kill_rate_floor():
    s = _scores()
    assert s["overall"]["kill_rate"] >= OVERALL_KILL_FLOOR, (
        f"overall kill rate {s['overall']['kill_rate']} fell below the recorded floor "
        f"{OVERALL_KILL_FLOOR} — oracle strength regressed")


def test_every_kata_has_mutation_score():
    s = _scores()
    missing = [k for k in KATAS if k not in s["packages"]]
    assert not missing, f"katas with no mutation measurement: {missing}"


def test_kill_rates_do_not_regress_below_recorded():
    """Ratchet: instrument/mutation_floors.json records each package's accepted minimum.
    Strengthening tests should raise floors; a fresh measurement below its floor fails."""
    s = _scores()
    floors = json.loads((ROOT / "instrument" / "mutation_floors.json").read_text())
    regressed = {k: (v["kill_rate"], floors[k]) for k, v in s["packages"].items()
                 if k in floors and v["kill_rate"] is not None
                 and v["kill_rate"] < floors[k]}
    assert not regressed, f"kill-rate regressions (measured, floor): {regressed}"
