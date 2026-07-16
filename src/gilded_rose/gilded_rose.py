"""Gilded Rose inventory: daily quality updates per item category."""

from dataclasses import dataclass

AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"
CONJURED_PREFIX = "Conjured"

MIN_QUALITY = 0
MAX_QUALITY = 50
SULFURAS_QUALITY = 80


@dataclass
class Item:
    """A stock item: its name, days left to sell, and quality score."""

    name: str
    sell_in: int
    quality: int


class GildedRose:
    """Applies the end-of-day inventory rules to a collection of items."""

    def __init__(self, items: list[Item]) -> None:
        self.items = items

    def update_quality(self) -> None:
        """Advance every item by one day, adjusting quality and sell_in."""
        for item in self.items:
            self._update_item(item)

    def _update_item(self, item: Item) -> None:
        if item.name == SULFURAS:
            return
        if item.name == AGED_BRIE:
            self._age_brie(item)
        elif item.name == BACKSTAGE_PASS:
            self._age_backstage_pass(item)
        else:
            self._age_degrading_item(item)
        item.sell_in -= 1

    def _age_brie(self, item: Item) -> None:
        gain = 2 if item.sell_in <= 0 else 1
        item.quality = min(MAX_QUALITY, item.quality + gain)

    def _age_backstage_pass(self, item: Item) -> None:
        if item.sell_in <= 0:
            item.quality = 0
        elif item.sell_in <= 5:
            item.quality = min(MAX_QUALITY, item.quality + 3)
        elif item.sell_in <= 10:
            item.quality = min(MAX_QUALITY, item.quality + 2)
        else:
            item.quality = min(MAX_QUALITY, item.quality + 1)

    def _age_degrading_item(self, item: Item) -> None:
        loss = 2 if item.name.startswith(CONJURED_PREFIX) else 1
        if item.sell_in <= 0:
            loss *= 2
        item.quality = max(MIN_QUALITY, item.quality - loss)
