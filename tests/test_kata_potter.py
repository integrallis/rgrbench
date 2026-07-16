"""
Tests for the Kata Potter bookshop pricing kata.
Base price, discount tiers for distinct titles, and optimal (non-greedy)
grouping of multi-copy baskets.
"""

import pytest


def test_empty_basket_costs_nothing() -> None:
    """Test 1: An empty basket costs 0.00"""
    from kata_potter import price

    assert price([]) == 0.0


def test_single_book_costs_eight_euros() -> None:
    """Test 2: One book costs the base price of 8.00"""
    from kata_potter import price

    assert price([1]) == pytest.approx(8.00)


def test_each_title_alone_costs_the_same() -> None:
    """Test 3: The base price does not depend on which title is bought"""
    from kata_potter import price

    for book in (1, 2, 3, 4, 5):
        assert price([book]) == pytest.approx(8.00)


def test_two_copies_of_the_same_title_get_no_discount() -> None:
    """Test 4: Identical copies never form a discounted set: 2 x 8.00"""
    from kata_potter import price

    assert price([2, 2]) == pytest.approx(16.00)


def test_three_copies_of_the_same_title_get_no_discount() -> None:
    """Test 5: Three identical copies cost 3 x 8.00"""
    from kata_potter import price

    assert price([1, 1, 1]) == pytest.approx(24.00)


def test_two_different_titles_get_five_percent_off() -> None:
    """Test 6: Two distinct books cost 16.00 * 0.95 = 15.20"""
    from kata_potter import price

    assert price([1, 2]) == pytest.approx(15.20)


def test_three_different_titles_get_ten_percent_off() -> None:
    """Test 7: Three distinct books cost 24.00 * 0.90 = 21.60"""
    from kata_potter import price

    assert price([1, 3, 5]) == pytest.approx(21.60)


def test_four_different_titles_get_twenty_percent_off() -> None:
    """Test 8: Four distinct books cost 32.00 * 0.80 = 25.60"""
    from kata_potter import price

    assert price([1, 2, 3, 4]) == pytest.approx(25.60)


def test_five_different_titles_get_twenty_five_percent_off() -> None:
    """Test 9: The full series costs 40.00 * 0.75 = 30.00"""
    from kata_potter import price

    assert price([1, 2, 3, 4, 5]) == pytest.approx(30.00)


def test_pair_plus_single_combines_discounted_and_full_price() -> None:
    """Test 10: [1, 1, 2] costs 15.20 + 8.00 = 23.20"""
    from kata_potter import price

    assert price([1, 1, 2]) == pytest.approx(23.20)


def test_two_full_series_cost_two_five_sets() -> None:
    """Test 11: Two copies of every title cost 2 x 30.00 = 60.00"""
    from kata_potter import price

    assert price([1, 1, 2, 2, 3, 3, 4, 4, 5, 5]) == pytest.approx(60.00)


def test_greedy_grouping_trap_is_avoided() -> None:
    """Test 12: 2x(1,2,3) + 1x(4,5) is 51.20 as two four-sets, not 51.60"""
    from kata_potter import price

    basket = [1, 1, 2, 2, 3, 3, 4, 5]

    assert price(basket) == pytest.approx(51.20)


def test_two_greedy_traps_in_one_basket() -> None:
    """Test 13: 4x(1,2,3) + 2x(4,5) is four four-sets: 4 x 25.60 = 102.40"""
    from kata_potter import price

    basket = [1] * 4 + [2] * 4 + [3] * 4 + [4] * 2 + [5] * 2

    assert price(basket) == pytest.approx(102.40)


def test_basket_order_does_not_change_the_price() -> None:
    """Test 14: Pricing depends only on title counts, not on order"""
    from kata_potter import price

    assert price([5, 3, 1, 2, 4, 1, 3, 5]) == price([1, 1, 2, 3, 3, 4, 5, 5])


def test_full_series_plus_one_extra_copy() -> None:
    """Test 15: [1..5] plus another book 1 costs 30.00 + 8.00 = 38.00"""
    from kata_potter import price

    assert price([1, 2, 3, 4, 5, 1]) == pytest.approx(38.00)


def test_larger_basket_prices_efficiently_and_correctly() -> None:
    """Test 16: Five full series (25 books) cost 5 x 30.00 = 150.00"""
    from kata_potter import price

    basket = [book for book in (1, 2, 3, 4, 5) for _ in range(5)]

    assert price(basket) == pytest.approx(150.00)


def test_mixed_basket_with_uneven_counts() -> None:
    """Test 17: 3x1, 2x2, 1x3 groups as (1,2,3)+(1,2)+(1): 21.60+15.20+8.00"""
    from kata_potter import price

    assert price([1, 1, 1, 2, 2, 3]) == pytest.approx(44.80)


@pytest.mark.parametrize("bad_book", [0, 6, -1, "one"])
def test_unknown_books_are_rejected(bad_book: object) -> None:
    """Test 18: Titles outside 1-5 raise ValueError"""
    from kata_potter import price

    with pytest.raises(ValueError):
        price([1, bad_book])


def test_price_returns_a_float_in_euros() -> None:
    """Test 19: The result is a numeric amount in euros"""
    from kata_potter import price

    result = price([1, 2])

    assert isinstance(result, float)


def test_unknown_book_error_names_the_offending_title() -> None:
    """Test 20: The rejection message identifies the unknown title"""
    from kata_potter import price

    with pytest.raises(ValueError) as excinfo:
        price([1, 6])
    assert str(excinfo.value) == "unknown book: 6"
