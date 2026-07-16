# Requirements derivation protocol

Each document in this directory is the *prompt-side* artifact of the benchmark: the
requirements a system under evaluation receives. The package's hand-verified test suite
remains the oracle that grades whatever the system builds. The two must stand in a strict
relationship, fixed by this protocol and enforced by `instrument/test_requirements_gates.py`:

1. **Derived from tests only.** The author of a requirements document reads the package's
   test file and nothing else — never the implementation. What the tests do not assert,
   the requirements must not claim.
2. **Abstraction raised.** Requirements are written at user-story level (the layer above
   acceptance criteria): domain language, observable behavior, no API signatures, no code,
   no test values recited verbatim except where a value IS the specification (rates, caps,
   exact message texts, worked examples that define the behavior).
3. **Full traceability, machine-checked.** Every test function maps to at least one
   acceptance criterion in a fenced JSON block at the end of the document; every mapped
   criterion exists. A test with no home in the requirements means the requirements are
   incomplete; a criterion no test checks would be an unverifiable promise.
4. **No implementation leakage, machine-checked.** No private identifiers, no file paths,
   no identifiers that exist only in the implementation.
5. **Provenance.** Documents are machine-authored from the human-verified test suites
   (2026); each ends with a provenance line stating exactly that. dataset.json records the
   same per package.

Document shape:

```markdown
# <Domain title>

## Overview
<one short paragraph: what the system is, in domain terms>

## User Stories

### US-1: <story title>
As a <role>, I want <capability>, so that <benefit>.

- AC-1.1: <observable behavior criterion>
- AC-1.2: ...

## Traceability
```json
{ "test_function_name": ["AC-1.1"], ... }
` ``  (fenced json block; every test in the suite appears)

<provenance line>
```
