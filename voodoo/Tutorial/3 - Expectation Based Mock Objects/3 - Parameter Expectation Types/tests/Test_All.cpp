#define VOODOO_EXPECT_Mocked_h

#include "Tested.h"

#include <stdio.h>

using namespace VoodooCommon::Expect;
using namespace VoodooCommon::Expect::Parameter;
class TestFailed {};

void testIgnore()
{
	Scenario scenario;
	scenario <<
		new CallReturnVoid( "setInterval" ) <<
			new Ignore< unsigned >();
	setDefaultInterval();
	scenario.assertFinished();
}

void testNamed()
{
	Scenario scenario;
	FakeND_Spreadsheet fakeSpreadSheet( "Fake Spreadsheet" );
	scenario <<
		new CallReturnVoid( "clear" ) <<
			new Named< Spreadsheet >( "Fake Spreadsheet" ) <<
		new CallReturnVoid( "clear" ) <<
			new Named< Spreadsheet >( "Fake Spreadsheet" );
	doubleClear( fakeSpreadSheet );
	scenario.assertFinished();
}

void testNamedOrCopyOf()
{
	Scenario scenario;
	FakeND_Spreadsheet fakeSpreadSheet( "Fake Spreadsheet" );
	scenario <<
		new CallReturnVoid( "clear" ) <<
			new Named< Spreadsheet >( "Copy of Fake Spreadsheet" ) <<
		new Destruction( "Copy of Fake Spreadsheet" );
	copyAndClear( fakeSpreadSheet );
	scenario.assertFinished();
}

void testEqualsValue()
{
	Scenario scenario;
	scenario <<
		new CallReturnVoid( "setInterval" ) <<
			new EqualsValue< unsigned >( 4 );
	setDefaultInterval();
	scenario.assertFinished();
}

void testEqualsReference()
{
	Scenario scenario;
	unsigned expected = 4;
	scenario <<
		new CallReturnVoid( "setInterval" ) <<
			new EqualsReference< unsigned >( expected ) <<
		new CallReturnVoid( "setInterval" ) <<
			new EqualsReference< unsigned >( expected );
	setDefaultInterval();
	expected = 10;
	setHighInterval();
	scenario.assertFinished();
}

void testSameDataValue()
{
	struct Data input = { 1, 2 };
	struct Data expected = { 2, 1 };
	Scenario scenario;
	scenario <<
		new CallReturnVoid( "giveData" ) <<
			new SameDataValue< struct Data >( expected );
	giveDataSwitched( input );
	scenario.assertFinished();
}

void testReferenceTo()
{
	struct Data input = { 1, 2 };
	struct Data expected = { 2, 1 };
	Scenario scenario;
	scenario <<
		new CallReturnVoid( "giveData" ) <<
			new SameDataValue< struct Data >( expected );
	giveDataSwitched( input );
	scenario.assertFinished();
}

void testSaveValue()
{
	struct Data input = { 1, 2 };
	struct Data * result;
	Scenario scenario;
	scenario <<
		new CallReturnVoid( "giveData" ) <<
			new SaveValue< struct Data >( result );
	giveDataSwitched( input );
	scenario.assertFinished();
	struct Data expected = { 2, 1 };
	if ( memcmp( result, & expected, sizeof( * result ) ) != 0 )
		throw TestFailed();
	delete result;
}

void testSaveSimpleValue()
{
	Scenario scenario;
	DoItInterface * saved;
	scenario <<
		new CallReturnVoid( "setCallback" ) <<
			new SaveSimpleValue< DoItInterface * >( saved );
	setCallbackByPointer();
	scenario.assertFinished();

	scenario <<
		new CallReturnVoid( "setInterval" ) <<
			new EqualsValue< unsigned >( 1 );
	saved->doIt();
	scenario.assertFinished();
}

void testSaveReference()
{
	Scenario scenario;
	DoItInterface * saved;
	scenario <<
		new CallReturnVoid( "setCallback" ) <<
			new SaveReference< DoItInterface >( saved );
	setCallbackByReference();
	scenario.assertFinished();

	scenario <<
		new CallReturnVoid( "setInterval" ) <<
			new EqualsValue< unsigned >( 0 );
	saved->doIt();
	scenario.assertFinished();
}

void testAssignValue()
{
	Scenario scenario;
	scenario <<
		new CallReturnVoid( "returnValueByReferenceOutParamter" ) <<
			new AssignValue< unsigned >( 100 );
	unsigned result = outParameterToReturnValue();
	scenario.assertFinished();
	if ( result != 100 )
		throw TestFailed();
}

void testAssignValueToPointer()
{
	Scenario scenario;
	scenario <<
		new CallReturnVoid( "returnValueByPointerOutParamter" ) <<
			new AssignValueToPointer< unsigned >( 400 );
	unsigned result = outPointerParameterToReturnValue();
	scenario.assertFinished();
	if ( result != 400 )
		throw TestFailed();
}

void testAssignRefernce()
{
	Scenario scenario;
	unsigned input = 101;
	scenario <<
		new CallReturnVoid( "returnValueByReferenceOutParamter" ) <<
			new AssignReference< unsigned >( input ) <<
		new CallReturnVoid( "returnValueByReferenceOutParamter" ) <<
			new AssignReference< unsigned >( input );
	unsigned result1 = outParameterToReturnValue();
	input = 102;
	unsigned result2 = outParameterToReturnValue();
	scenario.assertFinished();
	if ( result1 != 101 )
		throw TestFailed();
	if ( result2 != 102 )
		throw TestFailed();
}

void testSimplePredicate()
{
	class MarkString { public:
		bool operator () ( const char * string ) 
			{ return strcmp( string, "MARK" ) == 0; }
	};

	Scenario scenario;
	scenario <<
		new CallReturnVoid( "logMessage" ) <<
			new SimplePredicate< const char *, MarkString >();
	markLog();
	scenario.assertFinished();
}

void testPredicateValue()
{
	class Strcmp { public:
		Strcmp( const char * string ) : _string( string ) {}
		const char * _string;
		bool operator () ( const char * string ) 
			{ return strcmp( string, _string ) == 0; }
	};

	Scenario scenario;
	scenario <<
		new CallReturnVoid( "logMessage" ) <<
			new PredicateValue< const char *, Strcmp >( Strcmp( "MARK" ) );
	markLog();
	scenario.assertFinished();
}

void testPredicateReference()
{
	class Strcmp { public:
		Strcmp( const char * string ) : _string( string ) {}
		const char * _string;
		bool operator () ( const char * string ) 
			{ return strcmp( string, _string ) == 0; }
	private:
		Strcmp( const Strcmp & ) {}
	};

	Scenario scenario;
	scenario <<
		new CallReturnVoid( "logMessage" ) <<
			new PredicateReference< const char *, Strcmp >( Strcmp( "MARK" ) );
	markLog();
	scenario.assertFinished();
}

void testCustom()
{
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

	Scenario scenario;
	scenario <<
		new CallReturnVoid( "logMessage" ) <<
			new Strcmp( "MARK" );
	markLog();
	scenario.assertFinished();
}

int main()
{
	testIgnore();
	testNamed();
	testNamedOrCopyOf();
	testEqualsValue();
	testEqualsReference();
	testSameDataValue();
	testReferenceTo();
	testSaveValue();
	testSaveSimpleValue();
	testSaveReference();
	testAssignValue();
	testAssignValueToPointer();
	testAssignRefernce();
	testSimplePredicate();
	testPredicateValue();
	testPredicateReference();
	testCustom();

	printf( "OK!\n" );

	return 0;
}
