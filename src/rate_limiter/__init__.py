"""Rate Limiter kata: sliding-window request throttling per client.

`RateLimiter(max_requests, time_window, clock)` limits each client to
``max_requests`` within any sliding window of ``time_window`` seconds.
Time comes exclusively from the injected zero-argument ``clock``
callable returning seconds as a float, so behaviour is fully
deterministic under test.

`allow_request(client_id)` returns True and records the request when
the client has quota left, and False otherwise. Rules:

- Each client is tracked independently; one client exhausting its quota
  never affects another.
- The window slides: a recorded request stops counting as soon as a
  full ``time_window`` has elapsed since it was made (a request aged
  exactly ``time_window`` no longer counts), rather than resetting on
  fixed boundaries.
- Denied requests are not recorded and consume no quota.
- ``max_requests`` below 1 raises ValueError('max_requests must be
  positive'); a non-positive ``time_window`` raises
  ValueError('time_window must be positive').

Kata catalogued at tddbuddy.com/katas/rate-limiter; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""

from rate_limiter.rate_limiter import RateLimiter

__all__ = ["RateLimiter"]
