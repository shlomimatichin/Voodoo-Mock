#include <cxxtest/TestSuite.h>
#define VOODOO_EXPECT_cpp_Example_SomeInterface_h

#include "Example/SomeInterface.h"
#include "Example/UnderTest.h"

using namespace VoodooCommon::Expect;
using namespace VoodooCommon::Expect::Parameter;
using namespace Example;

class Test_Example: public CxxTest::TestSuite
{
public:
	SomeInterface * _fakeInterface;
	UnderTest     * _underTest;

	void setUp()
	{
		_fakeInterface = new FakeND_SomeInterface( "someInterface" );
		Scenario scenario;
		scenario <<
			new Construction< SomeInterface >( "Parent" );
		_underTest = new UnderTest( _fakeInterface );
		scenario.assertFinished();
	}

	void tearDown()
	{
		Scenario scenario;
		scenario <<
			new Destruction( "Parent" );
		delete _underTest;
		scenario.assertFinished();
		delete _fakeInterface;
	}

	void test_TemplateMethodCanBeMocked()
	{
		int someNum = 9;
		Scenario scenario;
		scenario <<
			new CallReturnVoid( "someInterface::doSomething" ) <<
			    new EqualsValue< int > ( someNum + 1 );
		_underTest->doSomething( someNum );
		scenario.assertFinished();
	}
};
