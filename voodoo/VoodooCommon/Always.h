#ifndef __VOODOO_EXPECT_ALWAYS_H__
#define __VOODOO_EXPECT_ALWAYS_H__

#include <VoodooCommon/Scenario.h>

#ifndef VOODOO_EXPECT_MAX_SCENARIO
#define VOODOO_EXPECT_MAX_SCENARIO 4096
#endif // VOODOO_EXPECT_MAX_SCENARIO

namespace VoodooCommon {
namespace Expect
{

class Always : public ExpectationList
{
public:
	Always() : 
		_lastExpectationsPassedCount( 0 ) ,
		_preIntercepter( 0 )
	{
		_next = alwaysTop();
		_previous = & alwaysTop();
		alwaysTop() = this;
		if ( _next != 0 )
			_next->_previous = & this->_next;
	}

	~Always()
	{
		VOODOO_ASSERT_NO_THROW( _preIntercepter == 0 );
		* _previous = _next;
		if ( _next != 0 )
			_next->_previous = _previous;
	}

	void check( const char * whatHappened )
	{
		_lastExpectationsPassedCount = 0;
		for ( int i = expectationsCount() - 1 ; i >= 0 ; -- i ) {
			try {
				expectation( i ).check( whatHappened );
				_lastExpectationsPassed[ _lastExpectationsPassedCount ] = i;
				++ _lastExpectationsPassedCount;
			} catch ( ErrorMessage & e ) {
			}
		}
		if ( _lastExpectationsPassedCount == 0 ) {
			ErrorMessage error;
			error.append( "No expectation in always, expects " );
			error.append( whatHappened );
			throw error;
		}
	}

	void check(	unsigned			parameterIndex ,
				const char *		typeString ,
				const void *		pointerToValue )
	{
		VOODOO_ASSERT( _lastExpectationsPassedCount > 0 );
		bool hasMatch = false;
		for ( unsigned i = 0 ; i < _lastExpectationsPassedCount ; ++ i ) {
			unsigned index = _lastExpectationsPassed[ i ];	
			VOODOO_ASSERT( index <= expectationsCount() );
            expectation( index );
			try {
				expectation( index ).check( parameterIndex , typeString , pointerToValue );
				hasMatch = true;
				break;
			} catch ( ErrorMessage & ) {
			}
		}
		if ( hasMatch ) {
			unsigned i = 0;
			while ( i < _lastExpectationsPassedCount ) {
				unsigned index = _lastExpectationsPassed[ i ];	
				VOODOO_ASSERT( index <= expectationsCount() );
                expectation( index );
				try {
					expectation( index ).check( parameterIndex , typeString , pointerToValue );
					++ i;
				} catch ( ErrorMessage & ) {
					for ( unsigned j = i ; j < _lastExpectationsPassedCount - 1 ; ++ j ) {
						_lastExpectationsPassed[ j ] = _lastExpectationsPassed[ j + 1 ];
					}
					-- _lastExpectationsPassedCount;
				}
			}
		} else {
			ErrorMessage grandError;
			for ( unsigned i = 0 ; i < _lastExpectationsPassedCount ; ++ i ) {
				unsigned index = _lastExpectationsPassed[ i ];	
				VOODOO_ASSERT( index <= expectationsCount() );
                expectation( index );
				try {
					expectation( index ).check( parameterIndex , typeString , pointerToValue );
					VOODOO_ASSERT( 0 );
				} catch ( ErrorMessage & e ) {
					grandError.append( "\nIn Always expectation " );
					grandError.append( VOODOO_TO_STRING( index ) );
					grandError.append( ": " );
					grandError.append( e.result() );
				}
			}
			throw grandError;
		}
	}

	void effect(    unsigned        parameterIndex,
                    const char *    typeString,
                    const void *    pointerToValue )
	{
		VOODOO_ASSERT( _lastExpectationsPassedCount > 0 );
		unsigned index = _lastExpectationsPassed[ 0 ];
		VOODOO_ASSERT( index < expectationsCount() );
        expectation( index );
		try {
			expectation( index ).effect( parameterIndex, typeString, pointerToValue );
		} catch ( ErrorMessage & e ) {
			ErrorMessage error;
			error.append( "In always scenario, Expectation " );
			error.append( VOODOO_TO_STRING( index ) );
			error.append( ": " );
			error.append( e.result() );
			throw error;
		}
	}

	void returnValue( const char * typeString , const void * & value )
	{
		VOODOO_ASSERT( _lastExpectationsPassedCount > 0 );
		unsigned index = _lastExpectationsPassed[ 0 ];
		VOODOO_ASSERT( index < expectationsCount() );
        expectation( index );
		_lastExpectationsPassedCount = 0;
		try {
			expectation( index ).returnValue( typeString , value );
		} catch ( ErrorMessage & e ) {
			ErrorMessage error;
			error.append( "In always scenario, Expectation " );
			error.append( VOODOO_TO_STRING( index ) );
			error.append( ": " );
			error.append( e.result() );
			throw error;
		}
	}

	static Always * & alwaysTop()
	{
		static Always * alwaysTop = NULL;
		return alwaysTop;
	}

	Always *		_next;
	Always * *		_previous;

private:
	unsigned				_lastExpectationsPassed[ VOODOO_EXPECT_MAX_SCENARIO ];
	unsigned				_lastExpectationsPassedCount;
	PreIntercepter *		_preIntercepter;
};

} // namespace Expect
} // namespace VoodooCommon

#endif // __VOODOO_EXPECT_ALWAYS_H__
