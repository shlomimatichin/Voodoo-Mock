#include <cxxtest/TestSuite.h>

#include "ToCover.h"

class Test_CoverageErrors: public CxxTest::TestSuite
{
public:
	void test_Coverage()
	{
		aFunction( 0 );
	}
};
