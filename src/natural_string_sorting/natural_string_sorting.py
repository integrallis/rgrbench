"""Natural String Sorting implementation - sorts strings with embedded numbers naturally"""

import re
from enum import Enum


class NaturalStringSorting:
    """Class for natural string sorting operations"""

    class SortOrder(Enum):
        """Sort order options"""

        ASCENDING = 1
        DESCENDING = 2

    def sort_string(
        self, strings: list[str], order: "NaturalStringSorting.SortOrder" = None
    ) -> list[str]:
        """Sort strings naturally with embedded numbers"""
        if order is None:
            order = NaturalStringSorting.SortOrder.ASCENDING

        def natural_key(text: str) -> tuple[tuple[int, int | str], ...]:
            """Convert a string into a tuple for natural sorting"""
            # Remove spaces for sorting purposes
            text_no_spaces = text.replace(" ", "")
            # Split on numeric sequences
            parts = re.split(r"([0-9]+)", text_no_spaces)
            # Convert numeric parts to integers, keep strings as is
            # Use tuples to ensure proper comparison
            result: list[tuple[int, int | str]] = []
            for part in parts:
                if part:  # Skip empty strings
                    try:
                        # Numbers are converted to (0, number) for sorting
                        result.append((0, int(part)))
                    except ValueError:
                        # Strings are converted to (1, string) for sorting
                        result.append((1, part))
            return tuple(result)

        if order == NaturalStringSorting.SortOrder.DESCENDING:
            return sorted(strings, key=natural_key, reverse=True)
        else:
            return sorted(strings, key=natural_key)
