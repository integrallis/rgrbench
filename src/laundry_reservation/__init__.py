"""Laundry Reservation kata (Wunda Wash).

Patrons book washing machines that are secured by PIN-locked IoT devices.
Creating a reservation takes the slot date/time, a cell phone number and an
email address as inputs (the slot time is always injected, never read from a
clock): the service randomly picks one of the 25 machines that is free,
generates a five-digit PIN and a reservation id, stores the reservation,
emails a confirmation containing machine number, reservation id and PIN, and
sends a lock instruction to the machine through the Machine API. A patron
may only hold one active reservation at a time. Claiming a reservation takes
a machine number and PIN: on a match the reservation is marked used and the
machine unlocks; after five failed PIN attempts a fresh PIN is generated,
texted to the patron's phone, and pushed to the machine lock. Randomness
comes from an injected generator, and devices and notifications sit behind
narrow interfaces so tests can use recording fakes.

Kata catalogued at tddbuddy.com/katas/laundry-reservation; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from laundry_reservation.laundry_reservation import (
    MACHINE_COUNT,
    MAX_FAILED_ATTEMPTS,
    PIN_LENGTH,
    LaundryService,
    MachineApi,
    MachineDevice,
    Notifier,
    Reservation,
    ReservationError,
)

__all__ = [
    "MACHINE_COUNT",
    "MAX_FAILED_ATTEMPTS",
    "PIN_LENGTH",
    "LaundryService",
    "MachineApi",
    "MachineDevice",
    "Notifier",
    "Reservation",
    "ReservationError",
]
