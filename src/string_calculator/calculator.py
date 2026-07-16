class Calculator:
    @staticmethod
    def add(numbers: str | None) -> int:
        if numbers == "" or numbers is None:
            return 0

        # Check for custom delimiter
        if numbers.startswith("//"):
            delimiter_end = numbers.index("\n")
            delimiter = numbers[2:delimiter_end]
            numbers = numbers[delimiter_end + 1 :]
            parts = numbers.split(delimiter)
            # Check for negative numbers
            int_parts = [int(part) for part in parts]
            for num in int_parts:
                if num < 0:
                    raise ValueError(
                        f"string contains [{num}], which does not meet rule. entered number should not negative."
                    )
            return sum(num for num in int_parts if num <= 1000)

        if "," in numbers or "\n" in numbers:
            parts = numbers.replace("\n", ",").split(",")
            # Check for negative numbers
            int_parts = [int(part) for part in parts]
            for num in int_parts:
                if num < 0:
                    raise ValueError(
                        f"string contains [{num}], which does not meet rule. entered number should not negative."
                    )
            return sum(num for num in int_parts if num <= 1000)

        num = int(numbers)
        if num < 0:
            raise ValueError(
                f"string contains [{num}], which does not meet rule. entered number should not negative."
            )
        return num if num <= 1000 else 0
