"""Tests for the IP Validator kata.

A valid host-assignable IPv4 address has exactly four dotted-decimal
octets, each a digit-only value 0-255 with no leading zeros, and its final
octet must be neither 0 (network address) nor 255 (broadcast address).
"""


def test_all_ones_address_is_valid() -> None:
    """Test 1: 1.1.1.1 is valid"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("1.1.1.1") is True


def test_private_network_address_is_valid() -> None:
    """Test 2: 192.168.1.1 is valid"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("192.168.1.1") is True


def test_ten_dot_address_is_valid() -> None:
    """Test 3: 10.0.0.1 is valid"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("10.0.0.1") is True


def test_loopback_address_is_valid() -> None:
    """Test 4: 127.0.0.1 is valid"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("127.0.0.1") is True


def test_all_zeros_address_is_rejected() -> None:
    """Test 5: 0.0.0.0 ends in 0, a network address"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("0.0.0.0") is False


def test_all_255_address_is_rejected() -> None:
    """Test 6: 255.255.255.255 ends in 255, a broadcast address"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("255.255.255.255") is False


def test_final_octet_zero_is_rejected() -> None:
    """Test 7: 192.168.1.0 ends in 0 and is not host-assignable"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("192.168.1.0") is False


def test_final_octet_255_is_rejected() -> None:
    """Test 8: 192.168.1.255 ends in 255 and is not host-assignable"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("192.168.1.255") is False


def test_three_octets_are_rejected() -> None:
    """Test 9: 10.0.1 has only three octets"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("10.0.1") is False


def test_five_octets_are_rejected() -> None:
    """Test 10: 1.2.3.4.5 has five octets"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("1.2.3.4.5") is False


def test_leading_zero_in_middle_octet_is_rejected() -> None:
    """Test 11: 192.168.01.1 has a leading zero"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("192.168.01.1") is False


def test_leading_zero_in_final_octet_is_rejected() -> None:
    """Test 12: 192.168.1.00 has a leading zero in the final octet"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("192.168.1.00") is False


def test_octet_above_255_is_rejected() -> None:
    """Test 13: 256 is out of range in any position"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("256.1.1.1") is False
    assert validate_ipv4_address("1.1.1.256") is False


def test_empty_string_is_rejected() -> None:
    """Test 14: The empty string is not an address"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("") is False


def test_empty_octets_are_rejected() -> None:
    """Test 15: Consecutive or trailing dots leave empty octets"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("1..1.1") is False
    assert validate_ipv4_address("1.1.1.") is False


def test_non_digit_characters_are_rejected() -> None:
    """Test 16: Letters are not valid octet characters"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("a.b.c.d") is False


def test_whitespace_is_rejected() -> None:
    """Test 17: Surrounding whitespace makes the address invalid"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address(" 1.1.1.1") is False
    assert validate_ipv4_address("1.1.1.1 ") is False


def test_sign_characters_are_rejected() -> None:
    """Test 18: Signed numbers are not valid octets"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("1.1.1.-1") is False
    assert validate_ipv4_address("+1.1.1.1") is False


def test_zero_is_allowed_in_non_final_octets() -> None:
    """Test 19: Only the final octet is barred from being 0"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("0.1.2.3") is True


def test_255_is_allowed_in_non_final_octets() -> None:
    """Test 20: Only the final octet is barred from being 255"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("255.1.1.1") is True


def test_upper_boundary_final_octet_is_valid() -> None:
    """Test 21: 254 is the largest host-assignable final octet"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("1.1.1.254") is True


def test_uppercase_letters_are_rejected() -> None:
    """Test 22: Uppercase letters are not valid octet characters"""
    from ip_validator import validate_ipv4_address

    assert validate_ipv4_address("1.1.1.A") is False
    assert validate_ipv4_address("A.1.1.1") is False
