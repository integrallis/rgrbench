"""Metric Converter kata: one-directional metric-to-imperial unit conversions.

Kata catalogued at tddbuddy.com/katas/metric-converter; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""


def test_one_kilometer_to_miles() -> None:
    """Test 1: 1 km converts to 0.621371 miles"""
    import pytest

    from metric_converter import Unit, convert

    assert convert(1, Unit.KILOMETERS, Unit.MILES) == pytest.approx(0.621371)


def test_one_hundred_kilometers_to_miles() -> None:
    """Test 2: 100 km converts to 62.1371 miles"""
    import pytest

    from metric_converter import Unit, convert

    assert convert(100, Unit.KILOMETERS, Unit.MILES) == pytest.approx(62.1371)


def test_zero_kilometers_to_miles() -> None:
    """Test 3: 0 km converts to 0 miles"""
    from metric_converter import Unit, convert

    assert convert(0, Unit.KILOMETERS, Unit.MILES) == 0


def test_thirty_celsius_to_fahrenheit() -> None:
    """Test 4: 30 degrees Celsius converts to 86 degrees Fahrenheit"""
    import pytest

    from metric_converter import Unit, convert

    assert convert(30, Unit.CELSIUS, Unit.FAHRENHEIT) == pytest.approx(86.0)


def test_freezing_point_celsius_to_fahrenheit() -> None:
    """Test 5: 0 degrees Celsius converts to 32 degrees Fahrenheit"""
    import pytest

    from metric_converter import Unit, convert

    assert convert(0, Unit.CELSIUS, Unit.FAHRENHEIT) == pytest.approx(32.0)


def test_boiling_point_celsius_to_fahrenheit() -> None:
    """Test 6: 100 degrees Celsius converts to 212 degrees Fahrenheit"""
    import pytest

    from metric_converter import Unit, convert

    assert convert(100, Unit.CELSIUS, Unit.FAHRENHEIT) == pytest.approx(212.0)


def test_minus_forty_crossover_point() -> None:
    """Test 7: -40 degrees Celsius equals -40 degrees Fahrenheit"""
    import pytest

    from metric_converter import Unit, convert

    assert convert(-40, Unit.CELSIUS, Unit.FAHRENHEIT) == pytest.approx(-40.0)


def test_five_kilograms_to_pounds() -> None:
    """Test 8: 5 kg converts to approximately 11.02311310 pounds"""
    import pytest

    from metric_converter import Unit, convert

    assert convert(5, Unit.KILOGRAMS, Unit.POUNDS) == pytest.approx(11.02311310)


def test_one_kilogram_to_pounds() -> None:
    """Test 9: 1 kg converts to 1 / 0.45359237 pounds"""
    import pytest

    from metric_converter import Unit, convert

    assert convert(1, Unit.KILOGRAMS, Unit.POUNDS) == pytest.approx(1 / 0.45359237)


def test_one_us_gallon_worth_of_liters() -> None:
    """Test 10: 3.785411784 liters converts to exactly 1 US gallon"""
    import pytest

    from metric_converter import Unit, convert

    assert convert(3.785411784, Unit.LITERS, Unit.US_GALLONS) == pytest.approx(1.0)


def test_one_liter_to_us_gallons() -> None:
    """Test 11: 1 liter converts to 1 / 3.785411784 US gallons"""
    import pytest

    from metric_converter import Unit, convert

    expected = 1 / 3.785411784
    assert convert(1, Unit.LITERS, Unit.US_GALLONS) == pytest.approx(expected)


def test_one_uk_gallon_worth_of_liters() -> None:
    """Test 12: 4.54609 liters converts to exactly 1 UK gallon"""
    import pytest

    from metric_converter import Unit, convert

    assert convert(4.54609, Unit.LITERS, Unit.UK_GALLONS) == pytest.approx(1.0)


def test_ten_liters_to_uk_gallons() -> None:
    """Test 13: 10 liters converts to 10 / 4.54609 UK gallons"""
    import pytest

    from metric_converter import Unit, convert

    expected = 10 / 4.54609
    assert convert(10, Unit.LITERS, Unit.UK_GALLONS) == pytest.approx(expected)


def test_us_and_uk_gallons_differ() -> None:
    """Test 14: The same volume yields fewer UK gallons than US gallons"""
    from metric_converter import Unit, convert

    liters = 20.0
    assert convert(liters, Unit.LITERS, Unit.UK_GALLONS) < convert(
        liters, Unit.LITERS, Unit.US_GALLONS
    )


def test_reverse_direction_is_unsupported() -> None:
    """Test 15: Imperial-to-metric (miles to km) raises the domain error"""
    import pytest

    from metric_converter import Unit, UnsupportedConversionError, convert

    with pytest.raises(UnsupportedConversionError, match="unsupported conversion"):
        convert(1, Unit.MILES, Unit.KILOMETERS)


def test_fahrenheit_to_celsius_is_unsupported() -> None:
    """Test 16: Fahrenheit to Celsius is outside the one-directional set"""
    import pytest

    from metric_converter import Unit, UnsupportedConversionError, convert

    with pytest.raises(UnsupportedConversionError):
        convert(86, Unit.FAHRENHEIT, Unit.CELSIUS)


def test_cross_dimension_pair_is_unsupported() -> None:
    """Test 17: Kilometers to pounds is a nonsensical pair and raises"""
    import pytest

    from metric_converter import Unit, UnsupportedConversionError, convert

    with pytest.raises(UnsupportedConversionError):
        convert(1, Unit.KILOMETERS, Unit.POUNDS)


def test_identity_pair_is_unsupported() -> None:
    """Test 18: Converting a unit to itself is not a supported pair"""
    import pytest

    from metric_converter import Unit, UnsupportedConversionError, convert

    with pytest.raises(UnsupportedConversionError):
        convert(1, Unit.CELSIUS, Unit.CELSIUS)


def test_domain_error_is_a_value_error() -> None:
    """Test 19: The domain error is a ValueError subclass for easy handling"""
    from metric_converter import UnsupportedConversionError

    assert issubclass(UnsupportedConversionError, ValueError)


def test_error_message_names_both_units() -> None:
    """Test 20: The domain error message names the offending pair"""
    import pytest

    from metric_converter import Unit, UnsupportedConversionError, convert

    with pytest.raises(UnsupportedConversionError) as exc_info:
        convert(1, Unit.MILES, Unit.KILOMETERS)
    assert "miles" in str(exc_info.value)
    assert "kilometers" in str(exc_info.value)


def test_nine_units_are_recognised() -> None:
    """Test 21: The unit enum recognises exactly nine units"""
    from metric_converter import Unit

    assert len(Unit) == 9
