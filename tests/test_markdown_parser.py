"""Markdown Parser kata - render a small markdown subset to HTML.

Covers the six required constructs (paragraphs, bold, italic, headings,
links, unordered lists), their nesting, and the edge rules for heading
syntax, list grouping, blank lines, and empty input.
"""


def test_empty_input_returns_empty_string() -> None:
    """Test 1: Empty input returns an empty string

    The spec requires empty input to produce no HTML at all.
    """
    from markdown_parser import parse

    # GIVEN / WHEN
    result = parse("")

    # THEN
    assert result == ""


def test_plain_text_becomes_paragraph() -> None:
    """Test 2: Plain text becomes a paragraph

    A line with no markup renders as <p>text</p>.
    """
    from markdown_parser import parse

    assert parse("Hello") == "<p>Hello</p>"


def test_bold_text_becomes_strong() -> None:
    """Test 3: **text** becomes <strong>text</strong> inside a paragraph"""
    from markdown_parser import parse

    assert parse("**bold**") == "<p><strong>bold</strong></p>"


def test_italic_text_becomes_em() -> None:
    """Test 4: _text_ becomes <em>text</em> inside a paragraph"""
    from markdown_parser import parse

    assert parse("_italic_") == "<p><em>italic</em></p>"


def test_bold_and_italic_nest() -> None:
    """Test 5: **_text_** nests strong around em

    The spec's nesting example: bold wrapping italic.
    """
    from markdown_parser import parse

    result = parse("**_bold italic_**")

    assert result == "<p><strong><em>bold italic</em></strong></p>"


def test_inline_markup_within_surrounding_text() -> None:
    """Test 6: Inline markup renders in place within surrounding plain text"""
    from markdown_parser import parse

    result = parse("a **b** and _c_ here")

    assert result == "<p>a <strong>b</strong> and <em>c</em> here</p>"


def test_heading_levels_one_through_six() -> None:
    """Test 7: # through ###### produce <h1> through <h6>"""
    from markdown_parser import parse

    for level in range(1, 7):
        assert parse("#" * level + " Title") == f"<h{level}>Title</h{level}>"


def test_hash_without_space_is_a_paragraph() -> None:
    """Test 8: A hash not followed by a space is not a heading

    The spec: `#No space` renders as <p>#No space</p>.
    """
    from markdown_parser import parse

    assert parse("#No space") == "<p>#No space</p>"


def test_seven_hashes_is_a_paragraph() -> None:
    """Test 9: Seven or more hashes do not form a heading"""
    from markdown_parser import parse

    assert parse("####### Too deep") == "<p>####### Too deep</p>"


def test_heading_content_allows_inline_markup() -> None:
    """Test 10: Inline formats render inside headings"""
    from markdown_parser import parse

    assert parse("## The **End**") == "<h2>The <strong>End</strong></h2>"


def test_link_becomes_anchor_inside_paragraph() -> None:
    """Test 11: [text](url) becomes an anchor tag

    The spec example: a bare link line still gets a paragraph wrapper.
    """
    from markdown_parser import parse

    result = parse("[click](http://example.com)")

    assert result == '<p><a href="http://example.com">click</a></p>'


def test_link_within_sentence() -> None:
    """Test 12: A link renders in place within surrounding text"""
    from markdown_parser import parse

    result = parse("see [docs](http://example.com/a) now")

    assert result == '<p>see <a href="http://example.com/a">docs</a> now</p>'


def test_link_url_underscores_are_not_italicised() -> None:
    """Test 13: Underscores inside a link URL are not emphasis markers"""
    from markdown_parser import parse

    result = parse("[x](http://example.com/a_b_c)")

    assert result == '<p><a href="http://example.com/a_b_c">x</a></p>'


def test_link_text_allows_inline_markup() -> None:
    """Test 14: Bold inside link text renders within the anchor"""
    from markdown_parser import parse

    result = parse("[**bold link**](http://example.com)")

    assert result == '<p><a href="http://example.com"><strong>bold link</strong></a></p>'


def test_single_list_item() -> None:
    """Test 15: A single dash line becomes a one-item unordered list"""
    from markdown_parser import parse

    assert parse("- item") == "<ul><li>item</li></ul>"


def test_consecutive_list_items_share_one_ul() -> None:
    """Test 16: Consecutive dash lines share a single <ul> wrapper

    The spec forbids repeating <ul> tags between adjacent items.
    """
    from markdown_parser import parse

    result = parse("- one\n- two\n- three")

    assert result == "<ul><li>one</li><li>two</li><li>three</li></ul>"


def test_blank_line_separates_two_lists() -> None:
    """Test 17: A blank line ends a list; a later dash line starts a new one"""
    from markdown_parser import parse

    result = parse("- one\n\n- two")

    assert result == "<ul><li>one</li></ul>\n<ul><li>two</li></ul>"


def test_dash_without_space_is_a_paragraph() -> None:
    """Test 18: A dash not followed by a space is not a list item"""
    from markdown_parser import parse

    assert parse("-dash") == "<p>-dash</p>"


def test_list_item_allows_inline_markup() -> None:
    """Test 19: Inline formats render inside list items"""
    from markdown_parser import parse

    result = parse("- a _quiet_ item")

    assert result == "<ul><li>a <em>quiet</em> item</li></ul>"


def test_multiple_lines_become_multiple_blocks() -> None:
    """Test 20: Each non-blank line yields one block, joined by newlines"""
    from markdown_parser import parse

    result = parse("# Title\nFirst paragraph\nSecond paragraph")

    assert result == "<h1>Title</h1>\n<p>First paragraph</p>\n<p>Second paragraph</p>"


def test_blank_lines_emit_nothing() -> None:
    """Test 21: Blank lines produce no empty paragraphs"""
    from markdown_parser import parse

    assert parse("First\n\nSecond") == "<p>First</p>\n<p>Second</p>"


def test_list_followed_by_paragraph() -> None:
    """Test 22: A non-dash line immediately after a list closes the list"""
    from markdown_parser import parse

    result = parse("- item\nafter")

    assert result == "<ul><li>item</li></ul>\n<p>after</p>"
