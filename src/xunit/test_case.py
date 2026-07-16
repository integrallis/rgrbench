"""TestCase base class for all test cases"""

from typing import Any


class TestCase:
    """Base class for all test cases"""

    def __init__(self, name: str) -> None:
        """Store the test method name"""
        self.name = name

    def set_up(self) -> None:
        """Called before test method - override in subclass"""
        pass

    def tear_down(self) -> None:
        """Called after test method - override in subclass"""
        pass

    def run(self, result: Any) -> None:
        """Run the test case"""
        result.test_started()
        self.set_up()
        try:
            method = getattr(self, self.name)
            method()
        except Exception:
            result.test_failed()
        self.tear_down()
