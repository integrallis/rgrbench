"""Poker Hands kata: rank five-card poker hands and compare two players.

A hand is a space-separated string of five cards. Each card is a value
(2-9, 10 or T, J, Q, K, A - ace always high) followed by a suit
(C, D, H, S). Suits carry no ordering.

Categories from lowest to highest: high card, pair, two pairs, three of
a kind, straight (five consecutive values), flush (five cards of one
suit), full house, four of a kind, straight flush. A-2-3-4-5 does not
count as a straight because aces rank high only. Within a category, ties
break on card values in spec order: pair value before kickers, higher
pair before lower pair before kicker, triple before pair, otherwise
values descending.

`hand_category(hand)` names a hand's category. `compare_hands(black,
white)` reports the outcome: 'Tie.' when ranks are equal,
'<Name> wins. - with <category>' when categories differ, and
'<Name> wins. - with <category>: <value>' when the same category is
decided on values, naming the first value that differs (face cards and
aces are spelled out: Jack, Queen, King, Ace). Malformed cards or hands
without exactly five cards raise ValueError.

Kata catalogued at tddbuddy.com/katas/poker-hands; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""

from poker_hands.poker import CATEGORIES, compare_hands, hand_category

__all__ = ["CATEGORIES", "compare_hands", "hand_category"]
