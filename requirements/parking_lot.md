# Parking lot with tiered spots and hourly billing

## Overview
A parking lot offers three sizes of spot — motorcycle, compact, and large — and admits
three kinds of vehicle: motorcycles, cars, and buses. The lot is configured with a spot
count per spot type and an hourly rate per vehicle type. Vehicles check in at an entry
time and receive a ticket; on checkout at an exit time they receive a receipt billed in
whole hours at their vehicle type's rate. The lot reports occupancy per spot type at any
time.

## User Stories

### US-1: Configuring the lot
As a lot operator, I want to declare the spot inventory and hourly rates up front and have bad configurations refused, so that the lot can never open in an inconsistent state.

- AC-1.1: The lot is configured with a number of spots per spot type and an hourly rate
  per vehicle type.
- AC-1.2: A negative spot count is refused with a message naming the spot type and the
  offending count; for -1 compact spots the message is exactly
  "spot count for [compact] must be non-negative, got [-1]".
- AC-1.3: A lot with no spots at all is refused with the message exactly
  "parking lot must have at least one spot".
- AC-1.4: Every vehicle type must have a positive hourly rate: a missing rate is refused
  with a message such as "missing hourly rate for [bus]", and a non-positive rate with a
  message such as "hourly rate for [car] must be positive, got [0.0]".

### US-2: Assigning spots on arrival
As a driver, I want to be assigned the smallest suitable free spot for my vehicle, so that space is used efficiently and unsuitable spots are never given out.

- AC-2.1: A motorcycle takes a motorcycle spot when one is free, otherwise a compact
  spot, otherwise a large spot.
- AC-2.2: A car takes a compact spot when one is free, otherwise a large spot; a car
  never takes a motorcycle spot, and when only motorcycle spots remain the car is turned
  away with the message exactly "no available spot for [car]".
- AC-2.3: A bus parks only in a large spot; when no large spot is free it is turned away
  with the message exactly "no available spot for [bus]".
- AC-2.4: When every suitable spot is taken, checking in fails, and a lot whose every
  spot is occupied reports itself full.
- AC-2.5: A successful check-in issues a ticket recording the vehicle's identifier and
  the assigned spot type, and the vehicle is from then on reported as parked.
- AC-2.6: A vehicle that is already parked cannot check in again; the attempt fails with
  a message naming the vehicle, such as "vehicle [C-1] is already parked".

### US-3: Checking out
As a driver, I want checking out to free my spot and be safely refused for vehicles that are not in the lot, so that occupancy stays accurate.

- AC-3.1: After checkout the vehicle is no longer reported as parked and its spot can be
  assigned to the next arrival.
- AC-3.2: Checking out a vehicle that is not parked fails with a message naming it, such
  as "vehicle [ghost] is not parked".
- AC-3.3: Several vehicles of the same type occupy distinct spots and check out
  independently of one another.

### US-4: Billing the stay
As a lot operator, I want stays billed in whole hours at the vehicle type's rate, so that fees are predictable and every stay pays at least something.

- AC-4.1: The minimum charge is one hour; a zero-length stay and a ten-minute stay each
  bill as 1 hour.
- AC-4.2: Partial hours round up; a 90-minute stay bills as 2 hours, and even one second
  past a whole hour bills the next hour.
- AC-4.3: Stays lasting an exact number of hours are not rounded up; exactly 3 hours
  bills as 3 hours.
- AC-4.4: The fee is the billed hours multiplied by the hourly rate configured for the
  vehicle's type; with rates of 1.0 per hour for motorcycles, 2.0 for cars, and 5.0 for
  buses, a two-hour stay costs 2.0, 4.0, and 10.0 respectively.
- AC-4.5: An exit time earlier than the entry time is refused with a message showing
  both times, such as "exit_time [999.0] is before entry_time [1000.0]".
- AC-4.6: The checkout receipt records the vehicle identifier, vehicle type, spot type,
  entry time, exit time, billed hours, and fee.

### US-5: Reporting occupancy
As a lot operator, I want a live breakdown of capacity and availability, so that I can see how full the lot is at a glance.

- AC-5.1: The lot reports, for each spot type, its capacity, the number of occupied
  spots, and the number of available spots.
- AC-5.2: The available count for a spot type decreases when a vehicle checks in and
  increases when it checks out.

## Traceability
```json
{
  "test_motorcycle_parks_in_a_motorcycle_spot_first": ["AC-2.1", "AC-2.5"],
  "test_motorcycle_overflows_to_compact_then_large": ["AC-2.1"],
  "test_car_parks_in_compact_then_overflows_to_large": ["AC-2.2"],
  "test_car_never_takes_a_motorcycle_spot": ["AC-2.2"],
  "test_bus_requires_a_large_spot": ["AC-2.3"],
  "test_bus_is_rejected_when_no_large_spot_is_free": ["AC-2.3"],
  "test_parking_fails_when_the_lot_is_full": ["AC-2.4"],
  "test_same_vehicle_cannot_park_twice": ["AC-2.6"],
  "test_unparking_frees_the_spot_for_reuse": ["AC-3.1"],
  "test_unparking_an_unknown_vehicle_is_rejected": ["AC-3.2"],
  "test_minimum_charge_is_one_hour": ["AC-4.1"],
  "test_partial_hours_are_rounded_up": ["AC-4.2"],
  "test_one_second_past_the_hour_bills_the_next_hour": ["AC-4.2"],
  "test_exact_hours_are_not_rounded_up": ["AC-4.3"],
  "test_fee_uses_the_rate_for_the_vehicle_type": ["AC-4.4"],
  "test_exit_before_entry_is_rejected": ["AC-4.5"],
  "test_receipt_records_the_full_stay": ["AC-4.6"],
  "test_status_reports_capacity_occupancy_and_availability": ["AC-5.1"],
  "test_available_spots_tracks_parking_and_unparking": ["AC-5.2"],
  "test_multiple_vehicles_of_the_same_type_park_independently": ["AC-3.3"],
  "test_negative_spot_count_is_an_invalid_configuration": ["AC-1.2"],
  "test_lot_with_no_spots_is_an_invalid_configuration": ["AC-1.3"],
  "test_missing_or_non_positive_rate_is_an_invalid_configuration": ["AC-1.4"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
