"""
xUnit Testing Framework - TDD Implementation
Based on Kent Beck's Test-Driven Development book Part II
"""


def test_test_result_tracks_run_count() -> None:
    """Test 1: TestResult should track number of tests run"""
    from xunit.test_result import TestResult

    result = TestResult()
    assert result.run_count == 0


def test_test_started_increments_count() -> None:
    """Test 2: test_started should increment run_count"""
    from xunit.test_result import TestResult

    result = TestResult()
    result.test_started()
    assert result.run_count == 1


def test_test_result_tracks_error_count() -> None:
    """Test 3: TestResult should track error count"""
    from xunit.test_result import TestResult

    result = TestResult()
    assert result.error_count == 0


def test_test_failed_increments_error_count() -> None:
    """Test 4: test_failed should increment error_count"""
    from xunit.test_result import TestResult

    result = TestResult()
    result.test_failed()
    assert result.error_count == 1


def test_test_result_summary() -> None:
    """Test 5: TestResult should provide summary"""
    from xunit.test_result import TestResult

    result = TestResult()
    assert result.summary() == "0 run, 0 failed"


def test_test_result_summary_with_data() -> None:
    """Test 6: TestResult summary should use actual counts"""
    from xunit.test_result import TestResult

    result = TestResult()
    result.test_started()
    result.test_started()
    result.test_failed()
    assert result.summary() == "2 run, 1 failed"


def test_test_case_stores_name() -> None:
    """Test 7: TestCase should store test method name"""
    from xunit.test_case import TestCase

    test = TestCase("test_method")
    assert test.name == "test_method"


def test_test_case_run_calls_method() -> None:
    """Test 8: TestCase run should call test method"""
    from xunit.test_case import TestCase
    from xunit.test_result import TestResult

    class WasRun(TestCase):
        def __init__(self, name: str) -> None:
            super().__init__(name)
            self.was_run = False

        def test_method(self) -> None:
            self.was_run = True

    test = WasRun("test_method")
    result = TestResult()
    test.run(result)
    assert test.was_run


def test_test_case_run_updates_result() -> None:
    """Test 9: TestCase run should update TestResult"""
    from xunit.test_case import TestCase
    from xunit.test_result import TestResult

    class SimpleTest(TestCase):
        def test_method(self) -> None:
            pass

    test = SimpleTest("test_method")
    result = TestResult()
    test.run(result)
    assert result.summary() == "1 run, 0 failed"


def test_test_case_setup() -> None:
    """Test 10: setUp should be called before test method"""
    from xunit.test_case import TestCase
    from xunit.test_result import TestResult

    class WasSetUp(TestCase):
        def __init__(self, name: str) -> None:
            super().__init__(name)
            self.log = ""

        def set_up(self) -> None:
            self.log += "set_up "

        def test_method(self) -> None:
            self.log += "test_method"

    test = WasSetUp("test_method")
    result = TestResult()
    test.run(result)
    assert test.log == "set_up test_method"


def test_test_case_teardown() -> None:
    """Test 11: tearDown should be called after test method"""
    from xunit.test_case import TestCase
    from xunit.test_result import TestResult

    class WasTornDown(TestCase):
        def __init__(self, name: str) -> None:
            super().__init__(name)
            self.log = ""

        def test_method(self) -> None:
            self.log += "test_method "

        def tear_down(self) -> None:
            self.log += "tear_down"

    test = WasTornDown("test_method")
    result = TestResult()
    test.run(result)
    assert test.log == "test_method tear_down"


def test_test_case_captures_failures() -> None:
    """Test 12: TestCase should capture test failures"""
    from xunit.test_case import TestCase
    from xunit.test_result import TestResult

    class FailingTest(TestCase):
        def test_method(self) -> None:
            raise AssertionError("Test failed")

    test = FailingTest("test_method")
    result = TestResult()
    test.run(result)
    assert result.summary() == "1 run, 1 failed"


def test_test_suite_runs_multiple_tests() -> None:
    """Test 13: TestSuite should run multiple tests"""
    from xunit.test_case import TestCase
    from xunit.test_result import TestResult
    from xunit.test_suite import TestSuite

    class SimpleTest(TestCase):
        def test_one(self) -> None:
            pass

        def test_two(self) -> None:
            pass

    suite = TestSuite()
    suite.add(SimpleTest("test_one"))
    suite.add(SimpleTest("test_two"))

    result = TestResult()
    suite.run(result)
    assert result.summary() == "2 run, 0 failed"


def test_teardown_runs_even_if_test_fails() -> None:
    """Test 14: tearDown should run even if test fails"""
    from xunit.test_case import TestCase
    from xunit.test_result import TestResult

    class FailingTestWithTearDown(TestCase):
        def __init__(self, name: str) -> None:
            super().__init__(name)
            self.log = ""

        def test_method(self) -> None:
            self.log += "test_method "
            raise AssertionError("Test failed")

        def tear_down(self) -> None:
            self.log += "tear_down"

    test = FailingTestWithTearDown("test_method")
    result = TestResult()
    test.run(result)
    assert test.log == "test_method tear_down"
    assert result.summary() == "1 run, 1 failed"


def test_test_result_counts_each_failure() -> None:
    """Test 15: TestResult should count every failure, not just the first"""
    from xunit.test_case import TestCase
    from xunit.test_result import TestResult
    from xunit.test_suite import TestSuite

    class FailingTest(TestCase):
        def test_method(self) -> None:
            raise AssertionError("Test failed")

    suite = TestSuite()
    suite.add(FailingTest("test_method"))
    suite.add(FailingTest("test_method"))

    result = TestResult()
    suite.run(result)
    assert result.summary() == "2 run, 2 failed"
