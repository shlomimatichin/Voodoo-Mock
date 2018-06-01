#ifndef __VOODOO_UTILS_H__
#define __VOODOO_UTILS_H__

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <VoodooCommon/Common.h>
#ifdef VOODOO_HAS_BOOST
#include <boost/smart_ptr.hpp>
#endif
#include <memory>
#include <type_traits>

#ifndef VOODOO_MAX_TEMPLATE_TYPE
#define VOODOO_MAX_TEMPLATE_TYPE 256
#endif // VOODOO_MAX_TEMPLATE_TYPE

#ifndef VOODOO_MAX_DATA_DUMP
#define VOODOO_MAX_DATA_DUMP 1024
#endif // VOODOO_MAX_DATA_DUMP

#define _VOODOO_TEMPLATE_INSTANCE_OF_THIS_FUNCTION( identifier ) \
	( ( strstr( __FUNCTION__ , identifier "<" ) != 0 ) ? \
	  		( strstr( __FUNCTION__, identifier "<" ) ) : \
			( identifier ) )

#define VOODOO_ASSERT( x ) if ( ! ( x ) ) { VOODOO_FAIL_TEST( "Internal Voodoo Error: should not be reached" ); }
#define VOODOO_ASSERT_NO_THROW( x ) if ( ! ( x ) ) { VOODOO_FAIL_TEST_NO_THROW( "Internal Voodoo Error: should not be reached" ); }

namespace VoodooCommon
{

typedef __VoodooGrowingString ErrorMessage;

template< typename T >
class TemplateTypeString
{
public:
	TemplateTypeString()
	{
#ifdef __GNUC__
		const char * functionName = __PRETTY_FUNCTION__;
		const char * begin = strstr( functionName , "[with T = " );
		if ( begin == NULL ) {
			fprintf( stderr, "TemplateTypeString failed!\n" );
			abort();
		}
		const char * end = begin;
		while ( * end != '\0' ) ++ end;
		-- end;
		VOODOO_ASSERT( * end == ']' );
		begin += sizeof( "[with T = " ) - sizeof( '\0' );
#else // __GNUC__
		const char * functionName = __FUNCTION__;
		const char * begin = strstr( functionName , "TemplateTypeString<" );
		if ( begin == NULL ) {
			fprintf( stderr, "TemplateTypeString failed!\n" );
			abort();
		}
		begin += sizeof( "TemplateTypeString<" ) - sizeof( '\0' );
		const char * end = findClosingRightSpaceshipBracket( begin - 1 );
#endif // __GNUC__
		makeString( begin , end );
	}

	const char * typeString() const { return _typeString ; }

private:
	char _typeString [ VOODOO_MAX_TEMPLATE_TYPE ];

	void makeString( const char * begin , const char * end )
	{
		unsigned len = end - begin;
		VOODOO_ASSERT( begin != 0 );
		VOODOO_ASSERT( end != 0 );
		if ( len >= VOODOO_MAX_TEMPLATE_TYPE ) {
			ErrorMessage error;
			error.append( "The template type '" );
			error.append( begin );
			error.append( "' is more than " );
			error.append( __VOODOO_QUOTE( VOODOO_MAX_TEMPLATE_TYPE ) );
			error.append( " characters wide. Please #define " );
			error.append( "VOODOO_MAX_TEMPLATE_TYPE to your " );
			error.append( "longest template type" );
			VOODOO_FAIL_TEST( error.result() );
		}
		memcpy( _typeString , begin , len );
		_typeString[ len ] = '\0';
	}

	const char * findClosingRightSpaceshipBracket( const char * leftBracket )
	{
		VOODOO_ASSERT( * leftBracket == '<' );
		return strstr( leftBracket , ">::" );
	}

	const char * findClosingRightBracket( const char * leftBracket )
	{
		VOODOO_ASSERT( * leftBracket == '[' );
		unsigned length = strlen( leftBracket );
		VOODOO_ASSERT( leftBracket[ length - 1 ] == ']' );
		return leftBracket + length - 1;
	}
};

class PointerTypeString
{
public:
	template < typename T >
	PointerTypeString( T * )
	{
		strncpy( _typeString , TemplateTypeString< T >().typeString() ,
				VOODOO_MAX_TEMPLATE_TYPE );
	}

	const char * typeString() const { return _typeString ; }

private:
	char _typeString [ VOODOO_MAX_TEMPLATE_TYPE ];
};

class DataDumpString
{
public:
	template < typename T >
	DataDumpString( T & t )
	{
		fromPointerLength( & t, sizeof( t ) );
	}

	DataDumpString( const void * pointer, size_t size )
	{
		fromPointerLength( pointer, size );
	}

	const char * dataString() const { return _dataString ; }

private:
	char _dataString [ VOODOO_MAX_DATA_DUMP ];

	char toHex( unsigned char nibble )
	{
		VOODOO_ASSERT( nibble < 16 );
		if ( nibble < 10 )
			return '0' + nibble;
		else
			return 'A' + nibble - 10;
	}

	unsigned appendHexByte( char * string, unsigned char byte )
	{
		string[ 0 ] = toHex( ( byte >> 4 ) & 0xF );
		string[ 1 ] = toHex( ( byte >> 0 ) & 0xF );
		return 2;
	}

	void fromPointerLength( const void * pointer, size_t size )
	{
		#define TRUNCATED_MESSAGE "\t\n (Data truncated, you can increase VOODOO_MAX_DATA_DUMP)"
		unsigned stringLength = 0;
		unsigned pos = 0;
		while ( pos < size ) {
			VOODOO_ASSERT( stringLength < VOODOO_MAX_DATA_DUMP );
			if ( stringLength > VOODOO_MAX_DATA_DUMP - 100 ) {
				memcpy( _dataString + stringLength, TRUNCATED_MESSAGE, sizeof( TRUNCATED_MESSAGE ) );
				return;
			}
			if ( pos % 8 == 0 ) {
				_dataString[ stringLength ] = '\n';
				++ stringLength;
			}
			unsigned char byte = ( (unsigned char *) pointer )[ pos ];
			stringLength += appendHexByte( _dataString + stringLength, byte );
			_dataString[ stringLength ] = ' ';
			++ stringLength;
			++ pos;
		}
	}
};

template < typename T >
struct isReferenceType
{
    static const constexpr bool value = std::is_pointer< T >::value;
};

#define SPECIALIZE_IS_REFERENCE_TYPE_FOR_SMART_PTR( _type ) template < typename T > struct isReferenceType< _type< T > > : std::true_type \
{ \
    static const constexpr bool value = true; \
}
SPECIALIZE_IS_REFERENCE_TYPE_FOR_SMART_PTR( std::unique_ptr );
SPECIALIZE_IS_REFERENCE_TYPE_FOR_SMART_PTR( std::shared_ptr );
#ifdef VOODOO_HAS_BOOST
SPECIALIZE_IS_REFERENCE_TYPE_FOR_SMART_PTR( boost::shared_ptr );
SPECIALIZE_IS_REFERENCE_TYPE_FOR_SMART_PTR( boost::weak_ptr );
#endif

template < typename T >
auto dereference( T & t ) -> decltype( *t ) &
{
  return * t;
}

template < typename T >
auto dereference( T & t ) -> typename std::enable_if< !isReferenceType< T >::value, T >::type &
{
  return t;
}

} // namespace VoodooCommon

#endif // __VOODOO_UTILS_H__
