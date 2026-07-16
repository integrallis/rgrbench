# Pocket calculator digit entry

## Overview
The digit-entry display of a pocket calculator, modelled from switch-on through key presses, together with a small companion generator that supplies randomised digit keys for exercising it. The display follows ordinary calculator conventions: it opens on zero, shows digits in the order they are pressed, and never shows a redundant leading zero.

## User Stories

### US-1: Switch-on state
As a calculator user, I want the display to read zero when the calculator is first created, so that every calculation starts from a known value.

- AC-1.1: A freshly created calculator displays zero.

### US-2: Digit entry
As a calculator user, I want pressed digit keys to appear on the display in the order I press them, so that the display always shows the number I have entered.

- AC-2.1: A sequence of digit key presses beginning with a non-zero digit is displayed as those digits concatenated in entry order.
- AC-2.2: Pressing only the zero key, any number of times, displays a single zero.
- AC-2.3: A leading zero is replaced by the first non-zero digit: pressing zero then five reads "5", not "05".
- AC-2.4: Zeros pressed after a non-zero digit are significant: pressing one, zero, five reads "105".

### US-3: Randomised digit selection
As a specification author, I want a generator that picks an arbitrary digit key, optionally excluding one, so that behaviour can be described without hard-coding particular digits.

- AC-3.1: Asking for a digit key other than a given one always yields a valid digit key and never the excluded one, whichever digit key is excluded.
- AC-3.2: Asking for a value other than something that is not a digit key is refused with a not-implemented error naming the offending type; for a plain text value the message is exactly "other_than not implemented for <class 'str'>".

## Traceability
```json
{
  "test_should_display_0_when_created": ["AC-1.1"],
  "test_should_display_entered_digits": ["AC-2.1"],
  "test_should_display_only_one_zero_digit_if_it_is_the_only_entered_digit_even_if_it_is_entered_multiple_times": ["AC-2.2"],
  "test_any_other_than_never_returns_the_excluded_digit": ["AC-3.1"],
  "test_any_other_than_rejects_unsupported_types": ["AC-3.2"],
  "test_nonzero_digit_replaces_leading_zero": ["AC-2.3"],
  "test_zero_after_nonzero_digits_is_kept": ["AC-2.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
