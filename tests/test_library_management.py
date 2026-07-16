"""
Tests for the Library Management kata (tddbuddy.com/katas/library-management).
All dates flow through an injected clock; notifications through an injected
notifier. Copy states: available, checked_out, reserved.
"""

import pytest


class _FakeClock:
    """Controllable clock: a callable returning the current test date."""

    def __init__(self, today) -> None:
        self.today = today

    def __call__(self):
        return self.today

    def advance(self, days: int) -> None:
        from datetime import timedelta

        self.today += timedelta(days=days)


class _FakeNotifier:
    """Records (member_id, isbn) availability notifications."""

    def __init__(self) -> None:
        self.notifications: list[tuple[str, str]] = []

    def notify(self, member_id: str, isbn: str) -> None:
        self.notifications.append((member_id, isbn))


def _make_library(**kwargs):
    from datetime import date

    from library_management import Library

    clock = _FakeClock(date(2026, 1, 5))
    notifier = _FakeNotifier()
    return Library(clock, notifier, **kwargs), clock, notifier


def _library_with_one_copy(**kwargs):
    library, clock, notifier = _make_library(**kwargs)
    library.add_book("978-1", "Refactoring")
    copy_id = library.add_copy("978-1")
    library.register_member("m1", "Alice")
    library.register_member("m2", "Bob")
    return library, clock, notifier, copy_id


def test_added_copy_is_available() -> None:
    """Test 1: A newly added copy counts as available"""
    library, _, _, copy_id = _library_with_one_copy()

    assert library.available_copies("978-1") == 1
    assert library.status(copy_id) == "available"


def test_multiple_copies_of_the_same_title_are_tracked() -> None:
    """Test 2: A title supports several copies, each individually tracked"""
    library, _, _, first_copy = _library_with_one_copy()

    second_copy = library.add_copy("978-1")

    assert first_copy != second_copy
    assert library.available_copies("978-1") == 2


def test_book_info_keeps_category_and_location() -> None:
    """Test 3: The catalogue stores title, category and location"""
    library, _, _ = _make_library()

    library.add_book("978-2", "TDD by Example", category="Software", location="A-3")
    info = library.book_info("978-2")

    assert info.isbn == "978-2"
    assert info.title == "TDD by Example"
    assert info.category == "Software"
    assert info.location == "A-3"


def test_checkout_sets_due_date_from_loan_period() -> None:
    """Test 4: Due date is the clock's today plus the configured loan period"""
    from datetime import date

    library, _, _, copy_id = _library_with_one_copy(loan_period_days=14)

    loan = library.checkout("m1", "978-1")

    assert loan.copy_id == copy_id
    assert loan.isbn == "978-1"
    assert loan.member_id == "m1"
    assert loan.due_date == date(2026, 1, 19)


def test_checkout_marks_the_copy_checked_out() -> None:
    """Test 5: A checked-out copy leaves the available pool"""
    library, _, _, copy_id = _library_with_one_copy()

    library.checkout("m1", "978-1")

    assert library.status(copy_id) == "checked_out"
    assert library.available_copies("978-1") == 0


def test_checkout_without_available_copies_is_refused() -> None:
    """Test 6: Checking out a title with no free copies raises NoAvailableCopyError"""
    from library_management import NoAvailableCopyError

    library, _, _, _ = _library_with_one_copy()
    library.checkout("m1", "978-1")

    with pytest.raises(NoAvailableCopyError, match="No copies of 978-1"):
        library.checkout("m2", "978-1")


def test_checkout_of_unregistered_book_is_refused() -> None:
    """Test 7: Checking out an unknown ISBN raises UnknownBookError"""
    from library_management import UnknownBookError

    library, _, _, _ = _library_with_one_copy()

    with pytest.raises(UnknownBookError, match="978-404"):
        library.checkout("m1", "978-404")


def test_checkout_by_unregistered_member_is_refused() -> None:
    """Test 8: Checking out to an unknown member raises UnknownMemberError"""
    from library_management import UnknownMemberError

    library, _, _, _ = _library_with_one_copy()

    with pytest.raises(UnknownMemberError, match="ghost"):
        library.checkout("ghost", "978-1")


def test_return_on_or_before_the_due_date_costs_nothing() -> None:
    """Test 9: Returning exactly on the due date incurs no fine"""
    from decimal import Decimal

    library, clock, _, copy_id = _library_with_one_copy(loan_period_days=14)
    library.checkout("m1", "978-1")

    clock.advance(14)
    fine = library.return_copy(copy_id)

    assert fine == Decimal("0")


@pytest.mark.parametrize(
    "fine_per_day,days_late,expected_fine",
    [("0.50", 1, "0.50"), ("0.50", 3, "1.50"), ("0.25", 4, "1.00")],
)
def test_late_return_incurs_a_per_day_fine(
    fine_per_day: str, days_late: int, expected_fine: str
) -> None:
    """Test 10: A late return owes the per-day fine times the days overdue"""
    from decimal import Decimal

    library, clock, _, copy_id = _library_with_one_copy(
        loan_period_days=14, fine_per_day=Decimal(fine_per_day)
    )
    library.checkout("m1", "978-1")

    clock.advance(14 + days_late)
    fine = library.return_copy(copy_id)

    assert fine == Decimal(expected_fine)


def test_returned_copy_is_available_again() -> None:
    """Test 11: After a return the copy can be checked out by another member"""
    library, _, _, copy_id = _library_with_one_copy()
    library.checkout("m1", "978-1")
    library.return_copy(copy_id)

    assert library.status(copy_id) == "available"
    loan = library.checkout("m2", "978-1")
    assert loan.copy_id == copy_id


def test_returning_a_copy_that_is_not_checked_out_is_refused() -> None:
    """Test 12: Returning an available copy raises LibraryError"""
    from library_management import LibraryError

    library, _, _, copy_id = _library_with_one_copy()

    with pytest.raises(LibraryError, match="not checked out"):
        library.return_copy(copy_id)


def test_available_copy_can_be_removed() -> None:
    """Test 13: Removing an available copy shrinks the inventory"""
    library, _, _, copy_id = _library_with_one_copy()

    library.remove_copy(copy_id)

    assert library.available_copies("978-1") == 0


def test_checked_out_copy_cannot_be_removed() -> None:
    """Test 14: Removing a checked-out copy raises LibraryError"""
    from library_management import LibraryError

    library, _, _, copy_id = _library_with_one_copy()
    library.checkout("m1", "978-1")

    with pytest.raises(LibraryError, match="not available for removal"):
        library.remove_copy(copy_id)


def test_return_hands_the_copy_to_the_first_reserver_and_notifies() -> None:
    """Test 15: When a reserved title comes back, the reserver is notified and the copy is held"""
    library, _, notifier, copy_id = _library_with_one_copy()
    library.checkout("m1", "978-1")
    library.reserve("m2", "978-1")

    library.return_copy(copy_id)

    assert notifier.notifications == [("m2", "978-1")]
    assert library.status(copy_id) == "reserved"


def test_held_copy_cannot_be_checked_out_by_another_member() -> None:
    """Test 16: A copy held under a reservation is unavailable to other members"""
    from library_management import NoAvailableCopyError

    library, _, _, copy_id = _library_with_one_copy()
    library.checkout("m1", "978-1")
    library.reserve("m2", "978-1")
    library.return_copy(copy_id)

    with pytest.raises(NoAvailableCopyError):
        library.checkout("m1", "978-1")


def test_holder_can_check_out_the_held_copy() -> None:
    """Test 17: The reserving member checks out the copy held for them"""
    library, _, _, copy_id = _library_with_one_copy()
    library.checkout("m1", "978-1")
    library.reserve("m2", "978-1")
    library.return_copy(copy_id)

    loan = library.checkout("m2", "978-1")

    assert loan.copy_id == copy_id
    assert library.status(copy_id) == "checked_out"


def test_reservation_queue_serves_members_in_order() -> None:
    """Test 18: Two reservers are served first-come first-served"""
    library, _, notifier, copy_id = _library_with_one_copy()
    library.register_member("m3", "Cara")
    library.checkout("m1", "978-1")
    library.reserve("m2", "978-1")
    library.reserve("m3", "978-1")

    library.return_copy(copy_id)
    assert notifier.notifications == [("m2", "978-1")]

    library.checkout("m2", "978-1")
    library.return_copy(copy_id)
    assert notifier.notifications == [("m2", "978-1"), ("m3", "978-1")]


def test_reserving_an_available_copy_holds_it_immediately() -> None:
    """Test 19: Reserving while a copy sits on the shelf claims it at once"""
    library, _, notifier, copy_id = _library_with_one_copy()

    library.reserve("m2", "978-1")

    assert library.status(copy_id) == "reserved"
    assert library.available_copies("978-1") == 0
    assert notifier.notifications == [("m2", "978-1")]


def test_cancelled_queued_reservation_is_not_served() -> None:
    """Test 20: A cancelled reservation no longer claims the returned copy"""
    library, _, notifier, copy_id = _library_with_one_copy()
    library.checkout("m1", "978-1")
    library.reserve("m2", "978-1")

    library.cancel_reservation("m2", "978-1")
    library.return_copy(copy_id)

    assert library.status(copy_id) == "available"
    assert notifier.notifications == []


def test_cancelling_an_active_hold_releases_the_copy() -> None:
    """Test 21: Cancelling after the hold was granted frees the copy"""
    library, _, _, copy_id = _library_with_one_copy()
    library.checkout("m1", "978-1")
    library.reserve("m2", "978-1")
    library.return_copy(copy_id)

    library.cancel_reservation("m2", "978-1")

    assert library.status(copy_id) == "available"


def test_cancelling_a_nonexistent_reservation_is_refused() -> None:
    """Test 22: Cancelling without a reservation raises LibraryError"""
    from library_management import LibraryError

    library, _, _, _ = _library_with_one_copy()

    with pytest.raises(LibraryError, match="m2 has no reservation for 978-1"):
        library.cancel_reservation("m2", "978-1")


def test_hold_lapses_after_the_hold_period() -> None:
    """Test 23: An uncollected hold expires and the copy returns to the shelf"""
    library, clock, _, copy_id = _library_with_one_copy(hold_period_days=3)
    library.checkout("m1", "978-1")
    library.reserve("m2", "978-1")
    library.return_copy(copy_id)

    clock.advance(3)
    assert library.status(copy_id) == "reserved"

    clock.advance(1)
    assert library.status(copy_id) == "available"


def test_lapsed_hold_passes_to_the_next_reserver() -> None:
    """Test 24: When a hold lapses the next queued member is notified and served"""
    library, clock, notifier, copy_id = _library_with_one_copy(hold_period_days=3)
    library.register_member("m3", "Cara")
    library.checkout("m1", "978-1")
    library.reserve("m2", "978-1")
    library.reserve("m3", "978-1")
    library.return_copy(copy_id)

    clock.advance(4)

    assert library.status(copy_id) == "reserved"
    assert notifier.notifications == [("m2", "978-1"), ("m3", "978-1")]
    loan = library.checkout("m3", "978-1")
    assert loan.copy_id == copy_id


def test_duplicate_reservation_is_refused() -> None:
    """Test 25: A member cannot reserve the same title twice"""
    from library_management import DuplicateReservationError

    library, _, _, _ = _library_with_one_copy()
    library.checkout("m1", "978-1")
    library.reserve("m2", "978-1")

    with pytest.raises(DuplicateReservationError, match="m2 already has a reservation"):
        library.reserve("m2", "978-1")


def test_default_loan_period_is_fourteen_days() -> None:
    """Test 26: Without configuration a loan is due fourteen days out"""
    from datetime import date

    library, _, _, _ = _library_with_one_copy()

    loan = library.checkout("m1", "978-1")

    assert loan.due_date == date(2026, 1, 19)


def test_default_hold_period_is_three_days() -> None:
    """Test 27: Without configuration an uncollected hold lapses after three days"""
    library, clock, _, copy_id = _library_with_one_copy()
    library.checkout("m1", "978-1")
    library.reserve("m2", "978-1")
    library.return_copy(copy_id)

    clock.advance(3)
    assert library.status(copy_id) == "reserved"

    clock.advance(1)
    assert library.status(copy_id) == "available"


def test_copy_ids_number_copies_of_a_title_sequentially() -> None:
    """Test 28: Copy ids combine the ISBN with a 1-based sequence number"""
    library, _, _ = _make_library()
    library.add_book("978-1", "Refactoring")

    assert library.add_copy("978-1") == "978-1/1"
    assert library.add_copy("978-1") == "978-1/2"


def test_querying_an_unknown_copy_id_is_refused() -> None:
    """Test 29: Asking the status of an unknown copy id raises UnknownCopyError"""
    from library_management import UnknownCopyError

    library, _, _, _ = _library_with_one_copy()

    with pytest.raises(UnknownCopyError, match="978-1/99"):
        library.status("978-1/99")


def test_second_copy_remains_available_when_the_first_is_checked_out() -> None:
    """Test 30: Checkout finds an available copy even behind a checked-out one"""
    library, _, _, first_copy = _library_with_one_copy()
    second_copy = library.add_copy("978-1")
    library.checkout("m1", "978-1")

    loan = library.checkout("m2", "978-1")

    assert loan.copy_id == second_copy
    assert first_copy != second_copy


def test_holder_checks_out_their_copy_even_behind_anothers_hold() -> None:
    """Test 31: A member's held copy is found behind a copy held for someone else"""
    library, _, _, first_copy = _library_with_one_copy()
    second_copy = library.add_copy("978-1")
    library.register_member("m3", "Cara")
    library.register_member("m4", "Dave")
    library.checkout("m1", "978-1")
    library.checkout("m2", "978-1")
    library.reserve("m3", "978-1")
    library.reserve("m4", "978-1")
    library.return_copy(first_copy)
    library.return_copy(second_copy)

    loan = library.checkout("m4", "978-1")

    assert loan.copy_id == second_copy


def test_cancelling_anothers_hold_is_refused_and_keeps_the_hold() -> None:
    """Test 32: A member cannot cancel a hold granted to someone else"""
    from library_management import LibraryError

    library, _, _, copy_id = _library_with_one_copy()
    library.reserve("m2", "978-1")

    with pytest.raises(LibraryError):
        library.cancel_reservation("m1", "978-1")

    assert library.status(copy_id) == "reserved"
    loan = library.checkout("m2", "978-1")
    assert loan.copy_id == copy_id


def test_duplicate_reservation_while_holding_a_copy_is_refused() -> None:
    """Test 33: A member holding a copy cannot reserve the same title again"""
    from library_management import DuplicateReservationError

    library, _, _, _ = _library_with_one_copy()
    library.reserve("m2", "978-1")

    with pytest.raises(DuplicateReservationError):
        library.reserve("m2", "978-1")


def test_second_member_can_reserve_while_a_copy_is_held_for_another() -> None:
    """Test 34: A copy held for one member does not block another's reservation"""
    library, _, notifier, copy_id = _library_with_one_copy()
    library.reserve("m2", "978-1")

    library.reserve("m1", "978-1")

    library.cancel_reservation("m2", "978-1")
    assert library.status(copy_id) == "reserved"
    assert notifier.notifications == [("m2", "978-1"), ("m1", "978-1")]
