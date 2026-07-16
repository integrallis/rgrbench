"""Rate Limiter kata - sliding-window request throttling with an injected clock.

Covers quota enforcement, per-client isolation, sliding-window expiry
(including the exact window boundary), the rule that denied requests
consume no quota, and constructor validation. All tests drive time
through an injected clock; no wall-clock time is used.
"""


def test_first_request_is_allowed() -> None:
    """Test 1: A fresh client's first request is allowed"""
    from rate_limiter import RateLimiter

    # GIVEN
    limiter = RateLimiter(3, 10.0, lambda: 0.0)

    # WHEN / THEN
    assert limiter.allow_request("alice") is True


def test_requests_up_to_the_limit_are_allowed() -> None:
    """Test 2: All requests within the quota return True

    Spec scenario: three requests in seconds 0-2 all succeed.
    """
    from rate_limiter import RateLimiter

    # GIVEN
    now = {"time": 0.0}
    limiter = RateLimiter(3, 10.0, lambda: now["time"])

    # WHEN / THEN
    for second in (0.0, 1.0, 2.0):
        now["time"] = second
        assert limiter.allow_request("alice") is True


def test_request_beyond_the_limit_is_denied() -> None:
    """Test 3: The request after the quota is exhausted returns False

    Spec scenario: the fourth request at second 3 is denied.
    """
    from rate_limiter import RateLimiter

    # GIVEN
    now = {"time": 0.0}
    limiter = RateLimiter(3, 10.0, lambda: now["time"])
    for second in (0.0, 1.0, 2.0):
        now["time"] = second
        limiter.allow_request("alice")

    # WHEN
    now["time"] = 3.0

    # THEN
    assert limiter.allow_request("alice") is False


def test_clients_have_independent_quotas() -> None:
    """Test 4: One client exhausting its quota does not affect another

    Spec scenario: alice is denied at second 3 while bob is approved.
    """
    from rate_limiter import RateLimiter

    # GIVEN
    now = {"time": 0.0}
    limiter = RateLimiter(3, 10.0, lambda: now["time"])
    for second in (0.0, 1.0, 2.0):
        now["time"] = second
        limiter.allow_request("alice")

    # WHEN
    now["time"] = 3.0

    # THEN
    assert limiter.allow_request("alice") is False
    assert limiter.allow_request("bob") is True


def test_quota_refreshes_when_old_requests_expire() -> None:
    """Test 5: Requests older than the window stop counting

    Spec scenario: at second 11 alice's earliest requests have expired,
    so she is allowed again.
    """
    from rate_limiter import RateLimiter

    # GIVEN
    now = {"time": 0.0}
    limiter = RateLimiter(3, 10.0, lambda: now["time"])
    for second in (0.0, 1.0, 2.0):
        now["time"] = second
        limiter.allow_request("alice")

    # WHEN
    now["time"] = 11.0

    # THEN
    assert limiter.allow_request("alice") is True


def test_request_expires_at_exactly_one_window() -> None:
    """Test 6: A request aged exactly time_window no longer counts"""
    from rate_limiter import RateLimiter

    # GIVEN
    now = {"time": 0.0}
    limiter = RateLimiter(1, 10.0, lambda: now["time"])
    limiter.allow_request("alice")

    # WHEN
    now["time"] = 10.0

    # THEN
    assert limiter.allow_request("alice") is True


def test_request_still_counts_just_inside_the_window() -> None:
    """Test 7: A request aged just under time_window still counts"""
    from rate_limiter import RateLimiter

    # GIVEN
    now = {"time": 0.0}
    limiter = RateLimiter(1, 10.0, lambda: now["time"])
    limiter.allow_request("alice")

    # WHEN
    now["time"] = 9.999

    # THEN
    assert limiter.allow_request("alice") is False


def test_window_slides_rather_than_resetting() -> None:
    """Test 8: Expiry is per-request, not a fixed reset period

    With requests at 0, 4, and 8 (limit 3, window 10), second 9 is
    denied, second 10 frees exactly one slot, and the slot is consumed
    immediately.
    """
    from rate_limiter import RateLimiter

    # GIVEN
    now = {"time": 0.0}
    limiter = RateLimiter(3, 10.0, lambda: now["time"])
    for second in (0.0, 4.0, 8.0):
        now["time"] = second
        assert limiter.allow_request("alice") is True

    # WHEN / THEN
    now["time"] = 9.0
    assert limiter.allow_request("alice") is False
    now["time"] = 10.0
    assert limiter.allow_request("alice") is True
    assert limiter.allow_request("alice") is False


def test_denied_requests_consume_no_quota() -> None:
    """Test 9: A rejected request is not recorded against the window

    With limit 1 and window 10: allowed at 0, denied at 5, and allowed
    again at 10 - the denial at 5 must not have started a new window.
    """
    from rate_limiter import RateLimiter

    # GIVEN
    now = {"time": 0.0}
    limiter = RateLimiter(1, 10.0, lambda: now["time"])
    assert limiter.allow_request("alice") is True

    # WHEN
    now["time"] = 5.0
    assert limiter.allow_request("alice") is False

    # THEN
    now["time"] = 10.0
    assert limiter.allow_request("alice") is True


def test_limit_of_one_allows_exactly_one_per_window() -> None:
    """Test 10: max_requests=1 permits a single request per window"""
    from rate_limiter import RateLimiter

    # GIVEN
    now = {"time": 0.0}
    limiter = RateLimiter(1, 5.0, lambda: now["time"])

    # WHEN / THEN
    assert limiter.allow_request("alice") is True
    now["time"] = 4.0
    assert limiter.allow_request("alice") is False
    now["time"] = 5.0
    assert limiter.allow_request("alice") is True


def test_interleaved_clients_keep_separate_windows() -> None:
    """Test 11: Interleaved traffic from two clients is tracked separately"""
    from rate_limiter import RateLimiter

    # GIVEN
    now = {"time": 0.0}
    limiter = RateLimiter(2, 10.0, lambda: now["time"])

    # WHEN / THEN
    assert limiter.allow_request("alice") is True
    assert limiter.allow_request("bob") is True
    now["time"] = 1.0
    assert limiter.allow_request("alice") is True
    now["time"] = 2.0
    assert limiter.allow_request("alice") is False
    assert limiter.allow_request("bob") is True
    assert limiter.allow_request("bob") is False


def test_quota_fully_refreshes_after_idle_period() -> None:
    """Test 12: After a full idle window the whole quota is available"""
    from rate_limiter import RateLimiter

    # GIVEN
    now = {"time": 0.0}
    limiter = RateLimiter(2, 10.0, lambda: now["time"])
    assert limiter.allow_request("alice") is True
    assert limiter.allow_request("alice") is True

    # WHEN
    now["time"] = 100.0

    # THEN
    assert limiter.allow_request("alice") is True
    assert limiter.allow_request("alice") is True
    assert limiter.allow_request("alice") is False


def test_zero_max_requests_is_rejected() -> None:
    """Test 13: max_requests below 1 raises ValueError"""
    import pytest

    from rate_limiter import RateLimiter

    with pytest.raises(ValueError, match="^max_requests must be positive$"):
        RateLimiter(0, 10.0, lambda: 0.0)


def test_non_positive_time_window_is_rejected() -> None:
    """Test 14: A zero or negative time_window raises ValueError"""
    import pytest

    from rate_limiter import RateLimiter

    with pytest.raises(ValueError, match="^time_window must be positive$"):
        RateLimiter(3, 0.0, lambda: 0.0)


def test_sub_second_time_window_is_accepted_and_enforced() -> None:
    """Test 15: Any positive time_window is valid, including fractions of a second"""
    from rate_limiter import RateLimiter

    # GIVEN
    now = {"time": 0.0}
    limiter = RateLimiter(1, 0.5, lambda: now["time"])

    # WHEN / THEN
    assert limiter.allow_request("alice") is True
    now["time"] = 0.4
    assert limiter.allow_request("alice") is False
    now["time"] = 0.5
    assert limiter.allow_request("alice") is True
