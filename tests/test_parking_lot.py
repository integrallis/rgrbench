"""Tests for the Parking Lot kata.

Entry and exit times are injected as plain timestamps (seconds), and hourly
rates are injected at construction, so every fee assertion is deterministic.
"""


def _rates() -> dict:
    """Hourly rates keyed by VehicleType: motorcycle 1.0, car 2.0, bus 5.0."""
    from parking_lot import VehicleType

    return {
        VehicleType.MOTORCYCLE: 1.0,
        VehicleType.CAR: 2.0,
        VehicleType.BUS: 5.0,
    }


def test_motorcycle_parks_in_a_motorcycle_spot_first() -> None:
    """Test 1: A motorcycle takes a motorcycle spot when one is free"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot(
        {SpotType.MOTORCYCLE: 1, SpotType.COMPACT: 1, SpotType.LARGE: 1}, _rates()
    )

    ticket = lot.park("M-1", VehicleType.MOTORCYCLE, entry_time=0.0)

    assert ticket.spot_type is SpotType.MOTORCYCLE
    assert ticket.vehicle_id == "M-1"
    assert lot.is_parked("M-1") is True


def test_motorcycle_overflows_to_compact_then_large() -> None:
    """Test 2: Motorcycles fit in any spot type, preferring smaller ones"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot(
        {SpotType.MOTORCYCLE: 1, SpotType.COMPACT: 1, SpotType.LARGE: 1}, _rates()
    )

    first = lot.park("M-1", VehicleType.MOTORCYCLE, entry_time=0.0)
    second = lot.park("M-2", VehicleType.MOTORCYCLE, entry_time=0.0)
    third = lot.park("M-3", VehicleType.MOTORCYCLE, entry_time=0.0)

    assert first.spot_type is SpotType.MOTORCYCLE
    assert second.spot_type is SpotType.COMPACT
    assert third.spot_type is SpotType.LARGE


def test_car_parks_in_compact_then_overflows_to_large() -> None:
    """Test 3: Cars prefer compact spots and fall back to large ones"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot({SpotType.COMPACT: 1, SpotType.LARGE: 1}, _rates())

    first = lot.park("C-1", VehicleType.CAR, entry_time=0.0)
    second = lot.park("C-2", VehicleType.CAR, entry_time=0.0)

    assert first.spot_type is SpotType.COMPACT
    assert second.spot_type is SpotType.LARGE


def test_car_never_takes_a_motorcycle_spot() -> None:
    """Test 4: A car cannot park when only motorcycle spots remain"""
    import pytest

    from parking_lot import NoAvailableSpotError, ParkingLot, SpotType, VehicleType

    lot = ParkingLot({SpotType.MOTORCYCLE: 3}, _rates())

    with pytest.raises(NoAvailableSpotError) as excinfo:
        lot.park("C-1", VehicleType.CAR, entry_time=0.0)
    assert str(excinfo.value) == "no available spot for [car]"


def test_bus_requires_a_large_spot() -> None:
    """Test 5: A bus parks only in a large spot"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot(
        {SpotType.MOTORCYCLE: 1, SpotType.COMPACT: 1, SpotType.LARGE: 1}, _rates()
    )

    ticket = lot.park("B-1", VehicleType.BUS, entry_time=0.0)

    assert ticket.spot_type is SpotType.LARGE


def test_bus_is_rejected_when_no_large_spot_is_free() -> None:
    """Test 6: A bus cannot use motorcycle or compact spots"""
    import pytest

    from parking_lot import NoAvailableSpotError, ParkingLot, SpotType, VehicleType

    lot = ParkingLot({SpotType.MOTORCYCLE: 2, SpotType.COMPACT: 2}, _rates())

    with pytest.raises(NoAvailableSpotError) as excinfo:
        lot.park("B-1", VehicleType.BUS, entry_time=0.0)
    assert str(excinfo.value) == "no available spot for [bus]"


def test_parking_fails_when_the_lot_is_full() -> None:
    """Test 7: Once every suitable spot is taken, parking raises NoAvailableSpotError"""
    import pytest

    from parking_lot import NoAvailableSpotError, ParkingLot, SpotType, VehicleType

    lot = ParkingLot({SpotType.COMPACT: 1}, _rates())
    lot.park("C-1", VehicleType.CAR, entry_time=0.0)

    with pytest.raises(NoAvailableSpotError):
        lot.park("C-2", VehicleType.CAR, entry_time=0.0)
    assert lot.is_full() is True


def test_same_vehicle_cannot_park_twice() -> None:
    """Test 8: Parking an already-parked vehicle raises VehicleAlreadyParkedError"""
    import pytest

    from parking_lot import ParkingLot, SpotType, VehicleAlreadyParkedError, VehicleType

    lot = ParkingLot({SpotType.COMPACT: 2}, _rates())
    lot.park("C-1", VehicleType.CAR, entry_time=0.0)

    with pytest.raises(VehicleAlreadyParkedError) as excinfo:
        lot.park("C-1", VehicleType.CAR, entry_time=100.0)
    assert str(excinfo.value) == "vehicle [C-1] is already parked"


def test_unparking_frees_the_spot_for_reuse() -> None:
    """Test 9: After a vehicle exits, its spot can be assigned again"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot({SpotType.COMPACT: 1}, _rates())
    lot.park("C-1", VehicleType.CAR, entry_time=0.0)
    lot.unpark("C-1", exit_time=3600.0)

    ticket = lot.park("C-2", VehicleType.CAR, entry_time=3600.0)

    assert ticket.spot_type is SpotType.COMPACT
    assert lot.is_parked("C-1") is False


def test_unparking_an_unknown_vehicle_is_rejected() -> None:
    """Test 10: Removing a vehicle that is not parked raises UnknownVehicleError"""
    import pytest

    from parking_lot import ParkingLot, SpotType, UnknownVehicleError

    lot = ParkingLot({SpotType.COMPACT: 1}, _rates())

    with pytest.raises(UnknownVehicleError) as excinfo:
        lot.unpark("ghost", exit_time=100.0)
    assert str(excinfo.value) == "vehicle [ghost] is not parked"


def test_minimum_charge_is_one_hour() -> None:
    """Test 11: A stay shorter than an hour (even zero) is billed as one hour"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot({SpotType.COMPACT: 2}, _rates())
    lot.park("C-1", VehicleType.CAR, entry_time=0.0)
    lot.park("C-2", VehicleType.CAR, entry_time=0.0)

    instant = lot.unpark("C-1", exit_time=0.0)
    ten_minutes = lot.unpark("C-2", exit_time=600.0)

    assert instant.hours == 1
    assert instant.fee == 2.0
    assert ten_minutes.hours == 1
    assert ten_minutes.fee == 2.0


def test_partial_hours_are_rounded_up() -> None:
    """Test 12: 90 minutes bills as 2 hours"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot({SpotType.COMPACT: 1}, _rates())
    lot.park("C-1", VehicleType.CAR, entry_time=0.0)

    receipt = lot.unpark("C-1", exit_time=5400.0)

    assert receipt.hours == 2
    assert receipt.fee == 4.0


def test_one_second_past_the_hour_bills_the_next_hour() -> None:
    """Test 12b: A stay of 3601 seconds bills as 2 hours"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot({SpotType.COMPACT: 1}, _rates())
    lot.park("C-1", VehicleType.CAR, entry_time=0.0)

    receipt = lot.unpark("C-1", exit_time=3601.0)

    assert receipt.hours == 2
    assert receipt.fee == 4.0


def test_exact_hours_are_not_rounded_up() -> None:
    """Test 13: Exactly 3 hours bills as 3 hours"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot({SpotType.COMPACT: 1}, _rates())
    lot.park("C-1", VehicleType.CAR, entry_time=1000.0)

    receipt = lot.unpark("C-1", exit_time=1000.0 + 3 * 3600.0)

    assert receipt.hours == 3
    assert receipt.fee == 6.0


def test_fee_uses_the_rate_for_the_vehicle_type() -> None:
    """Test 14: The same stay costs each vehicle type its own hourly rate"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot(
        {SpotType.MOTORCYCLE: 1, SpotType.COMPACT: 1, SpotType.LARGE: 1}, _rates()
    )
    lot.park("M-1", VehicleType.MOTORCYCLE, entry_time=0.0)
    lot.park("C-1", VehicleType.CAR, entry_time=0.0)
    lot.park("B-1", VehicleType.BUS, entry_time=0.0)

    two_hours = 2 * 3600.0
    assert lot.unpark("M-1", exit_time=two_hours).fee == 2.0
    assert lot.unpark("C-1", exit_time=two_hours).fee == 4.0
    assert lot.unpark("B-1", exit_time=two_hours).fee == 10.0


def test_exit_before_entry_is_rejected() -> None:
    """Test 15: An exit time earlier than the entry time raises ValueError"""
    import pytest

    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot({SpotType.COMPACT: 1}, _rates())
    lot.park("C-1", VehicleType.CAR, entry_time=1000.0)

    with pytest.raises(ValueError) as excinfo:
        lot.unpark("C-1", exit_time=999.0)
    assert str(excinfo.value) == "exit_time [999.0] is before entry_time [1000.0]"


def test_receipt_records_the_full_stay() -> None:
    """Test 16: The receipt carries vehicle, spot, times, hours, and fee"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot({SpotType.LARGE: 1}, _rates())
    lot.park("B-1", VehicleType.BUS, entry_time=100.0)

    receipt = lot.unpark("B-1", exit_time=100.0 + 3600.0)

    assert receipt.vehicle_id == "B-1"
    assert receipt.vehicle_type is VehicleType.BUS
    assert receipt.spot_type is SpotType.LARGE
    assert receipt.entry_time == 100.0
    assert receipt.exit_time == 3700.0
    assert receipt.hours == 1
    assert receipt.fee == 5.0


def test_status_reports_capacity_occupancy_and_availability() -> None:
    """Test 17: status() breaks down each spot type after some parking"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot(
        {SpotType.MOTORCYCLE: 2, SpotType.COMPACT: 2, SpotType.LARGE: 1}, _rates()
    )
    lot.park("M-1", VehicleType.MOTORCYCLE, entry_time=0.0)
    lot.park("C-1", VehicleType.CAR, entry_time=0.0)

    status = lot.status()

    assert status[SpotType.MOTORCYCLE] == {
        "capacity": 2,
        "occupied": 1,
        "available": 1,
    }
    assert status[SpotType.COMPACT] == {"capacity": 2, "occupied": 1, "available": 1}
    assert status[SpotType.LARGE] == {"capacity": 1, "occupied": 0, "available": 1}


def test_available_spots_tracks_parking_and_unparking() -> None:
    """Test 18: available_spots() falls when parking and rises when unparking"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot({SpotType.COMPACT: 2}, _rates())

    assert lot.available_spots(SpotType.COMPACT) == 2
    lot.park("C-1", VehicleType.CAR, entry_time=0.0)
    assert lot.available_spots(SpotType.COMPACT) == 1
    lot.unpark("C-1", exit_time=0.0)
    assert lot.available_spots(SpotType.COMPACT) == 2


def test_multiple_vehicles_of_the_same_type_park_independently() -> None:
    """Test 19: Several cars occupy distinct spots and exit independently"""
    from parking_lot import ParkingLot, SpotType, VehicleType

    lot = ParkingLot({SpotType.COMPACT: 3}, _rates())
    lot.park("C-1", VehicleType.CAR, entry_time=0.0)
    lot.park("C-2", VehicleType.CAR, entry_time=0.0)
    lot.park("C-3", VehicleType.CAR, entry_time=0.0)

    lot.unpark("C-2", exit_time=3600.0)

    assert lot.is_parked("C-1") is True
    assert lot.is_parked("C-2") is False
    assert lot.is_parked("C-3") is True
    assert lot.available_spots(SpotType.COMPACT) == 1


def test_negative_spot_count_is_an_invalid_configuration() -> None:
    """Test 20: A negative spot count raises InvalidLotConfigurationError"""
    import pytest

    from parking_lot import InvalidLotConfigurationError, ParkingLot, SpotType

    with pytest.raises(InvalidLotConfigurationError) as excinfo:
        ParkingLot({SpotType.COMPACT: -1}, _rates())
    assert (
        str(excinfo.value) == "spot count for [compact] must be non-negative, got [-1]"
    )


def test_lot_with_no_spots_is_an_invalid_configuration() -> None:
    """Test 21: A lot without a single spot raises InvalidLotConfigurationError"""
    import pytest

    from parking_lot import InvalidLotConfigurationError, ParkingLot

    with pytest.raises(InvalidLotConfigurationError) as excinfo:
        ParkingLot({}, _rates())
    assert str(excinfo.value) == "parking lot must have at least one spot"


def test_missing_or_non_positive_rate_is_an_invalid_configuration() -> None:
    """Test 22: Rates must exist and be positive for every vehicle type"""
    import pytest

    from parking_lot import (
        InvalidLotConfigurationError,
        ParkingLot,
        SpotType,
        VehicleType,
    )

    spots = {SpotType.COMPACT: 1}

    with pytest.raises(InvalidLotConfigurationError) as excinfo:
        ParkingLot(spots, {VehicleType.MOTORCYCLE: 1.0, VehicleType.CAR: 2.0})
    assert str(excinfo.value) == "missing hourly rate for [bus]"

    rates = _rates()
    rates[VehicleType.CAR] = 0.0
    with pytest.raises(InvalidLotConfigurationError) as excinfo:
        ParkingLot(spots, rates)
    assert str(excinfo.value) == "hourly rate for [car] must be positive, got [0.0]"
