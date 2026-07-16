"""Tests for the Pagination kata."""


def test_exactly_divisible_collection_yields_even_pages() -> None:
    """Test 1: 100 items at 10 per page make exactly 10 pages"""
    from pagination import paginate

    result = paginate(total_items=100, page_size=10, current_page=1)

    assert result.total_pages == 10
    assert result.current_page == 1
    assert result.page_size == 10


def test_remainder_items_add_a_final_partial_page() -> None:
    """Test 2: 95 items at 10 per page make 10 pages via ceiling division"""
    from pagination import paginate

    result = paginate(total_items=95, page_size=10, current_page=10)

    assert result.total_pages == 10
    assert result.start_item == 91
    assert result.end_item == 95


def test_middle_page_reports_its_item_range() -> None:
    """Test 3: Page 3 of 10-per-page covers items 21 through 30"""
    from pagination import paginate

    result = paginate(total_items=100, page_size=10, current_page=3)

    assert result.start_item == 21
    assert result.end_item == 30


def test_single_item_collection_has_one_page() -> None:
    """Test 4: One item makes a single one-item page with no neighbours"""
    from pagination import paginate

    result = paginate(total_items=1, page_size=10, current_page=1)

    assert result.total_pages == 1
    assert result.start_item == 1
    assert result.end_item == 1
    assert result.has_previous is False
    assert result.has_next is False


def test_zero_items_is_a_special_empty_result() -> None:
    """Test 5: An empty collection yields zero pages and no items"""
    from pagination import paginate

    result = paginate(total_items=0, page_size=10, current_page=1)

    assert result.total_pages == 0
    assert result.current_page == 0
    assert result.start_item == 0
    assert result.end_item == 0
    assert result.has_previous is False
    assert result.has_next is False


def test_current_page_below_one_clamps_to_first_page() -> None:
    """Test 6: Requests for page 0 or negative pages clamp to page 1"""
    from pagination import paginate

    assert paginate(100, 10, 0).current_page == 1
    assert paginate(100, 10, -7).current_page == 1


def test_current_page_beyond_last_clamps_to_last_page() -> None:
    """Test 7: Requests past the final page clamp to the final page"""
    from pagination import paginate

    result = paginate(total_items=95, page_size=10, current_page=42)

    assert result.current_page == 10
    assert result.start_item == 91
    assert result.end_item == 95


def test_first_page_has_next_but_no_previous() -> None:
    """Test 8: Page 1 of many reports has_next only"""
    from pagination import paginate

    result = paginate(total_items=100, page_size=10, current_page=1)

    assert result.has_previous is False
    assert result.has_next is True


def test_middle_page_has_both_neighbours() -> None:
    """Test 9: An interior page reports both has_previous and has_next"""
    from pagination import paginate

    result = paginate(total_items=100, page_size=10, current_page=5)

    assert result.has_previous is True
    assert result.has_next is True


def test_last_page_has_previous_but_no_next() -> None:
    """Test 10: The final page reports has_previous only"""
    from pagination import paginate

    result = paginate(total_items=100, page_size=10, current_page=10)

    assert result.has_previous is True
    assert result.has_next is False


def test_page_size_of_one_gives_one_item_per_page() -> None:
    """Test 11: With page size 1, page n holds exactly item n"""
    from pagination import paginate

    result = paginate(total_items=5, page_size=1, current_page=3)

    assert result.total_pages == 5
    assert result.start_item == 3
    assert result.end_item == 3


def test_collection_smaller_than_one_page_fits_on_page_one() -> None:
    """Test 12: 7 items at 10 per page make one page holding items 1-7"""
    from pagination import paginate

    result = paginate(total_items=7, page_size=10, current_page=1)

    assert result.total_pages == 1
    assert result.start_item == 1
    assert result.end_item == 7
    assert result.has_next is False


def test_negative_total_items_is_rejected() -> None:
    """Test 13: A negative item count raises ValueError with the offending value"""
    import pytest

    from pagination import paginate

    with pytest.raises(ValueError) as excinfo:
        paginate(total_items=-1, page_size=10, current_page=1)
    assert str(excinfo.value) == "total_items must be non-negative, got [-1]"


def test_page_size_below_one_is_rejected() -> None:
    """Test 14: A zero or negative page size raises ValueError"""
    import pytest

    from pagination import paginate

    with pytest.raises(ValueError) as excinfo:
        paginate(total_items=10, page_size=0, current_page=1)
    assert str(excinfo.value) == "page_size must be at least 1, got [0]"

    with pytest.raises(ValueError) as excinfo:
        paginate(total_items=10, page_size=-3, current_page=1)
    assert str(excinfo.value) == "page_size must be at least 1, got [-3]"


def test_page_window_is_centred_on_the_current_page() -> None:
    """Test 15: A 5-wide window around page 6 of 10 shows pages 4-8"""
    from pagination import paginate

    result = paginate(total_items=100, page_size=10, current_page=6)

    assert result.page_window(5) == [4, 5, 6, 7, 8]


def test_page_window_shifts_right_at_the_left_edge() -> None:
    """Test 16: Near page 1 the window anchors at page 1 instead of centring"""
    from pagination import paginate

    result = paginate(total_items=100, page_size=10, current_page=2)

    assert result.page_window(5) == [1, 2, 3, 4, 5]


def test_page_window_shifts_left_at_the_right_edge() -> None:
    """Test 17: Near the last page the window anchors at the last page"""
    from pagination import paginate

    result = paginate(total_items=100, page_size=10, current_page=10)

    assert result.page_window(5) == [6, 7, 8, 9, 10]


def test_page_window_larger_than_page_count_returns_all_pages() -> None:
    """Test 18: A window wider than the collection lists every page"""
    from pagination import paginate

    result = paginate(total_items=30, page_size=10, current_page=2)

    assert result.page_window(7) == [1, 2, 3]


def test_even_page_window_places_current_page_left_of_centre() -> None:
    """Test 19: A 4-wide window around page 6 of 10 shows pages 5-8"""
    from pagination import paginate

    result = paginate(total_items=100, page_size=10, current_page=6)

    assert result.page_window(4) == [5, 6, 7, 8]


def test_page_window_of_empty_collection_is_empty() -> None:
    """Test 20: Zero items yield an empty page window"""
    from pagination import paginate

    result = paginate(total_items=0, page_size=10, current_page=1)

    assert result.page_window(5) == []


def test_page_window_size_below_one_is_rejected() -> None:
    """Test 21: A window size below one raises ValueError"""
    import pytest

    from pagination import paginate

    result = paginate(total_items=100, page_size=10, current_page=1)

    with pytest.raises(ValueError) as excinfo:
        result.page_window(0)
    assert str(excinfo.value) == "window_size must be at least 1, got [0]"


def test_empty_result_still_reports_item_count_and_page_size() -> None:
    """Test 22: The empty-collection result echoes the requested sizes"""
    from pagination import paginate

    result = paginate(total_items=0, page_size=10, current_page=1)

    assert result.total_items == 0
    assert result.page_size == 10


def test_result_reports_the_total_item_count() -> None:
    """Test 23: The result carries the item count the pages were computed from"""
    from pagination import paginate

    result = paginate(total_items=95, page_size=10, current_page=3)

    assert result.total_items == 95


def test_second_page_has_a_previous_page() -> None:
    """Test 24: Page 2, the first page after page 1, reports has_previous"""
    from pagination import paginate

    result = paginate(total_items=100, page_size=10, current_page=2)

    assert result.has_previous is True
