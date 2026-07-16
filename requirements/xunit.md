# Minimal automated-test harness

## Overview
Developers need a small harness for running their own automated checks: each test case
names the check it exercises, runs it inside a set-up/tear-down lifecycle, and reports
into a shared result tally that counts how many tests ran and how many failed. Suites
gather cases so a whole collection can be run with one command and summarised in one
line.

## User Stories

### US-1: Tally test runs and failures
As a developer, I want a running tally of tests started and tests failed, so that one glance tells me the health of a run.

- AC-1.1: A fresh tally shows zero tests run and zero failures.
- AC-1.2: Recording that a test started increments the run count by one.
- AC-1.3: Recording a failure increments the failure count by one, and every failure is counted — two failing cases run under one tally show two failures, not one.
- AC-1.4: The tally summarises itself as the text "<runs> run, <failures> failed": a fresh tally reads "0 run, 0 failed"; after two starts and one failure it reads "2 run, 1 failed".

### US-2: Run a test case through its lifecycle
As a developer, I want each test case run with set-up before and tear-down after, so that every check starts from a clean context and cleans up after itself.

- AC-2.1: A test case is created with the name of the check it should exercise and exposes that name.
- AC-2.2: Running a test case invokes the named check.
- AC-2.3: Running a test case records the run in the supplied tally, which then reads "1 run, 0 failed" for a passing case.
- AC-2.4: A case's set-up step runs before the check itself.
- AC-2.5: A case's tear-down step runs after the check itself.
- AC-2.6: Tear-down runs even when the check fails, and the failure is still tallied.

### US-3: Capture failures without stopping the run
As a developer, I want a failing check caught and counted rather than crashing the harness, so that one bad test never hides the results of the rest.

- AC-3.1: An assertion failure inside a check is captured by the harness; the run completes and the tally reads "1 run, 1 failed".

### US-4: Run many cases as one suite
As a developer, I want to gather test cases into a suite and run them together, so that a whole collection reports into a single summary.

- AC-4.1: A suite accepts any number of test cases and runs each one against the same shared tally; two passing cases yield the summary "2 run, 0 failed".

## Traceability
```json
{
  "test_test_result_tracks_run_count": ["AC-1.1"],
  "test_test_started_increments_count": ["AC-1.2"],
  "test_test_result_tracks_error_count": ["AC-1.1"],
  "test_test_failed_increments_error_count": ["AC-1.3"],
  "test_test_result_summary": ["AC-1.4"],
  "test_test_result_summary_with_data": ["AC-1.4"],
  "test_test_case_stores_name": ["AC-2.1"],
  "test_test_case_run_calls_method": ["AC-2.2"],
  "test_test_case_run_updates_result": ["AC-2.3"],
  "test_test_case_setup": ["AC-2.4"],
  "test_test_case_teardown": ["AC-2.5"],
  "test_test_case_captures_failures": ["AC-3.1"],
  "test_test_suite_runs_multiple_tests": ["AC-4.1"],
  "test_teardown_runs_even_if_test_fails": ["AC-2.6"],
  "test_test_result_counts_each_failure": ["AC-1.3"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
