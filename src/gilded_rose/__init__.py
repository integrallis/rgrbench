"""Gilded Rose kata (greenfield spec implementation).

An inn's inventory system updates every item at the end of each day. Items
carry a name, a sell_in counter (days left to sell) and a quality score.
Each day sell_in drops by one and quality changes by category: regular items
lose 1 quality per day and 2 once the sell-by date has passed; quality never
falls below 0 nor rises above 50. "Aged Brie" gains quality instead — 1 per
day, 2 after its date, capped at 50. "Sulfuras, Hand of Ragnaros" is
legendary: its sell_in and quality (always 80) never change. Backstage passes
gain 1 quality per day, 2 when 10 or fewer days remain, 3 when 5 or fewer
remain, and drop to 0 once the concert has passed. Conjured items degrade
twice as fast as regular ones (2 per day, 4 after the date). This module
implements those rules directly as a clean behaviour suite rather than the
legacy-refactoring exercise.

Kata catalogued at tddbuddy.com/katas/gilded-rose; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from gilded_rose.gilded_rose import (
    AGED_BRIE,
    BACKSTAGE_PASS,
    CONJURED_PREFIX,
    MAX_QUALITY,
    MIN_QUALITY,
    SULFURAS,
    SULFURAS_QUALITY,
    GildedRose,
    Item,
)

__all__ = [
    "AGED_BRIE",
    "BACKSTAGE_PASS",
    "CONJURED_PREFIX",
    "MAX_QUALITY",
    "MIN_QUALITY",
    "SULFURAS",
    "SULFURAS_QUALITY",
    "GildedRose",
    "Item",
]
