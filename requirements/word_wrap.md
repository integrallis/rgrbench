# Text wrapping at a column width

## Overview
Text destined for a fixed-width display must be broken into lines no longer than a
given column width. The wrapper prefers to break at spaces so words stay whole,
hard-splits words that are longer than the width, respects line breaks already present
in the text, and treats spaces — but not tabs — as expendable at the points where it
breaks.

## User Stories

### US-1: Wrap text to fit a column width
As a reader of fixed-width output, I want text broken into lines that fit the column, so that nothing runs past the edge of the display.

- AC-1.1: Text that already fits within the width is returned unchanged, including a line exactly at the width — whether or not it contains a space ("ab cd" at width 5 stays one line).
- AC-1.2: When a line exceeds the width, the break goes at the last space that fits within the width window, and the space (or run of spaces) at the break is consumed: "Let's  Go" at width 5 becomes the lines "Let's" and "Go"; "Lets go outside now" at width 7 becomes "Lets go", "outside", "now".
- AC-1.3: A single word longer than the width is hard-split at the width: "extraordinary" at width 5 becomes "extra", "ordin", "ary".
- AC-1.4: A one-letter first word still breaks at its space: "a bcdef" at width 5 becomes "a" and "bcdef".
- AC-1.5: Column counting restarts after an inserted break: "aaa bb" at width 3 becomes "aaa" and "bb" with no further break.

### US-2: Handle missing, blank, and trailing-space input
As a reader of fixed-width output, I want blank or missing text to come out empty, so that the display never shows stray whitespace lines.

- AC-2.1: When no text is provided at all, the result is the empty string.
- AC-2.2: Whitespace-only text — a single space or a single tab — produces the empty string.
- AC-2.3: Trailing spaces beyond the width are dropped rather than wrapped: "hi  " at width 2 becomes just "hi", with no trailing break.

### US-3: Respect line breaks already in the text
As an author, I want the line breaks I typed to survive wrapping, so that my paragraph structure is preserved.

- AC-3.1: Existing line breaks are kept, and the text on each side wraps independently: a text of an empty first line, then "Let's Go", then "outside." at width 5 keeps its first break, breaks "Let's Go" at the space, and hard-splits "outside." into "outsi" and "de.".
- AC-3.2: Consecutive line breaks are preserved, not collapsed.
- AC-3.3: Column counting restarts after an existing line break: two three-letter segments either side of a break fit a width of 4 untouched.
- AC-3.4: Segments around an existing break that fit within the width stay exactly as they are.

### US-4: Consume only spaces at breaks and line starts
As an author, I want only spaces sacrificed when lines are broken, so that tabs and visible characters are never lost.

- AC-4.1: Only spaces are consumed at a break; a tab following the break-point space survives onto the new line: "ab \tcd" at width 3 becomes "ab" and a line starting with the tab, "\tcd".
- AC-4.2: Characters of the following word are never consumed at a break: "ab Xcd" at width 3 becomes "ab" and "Xcd" with the "X" intact.
- AC-4.3: Tab indentation at the start of a segment after a line break is preserved: "ab", a break, then a tab-indented "cd" passes through unchanged at width 10.
- AC-4.4: A line that starts with a space does not break at that space (which would leave an empty first line); it hard-breaks at the width instead: " hello" at width 3 becomes " he" and "llo".

## Traceability
```json
{
  "test_can_wrap_single_line": ["AC-1.2"],
  "test_can_handle_null_word": ["AC-2.1"],
  "test_can_handle_null_or_whitespace": ["AC-2.1", "AC-2.2"],
  "test_can_handle_newline_character": ["AC-3.1"],
  "test_can_wrap_multiple_lines": ["AC-1.2", "AC-3.3"],
  "test_word_longer_than_width_is_split_at_width": ["AC-1.3"],
  "test_can_handle_whitespace_only_tab": ["AC-2.2"],
  "test_can_preserve_consecutive_newlines": ["AC-3.2"],
  "test_segments_within_column_width_are_unchanged": ["AC-3.4"],
  "test_column_count_restarts_after_existing_newline": ["AC-3.3"],
  "test_column_count_restarts_after_inserted_break": ["AC-1.5"],
  "test_text_shorter_than_column_width_is_unchanged": ["AC-1.1"],
  "test_preserves_tab_indentation_after_newline": ["AC-4.3"],
  "test_line_exactly_at_width_with_space_is_unchanged": ["AC-1.1"],
  "test_break_at_space_in_second_position": ["AC-1.4"],
  "test_leading_space_line_hard_breaks_at_width": ["AC-4.4"],
  "test_tab_after_break_space_is_preserved": ["AC-4.1"],
  "test_word_starting_with_x_survives_break": ["AC-4.2"],
  "test_trailing_spaces_do_not_produce_trailing_newline": ["AC-2.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
