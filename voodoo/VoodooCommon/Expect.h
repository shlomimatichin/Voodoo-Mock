#ifndef __VOODOO_EXPECTATION_H__
#define __VOODOO_EXPECTATION_H__

#include <VoodooCommon/ExpectParameter.h>

#ifndef VOODOO_EXPECT_MAX_PARAMETERS
#define VOODOO_EXPECT_MAX_PARAMETERS 16
#endif // VOODOO_EXPECT_MAX_PARAMETERS

#define VOODOO_EXPECT_MAX_INSTANCE_NAME 256
#define VOODOO_EXPECT_MAX_CALL_DESCRIPTION 512

namespace VoodooCommon {
namespace Expect
{

class Interface
{
public:
	virtual ~Interface() {}

	virtual void check( const char * whatHappened ) = 0;
	virtual void check(	unsigned			parameterIndex ,
						const char *		typeString ,
						const void *		pointerToValue ) = 0;
	virtual void effect(    unsigned        parameterIndex,
                            const char *    typeString,
                            const void *    pointerToValue ) = 0;
	virtual void returnValue( const char * typeString , const void * & value ) = 0;
	virtual void operator << ( Parameter::Interface * parameter ) = 0;
};

static inline const char * _removePossibleCopyOf( const char * voodooInstanceName )
{
	enum { COPY_OF_LENGTH = sizeof( "Copy of " ) - sizeof( '\0' ) };
	while ( strlen( voodooInstanceName ) > COPY_OF_LENGTH &&
			memcmp( voodooInstanceName, "Copy of ", COPY_OF_LENGTH ) == 0 )
		voodooInstanceName += COPY_OF_LENGTH;
	return voodooInstanceName;
}

class Intercepter : public Interface
{
public:
	Intercepter() :
		_intercepted( 0 )
	{
	}

	~Intercepter()
	{
		if ( _intercepted != 0 )
			delete _intercepted;
	}

	Intercepter * operator << ( Interface * intercepted )
	{
		VOODOO_ASSERT( intercepted != 0 );
		VOODOO_ASSERT( _intercepted == 0 );
		_intercepted = intercepted;
		return this;
	}

protected:
	void returnValue( const char * typeString , const void * & value )
	{
		VOODOO_ASSERT( _intercepted != 0 );
		_intercepted->returnValue( typeString, value );
	}

	void check( const char * whatHappened )
	{
		VOODOO_ASSERT( _intercepted != 0 );
		_intercepted->check( whatHappened );
	}

	void check(	unsigned			parameterIndex ,
				const char *		typeString ,
				const void *		pointerToValue )
	{
		VOODOO_ASSERT( _intercepted != 0 );
		_intercepted->check( parameterIndex, typeString, pointerToValue );
	}

	void effect(    unsigned        parameterIndex,
                    const char *    typeString,
                    const void *    pointerToValue )
	{
		VOODOO_ASSERT( _intercepted != 0 );
		_intercepted->effect( parameterIndex, typeString, pointerToValue );
	}

	void operator << ( Parameter::Interface * parameter )
	{
		VOODOO_ASSERT( _intercepted != 0 );
		* _intercepted << parameter;
	}

private:
	Interface * _intercepted;
};

class PreIntercepter : public Intercepter { };
class PostIntercepter : public Intercepter { };

class WithoutParameters : public Interface
{
private:
	void check(	unsigned			parameterIndex ,
				const char *		typeString ,
				const void *		pointerToValue )
	{
		if ( parameterIndex > 0 || strcmp( typeString , "VOODOO_NO_MORE_PARAMETERS" ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected a call without Parameters, first parameter found " );
			error.append( typeString );
			throw error;
		}
	}

	void effect(    unsigned        parameterIndex,
                    const char *    typeString,
                    const void *    pointerToValue )
    {
        VOODOO_ASSERT(!"Should not have reached here");
    }
};

class WithParameters : public Interface
{
protected:
	WithParameters() : _parametersCount( 0 ) {}

	~WithParameters()
	{
		for ( unsigned i = 0 ; i < _parametersCount ; ++ i )
			delete _parameters[ i ];
	}

private:
	void operator << ( Parameter::Interface * parameter )
	{
		if ( _parametersCount >= VOODOO_EXPECT_MAX_PARAMETERS )	{
			VOODOO_FAIL_TEST( "You have a function with more than "
							__VOODOO_QUOTE( VOODOO_EXPECT_MAX_PARAMETERS )
							" parameters. Please #define VOODOO_EXPECT_MAX_PARAMETERS "
							" to your maximum number of parameters" );
		}
		_parameters[ _parametersCount ] = parameter;
		++ _parametersCount;
	}

	void check(	unsigned		parameterIndex ,
				const char *	typeString ,
				const void *	pointerToValue )
	{
		if ( parameterIndex == _parametersCount && strcmp( typeString , "VOODOO_NO_MORE_PARAMETERS" ) == 0 ) {
			return;
		}
		if ( parameterIndex >= _parametersCount ) {
			ErrorMessage error;
			error.append( "Expected " );
			error.append( VOODOO_TO_STRING( _parametersCount ) );
			error.append( " parameters, but call has more" );
			throw error;
		}
		try {
			_parameters[ parameterIndex ]->compare( typeString , pointerToValue );
		} catch( ErrorMessage & e ) {
			ErrorMessage error;
			error.append( "\nIn parameter " );
			error.append( VOODOO_TO_STRING( parameterIndex ) );
			error.append( ": " );
			error.append( e.result() );
			throw error;
		}
	}

	void effect(    unsigned        parameterIndex,
                    const char *    typeString,
                    const void *    pointerToValue )
	{
		if ( parameterIndex >= _parametersCount || strcmp( typeString , "VOODOO_NO_MORE_PARAMETERS" ) == 0 ) {
			VOODOO_ASSERT( ! "Should never happen" );
			return;
		}
		_parameters[ parameterIndex ]->effectVoidPointer( pointerToValue );
	}

private:
	Parameter::Interface *		_parameters[ VOODOO_EXPECT_MAX_PARAMETERS ];
	unsigned 					_parametersCount;
};

template < class T >
class Construction : public WithParameters
{
public:
	Construction( const char * instanceName )
	{
		if ( strlen( instanceName ) > VOODOO_EXPECT_MAX_CLASS_NAME ) {
			ErrorMessage error;
			error.append( "The instance name '" );
			error.append( instanceName );
			error.append( "' is too long. Please define VOODOO_EXPECT_MAX_CLASS_NAME" );
			error.append( " to more than " );
			error.append( VOODOO_TO_STRING( VOODOO_EXPECT_MAX_CLASS_NAME ) );
			VOODOO_FAIL_TEST( error.result() );
		}
		strncpy( _instanceName , instanceName , VOODOO_EXPECT_MAX_CLASS_NAME );
		_instanceName[ VOODOO_EXPECT_MAX_CLASS_NAME ] = '\0';
	}

private:
	void check( const char * whatHappened )
	{
		if ( strstr( whatHappened , "Construction of " ) != whatHappened || 
				strcmp( whatHappened + sizeof( "Construction of " ) - sizeof( '\0' ) ,
						TemplateTypeString<T>().typeString() ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected Construction of " );
			error.append( TemplateTypeString<T>().typeString() );
			error.append( ", but found " );
			error.append( whatHappened );
			throw error;
		}
	}

	void returnValue( const char * typeString , const void * & value )
	{
		VOODOO_ASSERT( strcmp( typeString , "const char *" ) == 0 );
		value = _instanceName;
	}

	char _instanceName[ VOODOO_EXPECT_MAX_CLASS_NAME + sizeof( '\0' ) ];
};

template < typename T, typename E >
class ConstructionThrowValue : public Construction< T >
{
public:
	ConstructionThrowValue( const E & exception ) :
		Construction< T >( "ConstructionThrowValue" ),
		_exception( exception )
	{
	}

	void returnValue( const char * typeString , const void * & value )
	{
		throw _exception;
	}

private:
	E _exception;
};

class Destruction : public Interface
{
public:
	Destruction( const char * instanceName )
	{
		if ( strlen( instanceName ) > VOODOO_EXPECT_MAX_CLASS_NAME ) {
			ErrorMessage error;
			error.append( "The instance name '" );
			error.append( instanceName );
			error.append( "' is too long. Please define VOODOO_EXPECT_MAX_CLASS_NAME" );
			error.append( " to more than " );
			error.append( VOODOO_TO_STRING( VOODOO_EXPECT_MAX_CLASS_NAME ) );
			VOODOO_FAIL_TEST( error.result() );
		}
		strncpy( _instanceName , instanceName , VOODOO_EXPECT_MAX_CLASS_NAME );
		_instanceName[ VOODOO_EXPECT_MAX_CLASS_NAME ] = '\0';
	}

private:
	void check(	unsigned			parameterIndex ,
				const char *		typeString ,
				const void *		pointerToValue )
	{
		VOODOO_FAIL_TEST( "Destruction Expectation does not support parameters" );
	}

	void effect(    unsigned        parameterIndex,
                    const char *    typeString,
                    const void *    pointerToValue )
	{
        VOODOO_ASSERT( ! "Should not have reached here" );
	}

	void check( const char * whatHappened )
	{
		if ( strstr( whatHappened , "Destruction of " ) != whatHappened || 
				strcmp( whatHappened + sizeof( "Destruction of " ) - sizeof( '\0' ) ,
						_instanceName ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected Destruction of " );
			error.append( _instanceName );
			error.append( ", but found " );
			error.append( whatHappened );
			throw error;
		}
	}

	void returnValue( const char * typeString , const void * & value )
	{
		VOODOO_ASSERT( typeString == 0 );
		VOODOO_ASSERT( value == 0 );
	}

	void operator << ( Parameter::Interface * parameter )
	{
		VOODOO_FAIL_TEST( "You attempted to add a parameter to a destruction expectation" );
	}

	char _instanceName[ VOODOO_EXPECT_MAX_CLASS_NAME + sizeof( '\0' ) ];
};

class Call : public WithParameters
{
protected:
	Call( const char * whatWasCalled )
	{
		if ( strlen( whatWasCalled ) > VOODOO_EXPECT_MAX_CALL_DESCRIPTION ) {
			ErrorMessage error;
			error.append( "The call description '" );
			error.append( whatWasCalled );
			error.append( "' is too long. Please define VOODOO_EXPECT_MAX_CALL_DESCRIPTION" );
			error.append( " to more than " );
			error.append( VOODOO_TO_STRING( VOODOO_EXPECT_MAX_CALL_DESCRIPTION ) );
			VOODOO_FAIL_TEST( error.result() );
		}
		strncpy( _whatWasCalled, whatWasCalled, VOODOO_EXPECT_MAX_CALL_DESCRIPTION );
		_whatWasCalled[ VOODOO_EXPECT_MAX_CALL_DESCRIPTION ] = '\0';
	}

private:
	void check( const char * whatHappened )
	{
		if ( strstr( whatHappened , "Call to " ) != whatHappened || 
				strcmp( whatHappened + sizeof( "Call to " ) - sizeof( '\0' ) ,
						_whatWasCalled ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected Call to " );
			error.append( _whatWasCalled );
			error.append( ", but found " );
			error.append( whatHappened );
			throw error;
		}
	}

	char _whatWasCalled[ VOODOO_EXPECT_MAX_CALL_DESCRIPTION + sizeof( '\0' ) ];
};

class CallOrCopyOf : public WithParameters
{
protected:
	CallOrCopyOf( const char * whatWasCalled )
	{
		if ( strlen( whatWasCalled ) > VOODOO_EXPECT_MAX_CALL_DESCRIPTION ) {
			ErrorMessage error;
			error.append( "The call description '" );
			error.append( whatWasCalled );
			error.append( "' is too long. Please define VOODOO_EXPECT_MAX_CALL_DESCRIPTION" );
			error.append( " to more than " );
			error.append( VOODOO_TO_STRING( VOODOO_EXPECT_MAX_CALL_DESCRIPTION ) );
			VOODOO_FAIL_TEST( error.result() );
		}
		strncpy( _whatWasCalled, whatWasCalled, VOODOO_EXPECT_MAX_CALL_DESCRIPTION );
		_whatWasCalled[ VOODOO_EXPECT_MAX_CALL_DESCRIPTION ] = '\0';
	}

private:
	void check( const char * whatHappened )
	{
		if ( strstr( whatHappened , "Call to " ) != whatHappened || 
				strcmp( _removePossibleCopyOf(
								whatHappened + sizeof( "Call to " ) - sizeof( '\0' ) ),
						_whatWasCalled ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected Call to " );
			error.append( _whatWasCalled );
			error.append( " (or Copy of), but found " );
			error.append( whatHappened );
			throw error;
		}
	}

	char _whatWasCalled[ VOODOO_EXPECT_MAX_CALL_DESCRIPTION + sizeof( '\0' ) ];
};

template < class Call >
class _CallReturnVoid : public Call
{
public:
	_CallReturnVoid( const char * whatWasCalled ) : Call( whatWasCalled ) {}

private:
	void returnValue( const char * typeString , const void * & value )
	{
		if ( strcmp( typeString , "void" ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected call to return void, but found " );
			error.append( typeString );
			throw error;
		}
	}
};

typedef _CallReturnVoid< Call > CallReturnVoid;
typedef _CallReturnVoid< CallOrCopyOf > CallOrCopyOfReturnVoid;

template < class Call, typename E >
class _CallThrowValue : public Call
{
public:
	_CallThrowValue( const char * whatWasCalled, const E & exception ) :
		Call( whatWasCalled ),
		_exception( exception )
	{
	}

private:
	E _exception;

	void returnValue( const char * typeString, const void * & value )
	{
		throw _exception;
	}
};

template < typename T >
class CallThrowValue : public _CallThrowValue< Call, T >
{
public:
	CallThrowValue( const char * whatWasCalled , T value ) :
		_CallThrowValue< Call, T >( whatWasCalled, value ) {}
};

template < typename T >
class CallOrCopyOfThrowValue : public _CallThrowValue< CallOrCopyOf, T >
{
public:
	CallOrCopyOfThrowValue( const char * whatWasCalled , T value ) :
		_CallThrowValue< CallOrCopyOf, T >( whatWasCalled, value ) {}
};

template < typename T >
class CallReturnRValue : public Call
{
public:
	CallReturnRValue( const char * whatWasCalled , T value ) :
		Call( whatWasCalled ) ,
		_value( std::move( value ) )
	{
	}

private:
	void returnValue( const char * typeString , const void * & value )
	{
		if ( strcmp( typeString , TemplateTypeString< T >().typeString() ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected call to return " );
			error.append( TemplateTypeString< T >().typeString() );
			error.append( " but found " );
			error.append( typeString );
			throw error;
		}
		value = std::move( & _value );
	}

	T _value;
};

template < typename Call, typename T >
class _CallReturnValue : public Call
{
public:
	_CallReturnValue( const char * whatWasCalled , T value ) :
		Call( whatWasCalled ) ,
		_value( value )
	{
	}

private:
	void returnValue( const char * typeString , const void * & value )
	{
		if ( strcmp( typeString , TemplateTypeString< T >().typeString() ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected call to return " );
			error.append( TemplateTypeString< T >().typeString() );
			error.append( " but found " );
			error.append( typeString );
			throw error;
		}
		value = & _value;
	}

	T _value;
};

template < typename T >
class CallReturnValue : public _CallReturnValue< Call, T >
{
public:
	CallReturnValue( const char * whatWasCalled , T value ) :
		_CallReturnValue< Call, T >( whatWasCalled, value ) {}
};

template < typename T >
class CallOrCopyOfReturnValue : public _CallReturnValue< CallOrCopyOf, T >
{
public:
	CallOrCopyOfReturnValue( const char * whatWasCalled , T value ) :
		_CallReturnValue< CallOrCopyOf, T >( whatWasCalled, value ) {}
};

template < class Call, typename T >
class _CallReturnReference : public Call
{
public:
	_CallReturnReference( const char * whatWasCalled , T & value ) :
		Call( whatWasCalled ) ,
		_value( value )
	{
	}

private:
	void returnValue( const char * typeString , const void * & value )
	{
		if ( strcmp( typeString , TemplateTypeString< T >().typeString() ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected call to return " );
			error.append( TemplateTypeString< T >().typeString() );
			error.append( " but found " );
			error.append( typeString );
			throw error;
		}
		value = & _value;
	}

	T & _value;
};

template < typename T >
class CallReturnReference : public _CallReturnReference< Call, T >
{
public:
	CallReturnReference( const char * whatWasCalled , T & value ) :
		_CallReturnReference< Call, T >( whatWasCalled, value ) {}
};

template < typename T >
class CallOrCopyOfReturnReference : public _CallReturnReference< CallOrCopyOf, T >
{
public:
	CallOrCopyOfReturnReference( const char * whatWasCalled , T & value ) :
		_CallReturnReference< CallOrCopyOf, T >( whatWasCalled, value ) {}
};

template < typename Call, typename T >
class _CallReturnAuto : public Call
{
public:
	_CallReturnAuto( const char * whatWasCalled , T * value ) :
		Call( whatWasCalled ) ,
		_value( value )
	{
	}

	~_CallReturnAuto()
	{
		delete _value;
	}

private:
	void returnValue( const char * typeString , const void * & value )
	{
		if ( strcmp( typeString , TemplateTypeString< T >().typeString() ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected call to return " );
			error.append( TemplateTypeString< T >().typeString() );
			error.append( " but found " );
			error.append( typeString );
			throw error;
		}
		value = _value;
	}

	T * _value;
};

template < typename T >
class CallReturnAuto : public _CallReturnAuto< Call, T >
{
public:
	CallReturnAuto( const char * whatWasCalled, T * value ) :
		_CallReturnAuto< Call, T >( whatWasCalled, value ) {}
};

template < typename T >
class CallOrCopyOfReturnAuto : public _CallReturnAuto< CallOrCopyOf, T >
{
public:
	CallOrCopyOfReturnAuto( const char * whatWasCalled, T * value ) :
		_CallReturnAuto< CallOrCopyOf, T >( whatWasCalled, value ) {}
};

template < typename Call, typename T >
class _CallReturnPointerAuto : public Call
{
public:
	_CallReturnPointerAuto( const char * whatWasCalled , T * value ) :
		Call( whatWasCalled ) ,
		_value( value )
	{
	}

	~_CallReturnPointerAuto()
	{
		delete _value;
	}

private:
	void returnValue( const char * typeString , const void * & value )
	{
		if ( strcmp( typeString , TemplateTypeString< T * >().typeString() ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected call to return " );
			error.append( TemplateTypeString< T * >().typeString() );
			error.append( " but found " );
			error.append( typeString );
			throw error;
		}
		value = & _value;
	}

	T * _value;
};

template < typename T >
class CallReturnPointerAuto : public _CallReturnPointerAuto< Call, T >
{
public:
	CallReturnPointerAuto( const char * whatWasCalled, T * value ) :
		_CallReturnPointerAuto< Call, T >( whatWasCalled, value ) {}
};

template < typename T >
class CallOrCopyOfReturnPointerAuto : public _CallReturnPointerAuto< CallOrCopyOf, T >
{
public:
	CallOrCopyOfReturnPointerAuto( const char * whatWasCalled, T * value ) :
		_CallReturnPointerAuto< CallOrCopyOf, T >( whatWasCalled, value ) {}
};

template < typename Call, typename T, class Callback >
class _CallReturnCallbackReference : public Call
{
public:
	_CallReturnCallbackReference( const char * whatWasCalled , Callback & callback ) :
		Call( whatWasCalled ) ,
		_callback( callback )
	{
	}

private:
	void returnValue( const char * typeString , const void * & value )
	{
		if ( strcmp( typeString , TemplateTypeString< T >().typeString() ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected call to return " );
			error.append( TemplateTypeString< T >().typeString() );
			error.append( " but found " );
			error.append( typeString );
			throw error;
		}
		T * returnedValue = _callback();
		value = returnedValue;
	}

	Callback & _callback;
};

template < typename T, class Callback >
class CallReturnCallbackReference : public _CallReturnCallbackReference< Call, T, Callback >
{
public:
	CallReturnCallbackReference( const char * whatWasCalled, Callback & callback ) :
		_CallReturnCallbackReference< Call, T, Callback >( whatWasCalled, callback ) {}
};

template < typename T, class Callback >
class CallOrCopyOfReturnCallbackReference : public _CallReturnCallbackReference< CallOrCopyOf, T, Callback >
{
public:
	CallOrCopyOfReturnCallbackReference( const char * whatWasCalled, Callback & callback ) :
		_CallReturnCallbackReference< CallOrCopyOf, T, Callback >( whatWasCalled, callback ) {}
};

template < typename Call, typename T, class Callback >
class _CallReturnCallbackValue : public Call
{
public:
	_CallReturnCallbackValue( const char * whatWasCalled , Callback & callback ) :
		Call( whatWasCalled ) ,
		_callback( callback )
	{
	}

private:
	void returnValue( const char * typeString , const void * & value )
	{
		if ( strcmp( typeString , TemplateTypeString< T >().typeString() ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected call to return " );
			error.append( TemplateTypeString< T >().typeString() );
			error.append( " but found " );
			error.append( typeString );
			throw error;
		}
		T * returnedValue = _callback();
		value = returnedValue;
	}

	Callback _callback;
};

template < typename T, class Callback >
class CallReturnCallbackValue : public _CallReturnCallbackValue< Call, T, Callback >
{
public:
	CallReturnCallbackValue( const char * whatWasCalled, Callback & callback ) :
		_CallReturnCallbackValue< Call, T, Callback >( whatWasCalled, callback ) {}
};

template < typename T, class Callback >
class CallOrCopyOfReturnCallbackValue : public _CallReturnCallbackValue< CallOrCopyOf, T, Callback >
{
public:
	CallOrCopyOfReturnCallbackValue( const char * whatWasCalled, Callback & callback ) :
		_CallReturnCallbackValue< CallOrCopyOf, T, Callback >( whatWasCalled, callback ) {}
};

} // namespace Expect
} // namespace VoodooCommon

#endif // __VOODOO_EXPECTATION_H__
