# Sliding-window request throttling

## Overview
A service protects itself from overuse by throttling requests per client. The throttle is configured with a request quota, a time window measured in seconds, and a time source it consults for the current moment. Each incoming request names its client and is approved or denied on the spot: a client may make at most the configured number of requests within any window-length span of time, judged against a window that slides continuously rather than resetting at fixed intervals.

## User Stories

### US-1: Enforcing a per-client request quota
As an API operator, I want each client limited to a fixed number of requests per time window, so that no single client can overwhelm the service.

- AC-1.1: A client's first request is approved.
- AC-1.2: Every request within the quota is approved.
- AC-1.3: A request that would exceed the quota is denied.
- AC-1.4: With a quota of one, exactly one request is approved per window span.

### US-2: Isolating clients from one another
As an API operator, I want request accounting kept separately per client, so that one client exhausting its quota never affects another.

- AC-2.1: A client denied for exhausting its quota has no effect on a different client, whose requests are still approved.
- AC-2.2: Interleaved traffic from several clients is accounted per client, each against its own window.

### US-3: Refreshing quota with a sliding window
As an API operator, I want the window to slide continuously, so that capacity frees up request by request instead of in bursts.

- AC-3.1: Requests older than the window no longer count against the quota, so a previously denied client is approved again once its earliest requests age out.
- AC-3.2: A request aged exactly one window length no longer counts; at that boundary its slot is free again.
- AC-3.3: A request aged even slightly less than one window length still counts.
- AC-3.4: Expiry is per request, not a periodic reset: with a quota of three and a ten-second window, requests approved at seconds 0, 4, and 8 mean a request at second 9 is denied, second 10 frees exactly one slot, and that slot is consumed immediately.
- AC-3.5: After a full window of inactivity the client's entire quota is available again.

### US-4: Charging nothing for denied requests
As an API operator, I want denied requests to consume no quota, so that a throttled client is not punished further for retrying.

- AC-4.1: A denied request is not recorded against the window: with a quota of one and a ten-second window, a request approved at second 0 and one denied at second 5 leave the client approved again at second 10 — the denial did not start a new window.

### US-5: Validating the throttle configuration
As an API operator, I want nonsensical configurations rejected up front, so that misconfiguration surfaces immediately.

- AC-5.1: A quota below one is rejected with the exact error message "max_requests must be positive".
- AC-5.2: A zero or negative window length is rejected with the exact error message "time_window must be positive".
- AC-5.3: Any positive window length is accepted and enforced, including fractions of a second.

## Traceability
```json
{
  "test_first_request_is_allowed": ["AC-1.1"],
  "test_requests_up_to_the_limit_are_allowed": ["AC-1.2"],
  "test_request_beyond_the_limit_is_denied": ["AC-1.3"],
  "test_clients_have_independent_quotas": ["AC-2.1"],
  "test_quota_refreshes_when_old_requests_expire": ["AC-3.1"],
  "test_request_expires_at_exactly_one_window": ["AC-3.2"],
  "test_request_still_counts_just_inside_the_window": ["AC-3.3"],
  "test_window_slides_rather_than_resetting": ["AC-3.4"],
  "test_denied_requests_consume_no_quota": ["AC-4.1"],
  "test_limit_of_one_allows_exactly_one_per_window": ["AC-1.4"],
  "test_interleaved_clients_keep_separate_windows": ["AC-2.2"],
  "test_quota_fully_refreshes_after_idle_period": ["AC-3.5"],
  "test_zero_max_requests_is_rejected": ["AC-5.1"],
  "test_non_positive_time_window_is_rejected": ["AC-5.2"],
  "test_sub_second_time_window_is_accepted_and_enforced": ["AC-5.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
