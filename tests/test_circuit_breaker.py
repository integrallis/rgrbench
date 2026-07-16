"""Circuit Breaker Kata - closed/open/half-open transitions with an injected clock
Failure threshold defaults to 3 consecutive failures; reset timeout defaults to 30 seconds.
"""


def test_breaker_starts_closed() -> None:
    """Test 1: A new circuit breaker starts in the closed state"""
    from circuit_breaker import CircuitBreaker, CircuitState

    breaker = CircuitBreaker(clock=lambda: 0.0)
    assert breaker.state is CircuitState.CLOSED


def test_closed_breaker_returns_operation_result() -> None:
    """Test 2: While closed, execute passes through and returns the result"""
    from circuit_breaker import CircuitBreaker

    breaker = CircuitBreaker(clock=lambda: 0.0)
    assert breaker.execute(lambda: 42) == 42


def test_closed_breaker_propagates_operation_failure() -> None:
    """Test 3: While closed, an operation failure propagates to the caller"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitState

    breaker = CircuitBreaker(clock=lambda: 0.0)

    def failing() -> None:
        raise RuntimeError("service failure")

    with pytest.raises(RuntimeError, match="service failure"):
        breaker.execute(failing)
    assert breaker.state is CircuitState.CLOSED


def test_failures_below_threshold_keep_breaker_closed() -> None:
    """Test 4: Two consecutive failures stay below the default threshold of 3"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitState

    breaker = CircuitBreaker(clock=lambda: 0.0)

    def failing() -> None:
        raise RuntimeError("service failure")

    for _ in range(2):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)
    assert breaker.state is CircuitState.CLOSED


def test_success_resets_consecutive_failure_count() -> None:
    """Test 5: A success between failures resets the consecutive-failure count"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitState

    breaker = CircuitBreaker(clock=lambda: 0.0)

    def failing() -> None:
        raise RuntimeError("service failure")

    for _ in range(2):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)
    breaker.execute(lambda: "ok")
    for _ in range(2):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)
    assert breaker.state is CircuitState.CLOSED


def test_reaching_failure_threshold_opens_circuit() -> None:
    """Test 6: Three consecutive failures open the circuit"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitState

    breaker = CircuitBreaker(clock=lambda: 0.0)

    def failing() -> None:
        raise RuntimeError("service failure")

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)
    assert breaker.state is CircuitState.OPEN


def test_open_breaker_fails_fast_without_invoking_operation() -> None:
    """Test 7: While open, execute raises CircuitOpenError and never calls the service"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitOpenError

    breaker = CircuitBreaker(clock=lambda: 0.0)
    calls = {"count": 0}

    def failing() -> None:
        calls["count"] += 1
        raise RuntimeError("service failure")

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)
    assert calls["count"] == 3

    with pytest.raises(CircuitOpenError, match="^circuit breaker is open$"):
        breaker.execute(failing)
    assert calls["count"] == 3


def test_open_breaker_rejects_until_reset_timeout_elapses() -> None:
    """Test 8: Just before the reset timeout, calls are still rejected"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitOpenError

    now = {"time": 0.0}
    breaker = CircuitBreaker(clock=lambda: now["time"])

    def failing() -> None:
        raise RuntimeError("service failure")

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)

    now["time"] = 29.9
    with pytest.raises(CircuitOpenError):
        breaker.execute(lambda: "ok")


def test_transition_to_half_open_is_lazy() -> None:
    """Test 9: After the timeout, the stored state stays open until the next execute"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitState

    now = {"time": 0.0}
    breaker = CircuitBreaker(clock=lambda: now["time"])

    def failing() -> None:
        raise RuntimeError("service failure")

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)

    now["time"] = 30.0
    assert breaker.state is CircuitState.OPEN
    breaker.execute(lambda: "ok")
    assert breaker.state is CircuitState.CLOSED


def test_successful_probe_closes_circuit() -> None:
    """Test 10: After the timeout, a successful probe closes the circuit"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitState

    now = {"time": 0.0}
    breaker = CircuitBreaker(clock=lambda: now["time"])

    def failing() -> None:
        raise RuntimeError("service failure")

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)

    now["time"] = 30.0
    assert breaker.execute(lambda: "recovered") == "recovered"
    assert breaker.state is CircuitState.CLOSED


def test_failed_probe_reopens_circuit() -> None:
    """Test 11: After the timeout, a failing probe reopens the circuit"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitState

    now = {"time": 0.0}
    breaker = CircuitBreaker(clock=lambda: now["time"])

    def failing() -> None:
        raise RuntimeError("service failure")

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)

    now["time"] = 30.0
    with pytest.raises(RuntimeError, match="service failure"):
        breaker.execute(failing)
    assert breaker.state is CircuitState.OPEN


def test_failed_probe_restarts_reset_timeout() -> None:
    """Test 12: A failed probe restarts the timeout from the probe's time"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitOpenError, CircuitState

    now = {"time": 0.0}
    breaker = CircuitBreaker(clock=lambda: now["time"])

    def failing() -> None:
        raise RuntimeError("service failure")

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)

    now["time"] = 30.0
    with pytest.raises(RuntimeError):
        breaker.execute(failing)

    now["time"] = 59.9  # 29.9 seconds after the failed probe reopened the circuit
    with pytest.raises(CircuitOpenError):
        breaker.execute(lambda: "ok")

    now["time"] = 60.0
    assert breaker.execute(lambda: "ok") == "ok"
    assert breaker.state is CircuitState.CLOSED


def test_recovery_resets_failure_counter() -> None:
    """Test 13: After recovery, the threshold count starts from zero again"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitState

    now = {"time": 0.0}
    breaker = CircuitBreaker(clock=lambda: now["time"])

    def failing() -> None:
        raise RuntimeError("service failure")

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)
    now["time"] = 30.0
    breaker.execute(lambda: "recovered")

    for _ in range(2):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)
    assert breaker.state is CircuitState.CLOSED
    with pytest.raises(RuntimeError):
        breaker.execute(failing)
    assert breaker.state is CircuitState.OPEN


def test_custom_failure_threshold() -> None:
    """Test 14: A threshold of 1 opens the circuit after a single failure"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitState

    breaker = CircuitBreaker(clock=lambda: 0.0, failure_threshold=1)

    def failing() -> None:
        raise RuntimeError("service failure")

    with pytest.raises(RuntimeError):
        breaker.execute(failing)
    assert breaker.state is CircuitState.OPEN


def test_custom_reset_timeout() -> None:
    """Test 15: A custom reset timeout governs when the probe is allowed"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitOpenError, CircuitState

    now = {"time": 0.0}
    breaker = CircuitBreaker(clock=lambda: now["time"], reset_timeout=5.0)

    def failing() -> None:
        raise RuntimeError("service failure")

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)

    now["time"] = 4.9
    with pytest.raises(CircuitOpenError):
        breaker.execute(lambda: "ok")

    now["time"] = 5.0
    assert breaker.execute(lambda: "ok") == "ok"
    assert breaker.state is CircuitState.CLOSED


def test_probe_allowed_exactly_at_reset_timeout() -> None:
    """Test 16: The probe is allowed once the full timeout has elapsed"""
    import pytest

    from circuit_breaker import CircuitBreaker, CircuitState

    now = {"time": 10.0}
    breaker = CircuitBreaker(clock=lambda: now["time"])

    def failing() -> None:
        raise RuntimeError("service failure")

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.execute(failing)

    now["time"] = 40.0  # opened at 10.0 + reset timeout of 30.0
    assert breaker.execute(lambda: "ok") == "ok"
    assert breaker.state is CircuitState.CLOSED
