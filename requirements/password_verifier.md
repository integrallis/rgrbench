# Password strength verification

## Overview
A password verifier checks candidate passwords against a fixed set of strength rules:
the password must be present, longer than 8 characters, and contain at least one
uppercase letter, one lowercase letter, and one number. A password satisfying every rule
is accepted; a password breaking any rule is refused with a message that states the
broken rule verbatim.

## User Stories

### US-1: Accepting strong passwords
As a user setting a password, I want a password that meets every rule to be accepted, so that I can complete registration.

- AC-1.1: A password longer than 8 characters that contains at least one uppercase
  letter, one lowercase letter, and one number is accepted, and verification reports
  success.
- AC-1.2: The length rule is strict: a password of exactly 9 characters that meets the
  other rules is accepted.

### US-2: Refusing weak passwords with rule-specific messages
As a user setting a password, I want a refused password to tell me exactly which rule it broke, so that I can correct it.

- AC-2.1: A missing password is refused with the message exactly
  "Password should not be null".
- AC-2.2: A password of 8 or fewer characters is refused with the message exactly
  "Password should be longer than 8 characters"; exactly 8 characters is still too
  short.
- AC-2.3: A password with no uppercase letter is refused with the message exactly
  "Password should have at least one uppercase letter".
- AC-2.4: A password with no lowercase letter is refused with the message exactly
  "Password should have at least one lowercase letter".
- AC-2.5: A password with no number is refused with the message exactly
  "Password should have at least one number".
- AC-2.6: A password breaking several rules at once is refused for its shortness first:
  a too-short password is reported against the length rule even when it also lacks an
  uppercase letter and a number.

## Traceability
```json
{
  "test_password_shorter_than_8_chars_should_raise_exception": ["AC-2.2", "AC-2.6"],
  "test_password_longer_than_8_chars_should_be_valid": ["AC-1.1"],
  "test_password_null_should_raise_exception": ["AC-2.1"],
  "test_password_without_uppercase_should_raise_exception": ["AC-2.3"],
  "test_password_without_lowercase_should_raise_exception": ["AC-2.4"],
  "test_password_without_number_should_raise_exception": ["AC-2.5"],
  "test_valid_password_with_all_requirements_should_pass": ["AC-1.1"],
  "test_password_with_exactly_8_chars_should_raise_exception": ["AC-2.2"],
  "test_password_with_exactly_9_chars_should_be_valid": ["AC-1.2"],
  "test_null_password_error_message_should_be_exact": ["AC-2.1"],
  "test_short_password_error_message_should_be_exact": ["AC-2.2", "AC-2.6"],
  "test_password_without_uppercase_error_message_should_be_exact": ["AC-2.3"],
  "test_password_without_lowercase_error_message_should_be_exact": ["AC-2.4"],
  "test_password_without_number_error_message_should_be_exact": ["AC-2.5"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
