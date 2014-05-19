#include <cxxtest/TestSuite.h>

#include "ToCover.h"

class Test_CoverageErrors: public CxxTest::TestSuite
{
public:
	void test_DoesNothingButIncludeTheFile_EnforcementCodeDoesNotGetConfused()
	{
		TS_ASSERT_EQUALS( 1 + 1, 2 );
		anotherFunction();
	}
};
