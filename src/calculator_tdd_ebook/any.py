"""Any utility class for generating test data (simplified version from TDD Ebook)"""

import random
from typing import TypeVar

from .digit_keys import DigitKeys

T = TypeVar("T")


class Any:
    """Test data generation utility following TDD Ebook patterns"""

    @staticmethod
    def of(enum_type: type[T]) -> T:
        """Generate any value from the given enum type"""
        values = list(enum_type)  # type: ignore[call-overload]
        return random.choice(values)

    @staticmethod
    def other_than(excluded_value: T) -> T:
        """Generate any value from the same type except the excluded one"""
        if isinstance(excluded_value, DigitKeys):
            values = [key for key in DigitKeys if key != excluded_value]
            return random.choice(values)
        raise NotImplementedError(
            f"other_than not implemented for {type(excluded_value)}"
        )

    @staticmethod
    def string_consisting_of(*digit_keys: DigitKeys) -> str:
        """Convert digit keys to string representation"""
        return "".join(str(int(key)) for key in digit_keys)
