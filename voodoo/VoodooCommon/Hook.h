#ifndef __VOODOO_EXPECTATION_HOOK_H__
#define __VOODOO_EXPECTATION_HOOK_H__

#include <functional>
#include <VoodooCommon/ExpectLineMessage.h>
#include <VoodooCommon/HookMacros.h>

namespace VoodooCommon {
namespace Expect {
namespace Hook
{

template < class T >
class Simple : public PostIntercepter
{
private:
	void returnValue( const char * typeString , const void * & value )
	{
		PostIntercepter::returnValue( typeString, value );
		T()();
	}
};

template < class T >
class Value : public PostIntercepter
{
public:
	Value( const T & hook ) :
		_hook( hook )
	{
	}

private:
	T _hook;

	void returnValue( const char * typeString , const void * & value )
	{
		PostIntercepter::returnValue( typeString, value );
		_hook();
	}
};

template < class T >
class Reference : public PostIntercepter
{
public:
	Reference( T & hook ) :
		_hook( hook )
	{
	}

private:
	T & _hook;

	void returnValue( const char * typeString , const void * & value )
	{
		PostIntercepter::returnValue( typeString, value );
		_hook();
	}
};

template < bool ToState >
class SwitchBoolImpl
{
public:
	SwitchBoolImpl( bool & value ) :
		_value( value )
	{
	}

	void operator () ()
	{
		_value = ToState;
	}

private:
	bool & _value;
};

template < bool ToState >
class SwitchBool : public Hook::Value< SwitchBoolImpl< ToState > >
{
public:
	SwitchBool( bool & value ) :
		Hook::Value< SwitchBoolImpl< ToState > >( SwitchBoolImpl< ToState >( value ) )
	{
	}
};

template < bool ToState >
class SwitchLockImpl
{
public:
	SwitchLockImpl( bool & value ) :
		_value( value )
	{
	}

	void operator () ()
	{
		if ( ToState && _value )
			VOODOO_FAIL_TEST( "Expected Lock State to be false, but instead it was true" );
		if ( ! ToState && ! _value )
			VOODOO_FAIL_TEST( "Expected Lock State to be true, but instead it was false" );
		_value = ToState;
	}

private:
	bool & _value;
};

template < bool ToState >
class SwitchLock : public Hook::Value< SwitchLockImpl< ToState > >
{
public:
	SwitchLock( bool & value ) :
		Hook::Value< SwitchLockImpl< ToState > >( SwitchLockImpl< ToState >( value ) )
	{
	}
};

template < typename T >
class IncrementHookImpl
{
public:
	IncrementHookImpl( T & value ) :
		_value( value )
	{
	}

	void operator () ()
	{
		++ _value;
	}

private:
	T & _value;
};

template < typename T >
class IncrementHook : public Hook::Value< IncrementHookImpl< T > >
{
public:
	IncrementHook( T & value ) :
		Hook::Value< IncrementHookImpl< T > >( IncrementHookImpl< T >( value ) )
	{
	}
};

class LambdaImpl
{
public:
	LambdaImpl( std::function< void () > callback ) :
                _callback( callback )
	{
	}

	void operator () ()
	{
                _callback();
	}

private:
        std::function< void () > _callback;
};

class Lambda : public Hook::Value< LambdaImpl >
{
public:
	Lambda( std::function< void () > callback ):
		Hook::Value< LambdaImpl >( LambdaImpl( callback ) )
	{
	}
};

} // namespace Hook
} // namespace Expect
} // namespace VoodooCommon

#endif // __VOODOO_EXPECTATION_HOOK_H__
