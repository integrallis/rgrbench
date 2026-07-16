"""Circuit breaker state machine with an injected clock."""

from collections.abc import Callable
from enum import Enum
from typing import TypeVar

T = TypeVar("T")


class CircuitState(Enum):
    """The three circuit breaker states."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitOpenError(Exception):
    """Raised when a call is rejected because the circuit is open."""


class CircuitBreaker:
    """Guards an operation, failing fast while the circuit is open.

    The clock is a callable returning the current time in seconds; all
    timeout decisions are made against it, never against wall-clock
    time.
    """

    def __init__(
        self,
        clock: Callable[[], float],
        failure_threshold: int = 3,
        reset_timeout: float = 30.0,
    ) -> None:
        self._clock = clock
        self._failure_threshold = failure_threshold
        self._reset_timeout = reset_timeout
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._opened_at = 0.0

    @property
    def state(self) -> CircuitState:
        """The stored state; the open-to-half-open transition is lazy."""
        return self._state

    def execute(self, operation: Callable[[], T]) -> T:
        """Invoke the operation through the breaker and return its result.

        Raises CircuitOpenError without invoking the operation while the
        circuit is open and the reset timeout has not elapsed. Exceptions
        raised by the operation itself propagate to the caller.
        """
        if self._state is CircuitState.OPEN:
            if self._clock() - self._opened_at >= self._reset_timeout:
                self._state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError("circuit breaker is open")
        if self._state is CircuitState.HALF_OPEN:
            return self._probe(operation)
        return self._call_closed(operation)

    def _call_closed(self, operation: Callable[[], T]) -> T:
        try:
            result = operation()
        except Exception:
            self._failure_count += 1
            if self._failure_count >= self._failure_threshold:
                self._trip_open()
            raise
        self._failure_count = 0
        return result

    def _probe(self, operation: Callable[[], T]) -> T:
        try:
            result = operation()
        except Exception:
            self._trip_open()
            raise
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        return result

    def _trip_open(self) -> None:
        self._state = CircuitState.OPEN
        self._opened_at = self._clock()
