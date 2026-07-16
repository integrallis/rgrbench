class FizzBuzz:
    @staticmethod
    def print_fizz_buzz(number: int | None = None) -> str:
        # Port of parameterless PrintFizzBuzz()
        if number is None:
            result = []
            for i in range(1, 101):
                if i % 3 == 0 and i % 5 == 0:
                    result.append("FizzBuzz")
                elif i % 3 == 0:
                    result.append("Fizz")
                elif i % 5 == 0:
                    result.append("Buzz")
                else:
                    result.append(str(i))
            return " ".join(result)

        # Port of PrintFizzBuzz(int number)
        if number > 100 or number < 1:
            raise ValueError(
                f"entered number is [{number}], which does not meet rule, "
                f"entered number should be between 1 to 100."
            )
        if number % 3 == 0 and number % 5 == 0:
            return "FizzBuzz"
        if number % 3 == 0:
            return "Fizz"
        if number % 5 == 0:
            return "Buzz"
        return str(number)
