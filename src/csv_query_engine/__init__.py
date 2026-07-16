"""CSV Query Engine kata: chainable queries over in-memory CSV text.

The engine parses a CSV string whose first row is the header and offers
chainable operations applied in call order: select restricts rows to
the named columns, where filters rows with the operators =, !=, >, <,
>=, and <= (comparing numerically when both sides are numeric and as
strings otherwise), order_by sorts ascending or descending with a
stable sort, and limit keeps the first N rows. Terminal operations
rows() and count() return the result rows and their number. Quoted
fields may contain commas, column names may contain spaces, and
referencing a column absent from the header raises an error. All input
arrives as strings; the engine performs no file or network I/O.

Kata catalogued at tddbuddy.com/katas/csv-query; implementation and
tests original (MIT), machine-authored from the specification, 2026.
"""

from csv_query_engine.query import CsvQuery, UnknownColumnError

__all__ = ["CsvQuery", "UnknownColumnError"]
