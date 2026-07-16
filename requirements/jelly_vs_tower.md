# Jelly vs Tower combat

## Overview
A tower-defense skirmish. Towers, each with a color (Blue, Red, or the dual-color BlueRed)
and a level from 1 to 4, attack a wave of jellies, each with a color and a health total.
Damage follows a fixed table keyed by the tower's color and level and the target's color;
where the table gives a range, the amount is rolled from an externally supplied source of
randomness so battles can be reproduced. Combat proceeds in rounds: each tower attacks the
first living jelly, dead jellies leave the battle, and a log records every attack.

## User Stories

### US-1: Look up damage from the table
As a game designer, I want damage determined by a fixed color-and-level table, so that combat balance is predictable.

- AC-1.1: A pure-color tower attacking a jelly of its own color rolls damage in a range by level — level 1: 2 to 5, level 2: 5 to 9, level 3: 9 to 12, level 4: 12 to 15.
- AC-1.2: A pure-color tower attacking the opposite pure color deals a fixed amount by level — level 1: 0, level 2: 1, level 3: 2, level 4: 3.
- AC-1.3: A dual-color tower deals the same moderate damage to both pure colors — level 1: exactly 2, level 2: 2 to 4, level 3: 4 to 6, level 4: 6 to 8.
- AC-1.4: Against a dual-color jelly, the tower applies whichever of its Blue-target and Red-target table entries is higher.
- AC-1.5: Tower levels outside 1 to 4 are rejected — both when consulting the table and when building a tower — with an error stating "tower level must be between 1 and 4, got <value>".

### US-2: Track jelly health and death
As a game designer, I want jellies to live, take damage, and die by their health total, so that combat has consequences.

- AC-2.1: A jelly is alive while its health is positive and dead once its health reaches zero.
- AC-2.2: Taking damage reduces a jelly's health by exactly that amount.
- AC-2.3: A dead jelly cannot be attacked; the attempt is rejected as an error.

### US-3: Roll attacks reproducibly
As a game designer, I want ranged damage rolled from injected randomness, so that battles are fair yet replayable.

- AC-3.1: An attack reports the damage dealt and reduces the target's health by it, and rolled damage always falls within the table's range for the matchup and level.
- AC-3.2: Fixed table entries always deal exactly their amount; a zero-damage matchup leaves the jelly untouched.
- AC-3.3: Randomness comes from an externally supplied source: the same source seeded the same way reproduces the same sequence of damage rolls.

### US-4: Fight rounds with a combat log
As a player, I want combat resolved in logged rounds, so that I can follow exactly what happened.

- AC-4.1: In a round, the towers act in order and each attacks the first living jelly in the wave.
- AC-4.2: A round yields a combat log with one entry per attack, recording which tower attacked, which jelly was hit, and how much damage was dealt.
- AC-4.3: A jelly killed during a round is attacked no further — later towers move on to the next living jelly — and it leaves the battle by the round's end.
- AC-4.4: When no living jellies remain, whether from the start of a round or partway through one, the remaining towers stand idle and contribute no log entries.
- AC-4.5: Rounds can be fought in succession until the wave is worn down; once every jelly is gone, further rounds yield an empty log.

## Traceability
```json
{
  "test_damage_table_for_same_color_towers": ["AC-1.1"],
  "test_damage_table_for_off_color_towers_is_fixed": ["AC-1.2"],
  "test_damage_table_for_bluered_towers": ["AC-1.3"],
  "test_bluered_jelly_takes_the_higher_of_both_columns": ["AC-1.4"],
  "test_damage_range_rejects_levels_outside_one_to_four": ["AC-1.5"],
  "test_tower_cannot_be_built_with_invalid_level": ["AC-1.5"],
  "test_jelly_is_alive_while_health_is_positive": ["AC-2.1"],
  "test_jelly_dies_when_health_reaches_zero": ["AC-2.1", "AC-2.2"],
  "test_attack_damage_stays_within_the_table_range": ["AC-3.1"],
  "test_fixed_damage_attack_always_deals_the_same_amount": ["AC-3.2"],
  "test_level_one_blue_tower_cannot_hurt_red_jelly": ["AC-3.2"],
  "test_attacks_with_the_same_seed_are_reproducible": ["AC-3.3"],
  "test_dead_jelly_cannot_be_attacked": ["AC-2.3"],
  "test_fight_round_logs_tower_target_and_damage": ["AC-4.2"],
  "test_each_tower_attacks_the_first_living_jelly": ["AC-4.1"],
  "test_dead_jellies_are_removed_after_the_round": ["AC-4.3"],
  "test_later_towers_move_on_when_the_target_dies_mid_round": ["AC-4.3"],
  "test_towers_do_nothing_when_no_jellies_remain": ["AC-4.4"],
  "test_round_ends_early_once_every_jelly_is_dead": ["AC-4.4"],
  "test_battle_over_multiple_rounds_wears_a_jelly_down": ["AC-4.5"],
  "test_invalid_level_error_reports_the_valid_range": ["AC-1.5"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
