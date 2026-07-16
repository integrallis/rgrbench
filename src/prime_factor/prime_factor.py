"""Prime Factor implementation - generates prime factors of a number"""


class PrimeFactor:
    """Static class for generating prime factors"""

    @staticmethod
    def generate(n: int) -> list[int]:
        """Generate prime factors for a given number"""
        factors = []
        divisor = 2

        while n > 1:
            while n % divisor == 0:
                factors.append(divisor)
                n //= divisor
            divisor += 1

        return factors
