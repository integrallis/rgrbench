"""CSV Query Engine Kata - chainable select/where/order_by/limit/count over CSV text
Operators: =, !=, >, <, >=, <= (numeric when both sides are numeric, string otherwise).
"""

PEOPLE_CSV = """name,age,city,salary
Alice,35,London,75000
Bob,28,Paris,60000
Charlie,42,London,90000
Diana,31,Berlin,80000
Eve,28,Paris,55000
"""


def _names(rows: list[dict[str, str]]) -> list[str]:
    return [row["name"] for row in rows]


def test_rows_returns_every_data_row() -> None:
    """Test 1: rows() returns each data row as a dict keyed by header names"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).rows()
    assert len(result) == 5
    assert result[0] == {"name": "Alice", "age": "35", "city": "London", "salary": "75000"}


def test_select_single_column() -> None:
    """Test 2: select('name') keeps only the name column for every row"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).select("name").rows()
    assert result == [
        {"name": "Alice"},
        {"name": "Bob"},
        {"name": "Charlie"},
        {"name": "Diana"},
        {"name": "Eve"},
    ]


def test_select_preserves_requested_column_order() -> None:
    """Test 3: Selected columns appear in the order they were requested"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).select("age", "name").rows()
    assert list(result[0].keys()) == ["age", "name"]
    assert result[0] == {"age": "35", "name": "Alice"}


def test_where_equals_on_string_column() -> None:
    """Test 4: where city = London keeps the Alice and Charlie rows"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).where("city", "=", "London").rows()
    assert _names(result) == ["Alice", "Charlie"]


def test_where_not_equals() -> None:
    """Test 5: where city != London keeps the other three rows"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).where("city", "!=", "London").rows()
    assert _names(result) == ["Bob", "Diana", "Eve"]


def test_where_greater_than_numeric() -> None:
    """Test 6: where age > 30 keeps Alice, Charlie, and Diana"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).where("age", ">", 30).select("name").rows()
    assert _names(result) == ["Alice", "Charlie", "Diana"]


def test_where_greater_or_equal_includes_boundary() -> None:
    """Test 7: where age >= 35 includes the row whose age is exactly 35"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).where("age", ">=", 35).rows()
    assert _names(result) == ["Alice", "Charlie"]


def test_where_less_than_and_less_or_equal() -> None:
    """Test 8: < excludes the boundary value while <= includes it"""
    from csv_query_engine import CsvQuery

    below = CsvQuery(PEOPLE_CSV).where("age", "<", 31).rows()
    assert _names(below) == ["Bob", "Eve"]
    at_or_below = CsvQuery(PEOPLE_CSV).where("age", "<=", 31).rows()
    assert _names(at_or_below) == ["Bob", "Diana", "Eve"]


def test_numeric_comparison_is_not_lexicographic() -> None:
    """Test 9: age > 9 matches every row even though '28' < '9' as strings"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).where("age", ">", 9).rows()
    assert len(result) == 5


def test_where_equals_numeric_value() -> None:
    """Test 10: where age = 28 matches both 28-year-olds"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).where("age", "=", 28).rows()
    assert _names(result) == ["Bob", "Eve"]


def test_order_by_ascending_numeric_with_stable_ties() -> None:
    """Test 11: order_by age asc sorts numerically, keeping tied rows in input order"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).order_by("age", "asc").select("name", "age").rows()
    assert result == [
        {"name": "Bob", "age": "28"},
        {"name": "Eve", "age": "28"},
        {"name": "Diana", "age": "31"},
        {"name": "Alice", "age": "35"},
        {"name": "Charlie", "age": "42"},
    ]


def test_order_by_descending() -> None:
    """Test 12: order_by salary desc sorts from highest to lowest"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).order_by("salary", "desc").rows()
    assert _names(result) == ["Charlie", "Diana", "Alice", "Bob", "Eve"]


def test_order_by_string_column() -> None:
    """Test 13: order_by city asc sorts alphabetically with stable ties"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).order_by("city", "asc").rows()
    assert _names(result) == ["Diana", "Alice", "Charlie", "Bob", "Eve"]


def test_where_then_order_by_descending() -> None:
    """Test 14: where age >= 35 then order_by salary desc gives Charlie then Alice"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).where("age", ">=", 35).order_by("salary", "desc").rows()
    assert _names(result) == ["Charlie", "Alice"]
    assert [row["salary"] for row in result] == ["90000", "75000"]


def test_limit_returns_first_n_rows() -> None:
    """Test 15: limit(2) keeps only the first two rows"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).limit(2).select("name").rows()
    assert _names(result) == ["Alice", "Bob"]


def test_limit_beyond_row_count_returns_everything() -> None:
    """Test 16: A limit larger than the data returns all rows"""
    from csv_query_engine import CsvQuery

    assert CsvQuery(PEOPLE_CSV).limit(100).count() == 5


def test_limit_zero_and_negative() -> None:
    """Test 17: limit(0) empties the result; a negative limit is invalid"""
    import pytest

    from csv_query_engine import CsvQuery

    assert CsvQuery(PEOPLE_CSV).limit(0).count() == 0
    with pytest.raises(ValueError, match="non-negative"):
        CsvQuery(PEOPLE_CSV).limit(-1)


def test_count_matching_rows() -> None:
    """Test 18: count() reports all rows, filtered rows, and zero matches"""
    from csv_query_engine import CsvQuery

    assert CsvQuery(PEOPLE_CSV).count() == 5
    assert CsvQuery(PEOPLE_CSV).where("city", "=", "Paris").count() == 2
    assert CsvQuery(PEOPLE_CSV).where("city", "=", "Tokyo").count() == 0


def test_operations_apply_in_call_order() -> None:
    """Test 19: limit before where filters the trimmed rows, not the other way around"""
    from csv_query_engine import CsvQuery

    where_first = CsvQuery(PEOPLE_CSV).where("age", ">", 30).limit(2).rows()
    assert _names(where_first) == ["Alice", "Charlie"]
    limit_first = CsvQuery(PEOPLE_CSV).limit(2).where("age", ">", 30).rows()
    assert _names(limit_first) == ["Alice"]


def test_select_unknown_column_raises() -> None:
    """Test 20: Selecting a column absent from the header is an error"""
    import pytest

    from csv_query_engine import CsvQuery, UnknownColumnError

    with pytest.raises(UnknownColumnError, match="invalid_column"):
        CsvQuery(PEOPLE_CSV).select("invalid_column")


def test_where_and_order_by_unknown_column_raise() -> None:
    """Test 21: Filtering or sorting on a column absent from the header is an error"""
    import pytest

    from csv_query_engine import CsvQuery, UnknownColumnError

    with pytest.raises(UnknownColumnError, match="height"):
        CsvQuery(PEOPLE_CSV).where("height", ">", 100)
    with pytest.raises(UnknownColumnError, match="height"):
        CsvQuery(PEOPLE_CSV).order_by("height")


def test_unknown_operator_raises() -> None:
    """Test 22: Only =, !=, >, <, >=, and <= are valid operators"""
    import pytest

    from csv_query_engine import CsvQuery

    with pytest.raises(ValueError, match="unknown operator"):
        CsvQuery(PEOPLE_CSV).where("age", "~", 30)


def test_invalid_sort_direction_raises() -> None:
    """Test 23: order_by accepts only 'asc' or 'desc'"""
    import pytest

    from csv_query_engine import CsvQuery

    with pytest.raises(ValueError, match="asc"):
        CsvQuery(PEOPLE_CSV).order_by("age", "sideways")


def test_header_only_csv_yields_no_rows() -> None:
    """Test 24: A CSV with only a header row queries to an empty result"""
    from csv_query_engine import CsvQuery

    query = CsvQuery("name,age,city,salary\n")
    assert query.rows() == []
    assert query.count() == 0
    assert query.where("age", ">", 30).select("name").count() == 0


def test_single_row_csv() -> None:
    """Test 25: A single-row CSV supports the full pipeline"""
    from csv_query_engine import CsvQuery

    query = CsvQuery("name,age\nAlice,35\n")
    assert query.where("age", ">=", 35).order_by("age").limit(5).count() == 1


def test_quoted_field_containing_comma() -> None:
    """Test 26: A quoted field keeps its embedded comma as one value"""
    from csv_query_engine import CsvQuery

    csv_text = 'name,age,city\n"Smith, Jr.",45,London\nAlice,35,London\n'
    result = CsvQuery(csv_text).where("age", ">", 40).rows()
    assert result == [{"name": "Smith, Jr.", "age": "45", "city": "London"}]


def test_column_names_with_spaces() -> None:
    """Test 27: Columns whose names contain spaces are addressable"""
    from csv_query_engine import CsvQuery

    csv_text = "full name,age\nAlice Smith,35\nBob Jones,28\n"
    result = CsvQuery(csv_text).where("age", ">", 30).select("full name").rows()
    assert result == [{"full name": "Alice Smith"}]


def test_mixed_type_comparison_falls_back_to_string_ordering() -> None:
    """Test 28: When only one side is numeric, comparison is lexicographic"""
    from csv_query_engine import CsvQuery

    # Letters sort after digits, so every city name is > "1" as a string
    assert CsvQuery(PEOPLE_CSV).where("city", ">", 1).count() == 5
    # and every digit-leading age is < "x" as a string.
    assert CsvQuery(PEOPLE_CSV).where("age", "<", "x").count() == 5


def test_strictly_greater_excludes_the_boundary_value() -> None:
    """Test 29: where age > 28 excludes the rows whose age is exactly 28"""
    from csv_query_engine import CsvQuery

    result = CsvQuery(PEOPLE_CSV).where("age", ">", 28).rows()
    assert _names(result) == ["Alice", "Charlie", "Diana"]


def test_empty_csv_is_rejected_with_the_exact_message() -> None:
    """Test 30: CSV text without a header row is rejected, naming the requirement"""
    import pytest

    from csv_query_engine import CsvQuery

    with pytest.raises(ValueError) as excinfo:
        CsvQuery("")
    assert str(excinfo.value) == "CSV text must include a header row"


def test_select_result_supports_further_chaining() -> None:
    """Test 31: A selected query still filters and sorts by its remaining columns"""
    from csv_query_engine import CsvQuery

    result = (
        CsvQuery(PEOPLE_CSV)
        .select("name", "age")
        .where("age", ">", 30)
        .order_by("age", "desc")
        .rows()
    )
    assert result == [
        {"name": "Charlie", "age": "42"},
        {"name": "Alice", "age": "35"},
        {"name": "Diana", "age": "31"},
    ]


def test_order_by_numeric_column_sorts_by_value_not_text() -> None:
    """Test 32: Numeric sort puts 9 before 10 and 100 despite the string order"""
    from csv_query_engine import CsvQuery

    csv_text = "name,age\nOld,100\nKid,9\nTeen,10\n"
    result = CsvQuery(csv_text).order_by("age", "asc").rows()
    assert _names(result) == ["Kid", "Teen", "Old"]
