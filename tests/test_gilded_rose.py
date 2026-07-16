"""
Tests for the Gilded Rose kata (greenfield implementation of the canonical
requirements): regular items, Aged Brie, Sulfuras, backstage passes, and
Conjured items.
"""

import pytest


def _update_once(name: str, sell_in: int, quality: int) -> "object":
    """Run one daily update over a single item and return it."""
    from gilded_rose import GildedRose, Item

    item = Item(name, sell_in, quality)
    GildedRose([item]).update_quality()
    return item


def test_regular_item_loses_one_quality_and_one_sell_in_per_day() -> None:
    """Test 1: A regular item at (10, 20) becomes (9, 19)"""
    item = _update_once("Elixir of the Mongoose", 10, 20)

    assert item.sell_in == 9
    assert item.quality == 19


def test_regular_item_degrades_twice_as_fast_after_sell_by_date() -> None:
    """Test 2: A regular item at (0, 20) becomes (-1, 18)"""
    item = _update_once("Elixir of the Mongoose", 0, 20)

    assert item.sell_in == -1
    assert item.quality == 18


def test_regular_item_keeps_degrading_double_when_long_expired() -> None:
    """Test 3: A regular item at (-3, 20) becomes (-4, 18)"""
    item = _update_once("Elixir of the Mongoose", -3, 20)

    assert item.sell_in == -4
    assert item.quality == 18


def test_regular_item_quality_never_goes_negative() -> None:
    """Test 4: A regular item at (5, 0) keeps quality 0"""
    item = _update_once("Elixir of the Mongoose", 5, 0)

    assert item.sell_in == 4
    assert item.quality == 0


def test_expired_regular_item_with_quality_one_stops_at_zero() -> None:
    """Test 5: Double degradation still clamps at 0"""
    item = _update_once("Elixir of the Mongoose", 0, 1)

    assert item.quality == 0


def test_aged_brie_gains_quality_as_it_ages() -> None:
    """Test 6: Aged Brie at (10, 20) becomes (9, 21)"""
    from gilded_rose import AGED_BRIE

    item = _update_once(AGED_BRIE, 10, 20)

    assert item.sell_in == 9
    assert item.quality == 21


def test_aged_brie_gains_single_quality_on_the_last_day_before_the_date() -> None:
    """Test 6b: Aged Brie at (1, 20) becomes (0, 21); the double gain starts
    only once the sell-by date has passed"""
    from gilded_rose import AGED_BRIE

    item = _update_once(AGED_BRIE, 1, 20)

    assert item.sell_in == 0
    assert item.quality == 21


def test_aged_brie_gains_double_quality_after_sell_by_date() -> None:
    """Test 7: Aged Brie at (0, 20) becomes (-1, 22)"""
    from gilded_rose import AGED_BRIE

    item = _update_once(AGED_BRIE, 0, 20)

    assert item.sell_in == -1
    assert item.quality == 22


def test_aged_brie_quality_is_capped_at_fifty() -> None:
    """Test 8: Aged Brie at (5, 50) stays at quality 50"""
    from gilded_rose import AGED_BRIE

    item = _update_once(AGED_BRIE, 5, 50)

    assert item.sell_in == 4
    assert item.quality == 50


def test_expired_aged_brie_at_forty_nine_caps_at_fifty() -> None:
    """Test 9: The double gain after the date cannot exceed 50"""
    from gilded_rose import AGED_BRIE

    item = _update_once(AGED_BRIE, 0, 49)

    assert item.quality == 50


def test_sulfuras_never_changes() -> None:
    """Test 10: Sulfuras at (10, 80) stays at (10, 80)"""
    from gilded_rose import SULFURAS, SULFURAS_QUALITY

    item = _update_once(SULFURAS, 10, SULFURAS_QUALITY)

    assert item.sell_in == 10
    assert item.quality == 80


def test_sulfuras_is_unchanged_even_past_its_date() -> None:
    """Test 11: Sulfuras at (-1, 80) stays at (-1, 80)"""
    from gilded_rose import SULFURAS

    item = _update_once(SULFURAS, -1, 80)

    assert item.sell_in == -1
    assert item.quality == 80


@pytest.mark.parametrize(
    "sell_in,expected_quality",
    [
        (15, 21),
        (11, 21),
        (10, 22),
        (6, 22),
        (5, 23),
        (1, 23),
    ],
)
def test_backstage_pass_gains_faster_as_concert_approaches(
    sell_in: int, expected_quality: int
) -> None:
    """Test 12: Passes gain +1 above 10 days, +2 at 10-6 days, +3 at 5-1 days"""
    from gilded_rose import BACKSTAGE_PASS

    item = _update_once(BACKSTAGE_PASS, sell_in, 20)

    assert item.sell_in == sell_in - 1
    assert item.quality == expected_quality


def test_backstage_pass_drops_to_zero_after_concert() -> None:
    """Test 13: A pass at (0, 20) becomes (-1, 0)"""
    from gilded_rose import BACKSTAGE_PASS

    item = _update_once(BACKSTAGE_PASS, 0, 20)

    assert item.sell_in == -1
    assert item.quality == 0


def test_backstage_pass_stays_worthless_after_concert() -> None:
    """Test 14: A pass already past the concert remains at quality 0"""
    from gilded_rose import BACKSTAGE_PASS

    item = _update_once(BACKSTAGE_PASS, -2, 20)

    assert item.quality == 0


def test_backstage_pass_quality_is_capped_at_fifty() -> None:
    """Test 15: The +3 gain close to the concert cannot exceed 50"""
    from gilded_rose import BACKSTAGE_PASS

    item = _update_once(BACKSTAGE_PASS, 5, 49)

    assert item.quality == 50


def test_conjured_item_degrades_twice_as_fast_as_regular() -> None:
    """Test 16: A Conjured item at (10, 20) becomes (9, 18)"""
    item = _update_once("Conjured Mana Cake", 10, 20)

    assert item.sell_in == 9
    assert item.quality == 18


def test_conjured_item_degrades_four_per_day_after_sell_by_date() -> None:
    """Test 17: A Conjured item at (0, 20) becomes (-1, 16)"""
    item = _update_once("Conjured Mana Cake", 0, 20)

    assert item.sell_in == -1
    assert item.quality == 16


def test_conjured_item_quality_never_goes_negative() -> None:
    """Test 18: A Conjured item at (5, 1) clamps to quality 0"""
    item = _update_once("Conjured Mana Cake", 5, 1)

    assert item.quality == 0


def test_expired_conjured_item_with_quality_three_clamps_to_zero() -> None:
    """Test 19: The quadruple loss after the date clamps at 0"""
    item = _update_once("Conjured Mana Cake", 0, 3)

    assert item.quality == 0


def test_update_quality_processes_every_item_in_the_inventory() -> None:
    """Test 20: One call updates all items independently"""
    from gilded_rose import AGED_BRIE, SULFURAS, GildedRose, Item

    items = [
        Item("Elixir of the Mongoose", 10, 20),
        Item(AGED_BRIE, 10, 20),
        Item(SULFURAS, 10, 80),
    ]
    GildedRose(items).update_quality()

    assert [(item.sell_in, item.quality) for item in items] == [
        (9, 19),
        (9, 21),
        (10, 80),
    ]


def test_regular_item_over_three_days() -> None:
    """Test 21: Three updates take a regular item from (2, 10) to (-1, 6)"""
    from gilded_rose import GildedRose, Item

    item = Item("Elixir of the Mongoose", 2, 10)
    shop = GildedRose([item])
    for _ in range(3):
        shop.update_quality()

    assert item.sell_in == -1
    assert item.quality == 6


def test_backstage_pass_full_lifecycle_ends_at_zero() -> None:
    """Test 22: A pass at (12, 10) reaches quality 0 the day after the concert"""
    from gilded_rose import BACKSTAGE_PASS, GildedRose, Item

    item = Item(BACKSTAGE_PASS, 12, 10)
    shop = GildedRose([item])
    for _ in range(13):
        shop.update_quality()

    assert item.sell_in == -1
    assert item.quality == 0


def test_item_exposes_name_sell_in_and_quality() -> None:
    """Test 23: Item stores the three properties from the spec"""
    from gilded_rose import Item

    item = Item("Elixir of the Mongoose", 7, 33)

    assert item.name == "Elixir of the Mongoose"
    assert item.sell_in == 7
    assert item.quality == 33
