"""
Tests for the URL Shortener kata (tddbuddy.com/katas/url-shortener).
Identifiers are deterministic: sequential base-36 by default (first URL is '0',
eleventh is 'a', thirty-seventh is '10'), or an injected generator.
"""


def test_first_short_url_uses_identifier_zero() -> None:
    """Test 1: The first shortened URL gets base-36 identifier '0'"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()

    assert shortener.shorten("https://example.com/page") == "https://short.url/0"


def test_identifiers_are_sequential() -> None:
    """Test 2: The second distinct URL gets identifier '1'"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()
    shortener.shorten("https://example.com/one")

    assert shortener.shorten("https://example.com/two") == "https://short.url/1"


def test_eleventh_identifier_is_a() -> None:
    """Test 3: The eleventh URL gets identifier 'a' (base-36 rollover)"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()
    for number in range(10):
        shortener.shorten(f"https://example.com/{number}")

    assert shortener.shorten("https://example.com/eleventh") == "https://short.url/a"


def test_thirty_seventh_identifier_is_10() -> None:
    """Test 4: The thirty-seventh URL gets identifier '10' (two base-36 digits)"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()
    for number in range(36):
        shortener.shorten(f"https://example.com/{number}")

    assert (
        shortener.shorten("https://example.com/thirty-seventh")
        == "https://short.url/10"
    )


def test_custom_base_url() -> None:
    """Test 5: Short URLs are built on the configured base URL"""
    from url_shortener import UrlShortener

    shortener = UrlShortener(base_url="https://sho.rt/")

    assert shortener.shorten("https://example.com/page") == "https://sho.rt/0"


def test_injected_identifier_generator_is_used() -> None:
    """Test 6: An injected identifier generator drives short URL creation"""
    from url_shortener import UrlShortener

    shortener = UrlShortener(id_generator=iter(["abc1234", "xyz9876"]))

    assert shortener.shorten("https://example.com/a") == "https://short.url/abc1234"
    assert shortener.shorten("https://example.com/b") == "https://short.url/xyz9876"


def test_translate_short_url_returns_long_url() -> None:
    """Test 7: Translating a short URL returns the original long URL"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()
    short_url = shortener.shorten("https://example.com/page")

    assert shortener.translate(short_url) == "https://example.com/page"


def test_translate_long_url_returns_short_url() -> None:
    """Test 8: Translating a known long URL returns its short URL"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()
    short_url = shortener.shorten("https://example.com/page")

    assert shortener.translate("https://example.com/page") == short_url


def test_duplicate_long_url_returns_existing_short_url() -> None:
    """Test 9: Shortening the same long URL twice reuses the mapping"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()
    first = shortener.shorten("https://example.com/page")
    second = shortener.shorten("https://example.com/page")

    assert first == second


def test_duplicate_long_url_does_not_consume_an_identifier() -> None:
    """Test 10: A duplicate does not advance the identifier sequence"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()
    shortener.shorten("https://example.com/one")
    shortener.shorten("https://example.com/one")

    assert shortener.shorten("https://example.com/two") == "https://short.url/1"


def test_visits_start_at_zero() -> None:
    """Test 11: A freshly shortened URL has zero visits"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()
    short_url = shortener.shorten("https://example.com/page")

    assert shortener.stats(short_url).visits == 0


def test_translating_short_url_counts_visits() -> None:
    """Test 12: Each translation of a short URL increments its visit count"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()
    short_url = shortener.shorten("https://example.com/page")
    shortener.translate(short_url)
    shortener.translate(short_url)

    assert shortener.stats(short_url).visits == 2


def test_translating_long_url_does_not_count_visits() -> None:
    """Test 13: Visits track short URL accesses only"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()
    shortener.shorten("https://example.com/page")
    shortener.translate("https://example.com/page")

    assert shortener.stats("https://example.com/page").visits == 0


def test_stats_accepts_short_url() -> None:
    """Test 14: Stats looked up by short URL report both URLs and the count"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()
    short_url = shortener.shorten("https://example.com/page")
    shortener.translate(short_url)
    record = shortener.stats(short_url)

    assert record.short_url == short_url
    assert record.long_url == "https://example.com/page"
    assert record.visits == 1


def test_stats_accepts_long_url() -> None:
    """Test 15: Stats looked up by long URL report the same record"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()
    short_url = shortener.shorten("https://example.com/page")
    record = shortener.stats("https://example.com/page")

    assert record.short_url == short_url
    assert record.long_url == "https://example.com/page"


def test_url_without_scheme_is_rejected() -> None:
    """Test 16: A URL without an http(s) scheme raises ValueError"""
    import pytest

    from url_shortener import UrlShortener

    with pytest.raises(ValueError) as excinfo:
        UrlShortener().shorten("example.com/page")
    assert str(excinfo.value) == "Invalid URL: 'example.com/page'"


def test_scheme_only_url_is_rejected() -> None:
    """Test 17: A bare scheme with nothing after it raises ValueError"""
    import pytest

    from url_shortener import UrlShortener

    with pytest.raises(ValueError):
        UrlShortener().shorten("https://")


def test_translate_unknown_url_raises() -> None:
    """Test 18: Translating an unknown URL raises ValueError"""
    import pytest

    from url_shortener import UrlShortener

    with pytest.raises(ValueError) as excinfo:
        UrlShortener().translate("https://short.url/0")
    assert str(excinfo.value) == "Unknown URL: 'https://short.url/0'"


def test_stats_for_unknown_url_raises() -> None:
    """Test 19: Requesting stats for an unknown URL raises ValueError"""
    import pytest

    from url_shortener import UrlShortener

    with pytest.raises(ValueError) as excinfo:
        UrlShortener().stats("https://example.com/never-shortened")
    assert str(excinfo.value) == "Unknown URL: 'https://example.com/never-shortened'"


def test_history_records_injected_clock_timestamps_in_order() -> None:
    """Test 20: With an injected clock, each visit's timestamp is recorded"""
    from datetime import datetime, timedelta

    from url_shortener import UrlShortener

    now = [datetime(2026, 1, 1, 12, 0)]
    shortener = UrlShortener(clock=lambda: now[0])
    short_url = shortener.shorten("https://example.com/page")
    shortener.translate(short_url)
    now[0] += timedelta(minutes=5)
    shortener.translate(short_url)

    assert shortener.stats(short_url).history == (
        datetime(2026, 1, 1, 12, 0),
        datetime(2026, 1, 1, 12, 5),
    )


def test_history_is_empty_without_a_clock() -> None:
    """Test 21: Without an injected clock, visits are counted but not timestamped"""
    from url_shortener import UrlShortener

    shortener = UrlShortener()
    short_url = shortener.shorten("https://example.com/page")
    shortener.translate(short_url)
    record = shortener.stats(short_url)

    assert record.visits == 1
    assert record.history == ()


def test_log_lists_urls_visits_and_history() -> None:
    """Test 22: The log summary shows short URL, long URL, visit count and
    every access timestamp"""
    from datetime import datetime

    from url_shortener import UrlShortener

    shortener = UrlShortener(clock=lambda: datetime(2026, 1, 1, 12, 0))
    short_url = shortener.shorten("https://example.com/page")
    shortener.translate(short_url)

    assert shortener.log(short_url) == (
        "short_url: https://short.url/0\n"
        "long_url: https://example.com/page\n"
        "visits: 1\n"
        "2026-01-01 12:00:00"
    )
