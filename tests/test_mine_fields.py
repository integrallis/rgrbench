"""
Port of C# MineFields TestMineFields.cs
Complete port with all test cases
"""

import pytest

from mine_fields.mine_fields import Constants, MineFields


def test_build_field_size_of_one_by_one_and_zero_mine() -> None:
    """Port of test build_field_size_of_one_by_one_and_zero_mine"""
    fields = MineFields()
    fields.create(1, 1)
    assert fields.get_hint(0, 0) == 0


def test_build_field_size_of_one_by_one_and_one_mine() -> None:
    """Port of test build_field_size_of_one_by_one_and_one_mine"""
    fields = MineFields()
    fields.create(1, 1)
    fields.mine(0, 0)
    assert fields.get_hint(0, 0) == -1


# Port of build_two_by_two_field_and_one_of_mine_topleftcorner test cases
@pytest.mark.parametrize(
    "x_pos,y_pos,expect", [(0, 0, -1), (1, 0, 1), (0, 1, 1), (1, 1, 1)]
)
def test_build_two_by_two_field_and_one_of_mine_topleftcorner(
    x_pos: int, y_pos: int, expect: int
) -> None:
    """Port of TestCase parameters for topleftcorner"""
    fields = MineFields()
    fields.create(2, 2)
    fields.mine(0, 0)
    assert fields.get_hint(x_pos, y_pos) == expect


# Port of build_two_by_two_field_and_one_of_mine_bottomrightcorner test cases
@pytest.mark.parametrize(
    "x_pos,y_pos,expect", [(0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, Constants.MINE)]
)
def test_build_two_by_two_field_and_one_of_mine_bottomrightcorner(
    x_pos: int, y_pos: int, expect: int
) -> None:
    """Port of TestCase parameters for bottomrightcorner"""
    fields = MineFields()
    fields.create(2, 2)
    fields.mine(1, 1)
    assert fields.get_hint(x_pos, y_pos) == expect


# Port of build_two_by_two_field_and_one_of_mine_bottomleftcorner test cases
@pytest.mark.parametrize(
    "x_pos,y_pos,expect", [(0, 0, 1), (1, 0, 1), (0, 1, Constants.MINE), (1, 1, 1)]
)
def test_build_two_by_two_field_and_one_of_mine_bottomleftcorner(
    x_pos: int, y_pos: int, expect: int
) -> None:
    """Port of TestCase parameters for bottomleftcorner"""
    fields = MineFields()
    fields.create(2, 2)
    fields.mine(0, 1)
    assert fields.get_hint(x_pos, y_pos) == expect


# Port of build_two_by_two_field_and_one_of_mine_toprightcorner test cases
@pytest.mark.parametrize(
    "x_pos,y_pos,expect", [(0, 0, 1), (1, 0, Constants.MINE), (0, 1, 1), (1, 1, 1)]
)
def test_build_two_by_two_field_and_one_of_mine_toprightcorner(
    x_pos: int, y_pos: int, expect: int
) -> None:
    """Port of TestCase parameters for toprightcorner"""
    fields = MineFields()
    fields.create(2, 2)
    fields.mine(1, 0)
    assert fields.get_hint(x_pos, y_pos) == expect


# Port of build_two_by_two_field_and_two_of_mine test cases
@pytest.mark.parametrize(
    "x_pos,y_pos,expect",
    [(0, 0, Constants.MINE), (1, 0, Constants.MINE), (0, 1, 2), (1, 1, 2)],
)
def test_build_two_by_two_field_and_two_of_mine(
    x_pos: int, y_pos: int, expect: int
) -> None:
    """Port of TestCase parameters for two mines"""
    fields = MineFields()
    fields.create(2, 2)
    fields.mine(0, 0)
    fields.mine(1, 0)
    assert fields.get_hint(x_pos, y_pos) == expect


# Port of build_two_by_two_field_and_three_of_mine test cases
@pytest.mark.parametrize(
    "x_pos,y_pos,expect",
    [(0, 0, Constants.MINE), (1, 0, Constants.MINE), (0, 1, Constants.MINE), (1, 1, 3)],
)
def test_build_two_by_two_field_and_three_of_mine(
    x_pos: int, y_pos: int, expect: int
) -> None:
    """Port of TestCase parameters for three mines"""
    fields = MineFields()
    fields.create(2, 2)
    fields.mine(0, 0)
    fields.mine(1, 0)
    fields.mine(0, 1)
    assert fields.get_hint(x_pos, y_pos) == expect


# Port of build_two_by_two_field_and_four_of_mine test cases
@pytest.mark.parametrize(
    "x_pos,y_pos,expect",
    [
        (0, 0, Constants.MINE),
        (1, 0, Constants.MINE),
        (0, 1, Constants.MINE),
        (1, 1, Constants.MINE),
    ],
)
def test_build_two_by_two_field_and_four_of_mine(
    x_pos: int, y_pos: int, expect: int
) -> None:
    """Port of TestCase parameters for four mines"""
    fields = MineFields()
    fields.create(2, 2)
    fields.mine(0, 0)
    fields.mine(1, 0)
    fields.mine(0, 1)
    fields.mine(1, 1)
    assert fields.get_hint(x_pos, y_pos) == expect


# Port of build_three_by_three_field_and_two_of_mine test cases
@pytest.mark.parametrize(
    "x_pos,y_pos,expect",
    [
        (0, 0, -1),
        (1, 0, -1),
        (2, 0, 1),
        (0, 1, 2),
        (1, 1, 2),
        (2, 1, 1),
        (0, 2, 0),
        (1, 2, 0),
        (2, 2, 0),
    ],
)
def test_build_three_by_three_field_and_two_of_mine(
    x_pos: int, y_pos: int, expect: int
) -> None:
    """Port of TestCase parameters for 3x3 field with two mines"""
    fields = MineFields()
    fields.create(3, 3)
    fields.mine(0, 0)
    fields.mine(1, 0)
    assert fields.get_hint(x_pos, y_pos) == expect


# Port of build_three_by_three_field_and_three_of_mine test cases
@pytest.mark.parametrize(
    "x_pos,y_pos,expect",
    [
        (0, 0, Constants.MINE),
        (1, 0, Constants.MINE),
        (2, 0, 1),
        (0, 1, 3),
        (1, 1, 3),
        (2, 1, 2),
        (0, 2, 1),
        (1, 2, -1),
        (2, 2, 1),
    ],
)
def test_build_three_by_three_field_and_three_of_mine(
    x_pos: int, y_pos: int, expect: int
) -> None:
    """Port of TestCase parameters for 3x3 field with three mines"""
    fields = MineFields()
    fields.create(3, 3)
    fields.mine(0, 0)
    fields.mine(1, 0)
    fields.mine(1, 2)
    assert fields.get_hint(x_pos, y_pos) == expect
