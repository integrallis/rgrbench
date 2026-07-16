# Markdown-to-HTML rendering

## Overview
A renderer for a small markdown subset that turns marked-up text into HTML. It covers six constructs — paragraphs, bold, italic, headings, links, and unordered lists — together with the rules for how lines group into blocks, how the constructs nest, and how near-miss markup falls back to plain text.

## User Stories

### US-1: Lines become blocks
As a writer, I want each line of my text to become one HTML block, so that my document structure survives rendering.

- AC-1.1: Empty input produces an empty result — no HTML at all.
- AC-1.2: A line of plain text renders as a paragraph: <p>text</p>.
- AC-1.3: Each non-blank line yields exactly one block, and the blocks are joined by newlines.
- AC-1.4: Blank lines emit nothing: no empty paragraphs appear in the output.

### US-2: Inline emphasis
As a writer, I want bold and italic markup, so that emphasis carries into the output.

- AC-2.1: A span wrapped in double asterisks renders as strong emphasis inside its block: **bold** becomes <p><strong>bold</strong></p>.
- AC-2.2: A span wrapped in single underscores renders as emphasis inside its block: the word italic wrapped in underscores becomes <p><em>italic</em></p>.
- AC-2.3: The two nest: a bold span wrapping an italic span renders as <strong><em>...</em></strong>.
- AC-2.4: Inline markup renders in place, leaving surrounding plain text untouched on either side.

### US-3: Headings
As a writer, I want hash-marked headings, so that my sections get proper heading tags.

- AC-3.1: A line opening with one to six hashes followed by a space renders as <h1> through <h6>, the level matching the hash count.
- AC-3.2: A hash not followed by a space is not a heading: the line renders as an ordinary paragraph (for example, #No space renders as <p>#No space</p>).
- AC-3.3: Seven or more hashes do not form a heading; the line renders as an ordinary paragraph.
- AC-3.4: Inline emphasis renders inside heading content.

### US-4: Links
As a writer, I want bracket-and-parenthesis links, so that my references become anchors.

- AC-4.1: Link markup of the form [text](url) renders as an anchor, <a href="url">text</a>, and a link standing alone on a line still gets a paragraph wrapper.
- AC-4.2: A link renders in place within its surrounding text.
- AC-4.3: Underscores inside a link URL are not emphasis markers: the URL passes through unchanged.
- AC-4.4: Inline emphasis renders inside the link text, within the anchor.

### US-5: Unordered lists
As a writer, I want dash-marked lists, so that bullet points render as HTML lists.

- AC-5.1: A line of a dash and a space followed by text becomes a one-item unordered list: <ul><li>item</li></ul>.
- AC-5.2: Consecutive dash lines share a single <ul> wrapper; the wrapper is never repeated between adjacent items.
- AC-5.3: A blank line ends a list; a later dash line starts a new list of its own.
- AC-5.4: A dash not followed by a space is not a list item; the line renders as an ordinary paragraph.
- AC-5.5: Inline emphasis renders inside list items.
- AC-5.6: A non-dash line immediately after a list closes the list and renders as its own block.

## Traceability
```json
{
  "test_empty_input_returns_empty_string": ["AC-1.1"],
  "test_plain_text_becomes_paragraph": ["AC-1.2"],
  "test_bold_text_becomes_strong": ["AC-2.1"],
  "test_italic_text_becomes_em": ["AC-2.2"],
  "test_bold_and_italic_nest": ["AC-2.3"],
  "test_inline_markup_within_surrounding_text": ["AC-2.4"],
  "test_heading_levels_one_through_six": ["AC-3.1"],
  "test_hash_without_space_is_a_paragraph": ["AC-3.2"],
  "test_seven_hashes_is_a_paragraph": ["AC-3.3"],
  "test_heading_content_allows_inline_markup": ["AC-3.4"],
  "test_link_becomes_anchor_inside_paragraph": ["AC-4.1"],
  "test_link_within_sentence": ["AC-4.2"],
  "test_link_url_underscores_are_not_italicised": ["AC-4.3"],
  "test_link_text_allows_inline_markup": ["AC-4.4"],
  "test_single_list_item": ["AC-5.1"],
  "test_consecutive_list_items_share_one_ul": ["AC-5.2"],
  "test_blank_line_separates_two_lists": ["AC-5.3"],
  "test_dash_without_space_is_a_paragraph": ["AC-5.4"],
  "test_list_item_allows_inline_markup": ["AC-5.5"],
  "test_multiple_lines_become_multiple_blocks": ["AC-1.3"],
  "test_blank_lines_emit_nothing": ["AC-1.4"],
  "test_list_followed_by_paragraph": ["AC-5.6"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
