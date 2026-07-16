# Ten-pin bowling scoring

## Overview
A scorekeeper for a game of ten-pin bowling. The game records how many pins fall on each roll and computes the total score under the standard rules: a game has ten frames; knocking all ten pins down in two rolls of a frame is a spare and earns the next roll as a bonus; knocking all ten down on the first roll is a strike and earns the next two rolls as a bonus; a perfect game of strikes scores 300.

## User Stories

### US-1: Score rolls with no bonuses
As a bowler, I want my knocked-down pins tallied, so that I can see my score at any point in the game.

- AC-1.1: A roll that knocks down no pins adds nothing; the score is available after any number of rolls, and a game of nothing but missed rolls scores 0.

### US-2: Spare bonus
As a bowler, I want a spare to earn the next roll as a bonus, so that clearing the frame in two rolls is rewarded.

- AC-2.1: A spare adds the value of the next roll to that frame (worked example: a spare of 5 and 5 followed by a 3, with every remaining roll a miss, totals 16).
- AC-2.2: The spare bonus applies equally when the spare comes after an open frame (worked example: an open frame of 1 and 2, then a spare of 5 and 5 followed by a 3, with every remaining roll a miss, totals 19).

### US-3: Strike bonus
As a bowler, I want a strike to earn the next two rolls as a bonus, so that clearing the frame in one roll is rewarded most.

- AC-3.1: A strike adds the value of the next two rolls to that frame (worked example: a strike followed by 3 and 4, with every remaining roll a miss, totals 24).
- AC-3.2: The strike bonus applies equally when the strike comes after an open frame (worked example: an open frame of 1 and 2, then a strike followed by 3 and 4, with every remaining roll a miss, totals 27).
- AC-3.3: A perfect game — twelve consecutive strikes, including the two bonus rolls of the final frame — scores 300.

## Traceability
```json
{
  "test_can_get_calculate_single_scores": ["AC-1.1"],
  "test_can_get_calculate_scores": ["AC-1.1"],
  "test_can_get_calculate_spare_scores": ["AC-2.1"],
  "test_can_get_calculate_strike_scores": ["AC-3.1"],
  "test_can_get_calculate_full_game_scores": ["AC-3.3"],
  "test_can_get_calculate_strike_in_second_frame_scores": ["AC-3.2"],
  "test_can_get_calculate_spare_in_second_frame_scores": ["AC-2.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
