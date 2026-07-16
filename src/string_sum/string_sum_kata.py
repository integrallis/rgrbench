class StringSumKata:
    @staticmethod
    def sum(num1: str | None, num2: str | None) -> str:
        """Port of Sum"""
        real_num1 = StringSumKata._get_zero_when_null_or_empty(num1)
        real_num2 = StringSumKata._get_zero_when_null_or_empty(num2)
        return str(StringSumKata._add(real_num1, real_num2))

    @staticmethod
    def _get_zero_when_null_or_empty(num: str | None) -> str:
        """Port of GetZeroWhenNullOrEmpty"""
        return num if num else "0"

    @staticmethod
    def _add(real_num1: str, real_num2: str) -> int:
        """Port of Add"""
        return int(real_num1) + int(real_num2)
