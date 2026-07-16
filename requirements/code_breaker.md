# Code-breaking feedback scorer

## Overview
A feedback scorer for a Mastermind-style code-breaking game. A secret code is fixed when the game is set up; each guess is answered with a feedback string holding one plus sign per digit that is correct and in the correct position and one minus sign per digit that occurs in the secret but sits in the wrong position, with every plus reported before any minus. Exact matches are consumed first, duplicated digits earn only as many symbols as the secret has copies to give, and there is no randomness anywhere.

## User Stories

### US-1: Score a guess against the secret
As a code-breaking player, I want each guess answered with plus-and-minus feedback, so that I can deduce the secret by elimination.

- AC-1.1: A guess sharing no digits with the secret earns empty feedback: secret 1234, guess 5678 gives "".
- AC-1.2: Each guess digit equal to the secret's digit in the same position earns one "+": secret 1234, guess 1578 gives "+"; a fully correct guess earns one "+" per position, so secret 1234, guess 1234 gives "++++".
- AC-1.3: Each guess digit that occurs in the secret at a different position earns one "-": secret 1234, guess 4321 gives "----".
- AC-1.4: All plusses precede all minuses, regardless of where in the guess the matches sit: secret 1234, guess 1243 gives "++--", and guess 2134 also gives "++--".
- AC-1.5: Exact matches are consumed before partial ones: with secret 1124, guess 5167 earns just "+" because the exactly-matched digit cannot also earn a "-"; with secret 1111, guess 1112 earns "+++".
- AC-1.6: Duplicated digits earn only as many symbols as the secret holds copies: secret 1234, guess 5115 gives "-", while secret 1122, guess 2211 gives "----".

### US-2: Reusable scorer
As a player, I want to score many guesses against one secret, so that a whole game can be played against a single setup.

- AC-2.1: The same scorer answers successive guesses independently, each judged afresh against the unchanged secret.

### US-3: Secret validation
As a game host, I want malformed secrets rejected at setup, so that every game starts from a playable code.

- AC-3.1: A secret shorter than 4 or longer than 6 characters is rejected with the message exactly "code must be 4 to 6 characters long".
- AC-3.2: A secret containing characters outside the digit alphabet — by default the digits 1 through 6 — is rejected with the message exactly "code may only contain characters from '123456'".

### US-4: Guess validation and tolerance
As a game host, I want guesses checked for shape but tolerated for content, so that any well-formed attempt can be scored.

- AC-4.1: A guess whose length differs from the secret's is rejected with the message exactly "guess must be the same length as the secret".
- AC-4.2: Guess digits outside the alphabet are legal but can never match anything: secret 1234, guess 1789 gives "+".

### US-5: Longer codes and wider alphabets
As a game host, I want longer secrets and wider digit ranges available, so that harder games can be offered.

- AC-5.1: Secrets of 5 and 6 digits are supported and scored position for position like 4-digit ones, including all-exact and all-partial feedback.
- AC-5.2: A custom alphabet may be supplied, admitting digits the default rejects: with an alphabet of 1 through 8, secret 1278 scores guess 1287 as "++--".

## Traceability
```json
{
  "test_no_matching_digits_gives_empty_feedback": ["AC-1.1"],
  "test_single_exact_match": ["AC-1.2"],
  "test_all_exact_matches": ["AC-1.2"],
  "test_all_partial_matches": ["AC-1.3"],
  "test_mixed_exact_and_partial_matches": ["AC-1.4"],
  "test_exact_match_consumes_duplicate_secret_digit": ["AC-1.5"],
  "test_guess_digit_absent_from_secret_earns_nothing": ["AC-1.1", "AC-1.2"],
  "test_plusses_precede_minuses_regardless_of_position": ["AC-1.4"],
  "test_duplicate_guess_digits_earn_only_available_copies": ["AC-1.6"],
  "test_duplicate_secret_digits_reward_duplicate_guesses": ["AC-1.6"],
  "test_same_instance_scores_multiple_guesses": ["AC-2.1"],
  "test_secret_shorter_than_four_digits_is_rejected": ["AC-3.1"],
  "test_secret_longer_than_six_digits_is_rejected": ["AC-3.1"],
  "test_secret_with_digit_outside_alphabet_is_rejected": ["AC-3.2"],
  "test_guess_digits_outside_alphabet_simply_never_match": ["AC-4.2"],
  "test_guess_length_must_match_secret_length": ["AC-4.1"],
  "test_bonus_five_digit_code_is_supported": ["AC-5.1"],
  "test_bonus_custom_digit_range_is_supported": ["AC-5.2"],
  "test_bonus_six_digit_code_is_supported": ["AC-5.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
