"""Jelly vs Tower combat: colors, damage table, and round resolution."""

from dataclasses import dataclass
from enum import Enum
from random import Random

MIN_LEVEL = 1
MAX_LEVEL = 4


class Color(Enum):
    """Color type shared by jellies and towers."""

    BLUE = "blue"
    RED = "red"
    BLUE_RED = "blue_red"


# Damage ranges (inclusive) by tower color and level against a Blue jelly.
_VS_BLUE: dict[Color, dict[int, tuple[int, int]]] = {
    Color.BLUE: {1: (2, 5), 2: (5, 9), 3: (9, 12), 4: (12, 15)},
    Color.RED: {1: (0, 0), 2: (1, 1), 3: (2, 2), 4: (3, 3)},
    Color.BLUE_RED: {1: (2, 2), 2: (2, 4), 3: (4, 6), 4: (6, 8)},
}

# Damage ranges (inclusive) by tower color and level against a Red jelly.
_VS_RED: dict[Color, dict[int, tuple[int, int]]] = {
    Color.BLUE: {1: (0, 0), 2: (1, 1), 3: (2, 2), 4: (3, 3)},
    Color.RED: {1: (2, 5), 2: (5, 9), 3: (9, 12), 4: (12, 15)},
    Color.BLUE_RED: {1: (2, 2), 2: (2, 4), 3: (4, 6), 4: (6, 8)},
}


def _validate_level(level: int) -> None:
    if not MIN_LEVEL <= level <= MAX_LEVEL:
        raise ValueError(
            f"tower level must be between {MIN_LEVEL} and {MAX_LEVEL}, got {level}"
        )


def damage_range(
    tower_color: Color, level: int, jelly_color: Color
) -> tuple[int, int]:
    """Inclusive (min, max) damage for a tower color/level against a jelly color.

    BlueRed jellies take damage from both the Blue and the Red columns of the
    table, using the higher value.
    """
    _validate_level(level)
    vs_blue = _VS_BLUE[tower_color][level]
    vs_red = _VS_RED[tower_color][level]
    if jelly_color is Color.BLUE:
        return vs_blue
    if jelly_color is Color.RED:
        return vs_red
    return (max(vs_blue[0], vs_red[0]), max(vs_blue[1], vs_red[1]))


@dataclass
class Jelly:
    """An attacker with an identifier, a color, and a health pool."""

    id: str
    color: Color
    health: int

    @property
    def is_alive(self) -> bool:
        """A jelly is dead once its health drops to zero or below."""
        return self.health > 0

    def take_damage(self, amount: int) -> None:
        """Reduce health by the given amount."""
        self.health -= amount


@dataclass
class Tower:
    """A defensive tower with a color and a level between 1 and 4."""

    id: str
    color: Color
    level: int

    def __post_init__(self) -> None:
        _validate_level(self.level)

    def attack(self, jelly: Jelly, rng: Random) -> int:
        """Roll damage against a living jelly and apply it; return the amount."""
        if not jelly.is_alive:
            raise ValueError("cannot attack a dead jelly")
        low, high = damage_range(self.color, self.level, jelly.color)
        damage = rng.randint(low, high)
        jelly.take_damage(damage)
        return damage


@dataclass(frozen=True)
class AttackReport:
    """One combat-log entry: which tower hit which jelly for how much."""

    tower_id: str
    jelly_id: str
    damage: int


class Battle:
    """Resolves combat rounds between a group of towers and a wave of jellies."""

    def __init__(
        self, towers: list[Tower], jellies: list[Jelly], rng: Random
    ) -> None:
        self._towers = list(towers)
        self._jellies = list(jellies)
        self._rng = rng

    @property
    def jellies(self) -> list[Jelly]:
        """The jellies still in the battle (dead ones are removed each round)."""
        return list(self._jellies)

    def fight_round(self) -> list[AttackReport]:
        """Each tower attacks the first living jelly; dead jellies are removed.

        Returns the combat log for the round. Towers do nothing once no
        living jelly remains.
        """
        log: list[AttackReport] = []
        for tower in self._towers:
            target = next((j for j in self._jellies if j.is_alive), None)
            if target is None:
                break
            damage = tower.attack(target, self._rng)
            log.append(AttackReport(tower.id, target.id, damage))
        self._jellies = [j for j in self._jellies if j.is_alive]
        return log
