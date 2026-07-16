"""
Port of C# RecentlyUsedListTest.cs
Tests for Recently Used List kata
"""


def test_can_add_items() -> None:
    """Test 1: Can add items to the list"""
    from recently_used_list.recently_used_list import RecentlyUsedList

    recently_used_list = RecentlyUsedList()
    recently_used_list.add("FirstList")

    list_count = recently_used_list.count()
    assert (
        list_count > 0
    ), f"List items count should be Greater than 0 but is {list_count}"


def test_can_add_unique_items() -> None:
    """Test 2: Can add unique items - duplicates should not be added twice"""
    from recently_used_list.recently_used_list import RecentlyUsedList

    recently_used_list = RecentlyUsedList()
    recently_used_list.add("FirstItem")
    recently_used_list.add("SecondItem")
    recently_used_list.add("SecondItem")  # Duplicate
    recently_used_list.add("ThirdItem")
    recently_used_list.add("FourthItem")
    recently_used_list.add("FifthItem")

    expected_list = ["FifthItem", "FourthItem", "ThirdItem", "SecondItem", "FirstItem"]
    actual_list = recently_used_list.to_list()

    assert actual_list == expected_list


def test_can_add_items_in_lifo_order() -> None:
    """Test 3: Can add items in LIFO (Last In First Out) order"""
    from recently_used_list.recently_used_list import RecentlyUsedList

    recently_used_list = RecentlyUsedList()
    recently_used_list.add("FirstItem")
    recently_used_list.add("SecondItem")
    recently_used_list.add("ThirdItem")
    recently_used_list.add("FourthItem")
    recently_used_list.add("FifthItem")

    expected_list = ["FifthItem", "FourthItem", "ThirdItem", "SecondItem", "FirstItem"]
    actual_list = recently_used_list.to_list()

    assert actual_list == expected_list


def test_can_avoid_insertion_of_items_beyond_list_size() -> None:
    """Test 4: Can avoid insertion of items beyond list size (default 5)"""
    from recently_used_list.recently_used_list import RecentlyUsedList

    recently_used_list = RecentlyUsedList()
    recently_used_list.add("FirstItem")
    recently_used_list.add("SecondItem")
    recently_used_list.add("SecondItem")  # Duplicate, shouldn't count
    recently_used_list.add("ThirdItem")
    recently_used_list.add("FourthItem")
    recently_used_list.add("FifthItem")
    recently_used_list.add("SixthItem")  # Should push out FirstItem
    recently_used_list.add("SeventhItem")  # Should push out SecondItem

    # List should only have 5 most recent items
    expected_list = ["SeventhItem", "SixthItem", "FifthItem", "FourthItem", "ThirdItem"]
    actual_list = recently_used_list.to_list()

    assert actual_list == expected_list


def test_can_test_item_by_index() -> None:
    """Test 5: Can test item by index - access list items by their position"""
    from recently_used_list.recently_used_list import RecentlyUsedList

    recently_used_list = RecentlyUsedList()
    recently_used_list.add("FirstItem")
    recently_used_list.add("SecondItem")
    recently_used_list.add("ThirdItem")
    recently_used_list.add("FourthItem")
    recently_used_list.add("FifthItem")

    # Index 3 should return "SecondItem" (0-based indexing)
    expected_list_item = "SecondItem"
    actual_list_item = recently_used_list.get_list_item(3)

    assert actual_list_item == expected_list_item


def test_can_test_default_list_size() -> None:
    """Test 6: Can test default list size - verify default size is 5"""
    from recently_used_list.recently_used_list import RecentlyUsedList

    recently_used_list = RecentlyUsedList()

    expected_list_size = 5
    actual_list_size = recently_used_list.size

    assert actual_list_size == expected_list_size


def test_can_throw_argument_exception_when_supplied_index_is_out_of_scope() -> None:
    """Test 7: Should throw ArgumentError when index is out of scope"""
    import pytest

    from recently_used_list.recently_used_list import RecentlyUsedList

    recently_used_list = RecentlyUsedList()
    recently_used_list.add("FirstItem")
    recently_used_list.add("SecondItem")
    recently_used_list.add("ThirdItem")
    recently_used_list.add("FourthItem")
    recently_used_list.add("FifthItem")

    index = 5  # Out of scope (valid indices are 0-4)

    with pytest.raises(ValueError) as excinfo:
        recently_used_list.get_list_item(index)

    expected_message = f"supplied index [{index}] should not greater than [{recently_used_list.count() - 1}]."
    assert str(excinfo.value) == expected_message


def test_can_throw_argument_exception_when_supplied_index_contain_negative_value() -> (
    None
):
    """Test 8: Should throw ArgumentError when index is negative"""
    import pytest

    from recently_used_list.recently_used_list import RecentlyUsedList

    recently_used_list = RecentlyUsedList()
    recently_used_list.add("FirstItem")
    recently_used_list.add("SecondItem")
    recently_used_list.add("ThirdItem")
    recently_used_list.add("FourthItem")
    recently_used_list.add("FifthItem")

    index = -1  # Negative index

    with pytest.raises(ValueError) as excinfo:
        recently_used_list.get_list_item(index)

    expected_message = f"supplied index [{index}] should be non-negative and not greater than [{recently_used_list.count() - 1}]."
    assert str(excinfo.value) == expected_message


def test_can_throw_argument_exception_when_supplied_item_is_null_or_empty() -> None:
    """Test 9: Should throw ArgumentError when adding null or empty items"""
    import pytest

    from recently_used_list.recently_used_list import RecentlyUsedList

    recently_used_list = RecentlyUsedList()

    # Test with None
    with pytest.raises(ValueError) as excinfo:
        recently_used_list.add(None)
    assert (
        str(excinfo.value)
        == "List items should not be Empty or Null. But it was [None]"
    )

    # Test with empty string
    with pytest.raises(ValueError) as excinfo:
        recently_used_list.add("")
    assert str(excinfo.value) == "List items should not be Empty or Null. But it was []"


def test_can_define_list_size() -> None:
    """Test 10: Can define custom list size"""
    from recently_used_list.recently_used_list import RecentlyUsedList

    custom_size = 10
    sizeable_list = RecentlyUsedList(custom_size)

    assert sizeable_list.size == custom_size


def test_can_get_most_recently_used_item_at_index_zero() -> None:
    """Test 11: Index 0 returns the most recently used item"""
    from recently_used_list.recently_used_list import RecentlyUsedList

    recently_used_list = RecentlyUsedList()
    recently_used_list.add("FirstItem")
    recently_used_list.add("SecondItem")
    recently_used_list.add("ThirdItem")

    expected_list_item = "ThirdItem"
    actual_list_item = recently_used_list.get_list_item(0)

    assert actual_list_item == expected_list_item
