"""Bank OCR kata: parse ASCII-art account numbers, validate the mod-11 checksum,
classify entries (ILL/ERR) and attempt single-segment error correction.

Kata catalogued at tddbuddy.com/katas/bank-ocr; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from bank_ocr.bank_ocr import account_status, checksum_valid, fix_entry, parse_entry

__all__ = ["account_status", "checksum_valid", "fix_entry", "parse_entry"]
