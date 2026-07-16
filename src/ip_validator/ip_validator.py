"""IP Validator kata.

validate_ipv4_address decides whether a string is a valid, host-assignable
IPv4 address in dotted-decimal notation. The string must consist of exactly
four octets separated by single dots; every octet must be a non-empty run
of decimal digits with a value from 0 to 255 and no leading zeros (a lone
"0" is the only octet that may start with zero). Because network and
broadcast addresses cannot be assigned to hosts, any address whose final
octet is 0 or 255 is rejected. Any other character, empty octet, or wrong
octet count makes the address invalid. The kata forbids regular
expressions, so validation is done with plain string checks.

Kata catalogued at tddbuddy.com/katas/ip-validator; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""


def validate_ipv4_address(address: str) -> bool:
    """Return True when the address is a valid host-assignable IPv4 address."""
    octets = address.split(".")
    if len(octets) != 4:
        return False
    if not all(_is_valid_octet(octet) for octet in octets):
        return False
    return int(octets[3]) not in (0, 255)


def _is_valid_octet(octet: str) -> bool:
    """Check one dotted-decimal octet: digits only, 0-255, no leading zeros."""
    if not octet or any(not "0" <= ch <= "9" for ch in octet):
        return False
    if len(octet) > 1 and octet[0] == "0":
        return False
    return int(octet) <= 255
