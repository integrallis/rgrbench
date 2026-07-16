# Gilded Rose inventory aging

## Overview
A small shop's inventory ages once per day. Every item carries a name, the number of days
remaining to sell it, and a quality value. A single daily update adjusts every item in the
inventory: the days remaining tick down and the quality changes according to the item's
category. Ordinary goods lose value, "Aged Brie" gains value, backstage passes surge and
then crash, "Conjured" goods decay doubly fast, and the legendary "Sulfuras" never changes.
Quality of non-legendary goods is always kept between 0 and 50.

## User Stories

### US-1: Age regular items
As a shopkeeper, I want ordinary goods to lose value day by day, so that stale stock is priced honestly.

- AC-1.1: Each daily update reduces a regular item's days remaining by 1 and its quality by 1.
- AC-1.2: Once the sell-by date has passed (no days remaining), a regular item's quality degrades twice as fast: 2 per day, indefinitely.
- AC-1.3: Quality never becomes negative, even under the doubled degradation.

### US-2: Appreciate Aged Brie
As a shopkeeper, I want "Aged Brie" to improve with age, so that its rising value is reflected.

- AC-2.1: "Aged Brie" gains 1 quality per daily update while its sell-by date has not yet passed, including on the final day before the date.
- AC-2.2: Once the sell-by date has passed, "Aged Brie" gains 2 quality per day.
- AC-2.3: Quality never exceeds 50, even under the doubled gain.

### US-3: Preserve the legendary Sulfuras
As a shopkeeper, I want "Sulfuras" exempt from aging, so that the legendary item keeps its fixed worth.

- AC-3.1: "Sulfuras" never changes: its days remaining and its quality of 80 stay exactly as they are, even past its date.

### US-4: Reprice backstage passes around the concert
As a shopkeeper, I want backstage passes to gain value as the concert nears and become worthless after it, so that their price tracks demand.

- AC-4.1: With more than 10 days remaining, a backstage pass gains 1 quality per day.
- AC-4.2: With 10 down to 6 days remaining, a backstage pass gains 2 quality per day.
- AC-4.3: With 5 down to 1 days remaining, a backstage pass gains 3 quality per day.
- AC-4.4: Once the concert date has passed (no days remaining), the pass's quality drops to 0 and stays there.
- AC-4.5: A pass's quality never exceeds 50, even under the steepest gain.

### US-5: Decay Conjured items doubly fast
As a shopkeeper, I want "Conjured" goods to decay twice as fast as regular goods, so that their magical shelf life is honored.

- AC-5.1: A "Conjured" item loses 2 quality per daily update before its sell-by date.
- AC-5.2: Once the sell-by date has passed, a "Conjured" item loses 4 quality per day.
- AC-5.3: Quality never becomes negative, even under the quadrupled loss.

### US-6: Update the whole inventory at once
As a shopkeeper, I want one daily update to age every item, so that the whole inventory stays current.

- AC-6.1: A single daily update processes every item in the inventory, each by its own category's rules, independently of the others.
- AC-6.2: An item records its name, its days remaining to sell, and its quality, exactly as supplied.

## Traceability
```json
{
  "test_regular_item_loses_one_quality_and_one_sell_in_per_day": ["AC-1.1"],
  "test_regular_item_degrades_twice_as_fast_after_sell_by_date": ["AC-1.2"],
  "test_regular_item_keeps_degrading_double_when_long_expired": ["AC-1.2"],
  "test_regular_item_quality_never_goes_negative": ["AC-1.3"],
  "test_expired_regular_item_with_quality_one_stops_at_zero": ["AC-1.3"],
  "test_aged_brie_gains_quality_as_it_ages": ["AC-2.1"],
  "test_aged_brie_gains_single_quality_on_the_last_day_before_the_date": ["AC-2.1"],
  "test_aged_brie_gains_double_quality_after_sell_by_date": ["AC-2.2"],
  "test_aged_brie_quality_is_capped_at_fifty": ["AC-2.3"],
  "test_expired_aged_brie_at_forty_nine_caps_at_fifty": ["AC-2.3"],
  "test_sulfuras_never_changes": ["AC-3.1"],
  "test_sulfuras_is_unchanged_even_past_its_date": ["AC-3.1"],
  "test_backstage_pass_gains_faster_as_concert_approaches": ["AC-4.1", "AC-4.2", "AC-4.3"],
  "test_backstage_pass_drops_to_zero_after_concert": ["AC-4.4"],
  "test_backstage_pass_stays_worthless_after_concert": ["AC-4.4"],
  "test_backstage_pass_quality_is_capped_at_fifty": ["AC-4.5"],
  "test_conjured_item_degrades_twice_as_fast_as_regular": ["AC-5.1"],
  "test_conjured_item_degrades_four_per_day_after_sell_by_date": ["AC-5.2"],
  "test_conjured_item_quality_never_goes_negative": ["AC-5.3"],
  "test_expired_conjured_item_with_quality_three_clamps_to_zero": ["AC-5.3"],
  "test_update_quality_processes_every_item_in_the_inventory": ["AC-6.1"],
  "test_regular_item_over_three_days": ["AC-1.1", "AC-1.2"],
  "test_backstage_pass_full_lifecycle_ends_at_zero": ["AC-4.2", "AC-4.3", "AC-4.4"],
  "test_item_exposes_name_sell_in_and_quality": ["AC-6.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
