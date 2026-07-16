"""Tests for the Greeting kata.

greet handles a single name, None, shouted (all-uppercase) names, lists of
two or more names with "and" and an Oxford comma, mixed normal and shouted
names, and the comma-splitting / quote-escaping extensions.
"""


def test_greets_a_single_name() -> None:
    """Test 1: greet("Bob") returns "Hello, Bob." """
    from greeting import greet

    assert greet("Bob") == "Hello, Bob."


def test_greets_none_as_a_friend() -> None:
    """Test 2: A missing name greets an anonymous friend"""
    from greeting import greet

    assert greet(None) == "Hello, my friend."


def test_shouts_back_at_a_shouted_name() -> None:
    """Test 3: An all-uppercase name gets a shouted greeting"""
    from greeting import greet

    assert greet("JERRY") == "HELLO JERRY!"


def test_greets_two_names_with_and() -> None:
    """Test 4: Two names are joined with "and" """
    from greeting import greet

    assert greet(["Jill", "Jane"]) == "Hello, Jill and Jane."


def test_greets_three_names_with_oxford_comma() -> None:
    """Test 5: Three names use commas and an Oxford comma before "and" """
    from greeting import greet

    assert greet(["Amy", "Brian", "Charlotte"]) == "Hello, Amy, Brian, and Charlotte."


def test_separates_shouted_names_from_normal_names() -> None:
    """Test 6: Mixed input yields a normal greeting followed by a shout"""
    from greeting import greet

    assert (
        greet(["Amy", "BRIAN", "Charlotte"])
        == "Hello, Amy and Charlotte. AND HELLO BRIAN!"
    )


def test_greets_a_single_name_in_a_list() -> None:
    """Test 7: A one-element list behaves like a single name"""
    from greeting import greet

    assert greet(["Bob"]) == "Hello, Bob."


def test_greets_four_names_with_oxford_comma() -> None:
    """Test 8: Four names keep the comma-separated Oxford style"""
    from greeting import greet

    assert (
        greet(["Amy", "Brian", "Charlotte", "Dan"])
        == "Hello, Amy, Brian, Charlotte, and Dan."
    )


def test_shouts_at_two_shouted_names_together() -> None:
    """Test 9: A list of only shouted names is answered with one shout"""
    from greeting import greet

    assert greet(["BRIAN", "JERRY"]) == "HELLO BRIAN AND JERRY!"


def test_shouts_at_a_single_shouted_name_in_a_list() -> None:
    """Test 10: A one-element list with a shouted name is shouted back"""
    from greeting import greet

    assert greet(["JERRY"]) == "HELLO JERRY!"


def test_mixes_one_normal_and_one_shouted_name() -> None:
    """Test 11: One normal and one shouted name produce both greetings"""
    from greeting import greet

    assert greet(["Amy", "BRIAN"]) == "Hello, Amy. AND HELLO BRIAN!"


def test_mixes_multiple_normal_and_multiple_shouted_names() -> None:
    """Test 12: Normal and shouted names each keep their joining rules"""
    from greeting import greet

    assert (
        greet(["Amy", "BRIAN", "Charlotte", "DAN"])
        == "Hello, Amy and Charlotte. AND HELLO BRIAN AND DAN!"
    )


def test_splits_comma_delimited_entries() -> None:
    """Test 13: An entry containing a comma is split into separate names"""
    from greeting import greet

    assert greet(["Bob", "Charlie, Dianne"]) == "Hello, Bob, Charlie, and Dianne."


def test_quoted_entries_keep_their_commas() -> None:
    """Test 14: A double-quoted entry is one name with its comma intact"""
    from greeting import greet

    assert greet(["Bob", '"Charlie, Dianne"']) == "Hello, Bob and Charlie, Dianne."


def test_greets_an_empty_list_as_a_friend() -> None:
    """Test 15: A list with no names greets an anonymous friend"""
    from greeting import greet

    assert greet([]) == "Hello, my friend."


def test_lowercase_name_is_not_shouted() -> None:
    """Test 16: A lowercase name gets the normal greeting"""
    from greeting import greet

    assert greet("bob") == "Hello, bob."


def test_mixed_case_name_is_not_shouted() -> None:
    """Test 17: A mixed-case name is not treated as shouting"""
    from greeting import greet

    assert greet("JeRRy") == "Hello, JeRRy."


def test_split_names_are_stripped_of_surrounding_spaces() -> None:
    """Test 18: Names split from a comma entry drop surrounding spaces"""
    from greeting import greet

    assert greet(["Charlie , Dianne"]) == "Hello, Charlie and Dianne."


def test_entry_with_only_an_opening_quote_is_not_quoted() -> None:
    """Test 19: An entry must be wrapped in quotes to keep them; a lone opening quote stays"""
    from greeting import greet

    assert greet(['"Bob']) == 'Hello, "Bob.'


def test_empty_quoted_entry_yields_an_empty_name() -> None:
    """Test 20: A bare pair of double quotes has its quotes removed, leaving an empty name"""
    from greeting import greet

    assert greet(['""']) == "Hello, ."
