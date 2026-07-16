"""Roman Numerals Converter"""


def to_roman(number: int) -> str:
    """Convert integer to Roman numeral"""
    # Mapping of values to Roman numerals in descending order
    val_map = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]

    result = ""
    for value, numeral in val_map:
        count = number // value
        if count:
            result += numeral * count
            number -= value * count

    return result
