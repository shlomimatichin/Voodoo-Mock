#ifndef __VOODOO_PARAMETER_EXPECTATIONS_H__
#define __VOODOO_PARAMETER_EXPECTATIONS_H__

#include <VoodooCommon/Utils.h>
#include <type_traits>

#ifndef VOODOO_EXPECT_MAX_CLASS_NAME
#define VOODOO_EXPECT_MAX_CLASS_NAME 256
#endif // VOODOO_EXPECT_MAX_CLASS_NAME

namespace VoodooCommon {
namespace Expect {
namespace Parameter
{

class Interface
{
public:
	virtual ~Interface() {}
	virtual void compare( const char * typeString , const void * pointerToValue ) = 0;
	virtual void effectVoidPointer( const void * pointerToValue ) = 0;
};

template < typename T >
class StrongTyped : public Interface
{
public:
	StrongTyped( const char * expectationName ) :
		_expectationName( expectationName )
	{
	}

protected:
	virtual void compare( T & value ) = 0;
	virtual void effect( T & value ) {}
	const char * expectationName() const { return _expectationName; }

private:
	const char * _expectationName;

	void compare( const char * typeString , const void * pointerToValue ) override
	{
		if ( ! compareType( typeString ) ) {
			ErrorMessage error;
			error.append( "VoodooCommon::Expect::Parameter::" );
			error.append( _expectationName );
			error.append( " expects a parameter of type '" );
			error.append( TemplateTypeString<T>().typeString() );
			error.append( "', however '" );
			error.append( typeString );
			error.append( "' was found" );
			throw error;
		}
		compare( * (T *) pointerToValue );
	}

	bool compareType( const char * typeString )
	{
		return strcmp( TemplateTypeString<T>().typeString() , typeString ) == 0;
	}

	void effectVoidPointer( const void * pointerToValue ) override
	{
		effect( * (T *) pointerToValue );
	}
};

template < typename T >
class Ignore : public StrongTyped< T >
{
public:
	Ignore() : StrongTyped< T >( "Ignore" ) {}
	void compare( T & ) {}
};

template < typename T >
class Named : public StrongTyped< T >
{
public:
	Named( const char * expectedName ) :
		StrongTyped< T >( "Named" )
	{
		if ( strlen( expectedName ) > VOODOO_EXPECT_MAX_CLASS_NAME ) {
			ErrorMessage error;
			error.append( "The instance name '" );
			error.append( expectedName );
			error.append( "' is too long. Please define VOODOO_EXPECT_MAX_CLASS_NAME" );
			error.append( " to more than " );
			error.append( VOODOO_TO_STRING( VOODOO_EXPECT_MAX_CLASS_NAME ) );
			VOODOO_FAIL_TEST( error.result() );
		}
		strncpy( _expectedName , expectedName , VOODOO_EXPECT_MAX_CLASS_NAME );
		_expectedName[ VOODOO_EXPECT_MAX_CLASS_NAME ] = '\0';
	}

private:
	char _expectedName[ VOODOO_EXPECT_MAX_CLASS_NAME + sizeof( '\0' ) ];

	void compare( T & value )
	{
		if ( strcmp( value.voodooInstanceName() , _expectedName ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected instance '" );
			error.append( _expectedName );
			error.append( "' found '" );
			error.append( value.voodooInstanceName() );
			error.append( "'" );
			throw error;
		}	
	}
};

template < typename T >
class NamedOrCopyOf : public StrongTyped< T >
{
public:
	NamedOrCopyOf( const char * expectedName ) :
		StrongTyped< T >( "NamedOrCopyOf" )
	{
		if ( strlen( expectedName ) > VOODOO_EXPECT_MAX_CLASS_NAME ) {
			ErrorMessage error;
			error.append( "The instance name '" );
			error.append( expectedName );
			error.append( "' is too long. Please define VOODOO_EXPECT_MAX_CLASS_NAME" );
			error.append( " to more than " );
			error.append( VOODOO_TO_STRING( VOODOO_EXPECT_MAX_CLASS_NAME ) );
			VOODOO_FAIL_TEST( error.result() );
		}
		strncpy( _expectedName , expectedName , VOODOO_EXPECT_MAX_CLASS_NAME );
		_expectedName[ VOODOO_EXPECT_MAX_CLASS_NAME ] = '\0';
	}

private:
	char _expectedName[ VOODOO_EXPECT_MAX_CLASS_NAME + sizeof( '\0' ) ];

	void compare( T & value )
	{
		const char * voodooInstanceName = _removePossibleCopyOf( value.voodooInstanceName() );
		if ( strcmp( voodooInstanceName , _expectedName ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected instance, or copy of, '" );
			error.append( _expectedName );
			error.append( "' found '" );
			error.append( value.voodooInstanceName() );
			error.append( "'" );
			throw error;
		}	
	}
};

template < typename T >
class EqualsValue : public StrongTyped< T >
{
public:
	EqualsValue( T value ) :
		StrongTyped< T >( "EqualsValue" ),
		_value( value )
	{
	}

private:
	T _value;

	void compare( T & value )
	{
		if ( ! ( value == _value ) ) {
			ErrorMessage error;
			error.append( "Expected value '" );
			error.append( VOODOO_TO_STRING( _value ) );
			error.append( "' to be equal to found value '" );
			error.append( VOODOO_TO_STRING( value ) );
			error.append( "'" );
			throw error;
		}	
	}
};

template < typename T >
class PointerEqualsValue : public StrongTyped< T * >
{
public:
	PointerEqualsValue( T value ) :
		StrongTyped< T * >( "PointerEqualsValue" ),
		_value( value )
	{
	}

private:
	T _value;

	void compare( T * & value )
	{
		if ( value == 0 ) {
			ErrorMessage error;
			error.append( "Expected value '" );
			error.append( VOODOO_TO_STRING( _value ) );
			error.append( "' to be equal, but found NULL" );
			throw error;
		}
		if ( ! ( * value == _value ) ) {
			ErrorMessage error;
			error.append( "Expected value '" );
			error.append( VOODOO_TO_STRING( _value ) );
			error.append( "' to be equal to found value '" );
			error.append( VOODOO_TO_STRING( * value ) );
			error.append( "'" );
			throw error;
		}	
	}
};

template < typename T >
class PointerSameDataValue : public StrongTyped< T * >
{
public:
	PointerSameDataValue( T value ) :
		StrongTyped< T * >( "PointerEqualsValue" ),
		_value( value )
	{
	}

private:
	T _value;

	void compare( T * & value )
	{
		if ( value == 0 ) {
			ErrorMessage error;
			error.append( "Expected value '" );
			error.append( VOODOO_TO_STRING( _value ) );
			error.append( "' to be equal, but found NULL" );
			throw error;
		}
		if ( memcmp( value, & _value, sizeof( * value ) ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected value '" );
			error.append( VOODOO_TO_STRING( _value ) );
			error.append( "' to be equal to found value '" );
			error.append( VOODOO_TO_STRING( * value ) );
			error.append( "'" );
			throw error;
		}	
	}
};

template < typename T >
class EqualsReference : public StrongTyped< T >
{
public:
	EqualsReference( T & value ) :
		StrongTyped< T >( "EqualsReference" ),
		_value( value )
	{
	}

private:
	T & _value;

	void compare( T & value )
	{
		if ( ! ( value == _value ) ) {
			ErrorMessage error;
			error.append( "Expected value '" );
			error.append( VOODOO_TO_STRING( _value ) );
			error.append( "' to be equal to found value '" );
			error.append( VOODOO_TO_STRING( value ) );
			error.append( "'" );
			throw error;
		}	
	}
};

template < typename T >
class SameDataValue : public StrongTyped< T >
{
public:
	SameDataValue( T value ) :
		StrongTyped< T >( "SameDataValue" ),
		_value( value )
	{
	}

private:
	T _value;

	void compare( T & value )
	{
		if ( memcmp( & value , & _value , sizeof( value ) ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected value '" );
			error.append( DataDumpString( _value ).dataString() );
			error.append( "' to be memory wise identical to found value '" );
			error.append( DataDumpString( value ).dataString() );
			error.append( "'" );
			throw error;
		}	
	}
};

template < typename T >
class ReferenceTo : public StrongTyped< T >
{
public:
	ReferenceTo( T & to ) :
		StrongTyped< T >( "ReferenceTo" ),
		_to( to )
	{
	}

private:
	T & _to;

	void compare( T & value )
	{
		if ( & value != & _to ) {
			ErrorMessage error;
			error.append( "Expected Reference to " );
			T * pointer = & _to;
			error.append( VOODOO_TO_STRING( pointer ) );
			error.append( " found " );
			pointer = & value;
			error.append( VOODOO_TO_STRING( pointer ) );
			error.append( " (of type '" );
			error.append( TemplateTypeString<T>().typeString() );
			error.append( "')" );
			throw error;
		}	
	}
};

template < typename T >
class PredicateBase : public StrongTyped< T >
{
public:
	PredicateBase( const char * expectationName = "PredicateBase derevative" ) :
		StrongTyped< T >( expectationName )
	{
	}

	virtual bool operator () ( T & ) = 0;

	void compare( T & value )
	{
		if ( ! ( ( * this )( value ) ) ) {
			ErrorMessage error;
			error.append( "Expected predicate on type'" );
			error.append( TemplateTypeString<T>().typeString() );
			error.append( "' to return true on found value '" );
			error.append( VOODOO_TO_STRING( value ) );
			error.append( "'" );
			throw error;
		}	
	}
};

template < typename T , class P >
class PredicateValue : public PredicateBase< T >
{
public:
	PredicateValue( const P & predicate ) :
		PredicateBase< T >( "PredicateValue" ),
		_predicate( predicate )
	{
	}

	bool operator () ( T & value )
	{
		return _predicate( value );
	}

private:
	P _predicate;
};

template < typename T , class P >
class PredicateSimple : public PredicateBase< T >
{
public:
	PredicateSimple() :
		PredicateBase< T >( "PredicateValue" )
	{
	}

	bool operator () ( T & value )
	{
		return P()( value );
	}
};

template < typename T , class P >
class PredicateReference : public PredicateBase< T >
{
public:
	PredicateReference( P & predicate ) :
		PredicateBase< T >( "PredicateReference" ),
		_predicate( predicate )
	{
	}

	bool operator () ( T & value )
	{
		return _predicate( value );
	}

private:
	P & _predicate;
};

template < typename T , class P >
class PredicateAuto : public PredicateBase< T >
{
public:
	PredicateAuto( P * predicate ) :
		PredicateBase< T >( "PredicateAuto" ),
		_predicate( predicate )
	{
	}

	~PredicateAuto()
	{
		delete _predicate;
	}

	bool operator () ( T & value )
	{
		return ( * _predicate )( value );
	}

private:
	P * _predicate;
};

template < typename T >
class SaveValue : public StrongTyped< T >
{
public:
	SaveValue( T * & value ):
		StrongTyped< T >( "SaveValue" ),
		_value( value )
	{
		_value = 0;
	}

private:
	T * & _value;

	void compare( T & value ) {}

	void effect( T & value )
	{
		_value = new T( value );
	}
};

template < typename T >
class SaveRValue : public StrongTyped< T >
{
public:
	SaveRValue( T value ):
		StrongTyped< T >( "SaveRValue" ),
		_value( std::move( value ) )
	{
	}

	void compare( T & value ) {}

	void effect( T value )
	{
		_value = std::move( value );
	}

private:
	T _value;
};

template < typename T >
class SaveSimpleValue : public StrongTyped< T >
{
public:
	SaveSimpleValue( typename std::remove_const< T >::type & value ):
		StrongTyped< T >( "SaveSimpleValue" ),
		_value( value )
	{
	}

	void compare( T & value ) {}

	void effect( T & value )
	{
		_value = value;
	}

private:
	typename std::remove_const< T >::type & _value;
};

template < typename T >
class SaveReference : public StrongTyped< T >
{
public:
	SaveReference( T * & reference ):
		StrongTyped< T >( "SaveReference" ),
		_reference( reference )
	{
	}

private:
	T * & _reference;

	void compare( T & value )
	{
		_reference = & value;
	}
};

template < typename T >
class AssignValue : public StrongTyped< T >
{
public:
	AssignValue( T value ):
		StrongTyped< T >( "AssignValue" ),
		_value( value )
	{
	}

private:
	T _value;

	void compare( T & ) {}
	void effect( T & value )
	{
		value = _value;
	}
};

template < typename T >
class AssignValueToPointer : public StrongTyped< T * >
{
public:
	AssignValueToPointer( T value ):
		StrongTyped< T * >( "AssignValueToPointer" ),
		_value( value )
	{
	}

private:
	T _value;

	void compare( T * & value ) {}
	void effect( T * & value )
	{
		* value = _value;
	}
};

template < typename T >
class AssignReferenceToPointer : public StrongTyped< T * >
{
public:
	AssignReferenceToPointer( T & value ):
		StrongTyped< T * >( "AssignReferenceToPointer" ),
		_value( value )
	{
	}

private:
	T & _value;

	void compare( T * & value ) {}
	void effect( T * & value )
	{
		* value = _value;
	}
};

class StringEquals: public StrongTyped< const char * >
{
public:
	StringEquals( const char * value ) :
		StrongTyped< const char * >( "StringEquals" ),
		_value( value )
	{
	}

private:
	const char * _value;

	void compare( const char * & value )
	{
		if ( value == 0 && _value == 0 )
			return;
		if ( value == 0 ) {
			ErrorMessage error;
			error.append( "Expected string '" );
			error.append( _value );
			error.append( "' but found NULL" );
			throw error;
		}
		if ( strcmp( value, _value ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected string '" );
			error.append( _value );
			error.append( "' to be equal to found string '" );
			error.append( value );
			error.append( "'" );
			throw error;
		}	
	}
};

class MutableStringEquals: public StrongTyped< char * >
{
public:
	MutableStringEquals( const char * value ) :
		StrongTyped< char * >( "MutableStringEquals" ),
		_value( value )
	{
	}

private:
	const char * _value;

	void compare( char * & value )
	{
		if ( value == 0 && _value == 0 )
			return;
		if ( value == 0 ) {
			ErrorMessage error;
			error.append( "Expected string '" );
			error.append( _value );
			error.append( "' but found NULL" );
			throw error;
		}
		if ( strcmp( value, _value ) != 0 ) {
			ErrorMessage error;
			error.append( "Expected string '" );
			error.append( _value );
			error.append( "' to be equal to found string '" );
			error.append( value );
			error.append( "'" );
			throw error;
		}	
	}
};

template < typename T >
class LessThanValue : public StrongTyped< T >
{
public:
	LessThanValue( T value ) :
		StrongTyped< T >( "LessThanValue" ),
		_value( value )
	{
	}

private:
	T _value;

	void compare( T & value )
	{
		if ( ! ( value >= _value ) ) {
			ErrorMessage error;
			error.append( "Expected value '" );
			error.append( VOODOO_TO_STRING( _value ) );
			error.append( "' to be greater than found value '" );
			error.append( VOODOO_TO_STRING( value ) );
			error.append( "'" );
			throw error;
		}	
	}
};

template < typename T >
class SameDataPointer : public StrongTyped< T >
{
public:
	SameDataPointer( T value, size_t size ) :
		StrongTyped< T >( "SameDataPointer" ),
		_value( value ),
		_size( size )
	{
	}

private:
	T _value;
	size_t _size;

	void compare( T & value )
	{
		if ( value == 0 ) {
			VoodooCommon::ErrorMessage error;
			error.append( "Expected value '" );
			error.append( VOODOO_TO_STRING( _value ) );
			error.append( "', but found NULL" );
			throw error;
		}
		if ( memcmp( value, _value, _size ) != 0 ) {
			VoodooCommon::ErrorMessage error;
			error.append( "Expected value '" );
			error.append( DataDumpString( _value, _size ).dataString() );
			error.append( "' to be memory wise identical to found value '" );
			error.append( DataDumpString( value, _size ).dataString() );
			error.append( "'" );
			throw error;
		}	
	}
};

template < typename T >
class MemcpyDataPointer : public StrongTyped< T >
{
public:
	MemcpyDataPointer( T value, size_t size ) :
		StrongTyped< T >( "MemcpyDataPointer" ),
		_value( value ),
		_size( size )
	{
	}

private:
	T _value;
	size_t _size;

	void compare( T & value )
	{
		memcpy( value, _value, _size );
	}
};

} // namespace Parameter
} // namespace Expect
} // namespace VoodooCommon

#endif // __VOODOO_PARAMETER_EXPECTATIONS_H__
