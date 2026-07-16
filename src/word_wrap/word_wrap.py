"""Word Wrap kata - wraps text at a column width, breaking at word boundaries."""


class WordWrap:
    """Static class for wrapping text"""

    @staticmethod
    def wrap(text: str | None, column_width: int) -> str:
        """Wrap text at the column width.

        Lines break at the last space that fits within the width; a word longer
        than the width is split at the width. Existing newlines are preserved and
        wrapping restarts after each one. None and whitespace-only text wrap to "".
        """
        if text is None:
            return ""
        if "\n" in text:
            return "\n".join(
                WordWrap.wrap(segment, column_width) for segment in text.split("\n")
            )
        if text.strip() == "":
            return ""
        return WordWrap._wrap_line(text, column_width)

    @staticmethod
    def _wrap_line(line: str, column_width: int) -> str:
        if len(line) <= column_width:
            return line
        window = line[: column_width + 1]
        break_at = window.rfind(" ")
        if break_at > 0:
            head = line[:break_at]
            rest = line[break_at + 1 :].lstrip(" ")
        else:
            head = line[:column_width]
            rest = line[column_width:]
        if rest.strip() == "":
            return head
        return head + "\n" + WordWrap._wrap_line(rest, column_width)
