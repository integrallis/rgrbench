"""Metric Converter kata: one-directional metric-to-imperial conversions.

Kata catalogued at tddbuddy.com/katas/metric-converter; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""

from metric_converter.converter import Unit, UnsupportedConversionError, convert

__all__ = ["Unit", "UnsupportedConversionError", "convert"]
