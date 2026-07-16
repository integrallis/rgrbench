"""Clam Card kata: zone-priced subway journeys with day, week and month fare caps
and injected journey dates.

Kata catalogued at tddbuddy.com/katas/clam-card; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from clam_card.clam_card import (
    ZONE_A_STATIONS,
    ZONE_B_STATIONS,
    ClamCard,
    UnknownStationError,
)

__all__ = ["ZONE_A_STATIONS", "ZONE_B_STATIONS", "ClamCard", "UnknownStationError"]
