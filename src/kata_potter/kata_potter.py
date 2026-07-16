"""Potter bookshop pricing: minimal cost grouping with set discounts."""

from collections import Counter
from collections.abc import Iterable
from functools import lru_cache

BOOKS = (1, 2, 3, 4, 5)
BOOK_PRICE_CENTS = 800

# Price in cents of a bundle of N distinct titles (0%/5%/10%/20%/25% off).
_SET_PRICE_CENTS: dict[int, int] = {
    1: 800,
    2: 1520,
    3: 2160,
    4: 2560,
    5: 3000,
}


def price(basket: Iterable[int]) -> float:
    """Cheapest total price in euros for a basket of books (titles 1-5).

    Copies are grouped into discounted sets of distinct titles so that the
    overall cost is minimal; a plain greedy grouping is not always optimal.
    """
    books = list(basket)
    for book in books:
        if book not in BOOKS:
            raise ValueError(f"unknown book: {book!r}")
    counts = _normalize(Counter(books).values())
    return _min_cost_cents(counts) / 100


def _normalize(counts: Iterable[int]) -> tuple[int, ...]:
    """Sort positive title counts descending so equivalent baskets share a key."""
    return tuple(sorted((c for c in counts if c > 0), reverse=True))


@lru_cache(maxsize=None)
def _min_cost_cents(counts: tuple[int, ...]) -> int:
    """Minimal cost in cents for the given descending title-count profile.

    Each step forms one set of ``size`` distinct titles taken from the most
    abundant titles, then recurses; trying every set size covers the optimal
    grouping.
    """
    if not counts:
        return 0
    best: int | None = None
    for size in range(1, len(counts) + 1):
        remaining = list(counts)
        for i in range(size):
            remaining[i] -= 1
        cost = _SET_PRICE_CENTS[size] + _min_cost_cents(_normalize(remaining))
        if best is None or cost < best:
            best = cost
    return best
