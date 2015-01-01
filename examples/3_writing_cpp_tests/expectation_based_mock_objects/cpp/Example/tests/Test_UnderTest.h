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

	void test_Named()
	{
		FakeND_AMockedStruct fake( "fakeStruct" );

		Scenario scenario;
		scenario <<
			new CallReturnVoid( "operateOnStruct" ) <<
				new Named< AMockedStruct >( "fakeStruct" );
		doSomething( fake );
		scenario.assertFinished();
	}

	void test_NamedOfPtr()
	{
		FakeND_AMockedStruct fake( "fakeStruct" );

		Scenario scenario;
		scenario <<
			new CallReturnVoid( "operateOnStructPtr" ) <<
				new Named< AMockedStruct * >( "fakeStruct" );
		doSomethingOnPtr( &fake );
		scenario.assertFinished();
	}

	void test_NamedOfUniquePtr()
	{
		std::unique_ptr< FakeND_AMockedStruct> fake( new FakeND_AMockedStruct( "fakeStruct" ) );

		Scenario scenario;
		scenario <<
			new CallReturnVoid( "operateOnStructUniquePtr" ) <<
				new Named< std::unique_ptr< AMockedStruct > >( "fakeStruct" );
		doSomethingOnUniquePtr( std::move( fake ) );
		scenario.assertFinished();
	}

	void test_Ignore()
	{
		Scenario scenario;
		scenario <<
			new CallReturnVoid( "setInterval" ) <<
			new Ignore< unsigned >();
		setDefaultInterval();
		scenario.assertFinished();
	}

	void test_EqualsValue()
	{
		Scenario scenario;
		scenario <<
			new CallReturnVoid( "setInterval" ) <<
			new EqualsValue< unsigned >( 4 );
		setDefaultInterval();
		scenario.assertFinished();
	}

	void test_EqualsReference()
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

	void test_SameDataValue()
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

	void test_ReferenceTo()
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

	void test_MoveValueConstructor()
	{
		MoveableCtorData data( 15 );
		MoveableCtorData * outData;
		Scenario scenario;
		scenario <<
			new CallReturnVoid( "doMoveData" ) <<
			new MoveValueConstructor< MoveableCtorData >( outData );
		moveData( std::move( data ) );
		scenario.assertFinished();
		if ( outData->a != 15 ) throw TestFailed();
	}

	void test_MoveValueAssignment()
	{
		MoveableData data( 15 );
		MoveableData outData( 1 );
		Scenario scenario;
		scenario <<
			new CallReturnVoid( "doMoveData" ) <<
			new MoveValueAssignment< MoveableData >( & outData );
		moveData( std::move( data ) );
		scenario.assertFinished();
		if ( outData.a != 15 ) throw TestFailed();
	}

	void test_SaveValue()
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

	void test_SaveSimpleValue()
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

	void test_SaveReference()
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

	void test_AssignValue()
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

	void test_AssignValueToPointer()
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

	void test_SimplePredicate()
	{
		class MarkString { public:
			bool operator () ( const char * string )
			{ return strcmp( string, "MARK" ) == 0; }
		};

		Scenario scenario;
		scenario <<
			new CallReturnVoid( "logMessage" ) <<
			new PredicateSimple< const char *, MarkString >();
		markLog();
		scenario.assertFinished();
	}

	void test_PredicateValue()
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

	void test_PredicateReference()
	{
		class Strcmp { public:
			Strcmp( const char * string ) : _string( string ) {}
			const char * _string;
			bool operator () ( const char * string )
			{ return strcmp( string, _string ) == 0; }
		private:
			Strcmp( const Strcmp & ) {}
		};

		Strcmp comparer( "MARK" );

		Scenario scenario;
		scenario <<
			new CallReturnVoid( "logMessage" ) <<
			new PredicateReference< const char *, Strcmp >( comparer );
		markLog();
		scenario.assertFinished();
	}

	void test_Custom()
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

};
