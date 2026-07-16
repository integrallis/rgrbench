"""US-style Bingo kata: card state, marking called numbers, win detection.

A bingo card is a 5x5 grid whose columns B, I, N, G, and O hold unique
numbers drawn from the ranges 1-15, 16-30, 31-45, 46-60, and 61-75.
The centre space (third row of the N column) is a free space that is
marked from the start, so the N column holds only four numbers. Called
numbers are supplied as inputs: the game calls numbers between 1 and 75
with no repeats, and a call marks the matching space when the number is
on the card. A card has bingo once a full row, a full column, or either
main diagonal is completely marked; the free space counts toward any
line passing through it. Random card generation, caller services, and
game loops are out of scope.

Kata catalogued at tddbuddy.com/katas/bingo; implementation and tests
original (MIT), machine-authored from the specification, 2026.
"""

from bingo.card import COLUMN_RANGES, BingoCard, column_letter

__all__ = ["COLUMN_RANGES", "BingoCard", "column_letter"]
