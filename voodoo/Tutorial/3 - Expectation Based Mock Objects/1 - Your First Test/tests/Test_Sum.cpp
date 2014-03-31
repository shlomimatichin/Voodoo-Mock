// the following line replaces the implementation of Number.h with an
// expectation based mock objects implementation, which causes all the
// definitions in it, i.e., the definition of the class Number, to be
// mocked. This line must preceed any include directives to other code
// that might eventually include Number.h
#define VOODOO_EXPECT_Number_h

#include "Sum.h"

#include <stdio.h>

// this using directive is not mandatory, it just shortens the lines below.
using namespace VoodooCommon::Expect;

class TestFailed {};

int main()
{
	// a VoodooCommon::Expect::Scenario object is a pre-made recording. the
	// tester fills it with what ever is supposed to happen, in the order
	// it supposed to happen in.
	Scenario scenario;
	// 1. the method 'value' of the object called 'Fake Number 1' is called.
	//    it will return an 'unsigned': 100.
	// 2. the method 'value' of the object called 'Fake Number 2' is called.
	//    it will return an 'unsigned': 200.
	scenario <<
		new CallReturnValue< unsigned >( "Fake Number 1::value" , 100 ) <<
		new CallReturnValue< unsigned >( "Fake Number 2::value" , 200 );

	// The class FakeND_Number derives from Number. It allows the tester to
	// name the object. Also, this specific object destruction will not
	// be relayed to the scenario.
	FakeND_Number number1( "Fake Number 1" );
	FakeND_Number number2( "Fake Number 2" );

	// compare the result of the sum of the two fake objects: 100 + 200 == 300
	if ( Sum( number1 , number2 ).result() != 300 )
		throw TestFailed();

	// the scenario should be complete: both events accoured.
	scenario.assertFinished();

	printf( "OK!\n" );

	return 0;
}
