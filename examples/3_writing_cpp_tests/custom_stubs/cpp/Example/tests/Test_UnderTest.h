#include <cxxtest/TestSuite.h>

#define __EXAMPLE_MOCK_ME_H__ 1
//this macro will cause the real MockMe.h to be "skipped" when included. Instead, we can
//implement our stub here as we see fit (and pehaps even put the code in a separate makefile)

#include "VoodooCommon/Custom.h"
#include <memory>

using namespace VoodooCommon::Expect;
using namespace VoodooCommon::Expect::Parameter;

namespace Example {
class MockMe : public Custom::Klass
{
public:
	MockMe( int parameter ) :
		Custom::Klass( "Example::MockMe" )
	{
		voodooConstructor( parameter );
	}

	~MockMe()
	{
		voodooDestructor();
	}

	void justASimpleVoidMethod( int first, const char * second )
	{
		voodooVoidCall( "justASimpleVoidMethod", first, second );
	}

	int returnsAnInt()
	{
		return voodooCall< int >( "returnsAnInt" );
	}

	std::unique_ptr< int > returnsAUniquePtr()
	{
		return std::move( voodooMoveCall< std::unique_ptr< int > >( "returnsAUniquePtr" ) );
	}
};
void globalFunction( const char * str )
{
	Custom::voodooVoidCall( "Example::globalFunction", str );
}
int globalFunctionReturningInt()
{
	return Custom::voodooCall< int >( "Example::globalFunctionReturningInt" );
}
std::string globalFunctionMoveReturn()
{
	return std::move( Custom::voodooMoveCall< std::string >( "Example::globalFunctionMoveReturn" ) );
}

}

#include "Example/UnderTest.h"

using namespace Example;

class Test_Example: public CxxTest::TestSuite
{
public:
	void test_TemplateClassCanBeMocked()
	{
		UnderTest tested;

		Scenario scenario;
		scenario <<
			new Construction< MockMe >( "Fake MockMe" ) <<
				new EqualsValue< int >( 8 ) <<
			new CallReturnVoid( "Fake MockMe::justASimpleVoidMethod" ) <<
				new EqualsValue< int >( 1 ) <<
				new StringEquals( "yada" ) <<
			new CallReturnValue< int >( "Fake MockMe::returnsAnInt", 100 ) <<
			new CallMoveValue< std::unique_ptr< int > >( "Fake MockMe::returnsAUniquePtr",
				std::unique_ptr< int >( new int ) ) <<
			new CallReturnVoid( "Example::globalFunction" ) <<
				new StringEquals( "yada" ) <<
			new CallReturnValue< int >( "Example::globalFunctionReturningInt", 19 ) <<
			new CallMoveValue< std::string >( "Example::globalFunctionMoveReturn", std::string( "yep" ) ) <<
			new Destruction( "Fake MockMe" );
		tested.underTest();
		scenario.assertFinished();
	}
};
