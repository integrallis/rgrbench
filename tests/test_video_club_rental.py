"""
Tests for Video Club Rental kata - rental charges, renter points, statements
"""

import pytest


def test_regular_movie_base_charge() -> None:
    """Test 1: A regular movie costs 2.0 for a one-day rental"""
    from video_club_rental import Movie, PriceCode, Rental

    movie = Movie("Plan 9 from Outer Space", PriceCode.REGULAR)
    assert Rental(movie, 1).charge == 2.0


def test_regular_movie_two_days_still_base_charge() -> None:
    """Test 2: The regular base charge covers the first two days"""
    from video_club_rental import Movie, PriceCode, Rental

    movie = Movie("Plan 9 from Outer Space", PriceCode.REGULAR)
    assert Rental(movie, 2).charge == 2.0


def test_regular_movie_charges_extra_after_two_days() -> None:
    """Test 3: Each regular day beyond the second adds 1.5"""
    from video_club_rental import Movie, PriceCode, Rental

    movie = Movie("Plan 9 from Outer Space", PriceCode.REGULAR)
    assert Rental(movie, 3).charge == 3.5
    assert Rental(movie, 5).charge == 6.5


def test_new_release_charges_per_day() -> None:
    """Test 4: A new release costs 3.0 per day rented"""
    from video_club_rental import Movie, PriceCode, Rental

    movie = Movie("Robot Overlords", PriceCode.NEW_RELEASE)
    assert Rental(movie, 1).charge == 3.0
    assert Rental(movie, 3).charge == 9.0


def test_childrens_movie_base_charge() -> None:
    """Test 5: A children's movie costs 1.5 for up to three days"""
    from video_club_rental import Movie, PriceCode, Rental

    movie = Movie("Totoro", PriceCode.CHILDRENS)
    assert Rental(movie, 1).charge == 1.5
    assert Rental(movie, 3).charge == 1.5


def test_childrens_movie_charges_extra_after_three_days() -> None:
    """Test 6: Each children's day beyond the third adds 1.5"""
    from video_club_rental import Movie, PriceCode, Rental

    movie = Movie("Totoro", PriceCode.CHILDRENS)
    assert Rental(movie, 4).charge == 3.0
    assert Rental(movie, 6).charge == 6.0


def test_every_rental_earns_one_point() -> None:
    """Test 7: Regular and children's rentals earn one point regardless of days"""
    from video_club_rental import Movie, PriceCode, Rental

    regular = Movie("Plan 9 from Outer Space", PriceCode.REGULAR)
    childrens = Movie("Totoro", PriceCode.CHILDRENS)
    assert Rental(regular, 10).frequent_renter_points == 1
    assert Rental(childrens, 10).frequent_renter_points == 1


def test_one_day_new_release_earns_one_point() -> None:
    """Test 8: A single-day new release earns no bonus point"""
    from video_club_rental import Movie, PriceCode, Rental

    movie = Movie("Robot Overlords", PriceCode.NEW_RELEASE)
    assert Rental(movie, 1).frequent_renter_points == 1


def test_multi_day_new_release_earns_bonus_point() -> None:
    """Test 9: A new release kept more than one day earns two points"""
    from video_club_rental import Movie, PriceCode, Rental

    movie = Movie("Robot Overlords", PriceCode.NEW_RELEASE)
    assert Rental(movie, 2).frequent_renter_points == 2
    assert Rental(movie, 5).frequent_renter_points == 2


def test_rental_must_last_at_least_one_day() -> None:
    """Test 10: Zero-day and negative rentals are rejected"""
    from video_club_rental import Movie, PriceCode, Rental

    movie = Movie("Plan 9 from Outer Space", PriceCode.REGULAR)
    with pytest.raises(ValueError, match="days_rented must be at least 1"):
        Rental(movie, 0)
    with pytest.raises(ValueError, match="days_rented must be at least 1"):
        Rental(movie, -2)


def test_customer_totals_sum_over_rentals() -> None:
    """Test 11: Customer totals aggregate charge and points across rentals"""
    from video_club_rental import Customer, Movie, PriceCode, Rental

    customer = Customer("Martin")
    customer.add_rental(Rental(Movie("Plan 9", PriceCode.REGULAR), 3))
    customer.add_rental(Rental(Movie("Robot Overlords", PriceCode.NEW_RELEASE), 2))
    customer.add_rental(Rental(Movie("Totoro", PriceCode.CHILDRENS), 4))
    assert customer.total_charge == 12.5
    assert customer.total_frequent_renter_points == 4


def test_customer_lists_recorded_rentals() -> None:
    """Test 12: A customer exposes the rentals recorded so far"""
    from video_club_rental import Customer, Movie, PriceCode, Rental

    customer = Customer("Alice")
    rental = Rental(Movie("Totoro", PriceCode.CHILDRENS), 1)
    customer.add_rental(rental)
    assert customer.rentals == (rental,)


def test_statement_with_no_rentals() -> None:
    """Test 13: An empty statement owes nothing and earns no points"""
    from video_club_rental import Customer

    expected = (
        "Rental Record for Alice\n"
        "Amount owed is 0.0\n"
        "You earned 0 frequent renter points"
    )
    assert Customer("Alice").statement() == expected


def test_statement_with_single_rental() -> None:
    """Test 14: A one-rental statement lists the title, charge, total, points"""
    from video_club_rental import Customer, Movie, PriceCode, Rental

    customer = Customer("Bob")
    customer.add_rental(Rental(Movie("Plan 9", PriceCode.REGULAR), 3))
    expected = (
        "Rental Record for Bob\n"
        "\tPlan 9\t3.5\n"
        "Amount owed is 3.5\n"
        "You earned 1 frequent renter points"
    )
    assert customer.statement() == expected


def test_statement_with_multiple_rentals() -> None:
    """Test 15: A multi-rental statement lists every title in rental order"""
    from video_club_rental import Customer, Movie, PriceCode, Rental

    customer = Customer("Martin")
    customer.add_rental(Rental(Movie("Plan 9", PriceCode.REGULAR), 3))
    customer.add_rental(Rental(Movie("Robot Overlords", PriceCode.NEW_RELEASE), 2))
    customer.add_rental(Rental(Movie("Totoro", PriceCode.CHILDRENS), 4))
    expected = (
        "Rental Record for Martin\n"
        "\tPlan 9\t3.5\n"
        "\tRobot Overlords\t6.0\n"
        "\tTotoro\t3.0\n"
        "Amount owed is 12.5\n"
        "You earned 4 frequent renter points"
    )
    assert customer.statement() == expected


def test_statement_renders_whole_amounts_with_decimal_point() -> None:
    """Test 16: Whole charges render with a trailing .0"""
    from video_club_rental import Customer, Movie, PriceCode, Rental

    customer = Customer("Carol")
    customer.add_rental(Rental(Movie("Plan 9", PriceCode.REGULAR), 2))
    expected = (
        "Rental Record for Carol\n"
        "\tPlan 9\t2.0\n"
        "Amount owed is 2.0\n"
        "You earned 1 frequent renter points"
    )
    assert customer.statement() == expected


def test_movie_carries_title_and_price_code() -> None:
    """Test 17: A movie exposes its title and pricing category"""
    from video_club_rental import Movie, PriceCode

    movie = Movie("Totoro", PriceCode.CHILDRENS)
    assert movie.title == "Totoro"
    assert movie.price_code is PriceCode.CHILDRENS


def test_price_codes_are_three_distinct_categories() -> None:
    """Test 18: The catalogue has exactly regular, new release, children's"""
    from video_club_rental import PriceCode

    assert {code.name for code in PriceCode} == {
        "REGULAR",
        "NEW_RELEASE",
        "CHILDRENS",
    }
