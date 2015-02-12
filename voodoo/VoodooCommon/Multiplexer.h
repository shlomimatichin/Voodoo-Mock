#ifndef __VOODOO_EXPECT_MULTIPLEXER_H__
#define __VOODOO_EXPECT_MULTIPLEXER_H__

#include <VoodooCommon/Scenario.h>
#include <VoodooCommon/Always.h>

namespace VoodooCommon {
namespace Expect
{

class Multiplexer
{
public:
	Multiplexer( const char * whatHappened ) :
		_scenarioCandidatesCount( 0 ) ,
		_selectedAlways( 0 )
	{
		ErrorMessage error;
		error.append( "Unable to find a scenario which expects " );
		error.append( whatHappened );
		error.append( "\n" );
		for ( Scenario * current = Scenario::scenarioTop() ; current != 0 ; current = current->_next ) {
			try {
				current->check( whatHappened );
				VOODOO_ASSERT( _scenarioCandidatesCount < MAX_SCENARIO_CANDIDATES );
				_scenarioCandidates[ _scenarioCandidatesCount ] = current;
				++ _scenarioCandidatesCount;
			} catch ( ErrorMessage & e ) {
				error.append( "\t\t" );
				error.append( e.result() );
				error.append( "\n" );
			}
		}
		if ( _scenarioCandidatesCount > 0 )
			return;
		if ( Scenario::scenarioTop() == 0 )
			error.append( "\t\tNo scenario objects exist!\n" );
		for ( Always * current = Always::alwaysTop() ; current != 0 ; current = current->_next ) {
			try {
				current->check( whatHappened );
				_selectedAlways = current;
				return;
			} catch ( ErrorMessage & e ) {
			}
		}
		throw error;
	}

	void check(	unsigned			parameterIndex ,
				const char *		typeString ,
				const void *		pointerToValue )
	{
		if ( _scenarioCandidatesCount > 0 ) {
			unsigned i = 0;
			ErrorMessage error;
			error.append( "Unable to find a scenario which expects " );
			error.append( VOODOO_TO_STRING( parameterIndex + 1 ) );
			error.append( "th parameter:\n" );
			while ( i < _scenarioCandidatesCount ) {
				try {
					_scenarioCandidates[ i ]->check( parameterIndex , typeString , pointerToValue );
					++ i;
				} catch ( ErrorMessage & e ) {
					error.append( "\t\t" );
					error.append( e.result() );
					error.append( "\n" );
					for ( unsigned j = i ; j < _scenarioCandidatesCount - 1 ; ++ j )
						_scenarioCandidates[ j ] = _scenarioCandidates[ j + 1 ];
					-- _scenarioCandidatesCount;
				}
			}
			if ( _scenarioCandidatesCount == 0 )
				throw error;
		} else {
			VOODOO_ASSERT( _selectedAlways != 0 );
			_selectedAlways->check( parameterIndex , typeString , pointerToValue );
		}
	}

	void effect(    unsigned        parameterIndex,
                    const char *    typeString,
                    const void *    pointerToValue )
	{
		if ( _scenarioCandidatesCount > 0 ) {
            _scenarioCandidates[ 0 ]->effect( parameterIndex , typeString , pointerToValue );
		} else {
			VOODOO_ASSERT( _selectedAlways != 0 );
			_selectedAlways->effect( parameterIndex , typeString , pointerToValue );
		}
	}

	void returnValue( const char * typeString , const void * & value )
	{
		if ( _scenarioCandidatesCount > 0 ) {
			_scenarioCandidatesCount = 1;
			_scenarioCandidates[ 0 ]->returnValue( typeString , value );
		} else {
			VOODOO_ASSERT( _selectedAlways != 0 );
			_selectedAlways->returnValue( typeString , value );
		}
	}

	static void trigger( const char * description )
	{
		try {
			__VoodooGrowingString growingString;
			growingString.append( "Call to " );
			growingString.append( description );
			Multiplexer multiplexer( growingString.result() );
			multiplexer.check( 0, "VOODOO_NO_MORE_PARAMETERS", 0 );
			const void * returnValueAsVoid = 0;
			void * returnValueUnused = 0;
			multiplexer.returnValue(	PointerTypeString( returnValueUnused ).typeString(),
										returnValueAsVoid );
		} catch ( VoodooCommon::ErrorMessage & e ) {
			VoodooCommon::ErrorMessage error;
			error.append( "From " );
			error.append( __FUNCTION__ );
			error.append( "(" );
			error.append( description );
			error.append( "): " );
			error.append( e.result() );
			VOODOO_FAIL_TEST( error.result() );
			throw "VOODOO_FAIL_TEST must throw";
		}
	}

void checkParameterPack( unsigned parameterIndex )
{
	check( parameterIndex, "VOODOO_NO_MORE_PARAMETERS", 0 );
}

template < typename P, typename... Params >
void checkParameterPack( unsigned parameterIndex, P & p1, Params&... params )
{
	check( parameterIndex, VoodooCommon::PointerTypeString( & p1 ).typeString(), & p1 );
	checkParameterPack( parameterIndex + 1, params... );
}

void effectParameterPack( unsigned parameterIndex )
{
	// no-op
}

template < typename P, typename... Params >
void effectParameterPack( unsigned parameterIndex, P &	p1, Params&... params )
{
	effect( parameterIndex, VoodooCommon::PointerTypeString( & p1 ).typeString(), & p1 );
	effectParameterPack( parameterIndex + 1, params... );
}

private:
	enum { MAX_SCENARIO_CANDIDATES = 64 };
	Scenario *	_scenarioCandidates[ MAX_SCENARIO_CANDIDATES ];
	unsigned	_scenarioCandidatesCount;
	Always *	_selectedAlways;
};

} // namespace Expect
} // namespace VoodooCommon

#endif // __VOODOO_EXPECT_MULTIPLEXER_H__
