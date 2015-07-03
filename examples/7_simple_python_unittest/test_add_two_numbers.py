from pytestsuite import * 

class OtherTestingSuite(object):
    pass

class TestCase(PyTestSuite, OtherTestingSuite):
    def test_add_two_numbers(self):
        TS_ASSERT_EQUALS(1+1, 2)
