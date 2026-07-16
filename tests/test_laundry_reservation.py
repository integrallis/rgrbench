"""
Tests for the Laundry Reservation kata.
Reservation creation with injected slot times and randomness, confirmation
messages, machine locking, and PIN-based claims with the five-attempt reset.
"""

from datetime import datetime

import pytest

SLOT = datetime(2026, 3, 14, 10, 30)


class FakeDevice:
    """Recording fake for the IoT lock SDK."""

    def __init__(self) -> None:
        self.lock_calls: list[tuple[str, datetime, str]] = []
        self.unlock_calls: list[str] = []

    def lock(
        self, reservation_id: str, reservation_time: datetime, pin: str
    ) -> bool:
        self.lock_calls.append((reservation_id, reservation_time, pin))
        return True

    def unlock(self, reservation_id: str) -> None:
        self.unlock_calls.append(reservation_id)


class FakeNotifier:
    """Recording fake for outbound email and SMS."""

    def __init__(self) -> None:
        self.emails: list[tuple[str, str]] = []
        self.smses: list[tuple[str, str]] = []

    def send_email(self, address: str, message: str) -> None:
        self.emails.append((address, message))

    def send_sms(self, phone: str, message: str) -> None:
        self.smses.append((phone, message))


def _make_service(seed: int = 7, machine_count: int = 25) -> tuple:
    """Wire a LaundryService to recording fakes and a seeded generator."""
    from random import Random

    from laundry_reservation import LaundryService, MachineApi

    devices = {number: FakeDevice() for number in range(1, machine_count + 1)}
    api = MachineApi(devices)
    notifier = FakeNotifier()
    service = LaundryService(
        api, notifier, Random(seed), machine_count=machine_count
    )
    return service, devices, notifier


def test_reservation_assigns_a_machine_between_one_and_twenty_five() -> None:
    """Test 1: The reserved machine number is one of the 25 machines"""
    service, _, _ = _make_service()

    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")

    assert 1 <= reservation.machine_number <= 25


def test_reservation_generates_a_five_digit_pin() -> None:
    """Test 2: The PIN is a string of exactly five digits"""
    service, _, _ = _make_service()

    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")

    assert len(reservation.pin) == 5
    assert reservation.pin.isdigit()


def test_reservation_has_an_id_and_is_active() -> None:
    """Test 3: A new reservation carries a non-empty id and starts active"""
    service, _, _ = _make_service()

    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")

    assert reservation.reservation_id != ""
    assert reservation.is_active is True
    assert service.get_reservation(reservation.reservation_id) is reservation


def test_reservation_stores_the_injected_slot_time() -> None:
    """Test 4: The reservation keeps the date and time passed by the caller"""
    service, _, _ = _make_service()
    slot = datetime(2026, 12, 24, 18, 0)

    reservation = service.create_reservation(slot, "555-0100", "ada@example.com")

    assert reservation.reservation_time == slot


def test_confirmation_email_contains_machine_id_and_pin() -> None:
    """Test 5: The confirmation email carries machine number, reservation id and PIN"""
    service, _, notifier = _make_service()

    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")

    assert len(notifier.emails) == 1
    address, message = notifier.emails[0]
    assert address == "ada@example.com"
    assert str(reservation.machine_number) in message
    assert reservation.reservation_id in message
    assert reservation.pin in message


def test_lock_instruction_is_sent_to_the_reserved_machine() -> None:
    """Test 6: Creating a reservation locks the chosen device with id, time and PIN"""
    service, devices, _ = _make_service()

    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")

    device = devices[reservation.machine_number]
    assert device.lock_calls == [
        (reservation.reservation_id, SLOT, reservation.pin)
    ]


def test_only_the_reserved_machine_receives_a_lock() -> None:
    """Test 7: No other device is touched during creation"""
    service, devices, _ = _make_service()

    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")

    untouched = [
        number
        for number, device in devices.items()
        if number != reservation.machine_number and device.lock_calls
    ]
    assert untouched == []


def test_user_cannot_hold_two_active_reservations() -> None:
    """Test 8: A second reservation for the same user raises ReservationError"""
    from laundry_reservation import ReservationError

    service, _, _ = _make_service()
    service.create_reservation(SLOT, "555-0100", "ada@example.com")

    with pytest.raises(ReservationError):
        service.create_reservation(SLOT, "555-0100", "ada@example.com")


def test_different_users_get_different_machines() -> None:
    """Test 9: Active reservations never share a machine"""
    service, _, _ = _make_service()

    numbers = {
        service.create_reservation(
            SLOT, f"555-010{i}", f"user{i}@example.com"
        ).machine_number
        for i in range(5)
    }

    assert len(numbers) == 5


def test_no_machines_available_raises_reservation_error() -> None:
    """Test 10: With a single machine already reserved, the next user is refused"""
    from laundry_reservation import ReservationError

    service, _, _ = _make_service(machine_count=1)
    service.create_reservation(SLOT, "555-0100", "ada@example.com")

    with pytest.raises(ReservationError):
        service.create_reservation(SLOT, "555-0101", "bob@example.com")


def test_claim_with_correct_pin_succeeds_and_marks_reservation_used() -> None:
    """Test 11: A matching PIN claims the reservation"""
    service, _, _ = _make_service()
    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")

    assert service.claim_reservation(
        reservation.machine_number, reservation.pin
    ) is True
    assert reservation.used is True
    assert reservation.is_active is False


def test_claim_with_correct_pin_unlocks_the_machine() -> None:
    """Test 12: A successful claim sends the unlock to the device"""
    service, devices, _ = _make_service()
    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")

    service.claim_reservation(reservation.machine_number, reservation.pin)

    device = devices[reservation.machine_number]
    assert device.unlock_calls == [reservation.reservation_id]


def test_claim_with_wrong_pin_fails_and_keeps_reservation_active() -> None:
    """Test 13: A wrong PIN returns False and unlocks nothing"""
    service, devices, _ = _make_service()
    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")
    wrong_pin = "99999" if reservation.pin != "99999" else "00000"

    assert service.claim_reservation(reservation.machine_number, wrong_pin) is False
    assert reservation.is_active is True
    assert devices[reservation.machine_number].unlock_calls == []


def test_pin_is_unchanged_before_the_fifth_failed_attempt() -> None:
    """Test 14: Four wrong attempts trigger no SMS and no PIN change"""
    service, _, notifier = _make_service()
    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")
    original_pin = reservation.pin
    wrong_pin = "99999" if original_pin != "99999" else "00000"

    for _ in range(4):
        service.claim_reservation(reservation.machine_number, wrong_pin)

    assert reservation.pin == original_pin
    assert notifier.smses == []


def test_fifth_failed_attempt_texts_a_new_pin_to_the_patron() -> None:
    """Test 15: After five failures an SMS with the new PIN goes to the cell phone"""
    service, _, notifier = _make_service()
    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")
    original_pin = reservation.pin
    wrong_pin = "99999" if original_pin != "99999" else "00000"

    for _ in range(5):
        service.claim_reservation(reservation.machine_number, wrong_pin)

    assert reservation.pin != original_pin
    assert len(notifier.smses) == 1
    phone, message = notifier.smses[0]
    assert phone == "555-0100"
    assert reservation.pin in message


def test_fifth_failed_attempt_syncs_the_new_pin_to_the_machine_lock() -> None:
    """Test 16: The PIN reset re-locks the device with the fresh PIN"""
    service, devices, _ = _make_service()
    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")
    wrong_pin = "99999" if reservation.pin != "99999" else "00000"

    for _ in range(5):
        service.claim_reservation(reservation.machine_number, wrong_pin)

    device = devices[reservation.machine_number]
    assert len(device.lock_calls) == 2
    assert device.lock_calls[-1] == (
        reservation.reservation_id,
        SLOT,
        reservation.pin,
    )


def test_new_pin_claims_the_reservation_after_a_reset() -> None:
    """Test 17: The regenerated PIN is accepted"""
    service, _, _ = _make_service()
    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")
    wrong_pin = "99999" if reservation.pin != "99999" else "00000"

    for _ in range(5):
        service.claim_reservation(reservation.machine_number, wrong_pin)

    assert service.claim_reservation(
        reservation.machine_number, reservation.pin
    ) is True


def test_failed_attempt_counter_restarts_after_a_pin_reset() -> None:
    """Test 18: It takes five fresh failures to trigger the next SMS"""
    service, _, notifier = _make_service()
    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")

    for _ in range(5):
        service.claim_reservation(reservation.machine_number, "wrong")
    assert len(notifier.smses) == 1

    for _ in range(4):
        service.claim_reservation(reservation.machine_number, "wrong")
    assert len(notifier.smses) == 1

    service.claim_reservation(reservation.machine_number, "wrong")
    assert len(notifier.smses) == 2


def test_claim_on_a_machine_without_a_reservation_fails() -> None:
    """Test 19: Claiming an unreserved machine returns False"""
    service, _, _ = _make_service()

    assert service.claim_reservation(3, "12345") is False


def test_used_reservation_cannot_be_claimed_again() -> None:
    """Test 20: A claimed reservation no longer accepts its PIN"""
    service, _, _ = _make_service()
    reservation = service.create_reservation(SLOT, "555-0100", "ada@example.com")
    service.claim_reservation(reservation.machine_number, reservation.pin)

    assert service.claim_reservation(
        reservation.machine_number, reservation.pin
    ) is False


def test_user_may_reserve_again_after_claiming() -> None:
    """Test 21: Only active reservations count toward the one-per-user limit"""
    service, _, _ = _make_service()
    first = service.create_reservation(SLOT, "555-0100", "ada@example.com")
    service.claim_reservation(first.machine_number, first.pin)

    second = service.create_reservation(SLOT, "555-0100", "ada@example.com")

    assert second.is_active is True
    assert second.reservation_id != first.reservation_id


def test_same_seed_produces_the_same_machine_pin_and_id() -> None:
    """Test 22: Machine choice, PIN and id come from the injected generator"""
    service_a, _, _ = _make_service(seed=42)
    service_b, _, _ = _make_service(seed=42)

    first = service_a.create_reservation(SLOT, "555-0100", "ada@example.com")
    second = service_b.create_reservation(SLOT, "555-0100", "ada@example.com")

    assert first.machine_number == second.machine_number
    assert first.pin == second.pin
    assert first.reservation_id == second.reservation_id


def test_reservation_ids_are_eight_hex_digits_and_unique() -> None:
    """Test 23: Ids follow RSV- plus eight hex digits and never collide"""
    import re

    service, _, _ = _make_service()

    reservations = [
        service.create_reservation(SLOT, f"555-02{i:02d}", f"user{i}@example.com")
        for i in range(25)
    ]

    ids = [r.reservation_id for r in reservations]
    assert len(set(ids)) == 25
    for reservation_id in ids:
        assert re.fullmatch(r"RSV-[0-9A-F]{8}", reservation_id)


def test_pins_are_five_digits_drawn_from_the_full_range() -> None:
    """Test 24: Every PIN has five digits and PINs are not confined near zero"""
    service, _, _ = _make_service()

    pins = [
        service.create_reservation(SLOT, f"555-03{i:02d}", f"pin{i}@example.com").pin
        for i in range(25)
    ]

    assert all(len(pin) == 5 and pin.isdigit() for pin in pins)
    assert any(pin >= "00100" for pin in pins)


def test_double_booking_error_names_the_single_reservation_rule() -> None:
    """Test 25: The double-booking error explains the one-active-reservation rule"""
    from laundry_reservation import ReservationError

    service, _, _ = _make_service()
    service.create_reservation(SLOT, "555-0100", "ada@example.com")

    with pytest.raises(ReservationError) as excinfo:
        service.create_reservation(SLOT, "555-0100", "ada@example.com")

    assert str(excinfo.value) == (
        "a user may only have a single active reservation at a time"
    )


def test_full_house_error_says_no_machines_available() -> None:
    """Test 26: The all-machines-taken error reports that none are available"""
    from laundry_reservation import ReservationError

    service, _, _ = _make_service(machine_count=1)
    service.create_reservation(SLOT, "555-0100", "ada@example.com")

    with pytest.raises(ReservationError) as excinfo:
        service.create_reservation(SLOT, "555-0101", "bob@example.com")

    assert str(excinfo.value) == "no machines available"
