"""
Tests for the Linked List kata (tddbuddy.com/katas/linked-list).
A singly linked list built from Node(value, next) cells with a head pointer;
no built-in sequence backs the storage.
"""

import pytest


def test_new_list_is_empty() -> None:
    """Test 1: A new list has size 0, an empty to_list and no head"""
    from linked_list import LinkedList

    items = LinkedList()

    assert items.size() == 0
    assert items.to_list() == []
    assert items.head is None


def test_append_to_empty_list_creates_a_single_element_list() -> None:
    """Test 2: Appending to an empty list yields a single-element list"""
    from linked_list import LinkedList

    items = LinkedList()
    items.append("a")

    assert items.size() == 1
    assert items.to_list() == ["a"]


def test_append_adds_elements_at_the_end() -> None:
    """Test 3: Successive appends preserve insertion order"""
    from linked_list import LinkedList

    items = LinkedList()
    items.append(1)
    items.append(2)
    items.append(3)

    assert items.to_list() == [1, 2, 3]


def test_prepend_adds_elements_at_the_beginning() -> None:
    """Test 4: Prepend places the new element before existing ones"""
    from linked_list import LinkedList

    items = LinkedList()
    items.append(2)
    items.append(3)
    items.prepend(1)

    assert items.to_list() == [1, 2, 3]


def test_elements_are_linked_through_node_next_pointers() -> None:
    """Test 5: head exposes Node cells chained by value/next"""
    from linked_list import LinkedList

    items = LinkedList()
    items.append("x")
    items.append("y")

    assert items.head is not None
    assert items.head.value == "x"
    assert items.head.next is not None
    assert items.head.next.value == "y"
    assert items.head.next.next is None


def test_size_tracks_additions_and_removals() -> None:
    """Test 6: size() reflects appends, prepends and removals"""
    from linked_list import LinkedList

    items = LinkedList()
    items.append(10)
    items.prepend(5)
    items.append(20)
    assert items.size() == 3

    items.remove(1)
    assert items.size() == 2


def test_get_returns_the_value_at_each_index() -> None:
    """Test 7: get() is 0-based and reaches every position"""
    from linked_list import LinkedList

    items = LinkedList()
    for value in ["a", "b", "c"]:
        items.append(value)

    assert items.get(0) == "a"
    assert items.get(1) == "b"
    assert items.get(2) == "c"


@pytest.mark.parametrize("bad_index", [-1, 3, 99])
def test_get_with_an_invalid_index_is_an_error(bad_index: int) -> None:
    """Test 8: get() outside 0..size-1 raises IndexError('index out of bounds')"""
    from linked_list import LinkedList

    items = LinkedList()
    for value in [1, 2, 3]:
        items.append(value)

    with pytest.raises(IndexError, match="index out of bounds"):
        items.get(bad_index)


def test_get_on_an_empty_list_is_an_error() -> None:
    """Test 9: get(0) on an empty list raises IndexError"""
    from linked_list import LinkedList

    with pytest.raises(IndexError, match="index out of bounds"):
        LinkedList().get(0)


def test_remove_returns_the_removed_value() -> None:
    """Test 10: remove() hands back the value that was removed"""
    from linked_list import LinkedList

    items = LinkedList()
    for value in ["a", "b", "c"]:
        items.append(value)

    assert items.remove(1) == "b"


def test_remove_first_element_updates_the_head() -> None:
    """Test 11: Removing index 0 promotes the second element to head"""
    from linked_list import LinkedList

    items = LinkedList()
    for value in [1, 2, 3]:
        items.append(value)

    items.remove(0)

    assert items.to_list() == [2, 3]
    assert items.head is not None
    assert items.head.value == 2


def test_remove_middle_element_closes_the_gap() -> None:
    """Test 12: Removing a middle element links its neighbours together"""
    from linked_list import LinkedList

    items = LinkedList()
    for value in [1, 2, 3, 4]:
        items.append(value)

    items.remove(2)

    assert items.to_list() == [1, 2, 4]


def test_remove_last_element() -> None:
    """Test 13: Removing the final index drops the tail"""
    from linked_list import LinkedList

    items = LinkedList()
    for value in [1, 2, 3]:
        items.append(value)

    items.remove(2)

    assert items.to_list() == [1, 2]


def test_remove_the_only_element_leaves_an_empty_list() -> None:
    """Test 14: Removing the sole element empties the list"""
    from linked_list import LinkedList

    items = LinkedList()
    items.append("only")

    assert items.remove(0) == "only"
    assert items.size() == 0
    assert items.head is None


def test_remove_from_an_empty_list_is_an_error() -> None:
    """Test 15: remove(0) on an empty list raises IndexError"""
    from linked_list import LinkedList

    with pytest.raises(IndexError, match="index out of bounds"):
        LinkedList().remove(0)


@pytest.mark.parametrize("bad_index", [-1, 2])
def test_remove_with_an_invalid_index_is_an_error(bad_index: int) -> None:
    """Test 16: remove() outside 0..size-1 raises IndexError"""
    from linked_list import LinkedList

    items = LinkedList()
    items.append(1)
    items.append(2)

    with pytest.raises(IndexError, match="index out of bounds"):
        items.remove(bad_index)


def test_insert_at_the_beginning() -> None:
    """Test 17: insert_at(0, v) behaves like prepend"""
    from linked_list import LinkedList

    items = LinkedList()
    items.append(2)
    items.append(3)

    items.insert_at(0, 1)

    assert items.to_list() == [1, 2, 3]


def test_insert_at_a_middle_index_shifts_elements_right() -> None:
    """Test 18: insert_at pushes subsequent elements one position right"""
    from linked_list import LinkedList

    items = LinkedList()
    for value in [1, 3, 4]:
        items.append(value)

    items.insert_at(1, 2)

    assert items.to_list() == [1, 2, 3, 4]


def test_insert_at_size_is_equivalent_to_append() -> None:
    """Test 19: insert_at(size(), v) appends at the end"""
    from linked_list import LinkedList

    items = LinkedList()
    items.append(1)
    items.append(2)

    items.insert_at(items.size(), 3)

    assert items.to_list() == [1, 2, 3]


@pytest.mark.parametrize("bad_index", [-1, 3])
def test_insert_at_an_invalid_index_is_an_error(bad_index: int) -> None:
    """Test 20: insert_at outside 0..size raises IndexError"""
    from linked_list import LinkedList

    items = LinkedList()
    items.append(1)
    items.append(2)

    with pytest.raises(IndexError, match="index out of bounds"):
        items.insert_at(bad_index, 99)


def test_contains_reports_presence_and_absence() -> None:
    """Test 21: contains() is True for stored values and False otherwise"""
    from linked_list import LinkedList

    items = LinkedList()
    for value in ["a", "b"]:
        items.append(value)

    assert items.contains("a") is True
    assert items.contains("b") is True
    assert items.contains("z") is False


def test_index_of_returns_the_first_occurrence() -> None:
    """Test 22: index_of() finds the first match of a repeated value"""
    from linked_list import LinkedList

    items = LinkedList()
    for value in ["a", "b", "a"]:
        items.append(value)

    assert items.index_of("a") == 0
    assert items.index_of("b") == 1


def test_index_of_a_missing_value_is_minus_one() -> None:
    """Test 23: index_of() returns -1 when the value is absent"""
    from linked_list import LinkedList

    items = LinkedList()
    items.append("a")

    assert items.index_of("z") == -1


def test_reverse_reverses_the_element_order() -> None:
    """Test 24: reverse() flips the list in place"""
    from linked_list import LinkedList

    items = LinkedList()
    for value in [1, 2, 3, 4]:
        items.append(value)

    items.reverse()

    assert items.to_list() == [4, 3, 2, 1]
    assert items.size() == 4


def test_reverse_of_empty_and_single_element_lists_is_harmless() -> None:
    """Test 25: reverse() on empty and one-element lists leaves them intact"""
    from linked_list import LinkedList

    empty = LinkedList()
    empty.reverse()
    assert empty.to_list() == []

    single = LinkedList()
    single.append(7)
    single.reverse()
    assert single.to_list() == [7]


def test_insert_at_a_middle_index_grows_the_size_by_one() -> None:
    """Test 26: A middle insert increases size() by exactly one"""
    from linked_list import LinkedList

    items = LinkedList()
    for value in [1, 3, 4]:
        items.append(value)

    items.insert_at(1, 2)

    assert items.size() == 4


def test_index_of_reaches_positions_beyond_the_second() -> None:
    """Test 27: index_of() keeps counting past index 1 for later elements"""
    from linked_list import LinkedList

    items = LinkedList()
    for value in ["a", "b", "c", "d"]:
        items.append(value)

    assert items.index_of("c") == 2
    assert items.index_of("d") == 3
