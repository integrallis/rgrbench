"""Parking Lot kata: typed spots, vehicle fit rules, and hourly fees on exit.

Kata catalogued at tddbuddy.com/katas/parking-lot; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from parking_lot.parking_lot import (
    ALLOWED_SPOTS,
    InvalidLotConfigurationError,
    NoAvailableSpotError,
    ParkingLot,
    ParkingLotError,
    Receipt,
    SpotType,
    Ticket,
    UnknownVehicleError,
    VehicleAlreadyParkedError,
    VehicleType,
)

__all__ = [
    "ALLOWED_SPOTS",
    "InvalidLotConfigurationError",
    "NoAvailableSpotError",
    "ParkingLot",
    "ParkingLotError",
    "Receipt",
    "SpotType",
    "Ticket",
    "UnknownVehicleError",
    "VehicleAlreadyParkedError",
    "VehicleType",
]
