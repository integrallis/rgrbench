"""Robot Factory kata: cheapest-part sourcing across suppliers, seeded serial names.

Kata catalogued at tddbuddy.com/katas/robot-factory; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from robot_factory.robot_factory import (
    PART_OPTIONS,
    PartOrder,
    PartUnavailableError,
    Quote,
    Robot,
    RobotFactory,
    Supplier,
)

__all__ = [
    "PART_OPTIONS",
    "PartOrder",
    "PartUnavailableError",
    "Quote",
    "Robot",
    "RobotFactory",
    "Supplier",
]
