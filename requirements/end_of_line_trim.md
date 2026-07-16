# Trailing whitespace cleaner for multi-line text

## Overview
A text-tidying operation that removes trailing spaces and tabs from the end of every line in a piece of text while leaving everything else untouched: leading indentation, spacing inside the line, and each line's original ending all survive. It handles Unix (`\n`) and Windows (`\r\n`) line endings, even when both styles appear in the same text, and it treats a carriage return that is not part of a Windows ending as ordinary content rather than a line break.

## User Stories

### US-1: Remove trailing whitespace from every line
As a developer, I want trailing spaces and tabs stripped from the end of each line, so that my text is free of invisible end-of-line clutter.

- AC-1.1: A trailing space at the end of a line is removed.
- AC-1.2: A trailing tab at the end of a line is removed.
- AC-1.3: A mixed run of trailing spaces and tabs is removed entirely.
- AC-1.4: Every line of a multi-line text is trimmed — including the final line when it has no line ending.
- AC-1.5: Only spaces and tabs are ever removed; any other character at the end of a line stays, on every line-ending style.

### US-2: Preserve all other whitespace and content
As a developer, I want everything that is not trailing whitespace preserved exactly, so that trimming never changes the meaning or layout of my text.

- AC-2.1: Text containing no trailing whitespace is returned unchanged.
- AC-2.2: Leading spaces and tabs at the start of a line are preserved, on every line.
- AC-2.3: Whitespace between words inside a line is untouched.
- AC-2.4: The empty text trims to the empty text.

### US-3: Keep each line's original ending
As a developer, I want each line to keep its own line ending, so that files retain their Unix, Windows, or mixed line-ending style.

- AC-3.1: A Unix line ending (`\n`) is kept as-is.
- AC-3.2: A Windows line ending (`\r\n`) is kept as-is; trailing whitespace just before it is removed.
- AC-3.3: Unix and Windows endings mixed within a single text are each preserved where they occur.
- AC-3.4: A line consisting only of whitespace keeps just its line ending.
- AC-3.5: A text consisting solely of a line ending (`\n` alone, or `\r\n` alone) is returned unchanged.

### US-4: Treat lone carriage returns as content
As a developer, I want a carriage return that is not followed by a line feed treated as ordinary content, so that trimming never corrupts data containing stray carriage returns.

- AC-4.1: A carriage return not followed by a line feed does not end a line; it stays in place as content, including when it is the very last character of the text.
- AC-4.2: Whitespace before such a carriage return is interior, not trailing, and is preserved; spaces or tabs after it and before the line's ending are trailing and are removed.
- AC-4.3: A content carriage return sitting immediately before a Windows line ending survives: in the text `a\r\r\n`, the first carriage return is content and is kept.

## Traceability
```json
{
  "test_text_without_trailing_whitespace_is_unchanged": ["AC-2.1"],
  "test_trailing_space_is_removed": ["AC-1.1"],
  "test_trailing_tab_is_removed": ["AC-1.2"],
  "test_leading_whitespace_is_preserved": ["AC-2.2"],
  "test_windows_line_endings_are_preserved": ["AC-3.2"],
  "test_terminator_only_line_passes_through": ["AC-3.5"],
  "test_empty_string_is_unchanged": ["AC-2.4"],
  "test_mixed_line_endings_are_each_preserved": ["AC-3.1", "AC-3.2", "AC-3.3"],
  "test_lone_carriage_return_is_content": ["AC-4.1", "AC-4.2"],
  "test_mixed_trailing_spaces_and_tabs_are_removed": ["AC-1.3"],
  "test_interior_whitespace_is_preserved": ["AC-2.3"],
  "test_whitespace_only_unix_line_keeps_terminator": ["AC-3.4"],
  "test_every_line_is_trimmed": ["AC-1.4"],
  "test_bare_newline_is_unchanged": ["AC-3.5"],
  "test_leading_whitespace_preserved_on_every_line": ["AC-2.2"],
  "test_lone_carriage_return_at_end_of_input_is_content": ["AC-4.1"],
  "test_carriage_return_before_crlf_terminator_is_content": ["AC-4.3"],
  "test_content_carriage_return_survives_trimming_before_newline": ["AC-4.2"],
  "test_only_spaces_and_tabs_are_trimmed_never_other_characters": ["AC-1.5"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
