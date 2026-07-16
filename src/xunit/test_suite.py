"""TestSuite class for running multiple test cases"""

from typing import Any


class TestSuite:
    """Suite of test cases to run together"""

    def __init__(self) -> None:
        self.tests: list[Any] = []

    def add(self, test: Any) -> None:
        """Add a test to the suite"""
        self.tests.append(test)

    def run(self, result: Any) -> None:
        """Run all tests in the suite"""
        for test in self.tests:
            test.run(result)
