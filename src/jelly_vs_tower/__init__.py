"""Jelly vs Tower kata.

A tower-defense combat model inspired by JellyDefense. Jellies and towers
both have a unique identifier and a color — Blue, Red, or BlueRed — and
jellies carry a health pool: a jelly is dead once health reaches zero or
below. Towers additionally have a level from 1 to 4. Damage is drawn from a
table keyed by tower color, tower level, and target color: same-color
attacks roll within ranges that grow with level (2-5, 5-9, 9-12, 12-15),
off-color attacks deal a fixed 0/1/2/3, and BlueRed towers deal moderate
damage to everyone (2, 2-4, 4-6, 6-8). BlueRed jellies take damage from both
the Blue and Red columns, using the higher value. Randomness comes from an
injected generator. A battle resolves in rounds: each tower attacks the
first living jelly, a combat log records tower, target and damage, dead
jellies are removed, and towers stand idle once no jelly remains.

Kata catalogued at tddbuddy.com/katas/jelly-vs-tower; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from jelly_vs_tower.jelly_vs_tower import (
    MAX_LEVEL,
    MIN_LEVEL,
    AttackReport,
    Battle,
    Color,
    Jelly,
    Tower,
    damage_range,
)

__all__ = [
    "MAX_LEVEL",
    "MIN_LEVEL",
    "AttackReport",
    "Battle",
    "Color",
    "Jelly",
    "Tower",
    "damage_range",
]
