"""Robot factory that sources custom robot parts from competing suppliers.

A robot is configured by choosing one option per part category: head
(standard vision, infrared vision, night vision), body (square, round,
triangular, rectangular), arms (hands, pinchers, boxing gloves), movement
(wheels, legs, tracks), and power (solar, rechargeable battery, biomass).
The factory works against a roster of at least three suppliers whose parts
are interchangeable, though not every supplier carries every part. Costing
a robot queries the suppliers and returns, for each chosen part, the
cheapest offer (ties go to the supplier listed first) together with the
grand total; a part no supplier carries is an error, as is an incomplete or
invalid configuration. Purchasing a robot places each part order with its
chosen supplier, which the factory records per supplier, and stamps the
built robot with a unique serial name of two uppercase letters followed by
three digits. Names are drawn from an injected random generator, so a given
seed reproduces the same name sequence and no bare randomness exists in the
factory.

Kata catalogued at tddbuddy.com/katas/robot-factory; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

import string
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from random import Random

#: Valid options per part category.
PART_OPTIONS: dict[str, frozenset[str]] = {
    "head": frozenset({"standard vision", "infrared vision", "night vision"}),
    "body": frozenset({"square", "round", "triangular", "rectangular"}),
    "arms": frozenset({"hands", "pinchers", "boxing gloves"}),
    "movement": frozenset({"wheels", "legs", "tracks"}),
    "power": frozenset({"solar", "rechargeable battery", "biomass"}),
}


class PartUnavailableError(Exception):
    """No supplier on the roster carries the requested part."""


@dataclass(frozen=True)
class Supplier:
    """A parts supplier: a name and a catalog of part option -> price."""

    name: str
    catalog: Mapping[str, float]


@dataclass(frozen=True)
class PartOrder:
    """One sourced part: category, chosen option, supplier, and price."""

    category: str
    option: str
    supplier: str
    price: float


@dataclass(frozen=True)
class Quote:
    """The cheapest sourcing plan for a robot configuration."""

    parts: tuple[PartOrder, ...]

    @property
    def total(self) -> float:
        """Sum of all part prices in the quote."""
        return sum(part.price for part in self.parts)


@dataclass(frozen=True)
class Robot:
    """A purchased robot: unique serial name plus the parts it was built from."""

    name: str
    parts: tuple[PartOrder, ...]

    @property
    def total(self) -> float:
        """Total amount paid for the robot's parts."""
        return sum(part.price for part in self.parts)


class RobotFactory:
    """Costs and purchases custom robots from a roster of suppliers."""

    MIN_SUPPLIERS = 3

    def __init__(self, suppliers: Sequence[Supplier], rng: Random) -> None:
        if len(suppliers) < self.MIN_SUPPLIERS:
            raise ValueError(
                f"at least {self.MIN_SUPPLIERS} suppliers are required, "
                f"got [{len(suppliers)}]"
            )
        names = [supplier.name for supplier in suppliers]
        for name in names:
            if names.count(name) > 1:
                raise ValueError(f"duplicate supplier name [{name}]")
        self._suppliers = list(suppliers)
        self._rng = rng
        self._used_names: set[str] = set()
        self._orders: dict[str, list[PartOrder]] = {name: [] for name in names}

    def cost_robot(self, spec: Mapping[str, str]) -> Quote:
        """Return the cheapest offer per chosen part and the grand total."""
        self._validate_spec(spec)
        parts = []
        for category in PART_OPTIONS:
            option = spec[category]
            offers = [
                (supplier.catalog[option], supplier.name)
                for supplier in self._suppliers
                if option in supplier.catalog
            ]
            if not offers:
                raise PartUnavailableError(f"no supplier carries [{option}]")
            best_price = min(price for price, _ in offers)
            best_supplier = next(name for price, name in offers if price == best_price)
            parts.append(PartOrder(category, option, best_supplier, best_price))
        return Quote(parts=tuple(parts))

    def purchase_robot(self, spec: Mapping[str, str]) -> Robot:
        """Buy the quoted parts from their suppliers and name the built robot."""
        quote = self.cost_robot(spec)
        for part in quote.parts:
            self._orders[part.supplier].append(part)
        return Robot(name=self._next_name(), parts=quote.parts)

    def orders_for(self, supplier_name: str) -> tuple[PartOrder, ...]:
        """Every part order placed with the named supplier so far."""
        if supplier_name not in self._orders:
            raise ValueError(f"unknown supplier [{supplier_name}]")
        return tuple(self._orders[supplier_name])

    def _next_name(self) -> str:
        """Draw an unused serial name (two uppercase letters, three digits)."""
        while True:
            letters = "".join(self._rng.choices(string.ascii_uppercase, k=2))
            name = f"{letters}{self._rng.randrange(1000):03d}"
            if name not in self._used_names:
                self._used_names.add(name)
                return name

    @staticmethod
    def _validate_spec(spec: Mapping[str, str]) -> None:
        for category in spec:
            if category not in PART_OPTIONS:
                raise ValueError(f"unknown part category [{category}]")
        for category, options in PART_OPTIONS.items():
            if category not in spec:
                raise ValueError(f"missing part category [{category}]")
            if spec[category] not in options:
                raise ValueError(f"invalid {category} option [{spec[category]}]")
