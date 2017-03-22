#include <cxxtest/TestSuite.h>
#define VOODOO_EXPECT_cpp_Example_Mocked_h

#include "Example/UnderTest.h"

using namespace VoodooCommon::Expect;
using namespace VoodooCommon::Expect::Parameter;

class Test_Example: public CxxTest::TestSuite
{
public:
	class TestFailed {};

	void setUp()
	{
	}

	void tearDown()
	{
	}

	void test_printFoo()
	{
		Scenario scenario;
		scenario <<
			new Construction< FooWithStatic >( "foo" ) <<
			new CallReturnVoid( "foo::print" ) <<
			new Destruction( "foo" );

		printFoo();

		scenario.assertFinished();
	}
};
