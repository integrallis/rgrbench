"""String Helper - String manipulation utilities"""


class StringHelper:
    """Helper class for string manipulations"""

    def are_first_and_last_two_chars_same(self, text: str) -> bool:
        """Check if first 2 and last 2 characters are the same"""
        if len(text) < 2:
            return False

        first_two = text[:2]
        last_two = text[-2:]
        return first_two == last_two
