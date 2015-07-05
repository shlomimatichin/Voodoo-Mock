from pytestsuite import *

class TestCase(PyTestSuite):
    def test_add_two_numbers(self):
        TS_ASSERT_EQUALS(1+1, 2)
