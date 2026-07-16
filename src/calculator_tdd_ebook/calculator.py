"""Calculator - TDD Ebook Example Implementation"""

from .digit_keys import DigitKeys


class Calculator:
    """Calculator implementation following TDD Ebook narrative"""

    INITIAL_VALUE = "0"

    def __init__(self) -> None:
        """Initialize calculator with empty entered digits"""
        self._entered_digits: list[DigitKeys] = []

    def display(self) -> str:
        """Return the displayed value"""
        if not self._entered_digits:
            return Calculator.INITIAL_VALUE
        return "".join(str(int(digit)) for digit in self._entered_digits)

    def enter(self, digit: DigitKeys) -> None:
        """Enter a digit key"""
        only_zeros = bool(self._entered_digits) and all(
            d == DigitKeys.ZERO for d in self._entered_digits
        )
        if digit == DigitKeys.ZERO:
            # A zero after nothing starts the display; zeros after only zeros collapse
            if not self._entered_digits:
                self._entered_digits.append(digit)
            elif not only_zeros:
                self._entered_digits.append(digit)
        else:
            # A non-zero digit replaces a leading-zeros-only display
            if only_zeros:
                self._entered_digits.clear()
            self._entered_digits.append(digit)
