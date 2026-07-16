"""Markdown Parser kata: render a small markdown subset to HTML.

`parse(markdown)` converts a markdown string into an HTML string
supporting exactly six constructs:

- Paragraphs: a plain text line becomes ``<p>text</p>``.
- Bold: ``**text**`` becomes ``<strong>text</strong>``.
- Italic: ``_text_`` becomes ``<em>text</em>``.
- Headings: ``#`` through ``######`` followed by a single space become
  ``<h1>``..``<h6>``. Without the space (or with seven or more hashes)
  the line is an ordinary paragraph.
- Links: ``[text](url)`` becomes ``<a href="url">text</a>``.
- Unordered lists: consecutive lines starting with ``"- "`` become one
  ``<ul>`` containing an ``<li>`` per line, with no tags repeated
  between items.

Inline formats nest (bold, italic, and links may appear inside any block
and inside each other), each non-blank input line produces one HTML
block, blocks are joined with newlines, blank lines end a list and emit
nothing, and empty input yields the empty string.

Kata catalogued at tddbuddy.com/katas/markdown-parser; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""

from markdown_parser.parser import parse

__all__ = ["parse"]
