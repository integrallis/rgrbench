# Fixed-width text justification

## Overview
A typesetting service lays a passage of text out as fully justified lines of a fixed column width: words are packed greedily onto lines, the gaps inside every line but the last are padded so those lines are exactly the column width, and the final line sits flush-left. Words are never broken, messy source spacing is tolerated, and invalid requests are refused with clear messages.

## User Stories

### US-1: Flow words onto lines
As a typesetter, I want words flowed greedily onto lines of a fixed width, so that each line carries as many words as fit.

- AC-1.1: Text that fits within the width comes back as a single line, unchanged — a single short word likewise.
- AC-1.2: Text exactly as long as the width fits on one line.
- AC-1.3: Words are packed greedily: each line takes as many of the following words as fit within the width with at least one space between them, then the text flows on to the next line; the result is the sequence of lines. At width one, every word gets its own line; words that exactly fill a later line share that line.

### US-2: Justify to both margins
As a reader, I want full justification, so that both margins are straight.

- AC-2.1: Every line except the last is padded to exactly the column width.
- AC-2.2: Padding spaces are distributed across the gaps between a line's words as evenly as possible.
- AC-2.3: When padding cannot divide evenly, the leftover spaces go to the leftmost gaps ("a b c d" at width 6 gives "a  b c" then "d").
- AC-2.4: The final line sits flush-left with single spaces between words and no right padding.
- AC-2.5: A line before the last that carries a single word is right-padded with spaces out to the width.
- AC-2.6: Canonical worked example: "This is an example of text justification." at width 16 yields exactly the lines "This    is    an", "example  of text", "justification.".

### US-3: Keep oversize words whole
As a typesetter, I want words longer than the column width kept whole, so that no word is ever broken.

- AC-3.1: A word longer than the width is placed alone on its own line and overflows the width rather than being split; this holds even when it is the only word in the text.

### US-4: Tolerate messy source spacing
As a typesetter, I want any run of whitespace in the source treated as one word separator, so that sloppy spacing does not affect the layout.

- AC-4.1: Consecutive blanks in the source count as a single separator.
- AC-4.2: Tabs and line breaks separate words exactly like spaces.
- AC-4.3: Empty or whitespace-only text produces no lines at all.

### US-5: Refuse invalid requests
As a typesetter, I want invalid requests refused clearly, so that mistakes surface immediately.

- AC-5.1: The column width must be a positive whole number; a zero or negative width is refused with the message exactly "width must be a positive integer".
- AC-5.2: A missing text is refused with the message exactly "text must not be None".

## Traceability
```json
{
  "test_single_word_is_returned_as_is": ["AC-1.1"],
  "test_text_fitting_one_line_needs_no_justification": ["AC-1.1"],
  "test_text_exactly_at_width_fits_one_line": ["AC-1.2"],
  "test_break_into_two_lines_with_left_aligned_last_line": ["AC-1.3", "AC-2.4"],
  "test_even_space_distribution": ["AC-2.2"],
  "test_uneven_padding_is_left_heavy": ["AC-2.3"],
  "test_multiple_line_breaks": ["AC-1.3", "AC-2.2"],
  "test_classic_leetcode_example_with_flush_left_last_line": ["AC-2.6", "AC-2.4"],
  "test_single_word_non_last_line_is_right_padded": ["AC-2.5"],
  "test_oversize_word_overflows_instead_of_splitting": ["AC-3.1"],
  "test_oversize_single_word": ["AC-3.1"],
  "test_consecutive_spaces_collapse": ["AC-4.1"],
  "test_tabs_and_line_breaks_are_separators": ["AC-4.2"],
  "test_width_of_one": ["AC-1.3"],
  "test_empty_text_justifies_to_no_lines": ["AC-4.3"],
  "test_whitespace_only_text_justifies_to_no_lines": ["AC-4.3"],
  "test_zero_width_is_rejected": ["AC-5.1"],
  "test_negative_width_is_rejected": ["AC-5.1"],
  "test_none_text_is_rejected": ["AC-5.2"],
  "test_every_non_final_line_is_exactly_the_width": ["AC-2.1"],
  "test_words_exactly_filling_a_later_line_share_it": ["AC-1.3", "AC-2.5"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
