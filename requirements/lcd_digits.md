# LCD-style digit display

## Overview
A renderer that draws whole numbers the way a segment display would: as text art built from periods, underscores and vertical bars. Each digit occupies a cell three characters wide across three lines, and multi-digit numbers are laid out side by side on one three-line panel.

## User Stories

### US-1: Render a single digit
As a display builder, I want each digit drawn as three-line segment art, so that numbers read like an LCD panel.

- AC-1.1: The rendering of a number is three lines tall, and each of the three lines ends with a newline character.
- AC-1.2: The digit 0 renders exactly as the three-line cell:

  ```
  ._.
  |.|
  |_|
  ```

- AC-1.3: The digit 1 renders exactly as the three-line cell (unused segments are drawn as periods):

  ```
  ...
  ..|
  ..|
  ```

### US-2: Render multi-digit numbers
As a display builder, I want digits laid out side by side, so that whole numbers appear on a single panel.

- AC-2.1: For a number with several digits, each of the three output lines is the concatenation of the corresponding line of every digit's cell, in the number's own order, with no separator between cells.
- AC-2.2: Worked example: 10 renders exactly as

  ```
  ...._.
  ..||.|
  ..||_|
  ```

- AC-2.3: Worked example: 100 renders exactly as

  ```
  ...._.._.
  ..||.||.|
  ..||_||_|
  ```

## Traceability
```json
{
  "test_digit_the_number_0": ["AC-1.1", "AC-1.2"],
  "test_digit_the_number_1": ["AC-1.1", "AC-1.3"],
  "test_digit_the_number_10": ["AC-2.1", "AC-2.2"],
  "test_digit_the_number_100": ["AC-2.1", "AC-2.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
