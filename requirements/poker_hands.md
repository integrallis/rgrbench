# Poker hand ranking and showdown

## Overview
A poker judge reads five-card hands written in compact card notation, names the category
each hand belongs to, and decides a two-player showdown between Black and White. The
verdict announces the winner and the winning category, and when both players hold the
same category it also announces the card value that settled the contest.

## User Stories

### US-1: Reading hands in card notation
As a player, I want hands written in a compact, checkable notation, so that games can be recorded unambiguously and typos are caught.

- AC-1.1: A hand is five cards separated by single spaces; each card is a value followed
  by a suit letter, with suits hearts "H", diamonds "D", spades "S", and clubs "C".
- AC-1.2: Card values are 2 through 9, the ten (written either "T" or "10"), jack "J",
  queen "Q", king "K", and ace "A".
- AC-1.3: A hand with other than exactly five cards is refused with the message exactly
  "a hand must contain exactly 5 cards".
- AC-1.4: A card with an unknown value or an unknown suit is refused with a message
  naming the offending card, in the form "invalid card: '1Z'".

### US-2: Naming the hand category
As a player, I want each hand assigned its poker category, so that hands can be talked about and ranked by name.

- AC-2.1: Two cards of the same value form a "pair".
- AC-2.2: Two different pairs form "two pairs".
- AC-2.3: Three cards of the same value form "three of a kind".
- AC-2.4: Five consecutive values of mixed suits form a "straight".
- AC-2.5: Five cards of one suit with non-consecutive values form a "flush".
- AC-2.6: Three cards of one value plus a pair of another form a "full house".
- AC-2.7: Four cards of the same value form "four of a kind".
- AC-2.8: Five consecutive values in a single suit form a "straight flush".
- AC-2.9: A hand with none of these combinations is a "high card" hand.
- AC-2.10: Aces rank high only: ace-2-3-4-5 is not a straight and counts as a high card
  hand.

### US-3: Deciding a showdown
As a pair of players, we want two hands compared and the result announced, so that every game ends with a clear, explainable verdict.

- AC-3.1: A showdown compares Black's hand (given first) against White's hand (given
  second).
- AC-3.2: Categories rank, from lowest to highest: high card, pair, two pairs, three of
  a kind, straight, flush, full house, four of a kind, straight flush; a full house
  therefore beats a flush, and a straight flush beats four of a kind.
- AC-3.3: When the categories differ, the verdict names the winner and the winning
  category only, in the form "Black wins. - with full house" or
  "White wins. - with straight flush".
- AC-3.4: When both hands share a category, card values decide, and the verdict appends
  the deciding value, in the form "White wins. - with high card: Ace".
- AC-3.5: High card hands compare their highest values first; equal values fall through
  to the next highest, and the announced value is the one that decided (kings tie, so a
  9 beats an 8 and the verdict reads "Black wins. - with high card: 9").
- AC-3.6: Between pairs, the higher pair value wins ("Black wins. - with pair: 8");
  equal pairs fall through to the highest remaining card, which is announced as the
  deciding value ("Black wins. - with pair: King").
- AC-3.7: Between two-pair hands, the higher pair is compared first and equal high pairs
  fall through to the lower pair ("Black wins. - with two pairs: 5").
- AC-3.8: Between straights, the higher-topped run wins
  ("White wins. - with straight: 7").
- AC-3.9: Between flushes, high-card comparison decides
  ("Black wins. - with flush: Ace").
- AC-3.10: Between four-of-a-kind hands, the value of the four decides and outweighs any
  remaining card ("Black wins. - with four of a kind: 9").
- AC-3.11: Deciding values are announced with face cards spelled out ("Ace", "King"),
  the ten written "10", and other values as digits.
- AC-3.12: Hands equal in every value are a tie regardless of suits, and the verdict is
  exactly "Tie.".

## Traceability
```json
{
  "test_high_card_category": ["AC-2.9"],
  "test_pair_category": ["AC-2.1"],
  "test_two_pairs_category": ["AC-2.2"],
  "test_three_of_a_kind_category": ["AC-2.3"],
  "test_straight_category": ["AC-2.4"],
  "test_flush_category": ["AC-2.5"],
  "test_full_house_category": ["AC-2.6"],
  "test_four_of_a_kind_category": ["AC-2.7"],
  "test_straight_flush_category": ["AC-2.8", "AC-1.2"],
  "test_ace_is_high_only_so_wheel_is_not_a_straight": ["AC-2.10"],
  "test_t_is_the_ten_card": ["AC-1.2"],
  "test_high_card_decided_by_ace": ["AC-3.1", "AC-3.4", "AC-3.5", "AC-3.11"],
  "test_full_house_beats_flush": ["AC-3.2", "AC-3.3"],
  "test_high_card_tie_broken_by_next_highest": ["AC-3.5"],
  "test_identical_ranks_tie": ["AC-3.12"],
  "test_pair_decided_by_pair_value": ["AC-3.6"],
  "test_equal_pairs_decided_by_kicker": ["AC-3.6", "AC-3.11"],
  "test_two_pairs_decided_by_second_pair": ["AC-3.7"],
  "test_straight_decided_by_highest_card": ["AC-3.8"],
  "test_straight_flush_beats_four_of_a_kind": ["AC-3.2", "AC-3.3"],
  "test_flush_decided_by_high_card_rules": ["AC-3.9"],
  "test_four_of_a_kind_decided_by_quad_value": ["AC-3.10"],
  "test_ten_is_named_10_in_the_verdict": ["AC-3.11"],
  "test_wrong_card_count_is_rejected": ["AC-1.3"],
  "test_malformed_card_is_rejected": ["AC-1.4"],
  "test_card_with_unknown_suit_is_rejected": ["AC-1.4"],
  "test_card_with_unknown_value_is_rejected": ["AC-1.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
