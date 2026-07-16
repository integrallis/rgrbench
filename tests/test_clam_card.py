"""Clam Card kata tests.

Zone A journeys cost 2.50 and journeys touching Zone B cost 3.00, with charges
capped per day (7.00/8.00), per ISO week (40.00/47.00) and per calendar month
(145.00/165.00). Journey dates are injected; unknown stations raise
UnknownStationError.
"""

import pytest


def test_single_zone_a_journey_costs_2_50() -> None:
    """Test 1: Asterisk to Aldgate stays in Zone A and charges 2.50."""
    from datetime import date

    from clam_card import ClamCard

    card = ClamCard()

    assert card.journey("Asterisk", "Aldgate", date(2026, 1, 5)) == 2.50


def test_journey_touching_zone_b_costs_3_00() -> None:
    """Test 2: Asterisk to Barbican touches Zone B, so the Zone B price of 3.00
    is charged."""
    from datetime import date

    from clam_card import ClamCard

    card = ClamCard()

    assert card.journey("Asterisk", "Barbican", date(2026, 1, 5)) == 3.00


def test_zone_b_origin_also_charges_zone_b_price() -> None:
    """Test 3: starting from a Zone B station charges 3.00 no matter the
    destination zone."""
    from datetime import date

    from clam_card import ClamCard

    card = ClamCard()

    assert card.journey("Balham", "Angel", date(2026, 1, 5)) == 3.00


def test_journey_entirely_within_zone_b_costs_3_00() -> None:
    """Test 4: Bison to Bugel is wholly in Zone B and charges 3.00."""
    from datetime import date

    from clam_card import ClamCard

    card = ClamCard()

    assert card.journey("Bison", "Bugel", date(2026, 1, 5)) == 3.00


def test_two_journeys_in_a_day_sum_their_fares() -> None:
    """Test 5: kata scenario - Asterisk->Aldgate (2.50) then Asterisk->Balham
    (3.00) totals 5.50."""
    from datetime import date

    from clam_card import ClamCard

    card = ClamCard()
    card.journey("Asterisk", "Aldgate", date(2026, 1, 5))
    card.journey("Asterisk", "Balham", date(2026, 1, 5))

    assert card.total_charged == 5.50


def test_zone_a_journeys_cap_at_7_00_per_day() -> None:
    """Test 6: four Zone A journeys in one day charge 2.50, 2.50, 2.00, 0.00
    for a daily total of 7.00."""
    from datetime import date

    from clam_card import ClamCard

    card = ClamCard()
    charges = [card.journey("Asterisk", "Aldgate", date(2026, 1, 5)) for _ in range(4)]

    assert charges == [2.50, 2.50, 2.00, 0.00]
    assert card.total_charged == 7.00


def test_zone_b_journeys_cap_at_8_00_per_day() -> None:
    """Test 7: four Zone B journeys in one day charge 3.00, 3.00, 2.00, 0.00
    for a daily total of 8.00."""
    from datetime import date

    from clam_card import ClamCard

    card = ClamCard()
    charges = [card.journey("Balham", "Bullhead", date(2026, 1, 5)) for _ in range(4)]

    assert charges == [3.00, 3.00, 2.00, 0.00]
    assert card.total_charged == 8.00


def test_day_cap_resets_on_the_next_day() -> None:
    """Test 8: after the daily cap is reached, the next day's journey charges
    the full single fare again."""
    from datetime import date

    from clam_card import ClamCard

    card = ClamCard()
    for _ in range(4):
        card.journey("Asterisk", "Aldgate", date(2026, 1, 5))

    assert card.journey("Asterisk", "Aldgate", date(2026, 1, 6)) == 2.50


def test_zone_b_journey_raises_a_capped_day_to_the_zone_b_cap() -> None:
    """Test 9: a day capped at the Zone A limit (7.00) can still charge up to
    the Zone B cap (8.00) once a Zone B journey is made."""
    from datetime import date

    from clam_card import ClamCard

    card = ClamCard()
    for _ in range(3):
        card.journey("Asterisk", "Aldgate", date(2026, 1, 5))

    assert card.total_charged == 7.00
    assert card.journey("Asterisk", "Balham", date(2026, 1, 5)) == 1.00
    assert card.total_charged == 8.00


def test_unknown_origin_station_raises() -> None:
    """Test 10: an off-network origin raises UnknownStationError naming it."""
    from datetime import date

    from clam_card import ClamCard, UnknownStationError

    card = ClamCard()

    with pytest.raises(UnknownStationError, match="Atlantis"):
        card.journey("Atlantis", "Aldgate", date(2026, 1, 5))


def test_unknown_destination_station_raises() -> None:
    """Test 11: an off-network destination raises UnknownStationError."""
    from datetime import date

    from clam_card import ClamCard, UnknownStationError

    card = ClamCard()

    with pytest.raises(UnknownStationError, match="Brigadoon"):
        card.journey("Angel", "Brigadoon", date(2026, 1, 5))


def test_failed_journey_charges_nothing() -> None:
    """Test 12: a journey rejected for an unknown station leaves the card's
    total unchanged."""
    from datetime import date

    from clam_card import ClamCard, UnknownStationError

    card = ClamCard()
    card.journey("Asterisk", "Aldgate", date(2026, 1, 5))

    with pytest.raises(UnknownStationError):
        card.journey("Asterisk", "Nowhere", date(2026, 1, 5))

    assert card.total_charged == 2.50


def test_zone_a_journeys_cap_at_40_00_per_week() -> None:
    """Test 13: three Zone A journeys a day for six days of one ISO week
    (2026-01-05 is a Monday) hit the daily cap of 7.00 five times, then the
    weekly cap of 40.00."""
    from datetime import date, timedelta

    from clam_card import ClamCard

    card = ClamCard()
    monday = date(2026, 1, 5)
    for day_offset in range(6):
        for _ in range(3):
            card.journey("Asterisk", "Anerley", monday + timedelta(days=day_offset))

    assert card.total_charged == 40.00


def test_week_cap_resets_in_the_next_iso_week() -> None:
    """Test 14: once a week is capped at 40.00, a journey the following Monday
    charges the full single fare again."""
    from datetime import date, timedelta

    from clam_card import ClamCard

    card = ClamCard()
    monday = date(2026, 1, 5)
    for day_offset in range(6):
        for _ in range(3):
            card.journey("Asterisk", "Anerley", monday + timedelta(days=day_offset))

    next_monday = date(2026, 1, 12)

    assert card.journey("Asterisk", "Anerley", next_monday) == 2.50
    assert card.total_charged == 42.50


def test_zone_a_journeys_cap_at_145_00_per_month() -> None:
    """Test 15: three Zone A journeys every day of June 2026 accumulate 7.00
    per day, 40.00 per ISO week, and stop at the monthly cap of 145.00."""
    from datetime import date

    from clam_card import ClamCard

    card = ClamCard()
    for day in range(1, 31):
        for _ in range(3):
            card.journey("Amersham", "Angel", date(2026, 6, day))

    assert card.total_charged == 145.00


def test_total_charged_accumulates_across_days() -> None:
    """Test 16: total_charged sums the charges of every journey made."""
    from datetime import date

    from clam_card import ClamCard

    card = ClamCard()
    card.journey("Asterisk", "Aldgate", date(2026, 2, 2))
    card.journey("Asterisk", "Barbican", date(2026, 2, 3))
    card.journey("Bison", "Bullhead", date(2026, 2, 4))

    assert card.total_charged == 8.50
