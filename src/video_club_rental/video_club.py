"""Video Club Rental kata - customer rental statements for a video club.

Movies belong to one of three price categories. A regular film costs
2.0 for the first two days plus 1.5 for each additional day. A new
release costs 3.0 per day rented. A children's film costs 1.5 for the
first three days plus 1.5 for each additional day. Every rental earns
the customer one frequent renter point, and a new release kept for more
than one day earns one bonus point. A customer's statement opens with
``Rental Record for <name>``, lists each rented title with its charge on
a tab-indented line (``\\t<title>\\t<charge>``), then reports the total
with ``Amount owed is <total>`` and the points earned with ``You earned
<points> frequent renter points``. Rentals last at least one day.

Kata catalogued at tddbuddy.com/katas/video-club-rental; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from dataclasses import dataclass, field
from enum import Enum, auto


class PriceCode(Enum):
    """Pricing category of a movie."""

    REGULAR = auto()
    NEW_RELEASE = auto()
    CHILDRENS = auto()


@dataclass(frozen=True)
class Movie:
    """A movie in the club's catalogue."""

    title: str
    price_code: PriceCode


@dataclass(frozen=True)
class Rental:
    """A movie rented for a number of days."""

    movie: Movie
    days_rented: int

    def __post_init__(self) -> None:
        if self.days_rented < 1:
            raise ValueError("days_rented must be at least 1")

    @property
    def charge(self) -> float:
        """Rental charge under the movie's pricing category."""
        return _charge_for(self.movie.price_code, self.days_rented)

    @property
    def frequent_renter_points(self) -> int:
        """One point per rental, plus a bonus for multi-day new releases."""
        return _points_for(self.movie.price_code, self.days_rented)


def _charge_for(price_code: PriceCode, days_rented: int) -> float:
    if price_code is PriceCode.REGULAR:
        return 2.0 + max(days_rented - 2, 0) * 1.5
    if price_code is PriceCode.NEW_RELEASE:
        return days_rented * 3.0
    return 1.5 + max(days_rented - 3, 0) * 1.5


def _points_for(price_code: PriceCode, days_rented: int) -> int:
    if price_code is PriceCode.NEW_RELEASE and days_rented > 1:
        return 2
    return 1


def _render_statement(name: str, rentals: "tuple[Rental, ...]") -> str:
    lines = [f"Rental Record for {name}"]
    total_charge = 0.0
    total_points = 0
    for rental in rentals:
        total_charge += rental.charge
        total_points += rental.frequent_renter_points
        lines.append(f"\t{rental.movie.title}\t{rental.charge}")
    lines.append(f"Amount owed is {total_charge}")
    lines.append(f"You earned {total_points} frequent renter points")
    return "\n".join(lines)


@dataclass
class Customer:
    """A club member who accumulates rentals and receives statements."""

    name: str
    _rentals: list[Rental] = field(default_factory=list, init=False, repr=False)

    def add_rental(self, rental: Rental) -> None:
        """Record a rental for this customer."""
        self._rentals.append(rental)

    @property
    def rentals(self) -> tuple[Rental, ...]:
        """All rentals recorded so far."""
        return tuple(self._rentals)

    @property
    def total_charge(self) -> float:
        """Sum of the charges of all rentals."""
        return sum((rental.charge for rental in self._rentals), 0.0)

    @property
    def total_frequent_renter_points(self) -> int:
        """Sum of the frequent renter points of all rentals."""
        return sum(rental.frequent_renter_points for rental in self._rentals)

    def statement(self) -> str:
        """Render the customer's rental statement."""
        return _render_statement(self.name, self.rentals)
