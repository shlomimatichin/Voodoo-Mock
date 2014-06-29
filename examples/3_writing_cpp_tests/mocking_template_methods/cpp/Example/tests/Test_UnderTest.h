#include <cxxtest/TestSuite.h>

#define VOODOO_EXPECT_cpp_Example_MockMe_h

#include "Example/UnderTest.h"

using namespace VoodooCommon::Expect;
using namespace VoodooCommon::Expect::Parameter;
using namespace Example;

class Test_Example: public CxxTest::TestSuite
{
public:
	void test_TemplateMethodCanBeMocked()
	{
		UnderTest tested;

		Scenario scenario;
		scenario <<
			new Construction< MockMe >( "Fake MockMe" ) <<
			new CallReturnVoid( "Fake MockMe::mockMe" ) <<
				new Ignore< std::unique_ptr< int > >() <<
			new Destruction( "Fake MockMe" );
		tested.underTest();
		scenario.assertFinished();
	}
};
