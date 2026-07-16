# Judging rock-paper-scissors-Spock rounds

## Overview
A referee judges a single round of rock-paper-scissors extended with Spock. Given the player's move and the opponent's move, it delivers a verdict from the player's perspective — a win, a loss, or a tie — according to the classic circle plus Spock's extra rules.

## User Stories

### US-1: Judging the classic pairings
As a player, I want the classic rules enforced, so that familiar rounds resolve the way everyone expects.

- AC-1.1: Rock beats scissors: rock against scissors is a win for the player, and scissors against rock is a loss.
- AC-1.2: Scissors beat paper: scissors against paper is a win for the player, and paper against scissors is a loss.
- AC-1.3: Paper beats rock: paper against rock is a win for the player, and rock against paper is a loss.

### US-2: Judging Spock's pairings
As a player, I want Spock's rules enforced, so that the extended game resolves correctly.

- AC-2.1: Spock smashes scissors: Spock against scissors is a win for the player, and scissors against Spock is a loss.
- AC-2.2: Spock vaporizes rock: Spock against rock is a win for the player, and rock against Spock is a loss.
- AC-2.3: Paper disproves Spock: paper against Spock is a win for the player, and Spock against paper is a loss.

### US-3: Tying on identical moves
As a player, I want matching moves to tie, so that neither side is favored when both choose alike.

- AC-3.1: Identical moves tie: rock against rock, paper against paper, scissors against scissors, and Spock against Spock.
- AC-3.2: A round ties exactly when the two moves are identical; differing moves never tie.

### US-4: Completing and balancing the rule book
As a game designer, I want the rules total and symmetric, so that every possible round has one fair verdict.

- AC-4.1: Every pairing of the four moves yields one of the three verdicts.
- AC-4.2: Verdicts are symmetric: whenever a pairing is a win for the player, the same moves swapped are a loss.

### US-5: Closing the move and verdict vocabularies
As a game designer, I want the sets of moves and verdicts fixed, so that no unexpected values can enter play.

- AC-5.1: The moves are exactly four, named ROCK, PAPER, SCISSORS, and SPOCK.
- AC-5.2: The verdicts are exactly three, named PLAYER_WINS, PLAYER_LOSES, and TIE.

## Traceability
```json
{
  "test_rock_beats_scissors": ["AC-1.1"],
  "test_scissors_beat_paper": ["AC-1.2"],
  "test_paper_beats_rock": ["AC-1.3"],
  "test_scissors_lose_to_rock": ["AC-1.1"],
  "test_paper_loses_to_scissors": ["AC-1.2"],
  "test_rock_loses_to_paper": ["AC-1.3"],
  "test_rock_ties_rock": ["AC-3.1"],
  "test_paper_ties_paper": ["AC-3.1"],
  "test_scissors_tie_scissors": ["AC-3.1"],
  "test_spock_smashes_scissors": ["AC-2.1"],
  "test_spock_vaporizes_rock": ["AC-2.2"],
  "test_paper_disproves_spock": ["AC-2.3"],
  "test_spock_ties_spock": ["AC-3.1"],
  "test_every_pairing_has_a_verdict": ["AC-4.1"],
  "test_ties_happen_exactly_on_identical_moves": ["AC-3.2"],
  "test_wins_and_losses_are_symmetric": ["AC-4.2"],
  "test_moves_form_a_closed_set_of_four": ["AC-5.1"],
  "test_outcomes_form_a_closed_set_of_three": ["AC-5.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
