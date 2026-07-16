# Equivalent-mutant register

Mutants that survive mutation testing because they produce NO observable behavior difference
through any public interface — not because the tests are weak. Each entry was verified
empirically during the 2026-07 test-strengthening campaign (exhaustive input sweeps or
randomized comparison against the unmutated source; method noted per group). These are the
oracle's *accounted-for* residue: subtract them from survivors when computing effective
oracle strength.

Provenance note: the suites were hand-written in their katas' original languages and
machine-translated to Python in 2025; the campaign that produced this register restored
assertions lost in translation (return values, exact messages, boundaries) and classified
what remained.

## odd_even_kata (3) — verified by exhaustive sweep, n ∈ [-100, 500] + range grid
- `_is_prime_number__mutmut_1` / `__mutmut_2` — boundary change affects only n=2, which the
  even-check already routes to the same output.
- `_is_prime_number__mutmut_5` — primality of even numbers is masked by the caller, which
  prints "Even" before consulting primality.

## tennis_game (10) — verified by exhaustive sweep over score states 0–12 × 0–12
- `Scoresǁscore_name__mutmut_2` — duplicate-dict-key mutant; dropped key masked by `.get`
  default.
- `score_name__mutmut_11/_13/_14` — default-value changes observable only for point counts
  the kata never produces (post-win queries).
- `Setǁfirst_score__mutmut_2/_3/_8`, `second_score__mutmut_4/_5/_8` — boundary/comparator
  changes on branches shadowed by earlier guards; both paths emit identical score names.

## darts (4) — reasoned + per-mutant execution
- `__init____mutmut_3/_4` — dead store: `_last_turn_score` initial value overwritten before
  any possible read (a bust is unreachable in turn 1: three darts from 301 cannot reach 1).
- `dart__mutmut_14/_15` — boundary rewrites of `new_score < 0` (`<= 0`, `< 1`) absorbed by
  the explicit `== 0` and `== 1` disjuncts of the double-out bust rule; the guarded set
  {negative, 0, 1} is identical. (The former spec-conflict entries `dart__mutmut_18/_19`
  were resolved by the D-13 reference fix — the bust-on-zero rule is now implemented and
  test-pinned.)

## find_min / find_max (2) — verified exhaustively: 19,600 (args, low, high) combinations
- `get_min_bounded__mutmut_3`, `get_max_bounded__mutmut_2` — half-open-interval mutants
  whose excluded endpoint coincides with the empty-set fallback value in every affected
  case.

## bowling_game (1), recently_used_list (1), mine_fields (2) — reasoned + per-mutant execution
- `Gameǁ__init____mutmut_4` — rolls buffer 21→22: reachable only via an illegal 22nd roll,
  undefined by the kata.
- `RecentlyUsedListǁadd__mutmut_19` — trim on `>` vs `>=`: at the boundary the trim is a
  no-op slice of the whole list.
- `MineFieldsǁ__init____mutmut_1` — `[]` vs `None` initial grid: `create()` unconditionally
  reassigns; differs only in exception type for use-before-create, unspecified.
- `mine__mutmut_17/_18` — neighbor-offset sign flips visit the same symmetric 8-cell
  neighborhood.

## natural_string_sorting (2) — verified: 60,000 randomized sort calls, zero diffs
- `sort_string__mutmut_2` — `order=None` still routes to the ascending branch.
- `sort_string__mutmut_22` — uniform retagging of string parts preserves all pairwise
  orderings.

## tetris (20) — reasoned + per-mutant execution in a sandbox copy
- `Boardǁ__init____mutmut_8/_9/_10/_11` — dead stores: initial falling row/col overwritten
  by `drop()` before any observable read.
- `__str____mutmut_10`, `_can_piece_move_to__mutmut_11`, `_land_piece__mutmut_10`,
  `Pieceǁrotate_right__mutmut_2`, `rotate_left__mutmut_2` — `split(None)` ≡ `split("\n")`
  for valid whitespace-free shape strings.
- `_can_piece_move_to__mutmut_1/_3/_7/_8/_9`, `_land_piece__mutmut_1/_3/_7/_8` —
  Block-vs-Piece guard branches unreachable from the public API (every call site passes a
  falling Piece).
- `Pieceǁrotate_right__mutmut_8`, `rotate_left__mutmut_8` — rotation assigns every cell of
  the size×size grid (bijective index map); the filler value never appears in output.

**Legacy-corpus total: 46** (post-reference-fix landscape: the D-12/D-13 fixes removed the
leap_year and calculator entries and replaced the darts spec-conflict pair with two boundary
equivalents; word_wrap's rewrite produced four new killable survivors, all killed).
---

# tddbuddy-ingestion packages (2026-07 campaign: 314 survivors → 268 killed, entries below)

All entries verified by the same protocol: reasoning + empirical differential comparison
(mutmut-trampoline dispatch confirmed; exhaustive sweeps or randomized trace fuzzing with
positive-control mutants validating each harness).

## hundred_doors (1)
- `final_door_states__mutmut_15` — extra pass iterates an empty range (step = count+1);
  exhaustive counts 0–400, all public functions identical.

## anagram_detector (2)
- `group_anagrams__mutmut_4`, `_normalise__mutmut_2` — separator variants of the grouping
  key are injective over casefolded alnum characters (uppercase "X" cannot occur), so the
  partition and all comparisons are preserved; 4,000 randomized trials each, 0 diffs.

## mars_rover (2)
- `__init____mutmut_2` — default direction normalized by `.upper()` before any use.
- `_turn__mutmut_3` — `rindex ≡ index` on a 4-unique-char heading string.
  Both: exhaustive 1,449-scenario trace diff, positive control confirmed.

## shopping_cart (1)
- `add_item__mutmut_35` — `_LineItem.name` is write-only (lookups use the dict key); 3,000
  randomized differential trials, 0 diffs.

## supermarket_pricing (1)
- `total__mutmut_15` — `sum(lines, )` int-0 start added into an always-Decimal total is
  exact; 3,000 trials comparing value, type, and str, 0 diffs.

## zombie_survivor (13)
- `Gameǁ__init____mutmut_3` — `_end_recorded` only read as a truthiness (`None ≡ False`).
- `Levelǁfor_experience__mutmut_1` — differs only for negative experience, outside the
  domain (kill counts start at 0 and only increment).
- 11 slot-state sentinels (`_skill_slots__mutmut_17/_26`, `choose_skill__mutmut_7/_8/_9`,
  `_open_reached_slots__mutmut_8/_9/_10/_13/_14/_15`) — slot state is only compared to
  "locked"/"pending", so None/"DONE"/"XXdoneXX" all behave as "done". Verified: 60 seeded
  scenarios, 12,337 observation records, probe-confirmed coverage of every mutated branch.
  (Hardening note: enum-typed slot states would eliminate this family.)

## timesheet_calculator (2)
- `_parse_time__mutmut_8/_10` — error-path convergence: partition/rpartition and and/or
  variants reroute only inputs that every route rejects with the identical message;
  155,489 exhaustive+randomized inputs, 0 diffs.

## memory_cache (1)
- `put__mutmut_7` — `OrderedDict.popitem(last=None)` interprets `last` by truthiness;
  500 randomized 80-op traces identical.

## game_of_life (4)
- `live_neighbours__mutmut_2/_3`, `next_generation__mutmut_3/_4` — the 8-offset
  neighborhood is closed under sign negation of either axis; 300 random grids, identical
  generations. (Same family as mine_fields.)

## circuit_breaker (2)
- `__init____mutmut_9/_10` — initial `_opened_at` is dead: OPEN is entered solely via
  `_trip_open`, which assigns it first; 2,000 randomized 15-step scenarios identical.

## social_network (2)
- `__init____mutmut_6`, `_new_post__mutmut_3` — the internal sequence tiebreaker is never
  exposed; +1 offset and ×2 stride are strictly monotone relabelings; 500 randomized
  30-op scripts identical, positive control confirmed.

## library_management (6)
- `register_member__mutmut_1` — member name stored but never read (membership-only dict).
- `checkout__mutmut_19/_20`, `_release__mutmut_16/_17` — `held_for`/`hold_expires` are
  dead stores outside RESERVED status (every transition rewrites them; reads are guarded
  by `status == RESERVED`).
- `return_copy__mutmut_7` — invariant "loan exists iff CHECKED_OUT" collapses `or` ≡ `and`.
  All: 400-sequence randomized differential fuzz, 0 divergences.

## bank_ocr (3)
- `fix_entry__mutmut_4/_17` — "XX?XX" cannot occur in 9-char digit/'?' strings; the guard
  reduces to `checksum_valid`, which rejects '?' anyway.
- `fix_entry__mutmut_5` — a checksum-valid readable number has no checksum-valid one-digit
  variant: (d'−d)·w ≢ 0 (mod 11) for weights 1..9 and 11 prime.
  All: 12,012-entry empirical comparison, 0 diffs.

## linked_list (1)
- `insert_at__mutmut_1` — disabled range guard: every out-of-range index reaches
  `_node_at(index-1)`, which raises the identical IndexError before any state change;
  exhaustive sizes 0–5 × indices −4..size+4.

## poker_hands (1)
- `compare_hands__mutmut_9` — `>` vs `>=` behind an equality early-return; operands are
  never equal; 40,000 randomized hand pairs, 0 diffs.

## clam_card (2)
- `_station_zone__mutmut_2/_3` — Zone-A return value is consumed only by `"B" in zones`
  membership tests, so any non-"B" value is indistinguishable; exhaustive 121 station
  pairs + 200 randomized cap sequences.

## parking_lot (1)
- `__init____mutmut_6` — validation-loop default only feeds the `count < 0` check;
  capacity is rebuilt separately; exhaustive 64 configurations.

# Harness artifacts (measured limitations of mutmut, NOT test gaps)

## Instrument limitation: decorated members and module-level data are not mutated
mutmut's trampoline wraps plain functions and methods; it skips `@property` members of
dataclasses and never mutates module-level constants (lookup tables, enum values). Two
ingested packages originally had ALL their logic in those forms — `rock_paper_scissors`
(pure table lookup) and `video_club_rental` (properties on frozen dataclasses) — making
their oracles invisible to measurement (zero mutants generated). Both were restructured
(2026-07) so the logic lives in module-level pure functions that thin properties/wrappers
delegate to: public APIs and tests unchanged, logic now measurable. The structure gate
(`test_every_kata_has_mutation_score`) is what caught this; packages with zero generated
mutants fail it by design.

## kata_potter (1)
- `_normalize__mutmut_6` — killed by the existing suite in a cold process (15 failures),
  but survives mutmut because the module-level `@lru_cache` on `_min_cost_cents` is warmed
  by the baseline pass with the unmutated function and is not trampolined. Demonstrated
  both ways (cold vs warm cache under the mutant). A cache-clearing test would test
  internals, so none was added.

**Grand total: 46 legacy + 45 ingestion equivalents + 1 harness artifact = 92 accounted
survivors.**
