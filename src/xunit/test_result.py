"""TestResult class for tracking test execution results"""


class TestResult:
    """Tracks the results of test execution"""

    def __init__(self) -> None:
        self.run_count = 0
        self.error_count = 0

    def test_started(self) -> None:
        """Called when a test starts"""
        self.run_count += 1

    def test_failed(self) -> None:
        """Called when a test fails"""
        self.error_count += 1

    def summary(self) -> str:
        """Returns a summary of test results"""
        return f"{self.run_count} run, {self.error_count} failed"
