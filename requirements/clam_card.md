# Transit fare card with daily, weekly and monthly capping

## Overview
A pay-as-you-go transit card charges each journey by the zones it touches and trims charges so a traveller never pays more than fixed caps per day, per ISO week, and per calendar month. Journeys wholly within Zone A cost 2.50; any journey touching Zone B costs 3.00. The caps are 7.00 per day, 40.00 per ISO week and 145.00 per calendar month for Zone A travel, rising to 8.00, 47.00 and 165.00 once Zone B is involved. The card keeps a running total of everything charged, and journeys involving stations not on the network are rejected. Each journey is made on an explicitly supplied date.

## User Stories

### US-1: Zone-based journey fares
As a traveller, I want each journey charged according to the zones it touches, so that fares reflect where I travel.

- AC-1.1: A journey wholly within Zone A is charged 2.50.
- AC-1.2: A journey touching Zone B at either end — including journeys wholly within Zone B — is charged the Zone B price of 3.00.
- AC-1.3: The network's Zone A stations include Aldgate, Amersham, Anerley, Angel and Asterisk; its Zone B stations include Balham, Barbican, Bison, Bugel and Bullhead.
- AC-1.4: Each journey reports the amount it charged.

### US-2: Daily fare capping
As a traveller, I want my charges capped each day, so that a day of heavy travel never costs more than a day ticket.

- AC-2.1: Zone A travel is capped at 7.00 per day: journeys are charged in full until the remainder to the cap is smaller than the fare, then only the remainder, then nothing — four Zone A journeys in one day charge 2.50, 2.50, 2.00, 0.00.
- AC-2.2: Days including Zone B travel cap at 8.00 — four Zone B journeys in one day charge 3.00, 3.00, 2.00, 0.00.
- AC-2.3: The daily cap covers a single calendar day; the next day's first journey is charged the full single fare again.
- AC-2.4: On a day already capped at the Zone A limit, a Zone B journey lifts the day's cap to the Zone B limit and charges only the 1.00 difference.

### US-3: Weekly and monthly fare capping
As a frequent traveller, I want longer-period caps layered on the daily cap, so that commuting costs never exceed the price of a season ticket.

- AC-3.1: Zone A travel is capped at 40.00 per ISO week, applied on top of the daily caps: three Zone A journeys a day for six days reach the daily cap five times and stop at 40.00 for the week.
- AC-3.2: The weekly cap covers one ISO week; a journey on the following Monday is charged the full single fare again.
- AC-3.3: Zone A travel is capped at 145.00 per calendar month, applied on top of the daily and weekly caps: three Zone A journeys every day of a month accumulate to exactly 145.00.

### US-4: Unknown stations
As a traveller, I want journeys involving stations that are not on the network refused, so that I am never charged for an impossible trip.

- AC-4.1: A journey from or to a station not on the network is rejected with an unknown-station error naming the offending station.
- AC-4.2: A rejected journey charges nothing; the card's running total is unchanged.

### US-5: Running total
As a traveller, I want the card to report everything it has charged me, so that I can check my spending.

- AC-5.1: The card reports the accumulated total of every charge made, across days and zones.

## Traceability
```json
{
  "test_single_zone_a_journey_costs_2_50": ["AC-1.1", "AC-1.3", "AC-1.4"],
  "test_journey_touching_zone_b_costs_3_00": ["AC-1.2", "AC-1.3", "AC-1.4"],
  "test_zone_b_origin_also_charges_zone_b_price": ["AC-1.2", "AC-1.4"],
  "test_journey_entirely_within_zone_b_costs_3_00": ["AC-1.2", "AC-1.4"],
  "test_two_journeys_in_a_day_sum_their_fares": ["AC-1.1", "AC-1.2", "AC-5.1"],
  "test_zone_a_journeys_cap_at_7_00_per_day": ["AC-2.1"],
  "test_zone_b_journeys_cap_at_8_00_per_day": ["AC-2.2"],
  "test_day_cap_resets_on_the_next_day": ["AC-2.3"],
  "test_zone_b_journey_raises_a_capped_day_to_the_zone_b_cap": ["AC-2.4"],
  "test_unknown_origin_station_raises": ["AC-4.1"],
  "test_unknown_destination_station_raises": ["AC-4.1"],
  "test_failed_journey_charges_nothing": ["AC-4.2"],
  "test_zone_a_journeys_cap_at_40_00_per_week": ["AC-3.1"],
  "test_week_cap_resets_in_the_next_iso_week": ["AC-3.2"],
  "test_zone_a_journeys_cap_at_145_00_per_month": ["AC-3.3"],
  "test_total_charged_accumulates_across_days": ["AC-5.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
