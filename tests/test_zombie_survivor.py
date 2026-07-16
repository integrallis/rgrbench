"""
Tests for Zombie Survivor kata - survivors, equipment, game, experience, skills
"""

from datetime import datetime

import pytest

_NOON = datetime(2026, 1, 1, 12, 0)


def _clock() -> datetime:
    return _NOON


def test_new_survivor_defaults() -> None:
    """Test 1: A new survivor is unwounded, alive, unequipped, at Blue"""
    from zombie_survivor import Level, Survivor

    survivor = Survivor("Bill")
    assert survivor.name == "Bill"
    assert survivor.wounds == 0
    assert survivor.is_alive
    assert survivor.actions == 3
    assert survivor.in_hand == ()
    assert survivor.in_reserve == ()
    assert survivor.experience == 0
    assert survivor.level is Level.BLUE


def test_one_wound_leaves_survivor_alive() -> None:
    """Test 2: A single wound hurts but does not kill"""
    from zombie_survivor import Survivor

    survivor = Survivor("Bill")
    survivor.wound()
    assert survivor.wounds == 1
    assert survivor.is_alive


def test_second_wound_kills() -> None:
    """Test 3: A survivor dies upon receiving the second wound"""
    from zombie_survivor import Survivor

    survivor = Survivor("Bill")
    survivor.wound()
    survivor.wound()
    assert not survivor.is_alive


def test_wounds_beyond_death_are_ignored() -> None:
    """Test 4: Additional wounds to a dead survivor do not accumulate"""
    from zombie_survivor import Survivor

    survivor = Survivor("Bill")
    for _ in range(5):
        survivor.wound()
    assert survivor.wounds == 2
    assert not survivor.is_alive


def test_first_two_pieces_go_in_hand_then_reserve() -> None:
    """Test 5: Equipment fills the two hand slots first, then reserve"""
    from zombie_survivor import Survivor

    survivor = Survivor("Ana")
    for item in ["Baseball bat", "Pistol", "Bottled Water", "Molotov"]:
        survivor.pick_up(item)
    assert survivor.in_hand == ("Baseball bat", "Pistol")
    assert survivor.in_reserve == ("Bottled Water", "Molotov")


def test_unwounded_survivor_carries_at_most_five_pieces() -> None:
    """Test 6: The sixth piece of equipment is refused"""
    from zombie_survivor import Survivor

    survivor = Survivor("Ana")
    for item in ["Bat", "Pistol", "Water", "Molotov", "Axe"]:
        survivor.pick_up(item)
    with pytest.raises(ValueError, match="Ana cannot carry any more equipment"):
        survivor.pick_up("Chainsaw")


def test_wound_discards_most_recent_reserve_piece() -> None:
    """Test 7: A wound shrinks capacity and sheds the newest reserve piece"""
    from zombie_survivor import Survivor

    survivor = Survivor("Ana")
    for item in ["Bat", "Pistol", "Water", "Molotov", "Axe"]:
        survivor.pick_up(item)
    survivor.wound()
    assert survivor.in_hand == ("Bat", "Pistol")
    assert survivor.in_reserve == ("Water", "Molotov")


def test_wounded_survivor_capacity_is_four() -> None:
    """Test 8: With one wound only four pieces can be carried"""
    from zombie_survivor import Survivor

    survivor = Survivor("Ana")
    survivor.wound()
    for item in ["Bat", "Pistol", "Water", "Molotov"]:
        survivor.pick_up(item)
    with pytest.raises(ValueError, match="Ana cannot carry any more equipment"):
        survivor.pick_up("Axe")


def test_dead_survivor_cannot_pick_up_equipment() -> None:
    """Test 9: A dead survivor cannot acquire equipment"""
    from zombie_survivor import Survivor

    survivor = Survivor("Bill")
    survivor.wound()
    survivor.wound()
    with pytest.raises(ValueError, match="Bill is dead"):
        survivor.pick_up("Bat")


def test_killing_a_zombie_earns_one_experience_point() -> None:
    """Test 10: Each zombie kill is worth one experience point"""
    from zombie_survivor import Survivor

    survivor = Survivor("Bill")
    survivor.kill_zombie()
    survivor.kill_zombie()
    assert survivor.experience == 2


def test_level_thresholds() -> None:
    """Test 11: Levels are Blue at 0, Yellow at 7, Orange at 19, Red at 43"""
    from zombie_survivor import Level, Survivor

    survivor = Survivor("Bill")
    expectations = {
        0: Level.BLUE,
        6: Level.BLUE,
        7: Level.YELLOW,
        18: Level.YELLOW,
        19: Level.ORANGE,
        42: Level.ORANGE,
        43: Level.RED,
    }
    while survivor.experience <= 43:
        if survivor.experience in expectations:
            assert survivor.level is expectations[survivor.experience]
        survivor.kill_zombie()


def test_yellow_grants_plus_one_action_automatically() -> None:
    """Test 12: Reaching Yellow unlocks '+1 Action' without a choice"""
    from zombie_survivor import PLUS_ONE_ACTION, Survivor

    survivor = Survivor("Bill")
    for _ in range(7):
        survivor.kill_zombie()
    assert survivor.skills == (PLUS_ONE_ACTION,)
    assert survivor.actions == 4


def test_no_skill_choice_before_orange() -> None:
    """Test 13: Below Orange there is nothing to choose"""
    from zombie_survivor import Survivor

    survivor = Survivor("Bill")
    for _ in range(7):
        survivor.kill_zombie()
    assert survivor.skill_options == ()
    with pytest.raises(ValueError, match="Bill has no skill choice available"):
        survivor.choose_skill("Hoard")


def test_orange_offers_a_choice_of_two_skills() -> None:
    """Test 14: Reaching Orange opens a choice between Hoard and Sniper"""
    from zombie_survivor import HOARD, SNIPER, Survivor

    survivor = Survivor("Bill")
    for _ in range(19):
        survivor.kill_zombie()
    assert survivor.skill_options == (HOARD, SNIPER)


def test_hoard_raises_equipment_capacity() -> None:
    """Test 15: Choosing Hoard lets the survivor carry a sixth piece"""
    from zombie_survivor import HOARD, Survivor

    survivor = Survivor("Ana")
    for _ in range(19):
        survivor.kill_zombie()
    survivor.choose_skill(HOARD)
    for item in ["Bat", "Pistol", "Water", "Molotov", "Axe", "Rope"]:
        survivor.pick_up(item)
    assert survivor.in_reserve == ("Water", "Molotov", "Axe", "Rope")


def test_choosing_an_unavailable_skill_is_rejected() -> None:
    """Test 16: Only the offered skills can be chosen"""
    from zombie_survivor import Survivor

    survivor = Survivor("Bill")
    for _ in range(19):
        survivor.kill_zombie()
    with pytest.raises(ValueError, match="'Tough' is not an available skill choice"):
        survivor.choose_skill("Tough")


def test_red_choice_excludes_already_unlocked_skills() -> None:
    """Test 17: The Red slot offers three skills minus those already held"""
    from zombie_survivor import HOARD, SNIPER, TOUGH, Survivor

    survivor = Survivor("Bill")
    for _ in range(19):
        survivor.kill_zombie()
    survivor.choose_skill(SNIPER)
    for _ in range(43 - 19):
        survivor.kill_zombie()
    assert survivor.skill_options == (HOARD, TOUGH)
    survivor.choose_skill(TOUGH)
    assert survivor.skills[-1] == TOUGH


def test_skill_tree_restarts_after_red() -> None:
    """Test 18: Past 43 experience a second '+1 Action' arrives at 50"""
    from zombie_survivor import PLUS_ONE_ACTION, SNIPER, Survivor

    survivor = Survivor("Bill")
    for _ in range(19):
        survivor.kill_zombie()
    survivor.choose_skill(SNIPER)
    for _ in range(50 - 19):
        survivor.kill_zombie()
    assert survivor.skills.count(PLUS_ONE_ACTION) == 2
    assert survivor.actions == 5


def test_game_begins_with_zero_survivors_and_a_timestamped_start() -> None:
    """Test 19: A new game is empty and records its start time"""
    from zombie_survivor import Game

    game = Game(clock=_clock)
    assert game.survivors == ()
    assert game.history == ("Game started at 2026-01-01T12:00:00",)


def test_survivors_can_be_added_at_any_time() -> None:
    """Test 20: Survivors join the game whenever they arrive"""
    from zombie_survivor import Game, Survivor

    game = Game(clock=_clock)
    bill = Survivor("Bill")
    game.add_survivor(bill)
    bill.kill_zombie()
    ana = Survivor("Ana")
    game.add_survivor(ana)
    assert game.survivors == (bill, ana)


def test_survivor_names_must_be_unique_within_a_game() -> None:
    """Test 21: A duplicate survivor name is rejected"""
    from zombie_survivor import Game, Survivor

    game = Game(clock=_clock)
    game.add_survivor(Survivor("Bill"))
    with pytest.raises(ValueError, match="A survivor named 'Bill' already exists"):
        game.add_survivor(Survivor("Bill"))


def test_game_ends_only_when_all_survivors_are_dead() -> None:
    """Test 22: One living survivor keeps the game going"""
    from zombie_survivor import Game, Survivor

    game = Game(clock=_clock)
    bill = Survivor("Bill")
    ana = Survivor("Ana")
    game.add_survivor(bill)
    game.add_survivor(ana)
    bill.wound()
    bill.wound()
    assert not game.has_ended
    ana.wound()
    ana.wound()
    assert game.has_ended


def test_game_without_survivors_has_not_ended() -> None:
    """Test 23: An empty game is not over"""
    from zombie_survivor import Game

    assert not Game(clock=_clock).has_ended


def test_game_level_is_highest_among_living_survivors() -> None:
    """Test 24: The game level tracks its most experienced living survivor"""
    from zombie_survivor import Game, Level, Survivor

    game = Game(clock=_clock)
    bill = Survivor("Bill")
    ana = Survivor("Ana")
    game.add_survivor(bill)
    game.add_survivor(ana)
    assert game.level is Level.BLUE
    for _ in range(7):
        bill.kill_zombie()
    assert game.level is Level.YELLOW


def test_game_level_ignores_dead_survivors() -> None:
    """Test 25: A dead survivor's level no longer counts"""
    from zombie_survivor import Game, Level, Survivor

    game = Game(clock=_clock)
    bill = Survivor("Bill")
    ana = Survivor("Ana")
    game.add_survivor(bill)
    game.add_survivor(ana)
    for _ in range(7):
        bill.kill_zombie()
    bill.wound()
    bill.wound()
    assert game.level is Level.BLUE


def test_history_records_survivor_events() -> None:
    """Test 26: Joining, equipment, wounds, and death appear in the history"""
    from zombie_survivor import Game, Survivor

    game = Game(clock=_clock)
    bill = Survivor("Bill")
    game.add_survivor(bill)
    bill.pick_up("Baseball bat")
    bill.wound()
    bill.wound()
    assert game.history == (
        "Game started at 2026-01-01T12:00:00",
        "Bill joined the game",
        "Bill acquired Baseball bat",
        "Bill was wounded",
        "Bill was wounded",
        "Bill died",
        "The game has ended: all survivors died",
    )


def test_history_records_level_ups_and_game_level_changes() -> None:
    """Test 27: Survivor level-ups and game level changes are logged"""
    from zombie_survivor import Game, Survivor

    game = Game(clock=_clock)
    bill = Survivor("Bill")
    game.add_survivor(bill)
    for _ in range(7):
        bill.kill_zombie()
    assert "Bill advanced to Yellow" in game.history
    assert "Game level changed to Yellow" in game.history


def test_history_records_the_game_end_once() -> None:
    """Test 28: The end of the game is logged exactly once"""
    from zombie_survivor import Game, Survivor

    game = Game(clock=_clock)
    bill = Survivor("Bill")
    game.add_survivor(bill)
    for _ in range(4):
        bill.wound()
    end_events = [
        event
        for event in game.history
        if event == "The game has ended: all survivors died"
    ]
    assert end_events == ["The game has ended: all survivors died"]


def test_no_skills_before_reaching_yellow() -> None:
    """Test 29: Below seven experience no skill slot has opened"""
    from zombie_survivor import Survivor

    survivor = Survivor("Bill")
    for _ in range(6):
        survivor.kill_zombie()
    assert survivor.skills == ()
    assert survivor.actions == 3


def test_pick_up_announces_an_acquired_event() -> None:
    """Test 30: Picking up equipment announces an 'acquired' event"""
    from zombie_survivor import Survivor

    survivor = Survivor("Ana")
    events: list[tuple[str, str]] = []
    survivor.add_listener(lambda kind, message: events.append((kind, message)))
    survivor.pick_up("Baseball bat")
    assert events == [("acquired", "Ana acquired Baseball bat")]


def test_wound_announces_a_wounded_event() -> None:
    """Test 31: A wound announces a 'wounded' event"""
    from zombie_survivor import Survivor

    survivor = Survivor("Bill")
    events: list[tuple[str, str]] = []
    survivor.add_listener(lambda kind, message: events.append((kind, message)))
    survivor.wound()
    assert events == [("wounded", "Bill was wounded")]


def test_reaching_yellow_announces_a_level_up_event() -> None:
    """Test 32: Reaching Yellow announces a 'level-up' event"""
    from zombie_survivor import Survivor

    survivor = Survivor("Bill")
    events: list[tuple[str, str]] = []
    survivor.add_listener(lambda kind, message: events.append((kind, message)))
    for _ in range(7):
        survivor.kill_zombie()
    assert ("level-up", "Bill advanced to Yellow") in events


def test_kill_within_a_level_announces_no_level_up() -> None:
    """Test 33: A kill that does not change the level announces nothing"""
    from zombie_survivor import Survivor

    survivor = Survivor("Bill")
    events: list[tuple[str, str]] = []
    survivor.add_listener(lambda kind, message: events.append((kind, message)))
    survivor.kill_zombie()
    assert events == []


def test_adding_a_dead_survivor_can_end_the_game() -> None:
    """Test 34: A game whose only survivor joined dead records its end"""
    from zombie_survivor import Game, Survivor

    game = Game(clock=_clock)
    bill = Survivor("Bill")
    bill.wound()
    bill.wound()
    game.add_survivor(bill)
    assert game.has_ended
    assert game.history[-1] == "The game has ended: all survivors died"


def test_game_end_is_not_repeated_for_later_dead_joiners() -> None:
    """Test 35: A dead survivor joining an ended game does not repeat the end"""
    from zombie_survivor import Game, Survivor

    game = Game(clock=_clock)
    bill = Survivor("Bill")
    game.add_survivor(bill)
    bill.wound()
    bill.wound()
    ana = Survivor("Ana")
    ana.wound()
    ana.wound()
    game.add_survivor(ana)
    end_events = [
        event
        for event in game.history
        if event == "The game has ended: all survivors died"
    ]
    assert end_events == ["The game has ended: all survivors died"]


def test_game_level_change_is_logged_once_per_change() -> None:
    """Test 36: Later events do not repeat an old game level change"""
    from zombie_survivor import Game, Survivor

    game = Game(clock=_clock)
    bill = Survivor("Bill")
    game.add_survivor(bill)
    for _ in range(7):
        bill.kill_zombie()
    bill.pick_up("Baseball bat")
    changes = [
        event for event in game.history if event == "Game level changed to Yellow"
    ]
    assert changes == ["Game level changed to Yellow"]
