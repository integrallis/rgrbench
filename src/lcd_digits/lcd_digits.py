class LCDDigits:
    DIGIT_HEIGHT_DIMENSION: int = 1
    LCD_DIGITS_MAP: list[list[str]] = [
        ["._.", "|.|", "|_|"],  # 0
        ["...", "..|", "..|"],  # 1
        ["._.", "._|", "|_."],  # 2
        ["._.", "._|", "._|"],  # 3
        ["...", "|_|", "..|"],  # 4
        ["._.", "|_.", "._|"],  # 5
        ["._.", "|_.", "|_|"],  # 6
        ["._.", "..|", "..|"],  # 7
        ["._.", "|_|", "|_|"],  # 8
        ["._.", "|_|", "..|"],  # 9
    ]

    @staticmethod
    def get_digits(number: int) -> str:
        number_array = LCDDigits._convert_integer_to_array(number)

        output = []
        for digit_height in range(len(LCDDigits.LCD_DIGITS_MAP[0])):
            line = ""
            for number_index in range(len(number_array)):
                digit_value = LCDDigits._convert_char_array_to_integer(
                    number_array, number_index
                )
                line += LCDDigits._get_digit_line(digit_value, digit_height)
            output.append(line)

        return "\n".join(output) + "\n"

    @staticmethod
    def _convert_char_array_to_integer(number_array: str, number_index: int) -> int:
        return int(number_array[number_index])

    @staticmethod
    def _get_digit_line(number: int, digit_height: int) -> str:
        return LCDDigits.LCD_DIGITS_MAP[number][digit_height]

    @staticmethod
    def _convert_integer_to_array(number: int) -> str:
        return str(number)
