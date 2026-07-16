# Zombie survival game tracker

## Overview
A tabletop zombie-survival game needs a tracker for its survivors and the game around
them. Survivors take wounds and die, carry a limited load of equipment, earn
experience for zombie kills, climb through the levels Blue, Yellow, Orange, and Red,
and unlock skills along the way. The game keeps a roster of uniquely named survivors,
tracks its own level from its most experienced living survivor, decides when the game
is over, and writes a running history of everything notable that happens.

## User Stories

### US-1: Track a survivor's wounds and life
As a game master, I want each survivor's wounds and life state tracked, so that damage and death are applied by the rules and never miscounted.

- AC-1.1: A newly created survivor has a name, no wounds, is alive, can take three actions per turn, carries nothing, has zero experience, and is at level Blue.
- AC-1.2: One wound leaves a survivor alive; the second wound kills them.
- AC-1.3: Wounds inflicted past death are ignored — the count never rises beyond two.

### US-2: Manage a survivor's equipment load
As a game master, I want equipment pick-ups to follow the carrying rules, so that hand and reserve slots are filled and shed exactly as the game dictates.

- AC-2.1: Picked-up equipment fills the two "in hand" slots first; later pieces go "in reserve" in pick-up order.
- AC-2.2: An unwounded survivor can carry at most five pieces; a further pick-up is refused with an error whose message reads "<name> cannot carry any more equipment".
- AC-2.3: Each wound reduces carrying capacity by one, and the most recently acquired reserve piece is discarded to fit the smaller capacity.
- AC-2.4: A dead survivor cannot pick up equipment; the attempt is refused with an error whose message reads "<name> is dead".

### US-3: Earn experience and level up
As a player, I want kills to raise my survivor's experience and level, so that progress follows the published thresholds.

- AC-3.1: Each zombie killed earns the survivor one experience point.
- AC-3.2: A survivor's level follows their experience: Blue from 0 through 6, Yellow from 7 through 18, Orange from 19 through 42, and Red from 43 on.

### US-4: Unlock and choose skills
As a player, I want skills unlocked as my survivor levels, so that advancement grants the abilities the game promises.

- AC-4.1: Below Yellow a survivor has no skills and still has three actions; on reaching Yellow the skill "+1 Action" is granted automatically — no choice involved — raising the survivor's actions to four.
- AC-4.2: Below Orange there is no skill choice: the offered options are empty, and attempting a choice is refused with an error whose message reads "<name> has no skill choice available".
- AC-4.3: Reaching Orange opens a choice between exactly two skills, Hoard and Sniper, in that order.
- AC-4.4: Choosing Hoard raises carrying capacity by one, letting the survivor hold a sixth piece (two in hand, four in reserve).
- AC-4.5: Only a currently offered skill may be chosen; anything else is refused with an error whose message reads "'<skill>' is not an available skill choice".
- AC-4.6: Reaching Red opens a choice among the three skills Hoard, Sniper, and Tough, minus any already held (holding Sniper leaves Hoard and Tough); the chosen skill is added to the survivor's skills.
- AC-4.7: Past Red the progression restarts, so a second automatic "+1 Action" arrives at 50 experience, giving the survivor five actions.

### US-5: Run the game roster, level, and end condition
As a game master, I want the game to manage its survivors and know when it is over, so that play state never has to be reconstructed by hand.

- AC-5.1: A new game has no survivors and, using the clock it was given, records its start in the history as "Game started at <start timestamp>" (timestamp in ISO form, such as 2026-01-01T12:00:00).
- AC-5.2: Survivors may join the game at any time and are listed in joining order.
- AC-5.3: Survivor names are unique within a game; a duplicate is refused with an error whose message reads "A survivor named '<name>' already exists".
- AC-5.4: The game ends only when every survivor is dead; a game with no survivors has not ended, and a single living survivor keeps it going.
- AC-5.5: A survivor who joins already dead can thereby end the game, but a dead joiner arriving after the game has ended does not record the ending again.
- AC-5.6: The game's level is the highest level among its living survivors, starting at Blue.
- AC-5.7: Dead survivors' levels do not count toward the game level.

### US-6: Keep a history and announce survivor events
As a game master, I want a chronological history and live event announcements, so that everything notable is recorded and other parts of the game can react as it happens.

- AC-6.1: The game history records, in order after the start entry: joins as "<name> joined the game", pick-ups as "<name> acquired <item>", each wound as "<name> was wounded", and death as "<name> died".
- AC-6.2: The end of the game is recorded exactly once, as "The game has ended: all survivors died".
- AC-6.3: A survivor reaching a new level is recorded as "<name> advanced to <level>", and a change of the game's level as "Game level changed to <level>"; each game-level change is recorded once, and later events do not repeat it.
- AC-6.4: A survivor announces events to registered listeners as a kind plus a message: picking up equipment announces "acquired" with "<name> acquired <item>", a wound announces "wounded" with "<name> was wounded", and reaching a new level announces "level-up" with "<name> advanced to <level>".
- AC-6.5: A kill that does not change the survivor's level announces nothing.

## Traceability
```json
{
  "test_new_survivor_defaults": ["AC-1.1"],
  "test_one_wound_leaves_survivor_alive": ["AC-1.2"],
  "test_second_wound_kills": ["AC-1.2"],
  "test_wounds_beyond_death_are_ignored": ["AC-1.3"],
  "test_first_two_pieces_go_in_hand_then_reserve": ["AC-2.1"],
  "test_unwounded_survivor_carries_at_most_five_pieces": ["AC-2.2"],
  "test_wound_discards_most_recent_reserve_piece": ["AC-2.3"],
  "test_wounded_survivor_capacity_is_four": ["AC-2.3"],
  "test_dead_survivor_cannot_pick_up_equipment": ["AC-2.4"],
  "test_killing_a_zombie_earns_one_experience_point": ["AC-3.1"],
  "test_level_thresholds": ["AC-3.2"],
  "test_yellow_grants_plus_one_action_automatically": ["AC-4.1"],
  "test_no_skill_choice_before_orange": ["AC-4.2"],
  "test_orange_offers_a_choice_of_two_skills": ["AC-4.3"],
  "test_hoard_raises_equipment_capacity": ["AC-4.4"],
  "test_choosing_an_unavailable_skill_is_rejected": ["AC-4.5"],
  "test_red_choice_excludes_already_unlocked_skills": ["AC-4.6"],
  "test_skill_tree_restarts_after_red": ["AC-4.7"],
  "test_game_begins_with_zero_survivors_and_a_timestamped_start": ["AC-5.1"],
  "test_survivors_can_be_added_at_any_time": ["AC-5.2"],
  "test_survivor_names_must_be_unique_within_a_game": ["AC-5.3"],
  "test_game_ends_only_when_all_survivors_are_dead": ["AC-5.4"],
  "test_game_without_survivors_has_not_ended": ["AC-5.4"],
  "test_game_level_is_highest_among_living_survivors": ["AC-5.6"],
  "test_game_level_ignores_dead_survivors": ["AC-5.7"],
  "test_history_records_survivor_events": ["AC-6.1", "AC-6.2"],
  "test_history_records_level_ups_and_game_level_changes": ["AC-6.3"],
  "test_history_records_the_game_end_once": ["AC-6.2"],
  "test_no_skills_before_reaching_yellow": ["AC-4.1"],
  "test_pick_up_announces_an_acquired_event": ["AC-6.4"],
  "test_wound_announces_a_wounded_event": ["AC-6.4"],
  "test_reaching_yellow_announces_a_level_up_event": ["AC-6.4"],
  "test_kill_within_a_level_announces_no_level_up": ["AC-6.5"],
  "test_adding_a_dead_survivor_can_end_the_game": ["AC-5.5"],
  "test_game_end_is_not_repeated_for_later_dead_joiners": ["AC-5.5"],
  "test_game_level_change_is_logged_once_per_change": ["AC-6.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
