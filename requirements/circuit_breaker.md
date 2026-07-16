# Circuit breaker for an unreliable service

## Overview
A circuit breaker guards calls to an unreliable operation. While closed it passes calls straight through; after a run of consecutive failures it opens and rejects calls immediately; after a reset timeout it lets one probe call through, and the probe's outcome decides whether the circuit closes again or reopens. The failure threshold defaults to 3 consecutive failures and the reset timeout to 30 seconds; both are configurable, and the breaker measures time through a caller-supplied clock.

## User Stories

### US-1: Transparent pass-through while healthy
As a service client, I want the breaker to be invisible while the service is healthy, so that normal calls behave exactly as if the breaker were not there.

- AC-1.1: A new breaker reports the closed state.
- AC-1.2: While closed, a successful call's result is returned to the caller unchanged.
- AC-1.3: While closed, a failing call's error propagates to the caller, and the breaker stays closed.
- AC-1.4: Consecutive failures below the threshold leave the breaker closed.
- AC-1.5: A success between failures resets the consecutive-failure count, so the run must start over.

### US-2: Fail fast when the service is down
As a service client, I want calls rejected immediately once the service has repeatedly failed, so that callers stop hammering a broken dependency.

- AC-2.1: Reaching the threshold of consecutive failures — 3 by default — opens the circuit.
- AC-2.2: While open, calls are rejected with a dedicated circuit-open error whose message is exactly "circuit breaker is open", and the underlying operation is not invoked at all.
- AC-2.3: Calls keep being rejected for the whole reset timeout — 30 seconds by default — measured from when the circuit opened.

### US-3: Automatic recovery probing
As an operator, I want the breaker to test the service again after a cool-down period, so that traffic resumes on its own once the service recovers.

- AC-3.1: Reaching the timeout does not by itself change the reported state; the breaker still reports open until the next call is attempted.
- AC-3.2: Once the timeout has elapsed, the next call is let through as a probe; if it succeeds, its result is returned and the circuit closes.
- AC-3.3: If the probe fails, its error propagates to the caller and the circuit reopens.
- AC-3.4: A failed probe restarts the reset timeout from the moment of the probe.
- AC-3.5: After a successful recovery, failure counting starts again from zero: it takes a full new run of threshold failures to reopen the circuit.
- AC-3.6: The probe is permitted exactly when the full timeout has elapsed, and not a moment before.

### US-4: Tunable protection
As an operator, I want the failure threshold and reset timeout to be configurable, so that the breaker matches each service's failure profile.

- AC-4.1: A custom failure threshold is honoured: with a threshold of 1, a single failure opens the circuit.
- AC-4.2: A custom reset timeout governs when the probe is allowed, with the same just-before/at-the-boundary behaviour as the default.

## Traceability
```json
{
  "test_breaker_starts_closed": ["AC-1.1"],
  "test_closed_breaker_returns_operation_result": ["AC-1.2"],
  "test_closed_breaker_propagates_operation_failure": ["AC-1.3"],
  "test_failures_below_threshold_keep_breaker_closed": ["AC-1.4"],
  "test_success_resets_consecutive_failure_count": ["AC-1.5"],
  "test_reaching_failure_threshold_opens_circuit": ["AC-2.1"],
  "test_open_breaker_fails_fast_without_invoking_operation": ["AC-2.2"],
  "test_open_breaker_rejects_until_reset_timeout_elapses": ["AC-2.3"],
  "test_transition_to_half_open_is_lazy": ["AC-3.1"],
  "test_successful_probe_closes_circuit": ["AC-3.2"],
  "test_failed_probe_reopens_circuit": ["AC-3.3"],
  "test_failed_probe_restarts_reset_timeout": ["AC-3.4"],
  "test_recovery_resets_failure_counter": ["AC-3.5"],
  "test_custom_failure_threshold": ["AC-4.1"],
  "test_custom_reset_timeout": ["AC-4.2"],
  "test_probe_allowed_exactly_at_reset_timeout": ["AC-3.6"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
