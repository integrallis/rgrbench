# Account number optical character recognition

## Overview
A back-office tool that reads bank account numbers scanned from paper. Each scanned entry is three lines of 27 characters, forming nine cells three characters wide; each cell draws one digit out of pipes and underscores. The tool decodes entries into nine-digit account numbers, validates them with a checksum, classifies problem entries, and attempts to repair entries damaged by a single missing or spurious stroke.

The ten digits are drawn as follows (0 through 9, each three characters wide across the three lines):

```text
 _     _  _     _  _  _  _  _ 
| |  | _| _||_||_ |_   ||_||_|
|_|  ||_  _|  | _||_|  ||_| _|
```

## User Stories

### US-1: Decode a scanned entry
As a back-office operator, I want a scanned entry decoded into its nine digits, so that account numbers can be processed automatically.

- AC-1.1: Every one of the ten digit shapes is recognised, and a full entry decodes to its nine-digit account number (worked examples: all zeros, all ones, and the canonical ascending entry decoding to 123456789).
- AC-1.2: A cell that matches no digit shape is decoded as "?" in its position, with the remaining cells decoded normally.
- AC-1.3: An entry that does not consist of exactly three content lines is rejected with an error whose message is exactly "entry must have exactly three lines".
- AC-1.4: A trailing blank fourth line (a trailing newline) is tolerated and does not affect decoding.
- AC-1.5: Lines shorter than 27 characters are treated as padded with trailing spaces, so an entry whose trailing spaces were stripped decodes to the same digits.

### US-2: Validate the account number checksum
As a back-office operator, I want each decoded number checked against the bank's checksum, so that misreads are caught.

- AC-2.1: A nine-digit number is valid when the weighted sum — leftmost digit times 9, next times 8, on down to the rightmost digit times 1 — is divisible by 11 (worked examples: 345882865, 123456789, and 000000000 are valid).
- AC-2.2: 111111111 is invalid: its weighted sum is 45, which leaves remainder 1 when divided by 11.
- AC-2.3: A string containing any non-digit character, or not exactly nine characters long, is never valid.

### US-3: Classify decoded entries
As a back-office operator, I want each entry's status reported next to its number, so that problem entries can be routed for follow-up.

- AC-3.1: A fully readable entry that passes the checksum is reported as the bare account number.
- AC-3.2: A fully readable entry that fails the checksum is reported with the suffix " ERR" (e.g. "111111111 ERR").
- AC-3.3: An entry with one or more unreadable cells is reported with "?" in the unreadable positions and the suffix " ILL" (e.g. "?23456789 ILL").

### US-4: Repair single-stroke damage
As a back-office operator, I want plausibly damaged entries repaired automatically, so that fewer entries need manual review — on the assumption that at most one stroke (one pipe or underscore) was added or lost in scanning.

- AC-4.1: An entry that is already readable and checksum-valid is reported unchanged as its bare number.
- AC-4.2: When exactly one single-stroke change to one cell yields exactly one checksum-valid number, that corrected number is reported as the result — whether the flaw was a checksum failure (worked examples: 111111111 repairs to 711111111; 777777777 to 777777177; 200000000 to 200800000; 333333333 to 333393333) or a single unreadable cell whose unique one-stroke completion is valid (a damaged ascending entry repairs to 123456789).
- AC-4.3: When several single-stroke repairs each yield a valid number, the entry is ambiguous: the result is the decoded number, the marker " AMB ", and the candidate numbers in ascending order, formatted as a bracketed list of quoted values. Worked examples:
  - all eights: "888888888 AMB ['888886888', '888888880', '888888988']"
  - all fives: "555555555 AMB ['555655555', '559555555']"
  - "490067715 AMB ['490067115', '490067719', '490867715']"
- AC-4.4: An entry with two or more unreadable cells cannot be repaired by a single-stroke change and is reported with its "?" placeholders and the suffix " ILL".
- AC-4.5: A readable, checksum-failing entry with no valid single-stroke repair is reported with the suffix " ERR" (worked example: "222222222 ERR").

## Traceability
```json
{
  "test_parses_all_zeros": ["AC-1.1"],
  "test_parses_all_ones": ["AC-1.1"],
  "test_parses_ascending_digits": ["AC-1.1"],
  "test_parses_each_digit": ["AC-1.1"],
  "test_unreadable_cell_parses_as_question_mark": ["AC-1.2"],
  "test_parse_rejects_wrong_line_count": ["AC-1.3"],
  "test_parse_tolerates_trailing_blank_line": ["AC-1.4"],
  "test_checksum_accepts_spec_example": ["AC-2.1"],
  "test_checksum_accepts_ascending_digits": ["AC-2.1"],
  "test_checksum_accepts_all_zeros": ["AC-2.1"],
  "test_checksum_rejects_all_ones": ["AC-2.2"],
  "test_checksum_rejects_non_digit_and_wrong_length": ["AC-2.3"],
  "test_status_of_valid_entry_is_number_only": ["AC-3.1"],
  "test_status_of_checksum_failure_is_err": ["AC-3.2"],
  "test_status_of_unreadable_entry_is_ill": ["AC-3.3"],
  "test_fix_leaves_valid_entry_unchanged": ["AC-4.1"],
  "test_fix_all_ones_to_711111111": ["AC-4.2"],
  "test_fix_all_sevens_to_777777177": ["AC-4.2"],
  "test_fix_200000000_to_200800000": ["AC-4.2"],
  "test_fix_all_threes_to_333393333": ["AC-4.2"],
  "test_fix_all_eights_is_ambiguous": ["AC-4.3"],
  "test_fix_all_fives_is_ambiguous": ["AC-4.3"],
  "test_fix_490067715_is_ambiguous": ["AC-4.3"],
  "test_fix_recovers_single_unreadable_cell": ["AC-4.2"],
  "test_fix_cannot_recover_two_unreadable_cells": ["AC-4.4"],
  "test_fix_reports_err_when_no_candidate_exists": ["AC-4.5"],
  "test_parse_rejects_wrong_line_count_with_exact_message": ["AC-1.3"],
  "test_parse_pads_short_lines_with_trailing_spaces": ["AC-1.5"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
