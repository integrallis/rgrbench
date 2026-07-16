"""
Tests for the Jelly vs Tower kata.
Damage table lookups, injected randomness, death handling, and round-based
combat with a log.
"""

import pytest


def test_damage_table_for_same_color_towers() -> None:
    """Test 1: Same-color attacks use the ranged column per level"""
    from jelly_vs_tower import Color, damage_range

    assert damage_range(Color.BLUE, 1, Color.BLUE) == (2, 5)
    assert damage_range(Color.BLUE, 2, Color.BLUE) == (5, 9)
    assert damage_range(Color.BLUE, 3, Color.BLUE) == (9, 12)
    assert damage_range(Color.BLUE, 4, Color.BLUE) == (12, 15)
    assert damage_range(Color.RED, 1, Color.RED) == (2, 5)
    assert damage_range(Color.RED, 3, Color.RED) == (9, 12)


def test_damage_table_for_off_color_towers_is_fixed() -> None:
    """Test 2: Off-color attacks deal a fixed 0/1/2/3 by level"""
    from jelly_vs_tower import Color, damage_range

    assert damage_range(Color.BLUE, 1, Color.RED) == (0, 0)
    assert damage_range(Color.BLUE, 2, Color.RED) == (1, 1)
    assert damage_range(Color.BLUE, 3, Color.RED) == (2, 2)
    assert damage_range(Color.BLUE, 4, Color.RED) == (3, 3)
    assert damage_range(Color.RED, 2, Color.BLUE) == (1, 1)
    assert damage_range(Color.RED, 4, Color.BLUE) == (3, 3)


def test_damage_table_for_bluered_towers() -> None:
    """Test 3: BlueRed towers deal the same moderate damage to both colors"""
    from jelly_vs_tower import Color, damage_range

    assert damage_range(Color.BLUE_RED, 1, Color.BLUE) == (2, 2)
    assert damage_range(Color.BLUE_RED, 2, Color.BLUE) == (2, 4)
    assert damage_range(Color.BLUE_RED, 3, Color.RED) == (4, 6)
    assert damage_range(Color.BLUE_RED, 4, Color.RED) == (6, 8)
    assert damage_range(Color.BLUE_RED, 4, Color.BLUE) == (6, 8)


def test_bluered_jelly_takes_the_higher_of_both_columns() -> None:
    """Test 4: Against BlueRed jellies the higher of Blue/Red damage applies"""
    from jelly_vs_tower import Color, damage_range

    assert damage_range(Color.BLUE, 1, Color.BLUE_RED) == (2, 5)
    assert damage_range(Color.RED, 4, Color.BLUE_RED) == (12, 15)
    assert damage_range(Color.BLUE_RED, 4, Color.BLUE_RED) == (6, 8)


@pytest.mark.parametrize("level", [0, 5, -1])
def test_damage_range_rejects_levels_outside_one_to_four(level: int) -> None:
    """Test 5: Levels outside 1-4 raise ValueError"""
    from jelly_vs_tower import Color, damage_range

    with pytest.raises(ValueError):
        damage_range(Color.BLUE, level, Color.BLUE)


@pytest.mark.parametrize("level", [0, 5])
def test_tower_cannot_be_built_with_invalid_level(level: int) -> None:
    """Test 6: Tower construction validates the 1-4 level range"""
    from jelly_vs_tower import Color, Tower

    with pytest.raises(ValueError):
        Tower("t1", Color.BLUE, level)


def test_jelly_is_alive_while_health_is_positive() -> None:
    """Test 7: A jelly with positive health is alive"""
    from jelly_vs_tower import Color, Jelly

    jelly = Jelly("j1", Color.BLUE, 10)

    assert jelly.is_alive is True


def test_jelly_dies_when_health_reaches_zero() -> None:
    """Test 8: A jelly is dead at health zero or below"""
    from jelly_vs_tower import Color, Jelly

    jelly = Jelly("j1", Color.BLUE, 3)
    jelly.take_damage(3)

    assert jelly.health == 0
    assert jelly.is_alive is False


def test_attack_damage_stays_within_the_table_range() -> None:
    """Test 9: A Blue level-1 tower deals 2 to 5 damage to a Blue jelly"""
    from random import Random

    from jelly_vs_tower import Color, Jelly, Tower

    tower = Tower("t1", Color.BLUE, 1)
    rng = Random(0)

    for _ in range(20):
        jelly = Jelly("j1", Color.BLUE, 100)
        damage = tower.attack(jelly, rng)
        assert 2 <= damage <= 5
        assert jelly.health == 100 - damage


def test_fixed_damage_attack_always_deals_the_same_amount() -> None:
    """Test 10: A Red level-2 tower always deals exactly 1 to a Blue jelly"""
    from random import Random

    from jelly_vs_tower import Color, Jelly, Tower

    tower = Tower("t1", Color.RED, 2)
    rng = Random(123)

    for _ in range(10):
        jelly = Jelly("j1", Color.BLUE, 50)
        assert tower.attack(jelly, rng) == 1


def test_level_one_blue_tower_cannot_hurt_red_jelly() -> None:
    """Test 11: The 0-damage cell leaves the jelly untouched"""
    from random import Random

    from jelly_vs_tower import Color, Jelly, Tower

    tower = Tower("t1", Color.BLUE, 1)
    jelly = Jelly("j1", Color.RED, 10)

    assert tower.attack(jelly, Random(7)) == 0
    assert jelly.health == 10


def test_attacks_with_the_same_seed_are_reproducible() -> None:
    """Test 12: Injected randomness makes damage rolls deterministic"""
    from random import Random

    from jelly_vs_tower import Color, Jelly, Tower

    def roll_series(seed: int) -> list[int]:
        tower = Tower("t1", Color.BLUE, 4)
        rng = Random(seed)
        return [
            tower.attack(Jelly("j", Color.BLUE, 100), rng) for _ in range(5)
        ]

    assert roll_series(42) == roll_series(42)


def test_dead_jelly_cannot_be_attacked() -> None:
    """Test 13: Attacking a dead jelly raises ValueError"""
    from random import Random

    from jelly_vs_tower import Color, Jelly, Tower

    tower = Tower("t1", Color.BLUE, 4)
    dead = Jelly("j1", Color.BLUE, 0)

    with pytest.raises(ValueError):
        tower.attack(dead, Random(1))


def test_fight_round_logs_tower_target_and_damage() -> None:
    """Test 14: The combat log records one entry per attack"""
    from random import Random

    from jelly_vs_tower import Battle, Color, Jelly, Tower

    battle = Battle(
        [Tower("t1", Color.RED, 2)],
        [Jelly("j1", Color.BLUE, 10)],
        Random(5),
    )

    log = battle.fight_round()

    assert len(log) == 1
    assert log[0].tower_id == "t1"
    assert log[0].jelly_id == "j1"
    assert log[0].damage == 1


def test_each_tower_attacks_the_first_living_jelly() -> None:
    """Test 15: Both towers concentrate on the leading jelly"""
    from random import Random

    from jelly_vs_tower import Battle, Color, Jelly, Tower

    battle = Battle(
        [Tower("t1", Color.RED, 2), Tower("t2", Color.RED, 3)],
        [Jelly("front", Color.BLUE, 50), Jelly("back", Color.BLUE, 50)],
        Random(9),
    )

    log = battle.fight_round()

    assert [entry.jelly_id for entry in log] == ["front", "front"]


def test_dead_jellies_are_removed_after_the_round() -> None:
    """Test 16: A jelly killed during the round leaves the battle"""
    from random import Random

    from jelly_vs_tower import Battle, Color, Jelly, Tower

    battle = Battle(
        [Tower("t1", Color.BLUE, 4)],
        [Jelly("weak", Color.BLUE, 1), Jelly("strong", Color.BLUE, 100)],
        Random(3),
    )

    battle.fight_round()

    assert [jelly.id for jelly in battle.jellies] == ["strong"]


def test_later_towers_move_on_when_the_target_dies_mid_round() -> None:
    """Test 17: Once a jelly dies, the next tower attacks the next living one"""
    from random import Random

    from jelly_vs_tower import Battle, Color, Jelly, Tower

    battle = Battle(
        [Tower("t1", Color.BLUE, 4), Tower("t2", Color.BLUE, 4)],
        [Jelly("weak", Color.BLUE, 1), Jelly("next", Color.BLUE, 100)],
        Random(11),
    )

    log = battle.fight_round()

    assert log[0].jelly_id == "weak"
    assert log[1].jelly_id == "next"


def test_towers_do_nothing_when_no_jellies_remain() -> None:
    """Test 18: An empty wave produces an empty combat log"""
    from random import Random

    from jelly_vs_tower import Battle, Color, Tower

    battle = Battle([Tower("t1", Color.BLUE, 4)], [], Random(2))

    assert battle.fight_round() == []


def test_round_ends_early_once_every_jelly_is_dead() -> None:
    """Test 19: Remaining towers stand idle after the last jelly dies"""
    from random import Random

    from jelly_vs_tower import Battle, Color, Jelly, Tower

    battle = Battle(
        [
            Tower("t1", Color.BLUE, 4),
            Tower("t2", Color.BLUE, 4),
            Tower("t3", Color.BLUE, 4),
        ],
        [Jelly("only", Color.BLUE, 1)],
        Random(4),
    )

    log = battle.fight_round()

    assert len(log) == 1
    assert battle.jellies == []


def test_battle_over_multiple_rounds_wears_a_jelly_down() -> None:
    """Test 20: Fixed 3-damage hits kill a 9-health jelly in three rounds"""
    from random import Random

    from jelly_vs_tower import Battle, Color, Jelly, Tower

    jelly = Jelly("j1", Color.RED, 9)
    battle = Battle([Tower("t1", Color.BLUE, 4)], [jelly], Random(6))

    assert battle.fight_round()[0].damage == 3
    assert battle.fight_round()[0].damage == 3
    assert battle.fight_round()[0].damage == 3

    assert jelly.is_alive is False
    assert battle.jellies == []
    assert battle.fight_round() == []


def test_invalid_level_error_reports_the_valid_range() -> None:
    """Test 21: The level error names the 1-4 range and the offending value"""
    from jelly_vs_tower import Color, damage_range

    with pytest.raises(
        ValueError, match=r"tower level must be between 1 and 4, got 5"
    ):
        damage_range(Color.BLUE, 5, Color.BLUE)
