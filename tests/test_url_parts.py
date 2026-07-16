"""
Tests for the URL Parts kata (tddbuddy.com/katas/url-parts).
Expected decompositions come from the kata's example table plus the stated
grammar (query string and anchor are captured but excluded from the path).
"""


def test_url_with_subdomain_and_default_http_port() -> None:
    """Test 1: http://foo.bar.com/foobar.html splits into http/foo/bar.com/80
    with path foobar.html (kata example)"""
    from url_parts import parse_url

    parts = parse_url("http://foo.bar.com/foobar.html")

    assert parts.protocol == "http"
    assert parts.subdomain == "foo"
    assert parts.domain == "bar.com"
    assert parts.port == 80
    assert parts.path == "foobar.html"


def test_url_with_explicit_port_and_nested_path() -> None:
    """Test 2: https://www.foobar.com:8080/download/install.exe keeps its
    explicit port and full path (kata example)"""
    from url_parts import parse_url

    parts = parse_url("https://www.foobar.com:8080/download/install.exe")

    assert parts.protocol == "https"
    assert parts.subdomain == "www"
    assert parts.domain == "foobar.com"
    assert parts.port == 8080
    assert parts.path == "download/install.exe"


def test_ftp_url_without_subdomain() -> None:
    """Test 3: ftp://foo.com:9000/files has an empty subdomain (kata example)"""
    from url_parts import parse_url

    parts = parse_url("ftp://foo.com:9000/files")

    assert parts.protocol == "ftp"
    assert parts.subdomain == ""
    assert parts.domain == "foo.com"
    assert parts.port == 9000
    assert parts.path == "files"


def test_localhost_with_anchor() -> None:
    """Test 4: https://localhost/index.html#footer treats localhost as the
    domain and excludes the anchor from the path (kata example)"""
    from url_parts import parse_url

    parts = parse_url("https://localhost/index.html#footer")

    assert parts.protocol == "https"
    assert parts.subdomain == ""
    assert parts.domain == "localhost"
    assert parts.port == 443
    assert parts.path == "index.html"
    assert parts.anchor == "footer"


def test_sftp_default_port() -> None:
    """Test 5: sftp defaults to port 22 when none is given"""
    from url_parts import parse_url

    assert parse_url("sftp://foo.com/backup").port == 22


def test_ftp_default_port() -> None:
    """Test 6: ftp defaults to port 21 when none is given"""
    from url_parts import parse_url

    assert parse_url("ftp://foo.com/files").port == 21


def test_explicit_port_overrides_default() -> None:
    """Test 7: An explicit port wins over the protocol default"""
    from url_parts import parse_url

    assert parse_url("http://foo.com:8080/index.html").port == 8080


def test_multi_level_subdomain() -> None:
    """Test 8: Everything before the domain-plus-TLD is the subdomain"""
    from url_parts import parse_url

    parts = parse_url("http://a.b.bar.com/page")

    assert parts.subdomain == "a.b"
    assert parts.domain == "bar.com"


def test_url_without_path() -> None:
    """Test 9: A URL with no path yields an empty path"""
    from url_parts import parse_url

    assert parse_url("http://foo.com").path == ""


def test_url_with_trailing_slash_has_empty_path() -> None:
    """Test 10: A bare trailing slash yields an empty path"""
    from url_parts import parse_url

    assert parse_url("http://foo.com/").path == ""


def test_query_string_is_captured_and_excluded_from_path() -> None:
    """Test 11: The query string is its own part, not part of the path"""
    from url_parts import parse_url

    parts = parse_url("https://foo.com/search?q=kata&lang=en")

    assert parts.path == "search"
    assert parts.query == "q=kata&lang=en"
    assert parts.anchor == ""


def test_anchor_is_captured_and_excluded_from_path() -> None:
    """Test 12: The anchor is its own part, not part of the path"""
    from url_parts import parse_url

    parts = parse_url("https://foo.com/docs/guide.html#section")

    assert parts.path == "docs/guide.html"
    assert parts.query == ""
    assert parts.anchor == "section"


def test_query_string_and_anchor_together() -> None:
    """Test 13: Query string and anchor can both be present"""
    from url_parts import parse_url

    parts = parse_url("https://www.foo.com/search?q=1&x=2#top")

    assert parts.subdomain == "www"
    assert parts.domain == "foo.com"
    assert parts.path == "search"
    assert parts.query == "q=1&x=2"
    assert parts.anchor == "top"


def test_query_string_directly_after_host() -> None:
    """Test 14: A query string may follow the host without any path"""
    from url_parts import parse_url

    parts = parse_url("http://foo.com?x=1")

    assert parts.domain == "foo.com"
    assert parts.path == ""
    assert parts.query == "x=1"


def test_all_supported_top_level_domains() -> None:
    """Test 15: .com, .net, .org, .int, .edu, .gov and .mil are all accepted"""
    from url_parts import parse_url

    for tld in ("com", "net", "org", "int", "edu", "gov", "mil"):
        parts = parse_url(f"http://www.example.{tld}/index.html")
        assert parts.domain == f"example.{tld}"
        assert parts.subdomain == "www"


def test_unsupported_protocol_raises() -> None:
    """Test 16: Only http, https, ftp and sftp are supported; the error names
    the offending protocol"""
    import pytest

    from url_parts import parse_url

    with pytest.raises(ValueError) as excinfo:
        parse_url("gopher://foo.com/files")
    assert str(excinfo.value) == "Unsupported protocol: 'gopher'"


def test_url_without_protocol_marker_raises() -> None:
    """Test 17: A URL without '://' is rejected as malformed"""
    import pytest

    from url_parts import parse_url

    with pytest.raises(ValueError) as excinfo:
        parse_url("foo.com/index.html")
    assert str(excinfo.value) == "Malformed URL, missing '://': 'foo.com/index.html'"


def test_unsupported_top_level_domain_raises() -> None:
    """Test 18: A dotted host with an unsupported TLD is rejected"""
    import pytest

    from url_parts import parse_url

    with pytest.raises(ValueError):
        parse_url("http://foo.xyz/index.html")


def test_local_hostname_with_port_and_path() -> None:
    """Test 19: Local host names work with explicit ports and paths"""
    from url_parts import parse_url

    parts = parse_url("http://localhost:3000/api")

    assert parts.subdomain == ""
    assert parts.domain == "localhost"
    assert parts.port == 3000
    assert parts.path == "api"


def test_protocol_is_split_at_the_first_marker() -> None:
    """Test 20: A '://' inside the query string does not confuse the protocol
    split; the query keeps the embedded URL verbatim"""
    from url_parts import parse_url

    parts = parse_url("http://foo.com/redirect?target=https://bar.com/page")

    assert parts.protocol == "http"
    assert parts.domain == "foo.com"
    assert parts.path == "redirect"
    assert parts.query == "target=https://bar.com/page"


def test_invalid_port_raises_naming_the_port_text() -> None:
    """Test 21: A non-numeric port is rejected, and everything after the first
    colon counts as the port text"""
    import pytest

    from url_parts import parse_url

    with pytest.raises(ValueError) as excinfo:
        parse_url("http://foo.com:8080:9090/path")
    assert str(excinfo.value) == "Invalid port: '8080:9090'"


def test_url_with_empty_host_raises() -> None:
    """Test 22: A URL with nothing between '://' and the path is rejected"""
    import pytest

    from url_parts import parse_url

    with pytest.raises(ValueError) as excinfo:
        parse_url("http:///index.html")
    assert str(excinfo.value) == "Missing host"


def test_unsupported_tld_error_names_the_tld() -> None:
    """Test 23: The unsupported-TLD error names the host's last label, even
    for multi-label hosts"""
    import pytest

    from url_parts import parse_url

    with pytest.raises(ValueError) as excinfo:
        parse_url("http://www.foo.xyz/index.html")
    assert str(excinfo.value) == "Unsupported top-level domain: 'xyz'"
