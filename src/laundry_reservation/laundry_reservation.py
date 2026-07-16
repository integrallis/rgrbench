"""Wunda Wash laundry reservations: PIN-locked machines, claims, and resets."""

from dataclasses import dataclass
from datetime import datetime
from random import Random
from typing import Protocol

MACHINE_COUNT = 25
PIN_LENGTH = 5
MAX_FAILED_ATTEMPTS = 5


class MachineDevice(Protocol):
    """SDK interface of a single IoT lock device."""

    def lock(
        self, reservation_id: str, reservation_time: datetime, pin: str
    ) -> bool:
        """Lock the device for the reservation; True on success."""
        ...

    def unlock(self, reservation_id: str) -> None:
        """Unlock the device for the reservation."""
        ...


class Notifier(Protocol):
    """Outbound messaging used for confirmations and PIN resets."""

    def send_email(self, address: str, message: str) -> None:
        """Send an email message."""
        ...

    def send_sms(self, phone: str, message: str) -> None:
        """Send an SMS message."""
        ...


class ReservationError(Exception):
    """Raised when a reservation cannot be created."""


@dataclass
class Reservation:
    """An active or used booking of one machine for one time slot."""

    reservation_id: str
    machine_number: int
    reservation_time: datetime
    phone: str
    email: str
    pin: str
    used: bool = False
    failed_attempts: int = 0

    @property
    def is_active(self) -> bool:
        """A reservation stays active until it is claimed."""
        return not self.used


class MachineApi:
    """Routes lock/unlock instructions to IoT devices by machine number."""

    def __init__(self, devices: dict[int, MachineDevice]) -> None:
        self._devices = dict(devices)

    def lock_machine(
        self,
        machine_number: int,
        reservation_time: datetime,
        reservation_id: str,
        pin: str,
    ) -> bool:
        """Lock the given machine for a reservation; True on success."""
        return self._devices[machine_number].lock(
            reservation_id, reservation_time, pin
        )

    def unlock_machine(self, machine_number: int, reservation_id: str) -> None:
        """Unlock the given machine for a reservation."""
        self._devices[machine_number].unlock(reservation_id)


class LaundryService:
    """Creates reservations and handles PIN-based machine claims."""

    def __init__(
        self,
        machine_api: MachineApi,
        notifier: Notifier,
        rng: Random,
        machine_count: int = MACHINE_COUNT,
    ) -> None:
        self._machine_api = machine_api
        self._notifier = notifier
        self._rng = rng
        self._machine_count = machine_count
        self._reservations: dict[str, Reservation] = {}

    def create_reservation(
        self, reservation_time: datetime, phone: str, email: str
    ) -> Reservation:
        """Reserve a random available machine for the given time slot.

        Generates a five-digit PIN and a reservation id, stores the
        reservation, emails a confirmation carrying the machine number,
        reservation id and PIN, and sends the lock instruction to the
        machine. A patron may only hold one active reservation at a time.
        """
        if any(
            r.is_active and r.email == email
            for r in self._reservations.values()
        ):
            raise ReservationError(
                "a user may only have a single active reservation at a time"
            )
        machine_number = self._pick_available_machine()
        pin = self._generate_pin()
        reservation_id = f"RSV-{self._rng.randrange(16**8):08X}"
        reservation = Reservation(
            reservation_id=reservation_id,
            machine_number=machine_number,
            reservation_time=reservation_time,
            phone=phone,
            email=email,
            pin=pin,
        )
        self._reservations[reservation_id] = reservation
        self._machine_api.lock_machine(
            machine_number, reservation_time, reservation_id, pin
        )
        self._notifier.send_email(
            email,
            f"Reservation confirmed. Machine: {machine_number}. "
            f"Reservation ID: {reservation_id}. PIN: {pin}.",
        )
        return reservation

    def claim_reservation(self, machine_number: int, pin: str) -> bool:
        """Claim the active reservation on a machine by entering its PIN.

        A matching PIN marks the reservation used and unlocks the machine.
        After five failed attempts a fresh PIN is generated, texted to the
        patron, and pushed to the machine lock.
        """
        reservation = self._active_reservation_for(machine_number)
        if reservation is None:
            return False
        if pin == reservation.pin:
            reservation.used = True
            self._machine_api.unlock_machine(
                machine_number, reservation.reservation_id
            )
            return True
        reservation.failed_attempts += 1
        if reservation.failed_attempts >= MAX_FAILED_ATTEMPTS:
            self._reset_pin(reservation)
        return False

    def get_reservation(self, reservation_id: str) -> Reservation | None:
        """Look up a reservation by its id."""
        return self._reservations.get(reservation_id)

    def _active_reservation_for(self, machine_number: int) -> Reservation | None:
        return next(
            (
                r
                for r in self._reservations.values()
                if r.is_active and r.machine_number == machine_number
            ),
            None,
        )

    def _pick_available_machine(self) -> int:
        reserved = {
            r.machine_number
            for r in self._reservations.values()
            if r.is_active
        }
        available = [
            number
            for number in range(1, self._machine_count + 1)
            if number not in reserved
        ]
        if not available:
            raise ReservationError("no machines available")
        return self._rng.choice(available)

    def _generate_pin(self) -> str:
        return f"{self._rng.randrange(10**PIN_LENGTH):0{PIN_LENGTH}d}"

    def _reset_pin(self, reservation: Reservation) -> None:
        reservation.pin = self._generate_pin()
        reservation.failed_attempts = 0
        self._machine_api.lock_machine(
            reservation.machine_number,
            reservation.reservation_time,
            reservation.reservation_id,
            reservation.pin,
        )
        self._notifier.send_sms(
            reservation.phone,
            f"Too many failed attempts. Your new PIN for reservation "
            f"{reservation.reservation_id} is {reservation.pin}.",
        )
