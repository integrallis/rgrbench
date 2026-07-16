# Line-bounded character copying

## Overview
A copier moves characters from a source to a destination, stopping at the first newline, which is never written. It can work one character at a time or in fixed-size batches; either way nothing at or beyond the first newline reaches the destination, and a source that runs dry simply ends the copy.

## User Stories

### US-1: Copy one character at a time
As a consumer of the destination, I want every character before the first newline copied over in order, so that the destination holds exactly the first line of the source.

- AC-1.1: Characters before the newline are written one by one, in source order.
- AC-1.2: When the very first character is a newline, nothing is written.
- AC-1.3: The terminating newline itself is never written.
- AC-1.4: Content after the newline is never copied.
- AC-1.5: Reading stops immediately after the newline is consumed; later source content is left unread.
- AC-1.6: A source that runs out before any newline ends the copy, with everything read so far already written.
- AC-1.7: Ordinary characters — including spaces and punctuation — are copied verbatim.

### US-2: Copy in batches
As a consumer moving longer lines, I want the copier to transfer characters in fixed-size batches, so that copying needs fewer read and write operations.

- AC-2.1: A batch containing no newline is written whole, as a single write.
- AC-2.2: A batch containing the newline is written only up to, and excluding, the newline.
- AC-2.3: A source that begins with a newline produces no writes.
- AC-2.4: Batches keep being read and written until the newline appears, each full batch delivered as one write.
- AC-2.5: Nothing beyond the first newline is ever written, even when the newline falls in the middle of a batch.
- AC-2.6: A batch shorter than requested means the source is exhausted: the shortfall is still written, then copying stops.
- AC-2.7: An empty source produces no writes at all.
- AC-2.8: When a batch holds more than one newline, copying is cut at the first, not the last.

### US-3: Batch size validation
As a caller, I want impossible batch sizes rejected up front, so that misuse is caught instead of silently mis-copying.

- AC-3.1: A batch size below 1 is rejected with an error whose message is exactly "count must be at least 1".
- AC-3.2: A batch size of exactly 1 is accepted and copies one character per write.

## Traceability
```json
{
  "test_copies_a_single_character_before_newline": ["AC-1.1"],
  "test_copies_characters_in_order": ["AC-1.1"],
  "test_writes_nothing_when_first_character_is_newline": ["AC-1.2"],
  "test_newline_itself_is_never_written": ["AC-1.3"],
  "test_characters_after_newline_are_not_copied": ["AC-1.4"],
  "test_reading_stops_at_the_newline": ["AC-1.5"],
  "test_exhausted_source_stops_copying": ["AC-1.6"],
  "test_copies_spaces_and_punctuation": ["AC-1.7"],
  "test_copy_multiple_copies_chunk_before_newline": ["AC-2.1"],
  "test_copy_multiple_truncates_chunk_at_newline": ["AC-2.2"],
  "test_copy_multiple_writes_nothing_for_leading_newline": ["AC-2.3"],
  "test_copy_multiple_spans_several_chunks_until_newline": ["AC-2.4"],
  "test_copy_multiple_never_writes_past_the_newline": ["AC-2.5"],
  "test_copy_multiple_stops_on_short_chunk": ["AC-2.6"],
  "test_copy_multiple_with_empty_source_writes_nothing": ["AC-2.7"],
  "test_copy_multiple_rejects_non_positive_count": ["AC-3.1"],
  "test_copy_multiple_accepts_a_count_of_one": ["AC-3.2"],
  "test_copy_multiple_rejection_message_is_exact": ["AC-3.1"],
  "test_copy_multiple_stops_at_the_first_newline_in_a_chunk": ["AC-2.8"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
