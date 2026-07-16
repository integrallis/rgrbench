"""Tests for the 100 Doors kata.

N doors start closed; pass k of N toggles every k-th door. After all passes
only the doors at perfect-square positions remain open. The final state can
be reported as booleans, as open-door positions, or as a string of "@"
(open) and "#" (closed).
"""


def test_single_door_ends_open() -> None:
    """Test 1: With one door there is one pass, which opens door 1"""
    from hundred_doors import open_doors

    assert open_doors(1) == [1]


def test_zero_doors_yield_empty_results() -> None:
    """Test 2: Zero doors produce an empty state list, position list, and string"""
    from hundred_doors import final_door_states, open_doors, render_doors

    assert final_door_states(0) == []
    assert open_doors(0) == []
    assert render_doors(0) == ""


def test_ten_doors_leave_perfect_squares_open() -> None:
    """Test 3: With ten doors, doors 1, 4, and 9 end open"""
    from hundred_doors import open_doors

    assert open_doors(10) == [1, 4, 9]


def test_hundred_doors_leave_perfect_squares_open() -> None:
    """Test 4: With one hundred doors, the ten perfect squares end open"""
    from hundred_doors import open_doors

    assert open_doors(100) == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]


def test_final_states_for_three_doors() -> None:
    """Test 5: Three doors end open, closed, closed after three passes"""
    from hundred_doors import final_door_states

    assert final_door_states(3) == [True, False, False]


def test_state_list_length_matches_door_count() -> None:
    """Test 6: The state list has one entry per door"""
    from hundred_doors import final_door_states

    assert len(final_door_states(100)) == 100


def test_render_ten_doors() -> None:
    """Test 7: Ten doors render with "@" at positions 1, 4, 9 and "#" elsewhere"""
    from hundred_doors import render_doors

    assert render_doors(10) == "@##@####@#"


def test_render_single_door() -> None:
    """Test 8: A single door renders as one open-door marker"""
    from hundred_doors import render_doors

    assert render_doors(1) == "@"


def test_render_four_doors() -> None:
    """Test 9: Four doors render open at 1 and 4"""
    from hundred_doors import render_doors

    assert render_doors(4) == "@##@"


def test_hundred_doors_have_exactly_ten_open() -> None:
    """Test 10: Exactly ten of one hundred doors end open"""
    from hundred_doors import open_doors

    assert len(open_doors(100)) == 10


def test_door_two_ends_closed() -> None:
    """Test 11: Door 2 is toggled twice (passes 1 and 2) so it ends closed"""
    from hundred_doors import final_door_states

    assert final_door_states(100)[1] is False


def test_fifty_doors_leave_perfect_squares_open() -> None:
    """Test 12: With fifty doors the open positions are the squares up to 49"""
    from hundred_doors import open_doors

    assert open_doors(50) == [1, 4, 9, 16, 25, 36, 49]


def test_render_uses_only_open_and_closed_markers() -> None:
    """Test 13: The rendered string contains only "@" and "#" characters"""
    from hundred_doors import render_doors

    assert set(render_doors(20)) == {"@", "#"}


def test_negative_door_count_is_rejected() -> None:
    """Test 14: A negative door count raises ValueError"""
    import pytest

    from hundred_doors import final_door_states

    with pytest.raises(ValueError):
        final_door_states(-1)


def test_negative_door_count_error_names_the_rule() -> None:
    """Test 15: Rejecting a negative count reports "door count must be non-negative" """
    import pytest

    from hundred_doors import final_door_states

    with pytest.raises(ValueError) as excinfo:
        final_door_states(-1)
    assert str(excinfo.value) == "door count must be non-negative"
