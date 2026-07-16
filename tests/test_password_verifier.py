"""
Test-Driven Development for PasswordVerifier kata.
Starting fresh with proper TDD approach, one test at a time.
"""

import pytest


def test_password_shorter_than_8_chars_should_raise_exception() -> None:
    """Test 1: Password with 8 or fewer characters should raise exception"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()

    with pytest.raises(Exception) as excinfo:
        verifier.verify("short")  # 5 characters

    assert "password should be longer than 8 characters" in str(excinfo.value).lower()


def test_password_longer_than_8_chars_should_be_valid() -> None:
    """Test 2: Password with more than 8 characters should return True"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()
    result = verifier.verify("Validpass123")  # 12 characters with uppercase V

    assert result is True


def test_password_null_should_raise_exception() -> None:
    """Test 3: Null password should raise exception"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()

    with pytest.raises(Exception) as excinfo:
        verifier.verify(None)

    assert "password should not be null" in str(excinfo.value).lower()


def test_password_without_uppercase_should_raise_exception() -> None:
    """Test 4: Password without uppercase letter should raise exception"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()

    with pytest.raises(Exception) as excinfo:
        verifier.verify("alllowercase123")  # no uppercase

    assert (
        "password should have at least one uppercase letter"
        in str(excinfo.value).lower()
    )


def test_password_without_lowercase_should_raise_exception() -> None:
    """Test 5: Password without lowercase letter should raise exception"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()

    with pytest.raises(Exception) as excinfo:
        verifier.verify("ALLUPPERCASE123")  # no lowercase

    assert (
        "password should have at least one lowercase letter"
        in str(excinfo.value).lower()
    )


def test_password_without_number_should_raise_exception() -> None:
    """Test 6: Password without number should raise exception"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()

    with pytest.raises(Exception) as excinfo:
        verifier.verify("ValidPassWord")  # no numbers

    assert "password should have at least one number" in str(excinfo.value).lower()


def test_valid_password_with_all_requirements_should_pass() -> None:
    """Test 7: Password meeting all requirements should be valid"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()

    # Password with: >8 chars, uppercase, lowercase, number
    result = verifier.verify("ValidPass123")

    assert result is True


def test_password_with_exactly_8_chars_should_raise_exception() -> None:
    """Test 8: Boundary - 'longer than 8' means exactly 8 characters is too short"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()

    with pytest.raises(Exception) as excinfo:
        verifier.verify("Abcdef12")  # exactly 8 characters, all other rules satisfied

    assert "password should be longer than 8 characters" in str(excinfo.value).lower()


def test_password_with_exactly_9_chars_should_be_valid() -> None:
    """Test 9: Boundary - exactly 9 characters is longer than 8, so it is valid"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()
    result = verifier.verify("Abcdefg12")  # exactly 9 characters, meets all rules

    assert result is True


def test_null_password_error_message_should_be_exact() -> None:
    """Test 10: Null password error message matches the rule description exactly"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()

    with pytest.raises(Exception) as excinfo:
        verifier.verify(None)

    assert str(excinfo.value) == "Password should not be null"


def test_short_password_error_message_should_be_exact() -> None:
    """Test 11: Short password error message matches the rule description exactly"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()

    with pytest.raises(Exception) as excinfo:
        verifier.verify("short")  # 5 characters

    assert str(excinfo.value) == "Password should be longer than 8 characters"


def test_password_without_uppercase_error_message_should_be_exact() -> None:
    """Test 12: Missing-uppercase error message matches the rule description exactly"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()

    with pytest.raises(Exception) as excinfo:
        verifier.verify("alllowercase123")  # no uppercase

    assert str(excinfo.value) == "Password should have at least one uppercase letter"


def test_password_without_lowercase_error_message_should_be_exact() -> None:
    """Test 13: Missing-lowercase error message matches the rule description exactly"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()

    with pytest.raises(Exception) as excinfo:
        verifier.verify("ALLUPPERCASE123")  # no lowercase

    assert str(excinfo.value) == "Password should have at least one lowercase letter"


def test_password_without_number_error_message_should_be_exact() -> None:
    """Test 14: Missing-number error message matches the rule description exactly"""
    from password_verifier.password_verifier import PasswordVerifier

    verifier = PasswordVerifier()

    with pytest.raises(Exception) as excinfo:
        verifier.verify("ValidPassWord")  # no numbers

    assert str(excinfo.value) == "Password should have at least one number"
