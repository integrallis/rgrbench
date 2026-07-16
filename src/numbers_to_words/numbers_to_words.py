"""Numbers to Words kata.

Spell out an integer between 0 and 9999 in English words, as one would when
writing the number at the start of a sentence. Compound numbers from 21 to 99
are hyphenated ("twenty-one"), teens are single words ("nineteen"), a leading
unit is always spoken before "hundred" or "thousand" ("one hundred", not
"hundred"), and no "and" is inserted between a hundreds part and the
remainder ("three hundred three"). Values outside 0..9999 are rejected.

Kata catalogued at tddbuddy.com/katas/numbers-to-words; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""

_ONES = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
]

_TENS = [
    "",
    "",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
]


def _below_one_hundred(number: int) -> str:
    """Spell a value in 1..99, hyphenating compounds from 21 to 99."""
    if number < 20:
        return _ONES[number]
    tens, ones = divmod(number, 10)
    if ones == 0:
        return _TENS[tens]
    return f"{_TENS[tens]}-{_ONES[ones]}"


def number_to_words(number: int) -> str:
    """Return the English words for an integer in the range 0..9999."""
    if not 0 <= number <= 9999:
        raise ValueError(f"number must be in 0..9999, got {number}")
    if number == 0:
        return "zero"

    thousands, rest = divmod(number, 1000)
    hundreds, remainder = divmod(rest, 100)

    parts: list[str] = []
    if thousands:
        parts.append(f"{_ONES[thousands]} thousand")
    if hundreds:
        parts.append(f"{_ONES[hundreds]} hundred")
    if remainder:
        parts.append(_below_one_hundred(remainder))
    return " ".join(parts)
