"""Quality gates for the requirements layer.

Each kata package carries `requirements/<package>.md`: user-story-level requirements
derived from the package's TEST SUITE ONLY (never the implementation). The requirements
are the prompt-side artifact a system under evaluation receives; the tests remain the
oracle. These gates make the derivation contract executable:

- G-R1 completeness: every package has a requirements document.
- G-R2 traceability: the document ends with a fenced JSON block mapping EVERY test
  function in the package's suite to at least one acceptance-criterion ID defined in the
  document, and referencing no undefined IDs.
- G-R3 abstraction/leakage: the prose contains no Python code fences, no src file paths,
  no private (underscore-prefixed) identifiers, and no identifiers that exist only in the
  implementation (defined in src/ but never appearing in the test file) — requirements
  derived from tests cannot know them.
- G-R4 structure: a title, an Overview section, at least one user story in the
  "As a ... I want ... so that ..." form, and at least one acceptance criterion per story.
- G-R5 hygiene: no absolute paths, no benchmark identifiers.
"""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
TESTS = ROOT / "tests"
REQS = ROOT / "requirements"
KATAS = sorted(p.name for p in SRC.iterdir() if p.is_dir() and p.name != "__pycache__")

AC_ID = re.compile(r"\bAC-\d+(?:\.\d+)*\b")
STORY = re.compile(r"\bAs an? .+?,? I want .+?,? so that .+", re.IGNORECASE)


def suite_files_for(pkg: str) -> list[Path]:
    """All test files exercising the package (a package may have several)."""
    files = [f for f in TESTS.glob("test_*.py")
             if re.search(rf"\bfrom {pkg}[.\s]|\bimport {pkg}\b", f.read_text())]
    assert files, f"no test file found for {pkg}"
    return files


def doc_for(pkg: str) -> str:
    f = REQS / f"{pkg}.md"
    assert f.is_file(), f"missing requirements/{pkg}.md"
    return f.read_text()


def traceability(doc: str) -> dict:
    m = re.search(r"```json\s*\n(.*?)\n```", doc, re.DOTALL)
    assert m, "no fenced JSON traceability block"
    data = json.loads(m.group(1))
    assert isinstance(data, dict) and data, "traceability block must be a non-empty object"
    return data


@pytest.mark.parametrize("pkg", KATAS)
def test_gr1_document_exists(pkg):
    doc_for(pkg)


@pytest.mark.parametrize("pkg", KATAS)
def test_gr2_full_test_traceability(pkg):
    doc = doc_for(pkg)
    trace = traceability(doc)
    test_fns = {fn for f in suite_files_for(pkg)
                for fn in re.findall(r"^def (test_\w+)", f.read_text(), re.M)}
    mapped = set(trace)
    missing = test_fns - mapped
    stale = mapped - test_fns
    assert not missing, f"tests with no requirement mapping: {sorted(missing)}"
    assert not stale, f"mapped names that are not tests: {sorted(stale)}"
    defined_ids = set(AC_ID.findall(doc))
    for test, acs in trace.items():
        assert isinstance(acs, list) and acs, f"{test}: empty mapping"
        undefined = [ac for ac in acs if ac not in defined_ids]
        assert not undefined, f"{test} maps to undefined criteria {undefined}"


@pytest.mark.parametrize("pkg", KATAS)
def test_gr3_no_implementation_leakage(pkg):
    doc = doc_for(pkg)
    prose = re.sub(r"```json\s*\n.*?\n```", "", doc, flags=re.DOTALL)
    assert "```python" not in prose and "def test_" not in prose
    assert "src/" not in prose and ".py" not in prose
    private = [w for w in re.findall(r"\b_\w+", prose) if not w.startswith("__")]
    assert not private, f"private identifiers in prose: {private[:5]}"
    # identifiers defined only in the implementation can't be known from tests
    src_text = " ".join(f.read_text() for f in (SRC / pkg).glob("*.py"))
    test_text = " ".join(f.read_text() for f in suite_files_for(pkg))
    src_only = {
        name for name in re.findall(r"^(?:def|class) (\w+)", src_text, re.M)
        if not name.startswith("_") and name not in test_text
    }
    leaked = {name for name in src_only
              if re.search(rf"\b{re.escape(name)}\b", prose)}
    assert not leaked, f"implementation-only identifiers in prose: {sorted(leaked)}"


@pytest.mark.parametrize("pkg", KATAS)
def test_gr4_structure(pkg):
    doc = doc_for(pkg)
    assert doc.lstrip().startswith("#"), "must open with a title"
    assert re.search(r"^## Overview", doc, re.M), "missing Overview section"
    assert STORY.search(doc), "no user story in As-a/I-want/so-that form"
    assert AC_ID.search(doc), "no acceptance criteria IDs"


@pytest.mark.parametrize("pkg", KATAS)
def test_gr5_hygiene(pkg):
    doc = doc_for(pkg)
    assert not re.search(r"/home/|HumanEval|LiveCodeBench", doc)
