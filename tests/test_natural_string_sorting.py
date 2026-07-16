"""
Port of C# NaturalStringSortingTest.cs
Tests for Natural String Sorting kata - sorting strings with embedded numbers naturally
"""


def test_can_sort_string_default_order() -> None:
    """Test 1: Can sort strings in natural ascending order"""
    from natural_string_sorting.natural_string_sorting import NaturalStringSorting

    sorter = NaturalStringSorting()
    strings = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    result = sorter.sort_string(strings)
    expected = ["0", "1", "1a", "2", "3", "23", "21 1", "a1", "b1", "b3", "z 21", "z22"]

    assert result == expected


def test_can_sort_string_des_order() -> None:
    """Test 2: Can sort strings in natural descending order"""
    from natural_string_sorting.natural_string_sorting import NaturalStringSorting

    sorter = NaturalStringSorting()
    strings = ["a1", "1", "3", "2", "b1", "1a", "b3", "23", "z 21", "21 1", "z22", "0"]
    result = sorter.sort_string(strings, NaturalStringSorting.SortOrder.DESCENDING)
    expected = ["z22", "z 21", "b3", "b1", "a1", "21 1", "23", "3", "2", "1a", "1", "0"]

    assert result == expected
