#ifndef __VOODOO_EXPECT_CUSTOM_H__
#define __VOODOO_EXPECT_CUSTOM_H__

#include <VoodooCommon/All.h>

namespace VoodooCommon {
namespace Expect {
namespace Custom
{

void multiplexerCheckParameters( VoodooCommon::Expect::Multiplexer & multiplexer, unsigned parameterIndex )
{
	multiplexer.check( parameterIndex, "VOODOO_NO_MORE_PARAMETERS", 0 );
}

template < typename P, typename... Params >
void multiplexerCheckParameters( VoodooCommon::Expect::Multiplexer & multiplexer, unsigned parameterIndex, P & p1, Params&... params )
{
	multiplexer.check( parameterIndex, VoodooCommon::PointerTypeString( & p1 ).typeString(), & p1 );
	multiplexerCheckParameters( multiplexer, parameterIndex + 1, params... );
}

void multiplexerEffectParameters( VoodooCommon::Expect::Multiplexer & multiplexer, unsigned parameterIndex )
{
	// no-op
}

template < typename P, typename... Params >
void multiplexerEffectParameters( VoodooCommon::Expect::Multiplexer & multiplexer, unsigned parameterIndex, P &	p1, Params&... params )
{
	multiplexer.effect( parameterIndex, VoodooCommon::PointerTypeString( & p1 ).typeString(), & p1 );
	multiplexerEffectParameters( multiplexer, parameterIndex + 1, params... );
}

class Klass
{
public:
	const char * voodooInstanceName() const
	{
		return __voodooInstanceName;
	}

	void voodooSetInstanceName( const char * instanceName )
	{
		strncpy( __voodooInstanceName, instanceName, VOODOO_EXPECT_MAX_INSTANCE_NAME );
	}

protected:
	Klass( const char * className ) :
        __voodooClassName(),
        __voodooInstanceName()
	{
		strncpy( __voodooClassName, className, VOODOO_EXPECT_MAX_INSTANCE_NAME );
	}

	template < typename... Params >
	void voodooConstructor( Params&... params )
	{
		try {
			__VoodooGrowingString growingString;
			growingString.append( "Construction of " );
			growingString.append( __voodooClassName );
			VoodooCommon::Expect::Multiplexer multiplexer( growingString.result() );
			multiplexer.checkParameterPack( 0, params... );
			multiplexer.effectParameterPack( 0, params... );
			voodooSetInstanceName( "" );
			const void * instanceNameAsVoid;
			multiplexer.returnValue( "const char *", instanceNameAsVoid );
			const char * instanceName = (const char *) instanceNameAsVoid;
			voodooSetInstanceName( instanceName );
		} catch ( VoodooCommon::ErrorMessage & e ) {
			VoodooCommon::ErrorMessage error;
			error.append( "From " );
			error.append( __FUNCTION__ );
			error.append( " for custom class " );
			error.append( __voodooClassName );
			error.append( ": " );
			error.append( e.result() );
			VOODOO_FAIL_TEST( error.result() );
			throw "VOODOO_FAIL_TEST must throw";
		}
	}

	void voodooDestructor()
	{
		if ( __voodooInstanceName[ 0 ] != '\0' ) {
			try {
				__VoodooGrowingString growingString;
				growingString.append( "Destruction of " );
				growingString.append( __voodooInstanceName );
				VoodooCommon::Expect::Multiplexer multiplexer( growingString.result() );
				const void * unusedReturnValue = 0;
				multiplexer.returnValue( 0, unusedReturnValue );
			} catch ( VoodooCommon::ErrorMessage & e ) {
				VoodooCommon::ErrorMessage error;
				error.append( "From " );
				error.append( __FUNCTION__ );
				error.append( ": " );
				error.append( e.result() );
				VOODOO_FAIL_TEST( error.result() );
				throw "VOODOO_FAIL_TEST must throw";
			}
			voodooSetInstanceName( "" );
		}
	}

	void voodooCopyConstruct( const Klass & other )
	{
		__VoodooGrowingString growingString;
		growingString.append( "Copy of " );
		growingString.append( other.__voodooInstanceName );
		voodooSetInstanceName( growingString.result() );
	}

	template < typename... Params >
	void voodooVoidCall( const char * methodName, Params&... params ) const
	{
		try {
			__VoodooGrowingString growingString;
			growingString.append( "Call to " );
			growingString.append( __voodooInstanceName );
			growingString.append( "::" );
			growingString.append( methodName );
			VoodooCommon::Expect::Multiplexer multiplexer( growingString.result() );
			multiplexer.checkParameterPack( 0, params... );
			multiplexer.effectParameterPack( 0, params... );
			const void * returnValueAsVoid = 0;
			void * returnValueUnused = 0;
			multiplexer.returnValue( VoodooCommon::PointerTypeString( returnValueUnused ).typeString(), returnValueAsVoid );
		} catch ( VoodooCommon::ErrorMessage & e ) {
			VoodooCommon::ErrorMessage error;
			error.append( "From " );
			error.append( __FUNCTION__ );
			error.append( " for custom class " );
			error.append( __voodooClassName );
			error.append( " method " );
			error.append( methodName );
			error.append( ": " );
			error.append( e.result() );
			VOODOO_FAIL_TEST( error.result() );
			throw "VOODOO_FAIL_TEST must throw";
		}
	}

	template < typename ReturnValue, typename... Params >
	ReturnValue voodooCall( const char * methodName, Params&... params ) const
	{
		try {
			__VoodooGrowingString growingString;
			growingString.append( "Call to " );
			growingString.append( __voodooInstanceName );
			growingString.append( "::" );
			growingString.append( methodName );
			VoodooCommon::Expect::Multiplexer multiplexer( growingString.result() );
			multiplexer.checkParameterPack( 0, params... );
			multiplexer.effectParameterPack( 0, params... );
			const void * returnValueAsVoid = 0;
			ReturnValue * returnValueUnused = 0;
			multiplexer.returnValue( VoodooCommon::PointerTypeString( returnValueUnused ).typeString(), returnValueAsVoid );
			return * (ReturnValue *) returnValueAsVoid;
		} catch ( VoodooCommon::ErrorMessage & e ) {
			VoodooCommon::ErrorMessage error;
			error.append( "From " );
			error.append( __FUNCTION__ );
			error.append( " for custom class " );
			error.append( __voodooClassName );
			error.append( " method " );
			error.append( methodName );
			error.append( ": " );
			error.append( e.result() );
			VOODOO_FAIL_TEST( error.result() );
			throw "VOODOO_FAIL_TEST must throw";
		}
	}

	template < typename ReturnValue, typename... Params >
	ReturnValue voodooMoveCall( const char * methodName, Params&... params ) const
	{
		try {
			__VoodooGrowingString growingString;
			growingString.append( "Call to " );
			growingString.append( __voodooInstanceName );
			growingString.append( "::" );
			growingString.append( methodName );
			VoodooCommon::Expect::Multiplexer multiplexer( growingString.result() );
			multiplexer.checkParameterPack( 0, params... );
			multiplexer.effectParameterPack( 0, params... );
			const void * returnValueAsVoid = 0;
			ReturnValue * returnValueUnused = 0;
			multiplexer.returnValue( VoodooCommon::PointerTypeString( returnValueUnused ).typeString(), returnValueAsVoid );
			return std::move( * (ReturnValue *) returnValueAsVoid );
		} catch ( VoodooCommon::ErrorMessage & e ) {
			VoodooCommon::ErrorMessage error;
			error.append( "From " );
			error.append( __FUNCTION__ );
			error.append( " for custom class " );
			error.append( __voodooClassName );
			error.append( " method " );
			error.append( methodName );
			error.append( ": " );
			error.append( e.result() );
			VOODOO_FAIL_TEST( error.result() );
			throw "VOODOO_FAIL_TEST must throw";
		}
	}

private:
	char __voodooClassName[ VOODOO_EXPECT_MAX_INSTANCE_NAME + sizeof( '\0' ) ];
	char __voodooInstanceName[ VOODOO_EXPECT_MAX_INSTANCE_NAME + sizeof( '\0' ) ];
};

template < typename... Params >
void voodooVoidCall( const char * functionName, Params&... params )
{
	try {
		__VoodooGrowingString growingString;
		growingString.append( "Call to " );
		growingString.append( functionName );
		VoodooCommon::Expect::Multiplexer multiplexer( growingString.result() );
		multiplexer.checkParameterPack( 0, params... );
		multiplexer.effectParameterPack( 0, params... );
		const void * returnValueAsVoid = 0;
		void * returnValueUnused = 0;
		multiplexer.returnValue( VoodooCommon::PointerTypeString( returnValueUnused ).typeString(), returnValueAsVoid );
	} catch ( VoodooCommon::ErrorMessage & e ) {
		VoodooCommon::ErrorMessage error;
		error.append( "From " );
		error.append( __FUNCTION__ );
		error.append( " for custom function " );
		error.append( functionName );
		error.append( ": " );
		error.append( e.result() );
		VOODOO_FAIL_TEST( error.result() );
		throw "VOODOO_FAIL_TEST must throw";
	}
}

template < typename ReturnValue, typename... Params >
ReturnValue voodooCall( const char * functionName, Params&... params )
{
	try {
		__VoodooGrowingString growingString;
		growingString.append( "Call to " );
		growingString.append( functionName );
		VoodooCommon::Expect::Multiplexer multiplexer( growingString.result() );
		multiplexer.checkParameterPack( 0, params... );
		multiplexer.effectParameterPack( 0, params... );
		const void * returnValueAsVoid = 0;
		ReturnValue * returnValueUnused = 0;
		multiplexer.returnValue( VoodooCommon::PointerTypeString( returnValueUnused ).typeString(), returnValueAsVoid );
		return * (ReturnValue *) returnValueAsVoid;
	} catch ( VoodooCommon::ErrorMessage & e ) {
		VoodooCommon::ErrorMessage error;
		error.append( "From " );
		error.append( __FUNCTION__ );
		error.append( " for custom function " );
		error.append( functionName );
		error.append( ": " );
		error.append( e.result() );
		VOODOO_FAIL_TEST( error.result() );
		throw "VOODOO_FAIL_TEST must throw";
	}
}

template < typename ReturnValue, typename... Params >
ReturnValue voodooMoveCall( const char * functionName, Params&... params )
{
	try {
		__VoodooGrowingString growingString;
		growingString.append( "Call to " );
		growingString.append( functionName );
		VoodooCommon::Expect::Multiplexer multiplexer( growingString.result() );
		multiplexer.checkParameterPack( 0, params... );
		multiplexer.effectParameterPack( 0, params... );
		const void * returnValueAsVoid = 0;
		ReturnValue * returnValueUnused = 0;
		multiplexer.returnValue( VoodooCommon::PointerTypeString( returnValueUnused ).typeString(), returnValueAsVoid );
		return std::move( * (ReturnValue *) returnValueAsVoid );
	} catch ( VoodooCommon::ErrorMessage & e ) {
		VoodooCommon::ErrorMessage error;
		error.append( "From " );
		error.append( __FUNCTION__ );
		error.append( " for custom function " );
		error.append( functionName );
		error.append( ": " );
		error.append( e.result() );
		VOODOO_FAIL_TEST( error.result() );
		throw "VOODOO_FAIL_TEST must throw";
	}
}

} // namespace Custom
} // namespace Expect
} // namespace VoodooCommon

#endif // __VOODOO_EXPECT_CUSTOM_H__
