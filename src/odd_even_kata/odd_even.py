class OddEven:
    @staticmethod
    def print_odd_even(start_number: int, last_number: int) -> str:
        """Port of PrintOddEven"""
        return OddEven._get_odd_even_within_range(start_number, last_number)

    @staticmethod
    def print_single_odd_even(number: int) -> str:
        """Port of PrintSingleOddEven"""
        return OddEven._check_single_number_odd_even_prime_result(number)

    @staticmethod
    def _get_odd_even_within_range(start_number: int, last_number: int) -> str:
        """Port of GetOddEvenWithinRange"""
        result = ""
        start = 1 if start_number < 0 else start_number
        for number in range(start, last_number + 1):
            result = OddEven._check_single_number_odd_even_prime_result_with_string(
                result, number
            )
        return result

    @staticmethod
    def _check_single_number_odd_even_prime_result(number: int) -> str:
        """Port of CheckSingleNumberOddEvenPrimeResult(int)"""
        result = ""
        result = OddEven._check_single_number_odd_even_prime_result_with_string(
            result, number
        )
        return result

    @staticmethod
    def _check_single_number_odd_even_prime_result_with_string(
        result: str, number: int
    ) -> str:
        """Port of CheckSingleNumberOddEvenPrimeResult(string, int)"""
        odd_number = "Odd" if OddEven._is_odd_number(number) else str(number)
        prime_number = str(number) if OddEven._is_prime_number(number) else odd_number

        new_number = "Even" if OddEven._is_even_number(number) else prime_number

        result += " " + new_number
        return result.strip()

    @staticmethod
    def _is_even_number(number: int) -> bool:
        """Port of IsEvenNumber"""
        return number >= 2 and number % 2 == 0

    @staticmethod
    def _is_odd_number(number: int) -> bool:
        """Port of IsOddNumber"""
        return number % 2 != 0

    @staticmethod
    def _is_prime_number(number: int) -> bool:
        """Port of IsPrimeNumber"""
        if number < 2:
            return False
        if OddEven._is_even_number(number):
            return False
        divisible = 3
        while divisible * divisible <= number:
            if number % divisible == 0:
                return False
            divisible += 2
        return True
