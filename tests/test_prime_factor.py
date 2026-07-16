"""
Port of C# PrimeFactorTest.cs
Tests for Prime Factor kata - factorizing numbers into their prime components
"""


def test_one() -> None:
    """Test 1: Generate(1) should return empty list"""
    from prime_factor.prime_factor import PrimeFactor

    result = PrimeFactor.generate(1)
    expected: list[int] = []

    assert result == expected


def test_two() -> None:
    """Test 2: Generate(2) should return [2]"""
    from prime_factor.prime_factor import PrimeFactor

    result = PrimeFactor.generate(2)
    expected = [2]

    assert result == expected


def test_three() -> None:
    """Test 3: Generate(3) should return [3]"""
    from prime_factor.prime_factor import PrimeFactor

    result = PrimeFactor.generate(3)
    expected = [3]

    assert result == expected


def test_four() -> None:
    """Test 4: Generate(4) should return [2, 2]"""
    from prime_factor.prime_factor import PrimeFactor

    result = PrimeFactor.generate(4)
    expected = [2, 2]

    assert result == expected


def test_six() -> None:
    """Test 5: Generate(6) should return [2, 3]"""
    from prime_factor.prime_factor import PrimeFactor

    result = PrimeFactor.generate(6)
    expected = [2, 3]

    assert result == expected


def test_eight() -> None:
    """Test 6: Generate(8) should return [2, 2, 2]"""
    from prime_factor.prime_factor import PrimeFactor

    result = PrimeFactor.generate(8)
    expected = [2, 2, 2]

    assert result == expected


def test_nine() -> None:
    """Test 7: Generate(9) should return [3, 3]"""
    from prime_factor.prime_factor import PrimeFactor

    result = PrimeFactor.generate(9)
    expected = [3, 3]

    assert result == expected


def test_large_number() -> None:
    """Test 8: Generate(5**9 * 7**13) should factor large numbers exactly"""
    from prime_factor.prime_factor import PrimeFactor

    result = PrimeFactor.generate(5**9 * 7**13)
    expected = [5] * 9 + [7] * 13

    assert result == expected
