"""Parking lot manager with typed spots, fit rules, and time-based fees.

The lot is configured with a count of spots per spot type (motorcycle,
compact, large) and a positive hourly rate per vehicle type (motorcycle,
car, bus); negative spot counts, an empty lot, or missing/non-positive
rates are invalid configurations. Motorcycles fit in any spot, cars fit in
compact or large spots, and buses need large spots; a vehicle is always
assigned the smallest suitable spot type with space left. Parking a vehicle
that is already inside, or one that no spot can take, fails with a domain
error, as does removing a vehicle that is not parked. Entry and exit times
are injected as timestamps in seconds, keeping fee calculation
deterministic: the charge is the vehicle type's hourly rate times the
occupied duration rounded up to whole hours, with a minimum charge of one
hour. Status reporting exposes capacity, occupancy, and availability per
spot type.

Kata catalogued at tddbuddy.com/katas/parking-lot; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

import math
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


class VehicleType(Enum):
    """Kinds of vehicle the lot accepts."""

    MOTORCYCLE = "motorcycle"
    CAR = "car"
    BUS = "bus"


class SpotType(Enum):
    """Kinds of spot the lot offers."""

    MOTORCYCLE = "motorcycle"
    COMPACT = "compact"
    LARGE = "large"


#: Spot types each vehicle fits in, smallest (preferred) first.
ALLOWED_SPOTS: dict[VehicleType, tuple[SpotType, ...]] = {
    VehicleType.MOTORCYCLE: (SpotType.MOTORCYCLE, SpotType.COMPACT, SpotType.LARGE),
    VehicleType.CAR: (SpotType.COMPACT, SpotType.LARGE),
    VehicleType.BUS: (SpotType.LARGE,),
}


class ParkingLotError(Exception):
    """Base class for parking lot domain errors."""


class InvalidLotConfigurationError(ParkingLotError):
    """The lot was configured with invalid spot counts or rates."""


class VehicleAlreadyParkedError(ParkingLotError):
    """The vehicle is already occupying a spot."""


class NoAvailableSpotError(ParkingLotError):
    """No suitable spot is free for the vehicle."""


class UnknownVehicleError(ParkingLotError):
    """The vehicle is not currently parked in the lot."""


@dataclass(frozen=True)
class Ticket:
    """Issued when a vehicle parks; records where and when it entered."""

    vehicle_id: str
    vehicle_type: VehicleType
    spot_type: SpotType
    entry_time: float


@dataclass(frozen=True)
class Receipt:
    """Issued when a vehicle exits; records the stay and the fee charged."""

    vehicle_id: str
    vehicle_type: VehicleType
    spot_type: SpotType
    entry_time: float
    exit_time: float
    hours: int
    fee: float


class ParkingLot:
    """Assigns vehicles to suitable spots and charges hourly fees on exit."""

    def __init__(
        self,
        spots: Mapping[SpotType, int],
        hourly_rates: Mapping[VehicleType, float],
    ) -> None:
        for spot_type in SpotType:
            count = spots.get(spot_type, 0)
            if count < 0:
                raise InvalidLotConfigurationError(
                    f"spot count for [{spot_type.value}] must be non-negative, "
                    f"got [{count}]"
                )
        self._capacity = {spot_type: spots.get(spot_type, 0) for spot_type in SpotType}
        if sum(self._capacity.values()) == 0:
            raise InvalidLotConfigurationError(
                "parking lot must have at least one spot"
            )
        for vehicle_type in VehicleType:
            rate = hourly_rates.get(vehicle_type)
            if rate is None:
                raise InvalidLotConfigurationError(
                    f"missing hourly rate for [{vehicle_type.value}]"
                )
            if rate <= 0:
                raise InvalidLotConfigurationError(
                    f"hourly rate for [{vehicle_type.value}] must be positive, "
                    f"got [{rate}]"
                )
        self._rates = {
            vehicle_type: float(hourly_rates[vehicle_type])
            for vehicle_type in VehicleType
        }
        self._occupied = {spot_type: 0 for spot_type in SpotType}
        self._tickets: dict[str, Ticket] = {}

    def park(
        self, vehicle_id: str, vehicle_type: VehicleType, entry_time: float
    ) -> Ticket:
        """Assign the vehicle the smallest suitable free spot and issue a ticket."""
        if vehicle_id in self._tickets:
            raise VehicleAlreadyParkedError(f"vehicle [{vehicle_id}] is already parked")
        for spot_type in ALLOWED_SPOTS[vehicle_type]:
            if self._occupied[spot_type] < self._capacity[spot_type]:
                self._occupied[spot_type] += 1
                ticket = Ticket(vehicle_id, vehicle_type, spot_type, entry_time)
                self._tickets[vehicle_id] = ticket
                return ticket
        raise NoAvailableSpotError(f"no available spot for [{vehicle_type.value}]")

    def unpark(self, vehicle_id: str, exit_time: float) -> Receipt:
        """Free the vehicle's spot and charge for the stay, ceiled to whole hours."""
        ticket = self._tickets.get(vehicle_id)
        if ticket is None:
            raise UnknownVehicleError(f"vehicle [{vehicle_id}] is not parked")
        if exit_time < ticket.entry_time:
            raise ValueError(
                f"exit_time [{exit_time}] is before entry_time [{ticket.entry_time}]"
            )
        hours = max(1, math.ceil((exit_time - ticket.entry_time) / 3600))
        fee = hours * self._rates[ticket.vehicle_type]
        del self._tickets[vehicle_id]
        self._occupied[ticket.spot_type] -= 1
        return Receipt(
            vehicle_id=vehicle_id,
            vehicle_type=ticket.vehicle_type,
            spot_type=ticket.spot_type,
            entry_time=ticket.entry_time,
            exit_time=exit_time,
            hours=hours,
            fee=fee,
        )

    def is_parked(self, vehicle_id: str) -> bool:
        """Return whether the vehicle currently occupies a spot."""
        return vehicle_id in self._tickets

    def available_spots(self, spot_type: SpotType) -> int:
        """Number of free spots of the given type."""
        return self._capacity[spot_type] - self._occupied[spot_type]

    def is_full(self) -> bool:
        """Return whether every spot in the lot is occupied."""
        return all(
            self._occupied[spot_type] >= self._capacity[spot_type]
            for spot_type in SpotType
        )

    def status(self) -> dict[SpotType, dict[str, int]]:
        """Capacity, occupancy, and availability per spot type."""
        return {
            spot_type: {
                "capacity": self._capacity[spot_type],
                "occupied": self._occupied[spot_type],
                "available": self._capacity[spot_type] - self._occupied[spot_type],
            }
            for spot_type in SpotType
        }
