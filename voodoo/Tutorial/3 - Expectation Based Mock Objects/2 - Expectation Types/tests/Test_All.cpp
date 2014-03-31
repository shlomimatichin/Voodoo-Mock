#define VOODOO_EXPECT_Mocked_h

#include "Tested.h"

#include <stdio.h>

using namespace VoodooCommon::Expect;
class TestFailed {};

void testCallGlobalFunction()
{
	Scenario scenario;
	scenario <<
		new CallReturnVoid( "globalFunction" );

	callGlobalFunction();

	scenario.assertFinished();
}

void testCallGlobalNamespacedFunction()
{
	Scenario scenario;
	scenario <<
		new CallReturnValue< double >( "MockedNamespace::globalNamespacedFunction" , 0.1 );

	if ( callGlobalNamespacedFunction() != 0.1 )
		throw TestFailed();

	scenario.assertFinished();
}

void testCallStaticMethod()
{
	Scenario scenario;
	unsigned retVal = 10;
	scenario <<
		new CallReturnReference< unsigned >( "MockedClass::staticMethod" , retVal );

	++ callStaticMethod();

	if ( retVal != 11 )
		throw TestFailed();
	scenario.assertFinished();
}

void testConstructObjectCallMethodAndThenDestroy()
{
	Scenario scenario;
	scenario <<
		new Construction< MockedClass >( "The Fake Instance" ) <<
		new CallReturnValue< char >( "The Fake Instance::method" , '4' ) <<
		new Destruction( "The Fake Instance" );

	if ( constructClassToCallMethod() != '4' )
		throw TestFailed();
	scenario.assertFinished();
}

void testExceptionHandeled()
{
	Scenario scenario;
	scenario <<
		new CallThrowValue< std::runtime_error >( "makeRunTimeError",
									std::runtime_error( "ignored" ) );
	catchRunTimeError();
	scenario.assertFinished();
}

class Strcmp : public Parameter::StrongTyped< const char * >
{
public:
	Strcmp( const char * compareTo ) :
		StrongTyped< const char * >( "Strcmp" ),
		_compareTo( compareTo )
	{
	}

private:
	const char * _compareTo;

	void compare( const char * & parameter )
	{
		if ( strcmp( parameter, _compareTo ) != 0 ) {
			VoodooCommon::ErrorMessage e;
			e.append( "Strings not equal: '" );
			e.append( parameter );
			e.append( "', and '" );
			e.append( _compareTo );
			e.append( "'" );
			throw e;
		}
	}
};

void testLogWorks()
{
	Scenario scenario;
	scenario <<
		new Construction< File >( "Fake File" ) <<
			new Strcmp( "C:\\log.txt" ) <<
		new CallReturnVoid( "Fake File::writeString" ) <<
			new Strcmp( "fake log message" ) <<
		new Destruction( "Fake File" );
	logMessage( "fake log message" );
	scenario.assertFinished();
}

void testConstructorThrows()
{
	Scenario scenario;
	scenario <<
		new ConstructionThrowValue< File, std::runtime_error >(
			   						std::runtime_error( "File not found!" ) ) <<
			new Strcmp( "C:\\log.txt" );	
	logMessage( "message" );
	scenario.assertFinished();
}

int main()
{
	testCallGlobalFunction();
	testCallGlobalNamespacedFunction();
	testCallStaticMethod();
	testConstructObjectCallMethodAndThenDestroy();
	testExceptionHandeled();
	testLogWorks();
	testConstructorThrows();

	printf( "OK!\n" );

	return 0;
}
