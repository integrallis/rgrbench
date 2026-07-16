"""Library management kata.

Models a small lending library. Titles are registered by ISBN with optional
category and location, physical copies are added or removed, and members are
registered by id. A member checks out an available copy and receives a loan
whose due date is the injected clock's today plus the configured loan period.
Returning a copy on or before the due date costs nothing; late returns incur a
per-day fine. Members may reserve a title: when a copy frees up it is held for
the first member in the reservation queue and a notification is sent. A hold
lapses once the clock moves past its expiry date, passing the copy to the next
reserver (with a fresh hold and notification) or releasing it. Reservations
may be cancelled, whether still queued or already holding a copy. Every copy
is in exactly one state - "available", "checked_out" or "reserved" - and only
available copies may be removed. All dates come from the injected clock, so
behaviour is fully deterministic.

Kata catalogued at tddbuddy.com/katas/library-management; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from typing import Protocol

AVAILABLE = "available"
CHECKED_OUT = "checked_out"
RESERVED = "reserved"


class LibraryError(Exception):
    """Base error for invalid library operations."""


class UnknownBookError(LibraryError):
    """Raised when an ISBN has not been registered."""


class UnknownMemberError(LibraryError):
    """Raised when a member id has not been registered."""


class UnknownCopyError(LibraryError):
    """Raised when a copy id does not exist."""


class NoAvailableCopyError(LibraryError):
    """Raised when a checkout finds no copy available to that member."""


class DuplicateReservationError(LibraryError):
    """Raised when a member already has an active reservation for a title."""


class Notifier(Protocol):
    """Receives availability notifications for reserved titles."""

    def notify(self, member_id: str, isbn: str) -> None: ...


class _NullNotifier:
    def notify(self, member_id: str, isbn: str) -> None:
        return None


@dataclass(frozen=True)
class Loan:
    """A checkout record: which copy, which member, and when it is due."""

    copy_id: str
    isbn: str
    member_id: str
    due_date: date


@dataclass(frozen=True)
class BookInfo:
    """Catalogue data for a registered title."""

    isbn: str
    title: str
    category: str | None
    location: str | None


@dataclass
class _Copy:
    copy_id: str
    isbn: str
    status: str = AVAILABLE
    held_for: str | None = None
    hold_expires: date | None = None


class Library:
    """Aggregate root: catalogue, copies, members, loans and reservations."""

    def __init__(
        self,
        clock: Callable[[], date],
        notifier: Notifier | None = None,
        *,
        loan_period_days: int = 14,
        fine_per_day: Decimal = Decimal("0.50"),
        hold_period_days: int = 3,
    ) -> None:
        self._clock = clock
        self._notifier: Notifier = notifier if notifier is not None else _NullNotifier()
        self._loan_period_days = loan_period_days
        self._fine_per_day = fine_per_day
        self._hold_period_days = hold_period_days
        self._books: dict[str, BookInfo] = {}
        self._copies: dict[str, _Copy] = {}
        self._copy_sequence: dict[str, int] = {}
        self._members: dict[str, str] = {}
        self._loans: dict[str, Loan] = {}
        self._queues: dict[str, list[str]] = {}

    # -- catalogue ---------------------------------------------------------

    def add_book(
        self,
        isbn: str,
        title: str,
        category: str | None = None,
        location: str | None = None,
    ) -> None:
        """Register a title in the catalogue."""
        self._books[isbn] = BookInfo(isbn, title, category, location)

    def book_info(self, isbn: str) -> BookInfo:
        """Return the catalogue entry for ``isbn``."""
        self._require_book(isbn)
        return self._books[isbn]

    def add_copy(self, isbn: str) -> str:
        """Add a physical copy of a registered title; return its copy id."""
        self._require_book(isbn)
        sequence = self._copy_sequence.get(isbn, 0) + 1
        self._copy_sequence[isbn] = sequence
        copy_id = f"{isbn}/{sequence}"
        self._copies[copy_id] = _Copy(copy_id, isbn)
        return copy_id

    def remove_copy(self, copy_id: str) -> None:
        """Remove a copy from the system; only available copies may go."""
        copy = self._require_copy(copy_id)
        self._refresh()
        if copy.status != AVAILABLE:
            raise LibraryError(f"Copy {copy_id} is not available for removal")
        del self._copies[copy_id]

    # -- members -----------------------------------------------------------

    def register_member(self, member_id: str, name: str) -> None:
        """Register a library member."""
        self._members[member_id] = name

    # -- queries -----------------------------------------------------------

    def status(self, copy_id: str) -> str:
        """Return the current state of a copy."""
        copy = self._require_copy(copy_id)
        self._refresh()
        return copy.status

    def available_copies(self, isbn: str) -> int:
        """Return how many copies of ``isbn`` are available right now."""
        self._require_book(isbn)
        self._refresh()
        return sum(
            1
            for copy in self._copies.values()
            if copy.isbn == isbn and copy.status == AVAILABLE
        )

    # -- checkout / return -------------------------------------------------

    def checkout(self, member_id: str, isbn: str) -> Loan:
        """Check a copy of ``isbn`` out to ``member_id`` and return the loan.

        A copy held under the member's reservation is used first; otherwise
        any available copy is taken. Raises NoAvailableCopyError when neither
        exists.
        """
        self._require_member(member_id)
        self._require_book(isbn)
        self._refresh()
        copy = self._find_copy(isbn, RESERVED, held_for=member_id)
        if copy is None:
            copy = self._find_copy(isbn, AVAILABLE)
        if copy is None:
            raise NoAvailableCopyError(f"No copies of {isbn} available")
        copy.status = CHECKED_OUT
        copy.held_for = None
        copy.hold_expires = None
        due_date = self._clock() + timedelta(days=self._loan_period_days)
        loan = Loan(copy.copy_id, isbn, member_id, due_date)
        self._loans[copy.copy_id] = loan
        return loan

    def return_copy(self, copy_id: str) -> Decimal:
        """Return a checked-out copy and get the fine owed (0 if on time).

        The fine is the configured per-day amount for each day past the due
        date. The copy then goes to the first queued reserver or back to the
        shelf.
        """
        copy = self._require_copy(copy_id)
        self._refresh()
        loan = self._loans.pop(copy_id, None)
        if loan is None or copy.status != CHECKED_OUT:
            raise LibraryError(f"Copy {copy_id} is not checked out")
        days_late = max(0, (self._clock() - loan.due_date).days)
        self._release(copy)
        return self._fine_per_day * days_late

    # -- reservations ------------------------------------------------------

    def reserve(self, member_id: str, isbn: str) -> None:
        """Place a reservation for ``isbn`` on behalf of ``member_id``.

        If a copy is available it is held for the member immediately;
        otherwise the member joins the queue for the next freed copy.
        """
        self._require_member(member_id)
        self._require_book(isbn)
        self._refresh()
        if self._has_active_reservation(member_id, isbn):
            raise DuplicateReservationError(
                f"Member {member_id} already has a reservation for {isbn}"
            )
        self._queues.setdefault(isbn, []).append(member_id)
        available = self._find_copy(isbn, AVAILABLE)
        if available is not None:
            self._release(available)

    def cancel_reservation(self, member_id: str, isbn: str) -> None:
        """Cancel a queued reservation or release a copy held for the member."""
        self._require_member(member_id)
        self._require_book(isbn)
        self._refresh()
        queue = self._queues.get(isbn, [])
        if member_id in queue:
            queue.remove(member_id)
            return
        held = self._find_copy(isbn, RESERVED, held_for=member_id)
        if held is None:
            raise LibraryError(f"Member {member_id} has no reservation for {isbn}")
        self._release(held)

    # -- internals ---------------------------------------------------------

    def _release(self, copy: _Copy) -> None:
        """Hand a freed copy to the next queued reserver or make it available."""
        queue = self._queues.get(copy.isbn)
        if queue:
            member_id = queue.pop(0)
            copy.status = RESERVED
            copy.held_for = member_id
            copy.hold_expires = self._clock() + timedelta(days=self._hold_period_days)
            self._notifier.notify(member_id, copy.isbn)
        else:
            copy.status = AVAILABLE
            copy.held_for = None
            copy.hold_expires = None

    def _refresh(self) -> None:
        """Lapse any holds whose expiry date has passed."""
        today = self._clock()
        for copy in self._copies.values():
            while (
                copy.status == RESERVED
                and copy.hold_expires is not None
                and today > copy.hold_expires
            ):
                self._release(copy)

    def _find_copy(
        self, isbn: str, status: str, held_for: str | None = None
    ) -> _Copy | None:
        for copy in self._copies.values():
            if copy.isbn != isbn or copy.status != status:
                continue
            if held_for is not None and copy.held_for != held_for:
                continue
            return copy
        return None

    def _has_active_reservation(self, member_id: str, isbn: str) -> bool:
        if member_id in self._queues.get(isbn, []):
            return True
        return self._find_copy(isbn, RESERVED, held_for=member_id) is not None

    def _require_book(self, isbn: str) -> BookInfo:
        if isbn not in self._books:
            raise UnknownBookError(f"Unknown ISBN: {isbn}")
        return self._books[isbn]

    def _require_member(self, member_id: str) -> None:
        if member_id not in self._members:
            raise UnknownMemberError(f"Unknown member: {member_id}")

    def _require_copy(self, copy_id: str) -> _Copy:
        if copy_id not in self._copies:
            raise UnknownCopyError(f"Unknown copy: {copy_id}")
        return self._copies[copy_id]
