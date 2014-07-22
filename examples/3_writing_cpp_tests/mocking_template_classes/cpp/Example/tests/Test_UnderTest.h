#include <cxxtest/TestSuite.h>

#define VOODOO_EXPECT_cpp_Example_MockMe_h

#include "Example/UnderTest.h"

using namespace VoodooCommon::Expect;
using namespace VoodooCommon::Expect::Parameter;
using namespace Example;

class Test_Example: public CxxTest::TestSuite
{
public:
	void test_TemplateClassCanBeMocked()
	{
		UnderTest tested;

		Scenario scenario;
		scenario <<
			new Construction< MockMe< int > >( "Fake MockMe" ) <<
			new CallReturnValue< int >( "Fake MockMe::mockMe", 0 ) <<
				new EqualsValue< int >( 3 ) <<
			new Destruction( "Fake MockMe" );
		tested.underTest();
		scenario.assertFinished();
	}
};
