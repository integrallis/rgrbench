"""Zombie Survivor kata - survivors, wounds, equipment, experience, skills.

A survivor has a name, starts unwounded with 3 actions per turn, and
dies on the second wound; wounds dealt to the dead are ignored. A
survivor carries up to 5 pieces of equipment: the first two picked up
are "in hand", the rest "in reserve". Each wound lowers capacity by
one; when capacity drops below what is carried, the most recently
acquired reserve pieces are discarded first, then in-hand pieces.
Killing a zombie earns 1 experience point. Levels by experience: Blue
from 0, Yellow from 7, Orange from 19, Red from 43. Reaching a level
opens that level's skill slot: the Yellow slot always grants "+1
Action"; the Orange slot offers a choice of "Hoard" or "Sniper"; the
Red slot offers "Hoard", "Sniper", or "Tough". "+1 Action" adds an
action per copy held and "Hoard" raises equipment capacity by one; a
choice never offers a skill already unlocked. Past 43 experience the
skill tree restarts, repeating the slot thresholds offset by 43 per
completed cycle, for at most three complete cycles. Survivors announce
their notable events to registered listeners as (kind, message) pairs,
with kinds "acquired", "wounded", "died", and "level-up".

Kata catalogued at tddbuddy.com/katas/zombie-survivor; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

_BASE_ACTIONS = 3
_BASE_CAPACITY = 5
_IN_HAND_LIMIT = 2
_DEADLY_WOUNDS = 2
_MAX_CYCLES = 3

PLUS_ONE_ACTION = "+1 Action"
HOARD = "Hoard"
SNIPER = "Sniper"
TOUGH = "Tough"

_ORANGE_OPTIONS = (HOARD, SNIPER)
_RED_OPTIONS = (HOARD, SNIPER, TOUGH)


class Level(Enum):
    """Survivor level, valued by the experience needed to reach it."""

    BLUE = 0
    YELLOW = 7
    ORANGE = 19
    RED = 43

    @classmethod
    def for_experience(cls, experience: int) -> "Level":
        """The level a survivor with this much experience holds."""
        held = cls.BLUE
        for level in cls:
            if experience >= level.value:
                held = level
        return held


@dataclass
class _SkillSlot:
    threshold: int
    options: tuple[str, ...]
    automatic: bool
    state: str = field(default="locked")


def _skill_slots() -> list[_SkillSlot]:
    slots: list[_SkillSlot] = []
    for cycle in range(_MAX_CYCLES):
        base = cycle * Level.RED.value
        slots.append(_SkillSlot(base + Level.YELLOW.value, (PLUS_ONE_ACTION,), True))
        slots.append(_SkillSlot(base + Level.ORANGE.value, _ORANGE_OPTIONS, False))
        slots.append(_SkillSlot(base + Level.RED.value, _RED_OPTIONS, False))
    return slots


class Survivor:
    """A named survivor tracking wounds, gear, experience, and skills."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._wounds = 0
        self._in_hand: list[str] = []
        self._in_reserve: list[str] = []
        self._experience = 0
        self._skills: list[str] = []
        self._slots = _skill_slots()
        self._listeners: list[Callable[[str, str], None]] = []

    @property
    def name(self) -> str:
        """The survivor's unique name."""
        return self._name

    @property
    def wounds(self) -> int:
        """Wounds received, capped at the deadly count."""
        return self._wounds

    @property
    def is_alive(self) -> bool:
        """Whether the survivor is still alive."""
        return self._wounds < _DEADLY_WOUNDS

    @property
    def actions(self) -> int:
        """Actions per turn: three plus one per '+1 Action' skill."""
        return _BASE_ACTIONS + self._skills.count(PLUS_ONE_ACTION)

    @property
    def in_hand(self) -> tuple[str, ...]:
        """Equipment currently held in hand."""
        return tuple(self._in_hand)

    @property
    def in_reserve(self) -> tuple[str, ...]:
        """Equipment currently held in reserve."""
        return tuple(self._in_reserve)

    @property
    def capacity(self) -> int:
        """Pieces of equipment the survivor can carry right now."""
        return _BASE_CAPACITY + self._skills.count(HOARD) - self._wounds

    @property
    def experience(self) -> int:
        """Experience points earned from zombie kills."""
        return self._experience

    @property
    def level(self) -> Level:
        """Level implied by the survivor's experience."""
        return Level.for_experience(self._experience)

    @property
    def skills(self) -> tuple[str, ...]:
        """Skills unlocked so far, in unlock order."""
        return tuple(self._skills)

    @property
    def skill_options(self) -> tuple[str, ...]:
        """Choices open for the oldest pending skill slot, if any."""
        slot = self._pending_slot()
        if slot is None:
            return ()
        return tuple(option for option in slot.options if option not in self._skills)

    def add_listener(self, listener: Callable[[str, str], None]) -> None:
        """Register a callable to receive (kind, message) event pairs."""
        self._listeners.append(listener)

    def pick_up(self, item: str) -> None:
        """Acquire equipment: first into hand, then into reserve."""
        self._require_alive()
        if len(self._in_hand) + len(self._in_reserve) >= self.capacity:
            raise ValueError(f"{self._name} cannot carry any more equipment")
        if len(self._in_hand) < _IN_HAND_LIMIT:
            self._in_hand.append(item)
        else:
            self._in_reserve.append(item)
        self._notify("acquired", f"{self._name} acquired {item}")

    def wound(self) -> None:
        """Receive a wound; wounds to the dead are ignored."""
        if not self.is_alive:
            return
        self._wounds += 1
        self._notify("wounded", f"{self._name} was wounded")
        if not self.is_alive:
            self._notify("died", f"{self._name} died")
            return
        while len(self._in_hand) + len(self._in_reserve) > self.capacity:
            if self._in_reserve:
                self._in_reserve.pop()
            else:
                self._in_hand.pop()

    def kill_zombie(self) -> None:
        """Earn one experience point, levelling up and opening skill slots."""
        self._require_alive()
        previous_level = self.level
        self._experience += 1
        if self.level is not previous_level:
            self._notify(
                "level-up", f"{self._name} advanced to {self.level.name.title()}"
            )
        self._open_reached_slots()

    def choose_skill(self, skill: str) -> None:
        """Resolve the oldest pending skill slot with the chosen skill."""
        slot = self._pending_slot()
        if slot is None:
            raise ValueError(f"{self._name} has no skill choice available")
        if skill not in self.skill_options:
            raise ValueError(f"'{skill}' is not an available skill choice")
        self._skills.append(skill)
        slot.state = "done"

    def _open_reached_slots(self) -> None:
        for slot in self._slots:
            if slot.state != "locked" or self._experience < slot.threshold:
                continue
            if slot.automatic:
                self._skills.extend(slot.options)
                slot.state = "done"
            elif all(option in self._skills for option in slot.options):
                slot.state = "done"
            else:
                slot.state = "pending"

    def _pending_slot(self) -> _SkillSlot | None:
        for slot in self._slots:
            if slot.state == "pending":
                return slot
        return None

    def _require_alive(self) -> None:
        if not self.is_alive:
            raise ValueError(f"{self._name} is dead")

    def _notify(self, kind: str, message: str) -> None:
        for listener in self._listeners:
            listener(kind, message)
