# Rendering whole numbers as Roman numerals

## Overview
A converter renders whole numbers in classical Roman notation, the numbering carved on monuments and clock faces. Numbers are written with the seven symbols I (1), V (5), X (10), L (50), C (100), D (500), and M (1000), combined additively from largest to smallest, with subtractive forms for values one step below a five or a ten at each scale.

## User Stories

### US-1: Writing numbers in standard Roman notation
As a publisher of classical texts, I want whole numbers rendered as standard Roman numerals, so that dates and chapter numbers appear in traditional form.

- AC-1.1: Plain values combine symbols additively in descending order: 1 is I, 3 is III, 6 is VI, 20 is XX, 30 is XXX, 100 is C, 1000 is M, and 27 is XXVII.
- AC-1.2: Values one below a five or a ten use subtractive notation at every scale: 4 is IV, 9 is IX, 40 is XL, 90 is XC, 400 is CD, and 900 is CM.
- AC-1.3: Composite numbers weave both forms together, as in the canonical examples 49 as XLIX, 87 as LXXXVII, 239 as CCXXXIX, 444 as CDXLIV, 692 as DCXCII, 999 as CMXCIX, and 2016 as MMXVI.

## Traceability
```json
{
  "test_to_roman": ["AC-1.1", "AC-1.2", "AC-1.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
