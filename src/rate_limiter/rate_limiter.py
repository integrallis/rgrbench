"""Sliding-window rate limiter with an injected clock."""

from collections import defaultdict, deque
from collections.abc import Callable


class RateLimiter:
    """Per-client sliding-window rate limiter.

    Allows at most ``max_requests`` per client within any window of
    ``time_window`` seconds, measured with the injected ``clock``
    callable. A recorded request stops counting once a full window has
    elapsed since it was made; denied requests are never recorded.
    """

    def __init__(
        self,
        max_requests: int,
        time_window: float,
        clock: Callable[[], float],
    ) -> None:
        if max_requests < 1:
            raise ValueError("max_requests must be positive")
        if time_window <= 0:
            raise ValueError("time_window must be positive")
        self._max_requests = max_requests
        self._time_window = time_window
        self._clock = clock
        self._history: dict[str, deque[float]] = defaultdict(deque)

    def allow_request(self, client_id: str) -> bool:
        """Record and permit the request, or reject it without recording."""
        now = self._clock()
        history = self._history[client_id]
        while history and now - history[0] >= self._time_window:
            history.popleft()
        if len(history) >= self._max_requests:
            return False
        history.append(now)
        return True
