# Host-assignable IPv4 address validation

## Overview
A validator that decides whether a piece of text is an IPv4 address that could be assigned
to a host. A valid address has exactly four dotted-decimal octets, each written with digits
only, valued 0 through 255, and free of leading zeros. Beyond the syntax, the final octet
must be host-assignable: it may be neither 0 (which denotes a network address) nor 255
(which denotes a broadcast address). The validator answers with a plain accept-or-reject
verdict.

## User Stories

### US-1: Accept well-formed host addresses
As a network administrator, I want correctly written host addresses accepted, so that valid configuration entries pass.

- AC-1.1: Text consisting of exactly four dot-separated, digit-only octets, each valued 0 through 255 without leading zeros, whose final octet is between 1 and 254, is accepted (worked examples: 1.1.1.1, 192.168.1.1, 10.0.0.1, 127.0.0.1).

### US-2: Reject malformed text
As a network administrator, I want anything that is not four clean dotted-decimal octets rejected, so that typos never pass as addresses.

- AC-2.1: Text without exactly four octets is rejected: three octets, five octets, empty octets left by doubled or trailing dots, and the empty string all fail.
- AC-2.2: Octets must be digits only: letters of either case, sign characters, and leading or trailing whitespace all cause rejection.

### US-3: Enforce octet values
As a network administrator, I want each octet's numeric form checked, so that out-of-range or ambiguously written values are refused.

- AC-3.1: An octet greater than 255 is rejected, in any position.
- AC-3.2: An octet with a leading zero is rejected, in any position (a lone 0 is fine where 0 is allowed).

### US-4: Require a host-assignable final octet
As a network administrator, I want network and broadcast addresses refused, so that only addresses assignable to a host pass.

- AC-4.1: An address whose final octet is 0 denotes a network and is rejected (0.0.0.0 included).
- AC-4.2: An address whose final octet is 255 denotes a broadcast and is rejected (255.255.255.255 included).
- AC-4.3: The restriction applies only to the final octet: 0 and 255 remain acceptable in the first three positions, and 254 is the largest acceptable final octet.

## Traceability
```json
{
  "test_all_ones_address_is_valid": ["AC-1.1"],
  "test_private_network_address_is_valid": ["AC-1.1"],
  "test_ten_dot_address_is_valid": ["AC-1.1"],
  "test_loopback_address_is_valid": ["AC-1.1"],
  "test_all_zeros_address_is_rejected": ["AC-4.1"],
  "test_all_255_address_is_rejected": ["AC-4.2"],
  "test_final_octet_zero_is_rejected": ["AC-4.1"],
  "test_final_octet_255_is_rejected": ["AC-4.2"],
  "test_three_octets_are_rejected": ["AC-2.1"],
  "test_five_octets_are_rejected": ["AC-2.1"],
  "test_leading_zero_in_middle_octet_is_rejected": ["AC-3.2"],
  "test_leading_zero_in_final_octet_is_rejected": ["AC-3.2"],
  "test_octet_above_255_is_rejected": ["AC-3.1"],
  "test_empty_string_is_rejected": ["AC-2.1"],
  "test_empty_octets_are_rejected": ["AC-2.1"],
  "test_non_digit_characters_are_rejected": ["AC-2.2"],
  "test_whitespace_is_rejected": ["AC-2.2"],
  "test_sign_characters_are_rejected": ["AC-2.2"],
  "test_zero_is_allowed_in_non_final_octets": ["AC-4.3"],
  "test_255_is_allowed_in_non_final_octets": ["AC-4.3"],
  "test_upper_boundary_final_octet_is_valid": ["AC-4.3"],
  "test_uppercase_letters_are_rejected": ["AC-2.2"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
