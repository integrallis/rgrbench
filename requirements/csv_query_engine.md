# CSV query engine

## Overview
A chainable query engine over CSV text. The first line of the text names the columns; each following line is a record whose values are kept as text. Queries are built by chaining column projection, row filtering, ordering and limiting, then materialising the matching records or counting them. Comparisons are numeric when both sides are numeric and textual otherwise, and malformed queries fail with descriptive errors.

## User Stories

### US-1: Read CSV text into records
As a data analyst, I want CSV text parsed into records keyed by the header names, so that I can query the data by column.

- AC-1.1: Every data line becomes one record mapping each header name to that line's value, with values kept as text.
- AC-1.2: CSV with only a header line yields no records: listing is empty, the count is zero, and filtering or projecting still works.
- AC-1.3: A quoted field keeps an embedded comma as part of a single value.
- AC-1.4: Header names containing spaces are usable in every operation.
- AC-1.5: CSV text without a header line is rejected with the message exactly "CSV text must include a header row".

### US-2: Choose columns
As a data analyst, I want to project a query down to chosen columns, so that results carry only the data I need.

- AC-2.1: Projection keeps only the requested columns for every record.
- AC-2.2: Projected columns appear in the order they were requested.
- AC-2.3: A projected query can still be filtered and ordered by its remaining columns.

### US-3: Filter rows
As a data analyst, I want to keep only the records matching a comparison against a column, so that I can answer questions about subsets of the data.

- AC-3.1: Equality (=) and inequality (!=) keep exactly the records whose column value matches or differs, preserving input order.
- AC-3.2: When both the column value and the comparison value are numeric, the ordering comparisons (>, <, >=, <=) compare by numeric value, never character by character.
- AC-3.3: Boundary semantics: > and < exclude records equal to the boundary value; >= and <= include them.
- AC-3.4: Equality against a numeric comparison value matches records by numeric value.
- AC-3.5: Operators other than =, !=, >, <, >= and <= are rejected with an error mentioning "unknown operator".
- AC-3.6: When only one side is numeric, the comparison falls back to textual ordering.

### US-4: Order rows
As a data analyst, I want results sorted by a column in either direction, so that I can rank records.

- AC-4.1: Ascending order on a numeric column sorts by numeric value — 9 before 10 before 100 — keeping tied records in their input order.
- AC-4.2: Descending order sorts from highest to lowest.
- AC-4.3: Ordering on a textual column sorts alphabetically, with stable ties.
- AC-4.4: Only "asc" and "desc" are accepted directions; anything else is rejected with an error mentioning the accepted "asc" direction.

### US-5: Limit and count
As a data analyst, I want to cap and count results, so that I can page through data and report totals.

- AC-5.1: A limit keeps only the first n records at that point in the chain.
- AC-5.2: A limit larger than the number of records returns everything.
- AC-5.3: A limit of zero yields an empty result.
- AC-5.4: A negative limit is rejected with an error mentioning "non-negative".
- AC-5.5: Counting reports how many records match: all of them, a filtered subset, or zero.

### US-6: Compose queries predictably
As a data analyst, I want chained operations applied in the order I wrote them, so that query results are predictable.

- AC-6.1: Operations apply in call order: limiting before filtering trims the records first and then filters them, which can give a different result from filtering first.
- AC-6.2: Projecting, filtering or ordering by a column absent from the header is rejected with an unknown-column error naming the column.
- AC-6.3: The full chain — filter, order, limit, count — works on a dataset of a single record.

## Traceability
```json
{
  "test_rows_returns_every_data_row": ["AC-1.1"],
  "test_select_single_column": ["AC-2.1"],
  "test_select_preserves_requested_column_order": ["AC-2.2"],
  "test_where_equals_on_string_column": ["AC-3.1"],
  "test_where_not_equals": ["AC-3.1"],
  "test_where_greater_than_numeric": ["AC-3.2"],
  "test_where_greater_or_equal_includes_boundary": ["AC-3.3"],
  "test_where_less_than_and_less_or_equal": ["AC-3.3"],
  "test_numeric_comparison_is_not_lexicographic": ["AC-3.2"],
  "test_where_equals_numeric_value": ["AC-3.4"],
  "test_order_by_ascending_numeric_with_stable_ties": ["AC-4.1"],
  "test_order_by_descending": ["AC-4.2"],
  "test_order_by_string_column": ["AC-4.3"],
  "test_where_then_order_by_descending": ["AC-4.2", "AC-6.1"],
  "test_limit_returns_first_n_rows": ["AC-5.1"],
  "test_limit_beyond_row_count_returns_everything": ["AC-5.2"],
  "test_limit_zero_and_negative": ["AC-5.3", "AC-5.4"],
  "test_count_matching_rows": ["AC-5.5"],
  "test_operations_apply_in_call_order": ["AC-6.1"],
  "test_select_unknown_column_raises": ["AC-6.2"],
  "test_where_and_order_by_unknown_column_raise": ["AC-6.2"],
  "test_unknown_operator_raises": ["AC-3.5"],
  "test_invalid_sort_direction_raises": ["AC-4.4"],
  "test_header_only_csv_yields_no_rows": ["AC-1.2"],
  "test_single_row_csv": ["AC-6.3"],
  "test_quoted_field_containing_comma": ["AC-1.3"],
  "test_column_names_with_spaces": ["AC-1.4"],
  "test_mixed_type_comparison_falls_back_to_string_ordering": ["AC-3.6"],
  "test_strictly_greater_excludes_the_boundary_value": ["AC-3.3"],
  "test_empty_csv_is_rejected_with_the_exact_message": ["AC-1.5"],
  "test_select_result_supports_further_chaining": ["AC-2.3"],
  "test_order_by_numeric_column_sorts_by_value_not_text": ["AC-4.1"]
}
```

Machine-derived from the package's verified test suite, 2026; see requirements/PROTOCOL.md.
