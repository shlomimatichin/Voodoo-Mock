#ifndef __VOODOO_EXPECT_SCENARIO_H__
#define __VOODOO_EXPECT_SCENARIO_H__

#include <VoodooCommon/Expect.h>

#ifndef VOODOO_EXPECT_MAX_SCENARIO
#define VOODOO_EXPECT_MAX_SCENARIO 4096
#endif // VOODOO_EXPECT_MAX_SCENARIO

#ifndef VOODOO_EXPECT_MAX_SCENARIOS
#define VOODOO_EXPECT_MAX_SCENARIOS 32
#endif // VOODOO_EXPECT_MAX_SCENARIOS

namespace VoodooCommon {
namespace Expect
{

class ExpectationList
{
public:
	ExpectationList() :
		_expectationsCount( 0 ),
		_preIntercepter( 0 )
	{}

	~ ExpectationList()
	{
		VOODOO_ASSERT_NO_THROW( _preIntercepter == 0 );
		for ( unsigned i = 0 ; i < _expectationsCount ; ++ i )
			delete _expectations[ i ];
	}

	ExpectationList( const ExpectationList & other ) :
		_expectationsCount( 0 ),
		_preIntercepter( 0 )
	{
		insertBefore( _expectationsCount, * (ExpectationList *) & other );
	}

	ExpectationList & operator << ( PreIntercepter * preIntercepter )
	{
		VOODOO_ASSERT( preIntercepter != 0 );
		VOODOO_ASSERT( _preIntercepter == 0 );
		_preIntercepter = preIntercepter;
		return * this;
	}

	ExpectationList & operator << ( PostIntercepter * postIntercepter )
	{
		VOODOO_ASSERT( postIntercepter != 0 );
		VOODOO_ASSERT( _expectationsCount > 0 );
		( * postIntercepter ) << _expectations[ _expectationsCount - 1 ];
		_expectations[ _expectationsCount - 1 ] = postIntercepter;
		return * this;
	}

	ExpectationList & operator << ( Interface * expectation )
	{
		if ( expectation == 0 ) {
			VOODOO_FAIL_TEST( "You must not add a null pointer as an expectation to the scenario" );
		}
		if ( _expectationsCount >= VOODOO_EXPECT_MAX_SCENARIO ) {
			VOODOO_FAIL_TEST( "You have more than " __VOODOO_QUOTE( VOODOO_EXPECT_MAX_SCENARIO )
					" expectations in your scenario. Please #define "
					" VOODOO_EXPECT_MAX_SCENARIO to a larger value" );
		}
		if ( _preIntercepter ) {
			( * _preIntercepter ) << expectation;
			expectation = _preIntercepter;
			_preIntercepter = 0;
		}
		_expectations[ _expectationsCount ] = expectation;
		++ _expectationsCount;
		return * this;
	}

	ExpectationList & operator << ( Parameter::Interface * parameter )
	{
		if ( _expectationsCount == 0 ) {
			VOODOO_FAIL_TEST( "Attempted to added a parameter before any expectation" );
		}
		VOODOO_ASSERT( _expectations[ _expectationsCount - 1 ] != 0 );
		* _expectations[ _expectationsCount - 1 ] << parameter;
		return * this;
	}

	ExpectationList & operator << ( ExpectationList & ripFrom )
	{
		insertBefore( _expectationsCount, ripFrom );
		return * this;
	}

#ifdef __GNUC__
	ExpectationList & operator << ( ExpectationList ripFrom )
	{
		insertBefore( _expectationsCount, ripFrom );
		return * this;
	}
#endif // __GNUC__

	void insertBefore( unsigned pos, ExpectationList & inserted )
	{
		VOODOO_ASSERT( inserted._expectationsCount + _expectationsCount < VOODOO_EXPECT_MAX_SCENARIO );
		for ( int i = _expectationsCount - 1 ; i >= (int) pos ; -- i )
			_expectations[ i + inserted._expectationsCount ] = _expectations[ i ];
		for ( unsigned i = 0 ; i < inserted._expectationsCount ; ++ i )
			_expectations[ pos + i ] = inserted._expectations[ i ];
		_expectationsCount += inserted._expectationsCount;
		inserted._expectationsCount = 0;
	}

	void insertAfter( unsigned pos, ExpectationList & inserted )
	{
		insertBefore( pos + 1, inserted );
	}

	void truncateInclusive( const char * what )
	{
		truncateInclusive( find( what ) );
	}

	void truncateInclusive( unsigned pos )
	{
		VOODOO_ASSERT( pos <= _expectationsCount );
		VOODOO_ASSERT( _expectationsCount >= 1 );
		for ( int i = _expectationsCount - 1; i >= (int) pos ; -- i )
			delete _expectations[ i ];
		_expectationsCount = pos;
	}
	
	void truncateExclusive( const char * what )
	{
		truncateExclusive( find( what ) );
	}

	void truncateExclusive( unsigned pos )
	{
		truncateInclusive( pos + 1 );
	}

	void remove( unsigned pos )
	{
		VOODOO_ASSERT( pos < _expectationsCount );
		VOODOO_ASSERT( _expectations[ pos ] != 0 );
		delete _expectations[ pos ];
		for ( unsigned i = pos; i < _expectationsCount - 1; ++ i )
			_expectations[ i ] = _expectations[ i + 1 ];
		-- _expectationsCount;
	}

	void remove( const char * what )
	{
		remove( find( what ) );
	}

	unsigned find( const char * what )
	{
		for ( unsigned i = 0 ; i < _expectationsCount ; ++ i ) {
			VOODOO_ASSERT( _expectations[ i ] != 0 );
			try {
				_expectations[ i ]->check( what );
				return i;
			} catch ( ErrorMessage & e ) {
			}
		}

		ErrorMessage error;
		error.append( "Unable to find expectation that matches '" );
		error.append( what );
		error.append( "'" );
		throw error;
	}

protected:
	unsigned expectationsCount() const { return _expectationsCount; }

	Interface & expectation( unsigned pos )
	{
		VOODOO_ASSERT( pos < _expectationsCount );
		VOODOO_ASSERT( _expectations[ pos ] != 0 );
		return * _expectations[ pos ];
	}

private:
	Interface *				_expectations[ VOODOO_EXPECT_MAX_SCENARIO ];
	unsigned				_expectationsCount;
	PreIntercepter *		_preIntercepter;
};

class InsertingExpectationList : public ExpectationList
{
public:
	InsertingExpectationList( ExpectationList & edited, unsigned pos, bool after ) :
		_edited( & edited ),
		_insertionPos( pos + ( after ? 1 : 0 ) )
	{
	}

	InsertingExpectationList( ExpectationList & edited, const char * where, bool after ) :
		_edited( & edited ),
		_insertionPos( edited.find( where ) + ( after ? 1 : 0 ) )
	{
	}

	InsertingExpectationList( const InsertingExpectationList & other )
	{
		VOODOO_ASSERT( other.expectationsCount() == 0 );
		InsertingExpectationList & otherMutable = * (InsertingExpectationList *) & other;
		_edited = other._edited;
		_insertionPos = other._insertionPos;
		otherMutable._edited = 0;
		otherMutable._insertionPos = (unsigned) -1;
	}

	~ InsertingExpectationList()
	{
		if ( _edited != 0 )
			_edited->insertBefore( _insertionPos, * this );
	}

	unsigned insertionPos()
	{
		return _insertionPos;
	}

private:
	ExpectationList *	_edited;
	unsigned			_insertionPos;
};

class Scenario : public ExpectationList
{
public:
	Scenario( const char * scenarioName = "DEFAULT" ) : 
		_pos( 0 ) ,
		_scenarioName( scenarioName ) ,
		_finishCalled( false )
	{
		_next = scenarioTop();
		_previous = & scenarioTop();
		scenarioTop() = this;
		if ( _next != 0 )
			_next->_previous = & this->_next;
	}

	~Scenario()
	{
		if ( ! _finishCalled ) {
			ErrorMessage error;
			error.append( "Scenario::finish() was not called. Did you forget? " );
			error.append( "This might also happen if some other exception was thrown." );
			VOODOO_WARNING( error.result() );
		}
		* _previous = _next;
		if ( _next != 0 )
			_next->_previous = _previous;
	}

	void assertFinished()
	{
		_finishCalled = true;
		if ( _pos < expectationsCount() ) {
			ErrorMessage error;
			error.append( "Scenario " );
			error.append( _scenarioName );
			error.append( " expected " );
			error.append( VOODOO_TO_STRING( expectationsCount() ) );
			error.append( " events, but only " );
			error.append( VOODOO_TO_STRING( _pos ) );
			error.append( " happened. Next waiting: '" );
			try {
				expectation( _pos ).check( "nothing happened" );
			} catch ( ErrorMessage & next ) {
				error.append( next.result() );
			}
			error.append( "'" );
			VOODOO_FAIL_TEST( error.result() );
		}
	}

	void assertNotFinished()
	{
		_finishCalled = true;
		if ( _pos >= expectationsCount() ) {
			ErrorMessage error;
			error.append( "Scenario " );
			error.append( _scenarioName );
			error.append( " expected " );
			error.append( VOODOO_TO_STRING( expectationsCount() ) );
			error.append( " events, to not complete, but it did." );
			VOODOO_FAIL_TEST( error.result() );
		}
	}

	void check( const char * whatHappened )
	{
		if ( _pos >= expectationsCount() ) {
			ErrorMessage error;
			error.append( "Scenario expected " );
			error.append( VOODOO_TO_STRING( expectationsCount() ) );
			error.append( " events, but afterwards, came " );
			error.append( whatHappened );
			throw error;
		}
		try {
			expectation( _pos ).check( whatHappened );
		} catch ( ErrorMessage & e ) {
			ErrorMessage error;
			error.append( "In scenario " );
			error.append( _scenarioName );
			error.append( " Expectation " );
			error.append( VOODOO_TO_STRING( _pos ) );
			error.append( " : " );
			error.append( e.result() );
			throw error;
		}
	}

	void check(	unsigned			parameterIndex ,
				const char *		typeString ,
				const void *		pointerToValue )
	{
		VOODOO_ASSERT( _pos < expectationsCount() );
		try {
			expectation( _pos ).check( parameterIndex , typeString , pointerToValue );
		} catch ( ErrorMessage & e ) {
			ErrorMessage error;
			error.append( "In scenario " );
			error.append( _scenarioName );
			error.append( " Expectation " );
			error.append( VOODOO_TO_STRING( _pos ) );
			error.append( ": " );
			error.append( e.result() );
			throw error;
		}
	}

	void effect(    unsigned        parameterIndex,
                    const char *    typeString,
                    const void *    pointerToValue )
	{
		VOODOO_ASSERT( _pos < expectationsCount() );
		try {
			expectation( _pos ).effect( parameterIndex , typeString , pointerToValue );
		} catch ( ErrorMessage & e ) {
			ErrorMessage error;
			error.append( "In scenario " );
			error.append( _scenarioName );
			error.append( " Expectation " );
			error.append( VOODOO_TO_STRING( _pos ) );
			error.append( ": " );
			error.append( e.result() );
			throw error;
		}
	}

	void returnValue( const char * typeString , const void * & value )
	{
		VOODOO_ASSERT( _pos < expectationsCount() );
		unsigned pos = _pos;
		advance();
		try {
			expectation( pos ).returnValue( typeString , value );
		} catch ( ErrorMessage & e ) {
			ErrorMessage error;
			error.append( "In scenario " );
			error.append( _scenarioName );
			error.append( " Expectation " );
			error.append( VOODOO_TO_STRING( pos ) );
			error.append( ": " );
			error.append( e.result() );
			throw error;
		}
	}

	void advance()
	{
		++ _pos;
	}

	static Scenario * & scenarioTop()
	{
		static Scenario * scenarioTop;
		return scenarioTop;
	}

	InsertingExpectationList replace( const char * where )
	{
		InsertingExpectationList result( * this, where, false );
		remove( result.insertionPos() );
		return result;
	}

	InsertingExpectationList insertBefore( const char * where )
	{
		return InsertingExpectationList( * this, where, false );
	}

	InsertingExpectationList insertAfter( const char * where )
	{
		return InsertingExpectationList( * this, where, true );
	}

	InsertingExpectationList insertBefore( unsigned pos )
	{
		return InsertingExpectationList( * this, pos, false );
	}

	InsertingExpectationList insertAfter( unsigned pos )
	{
		return InsertingExpectationList( * this, pos, true );
	}

	Scenario *		_next;
	Scenario * *	_previous;

private:
	unsigned		_pos;
	const char *	_scenarioName;
	bool			_finishCalled;
};

class ScenarioList
{
public:
	ScenarioList() :
		_scenariosCount( 0 )
	{}

	Scenario & spawn()
	{
		if ( _scenariosCount >= VOODOO_EXPECT_MAX_SCENARIOS ) {
			VOODOO_FAIL_TEST( "You have more than " __VOODOO_QUOTE( VOODOO_EXPECT_MAX_SCENARIOS )
					" scenarios in your scenario list. Please #define "
					" VOODOO_EXPECT_MAX_SCENARIOS to a larger value" );
		}
		Scenario & scenario = _scenarios[ _scenariosCount ];
		++ _scenariosCount;
		return scenario;
	}

	void assertFinished()
	{
		for ( unsigned i = 0 ; i < VOODOO_EXPECT_MAX_SCENARIOS ; ++ i )
			_scenarios[ i ].assertFinished();
	}

private:
	Scenario _scenarios[ VOODOO_EXPECT_MAX_SCENARIOS ];
	unsigned _scenariosCount;

};

} // namespace Expect
} // namespace VoodooCommon

#endif // __VOODOO_EXPECT_SCENARIO_H__
