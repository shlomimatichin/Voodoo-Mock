#define VOODOO_EXPECT_PseudoSharedPtr_h

#include "GetAndSet.h"

#include <stdio.h>

using namespace VoodooCommon::Expect;
using namespace VoodooCommon::Expect::Parameter;
class TestFailed {};

void testConsiderCopyConstruction()
{
	Scenario scenario;
	scenario <<
		new CallReturnAuto< PseudoSharedPtr >( "get", new FakeND_PseudoSharedPtr( "IT" ) ) <<
		new CallReturnVoid( "setFirst" ) <<
			new Named< PseudoSharedPtr >( "Copy of Copy of IT" ) <<
		new Destruction( "Copy of Copy of IT" ) <<
		new CallReturnVoid( "setSecond" ) <<
			new Named< PseudoSharedPtr >( "Copy of Copy of IT" ) <<
		new Destruction( "Copy of Copy of IT" ) <<
		new Destruction( "Copy of IT" );
	getAndSet();
	scenario.assertFinished();
}

void testIgnoreCopyConstruction()
{
	Always always;
	always <<
		new Destruction( "Copy of Copy of IT" ) <<
		new Destruction( "Copy of IT" );
	Scenario scenario;
	scenario <<
		new CallReturnAuto< PseudoSharedPtr >( "get", new FakeND_PseudoSharedPtr( "IT" ) ) <<
		new CallReturnVoid( "setFirst" ) <<
			new NamedOrCopyOf< PseudoSharedPtr >( "IT" ) <<
		new CallReturnVoid( "setSecond" ) <<
			new NamedOrCopyOf< PseudoSharedPtr >( "IT" );
	getAndSet();
	scenario.assertFinished();
}

int main()
{
	testConsiderCopyConstruction();
	testIgnoreCopyConstruction();

	printf( "OK!\n" );

	return 0;
}
