"""Circuit Breaker kata: fail fast around an unreliable operation.

A circuit breaker wraps calls to an operation and moves between three
states. Closed: calls pass through; consecutive failures are counted,
a success resets the count, and reaching the failure threshold
(default 3) opens the circuit. Open: calls are rejected immediately
without invoking the operation until the reset timeout (default 30
seconds) has elapsed; the transition is lazy, checked on the next
execute rather than by a timer. Half-open: after the timeout, exactly
one probe call passes through - success closes the circuit and resets
the counters, failure reopens it and restarts the timeout. Time is
read from an injected clock so behaviour is fully deterministic.

Kata catalogued at tddbuddy.com/katas/circuit-breaker; implementation
and tests original (MIT), machine-authored from the specification,
2026.
"""

from circuit_breaker.breaker import CircuitBreaker, CircuitOpenError, CircuitState

__all__ = ["CircuitBreaker", "CircuitOpenError", "CircuitState"]
