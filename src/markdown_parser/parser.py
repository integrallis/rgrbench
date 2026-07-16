"""Markdown-to-HTML rendering for the subset described in the package docstring."""

import re

_HEADER = re.compile(r"^(#{1,6}) (.*)$")
_LINK = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITALIC = re.compile(r"_(.+?)_")


def _emphasis(text: str) -> str:
    """Apply bold then italic replacements to a text fragment."""
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    return _ITALIC.sub(r"<em>\1</em>", text)


def _inline(text: str) -> str:
    """Render links, bold, and italic within a single line of text.

    Links are converted first and shielded behind placeholders so that
    emphasis markers inside URLs are left untouched, while emphasis inside
    the link text itself is still rendered.
    """
    anchors: list[str] = []

    def _stash(match: re.Match[str]) -> str:
        anchors.append(f'<a href="{match.group(2)}">{_emphasis(match.group(1))}</a>')
        return f"\x00{len(anchors) - 1}\x00"

    text = _emphasis(_LINK.sub(_stash, text))
    for index, anchor in enumerate(anchors):
        text = text.replace(f"\x00{index}\x00", anchor)
    return text


def parse(markdown: str) -> str:
    """Convert markdown text to HTML.

    Each non-blank line becomes one block (heading, list item, or
    paragraph). Consecutive list items are wrapped in a single ``<ul>``.
    Blocks are joined with newlines; blank lines produce no output but do
    terminate a list.
    """
    blocks: list[str] = []
    list_items: list[str] = []

    def _flush_list() -> None:
        if list_items:
            blocks.append("<ul>" + "".join(list_items) + "</ul>")
            list_items.clear()

    for line in markdown.split("\n"):
        if line.strip() == "":
            _flush_list()
            continue
        if line.startswith("- "):
            list_items.append(f"<li>{_inline(line[2:])}</li>")
            continue
        _flush_list()
        header = _HEADER.match(line)
        if header:
            level = len(header.group(1))
            blocks.append(f"<h{level}>{_inline(header.group(2))}</h{level}>")
        else:
            blocks.append(f"<p>{_inline(line)}</p>")
    _flush_list()
    return "\n".join(blocks)
