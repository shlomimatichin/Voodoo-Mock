#ifndef __VOODOO_EXPECTATION_LINE_MESSAGE_H__
#define __VOODOO_EXPECTATION_LINE_MESSAGE_H__

#include <VoodooCommon/Expect.h>

#ifndef VOODOO_EXPECT_DISALBE_LINE_MESSAGES
#define CallOrCopyOfReturnAuto _LineMessageWrapper( __FILE__ , __LINE__ ) << new CallOrCopyOfReturnAuto
#define CallOrCopyOfReturnReference _LineMessageWrapper( __FILE__ , __LINE__ ) << new CallOrCopyOfReturnReference
#define CallOrCopyOfReturnValue _LineMessageWrapper(  __FILE__ , __LINE__ ) << new CallOrCopyOfReturnValue
#define CallOrCopyOfReturnVoid _LineMessageWrapper( __FILE__ , __LINE__ ) << new CallOrCopyOfReturnVoid
#define CallOrCopyOfReturnCallbackReference _LineMessageWrapper( __FILE__ , __LINE__ ) << new CallOrCopyOfReturnCallbackReference
#define CallOrCopyOfThrowReference _LineMessageWrapper( __FILE__ , __LINE__ ) << new CallOrCopyOfThrowReference
#define CallOrCopyOfThrowValue _LineMessageWrapper( __FILE__ , __LINE__ ) << new CallOrCopyOfThrowValue
#define CallReturnAuto _LineMessageWrapper( __FILE__ , __LINE__ ) << new CallReturnAuto
#define CallReturnReference _LineMessageWrapper( __FILE__ , __LINE__ ) << new CallReturnReference
#define CallReturnValue _LineMessageWrapper(  __FILE__ , __LINE__ ) << new CallReturnValue
#define CallMoveValue _LineMessageWrapper(  __FILE__ , __LINE__ ) << new CallMoveValue
#define CallReturnVoid _LineMessageWrapper( __FILE__ , __LINE__ ) << new CallReturnVoid
#define CallReturnCallbackReference _LineMessageWrapper( __FILE__ , __LINE__ ) << new CallReturnCallbackReference
#define CallThrowReference _LineMessageWrapper( __FILE__ , __LINE__ ) << new CallThrowReference
#define CallThrowValue _LineMessageWrapper( __FILE__ , __LINE__ ) << new CallThrowValue
#define CallThrowValue _LineMessageWrapper( __FILE__ , __LINE__ ) << new CallThrowValue
#define Construction _LineMessageWrapper( __FILE__ , __LINE__ ) << new Construction
#define ConstructionThrowValue _LineMessageWrapper( __FILE__ , __LINE__ ) << new ConstructionThrowValue
#define Destruction _LineMessageWrapper( __FILE__ , __LINE__ ) << new Destruction
#endif // VOODOO_EXPECT_DISALBE_LINE_MESSAGES

namespace VoodooCommon {
namespace Expect
{

class _LineMessageWrapper : public PreIntercepter
{
public:
	_LineMessageWrapper( const char * filename , unsigned lineNo ) :
		_filename( filename ) ,
		_lineNo( lineNo )
	{
	}

	void check( const char * whatHappened )
	{
		try {
			PreIntercepter::check( whatHappened );
		} catch ( ErrorMessage & e ) {
			throwNewMessage( e );
		}
	}

	void check(	unsigned			parameterIndex ,
				const char *		typeString ,
				const void *		pointerToValue )
	{
		try {
			PreIntercepter::check( parameterIndex , typeString , pointerToValue );
		} catch ( ErrorMessage & e ) {
			throwNewMessage( e );
		}
	}

	void returnValue( const char * typeString , const void * & value )
	{
		try {
			PreIntercepter::returnValue( typeString , value );
		} catch ( ErrorMessage & e ) {
			throwNewMessage( e );
		}
	}

	void operator << ( Parameter::Interface * parameter )
	{
		try {
			PreIntercepter::operator << ( parameter );
		} catch ( ErrorMessage & e ) {
			throwNewMessage( e );
		}
	}

private:
	const char *	_filename;
	unsigned		_lineNo;

	void throwNewMessage( ErrorMessage & old )
	{
		ErrorMessage newMessage;
		newMessage.append( "\n" );
		newMessage.append( _filename );
		newMessage.append( ":" );
		newMessage.append( VOODOO_TO_STRING( _lineNo ) );
		newMessage.append( ": " );
		newMessage.append( old.result() );
		throw newMessage;
	}
};

} // namesapce Expect
} // namespace VoodooCommon

#endif // __VOODOO_EXPECTATION_LINE_MESSAGE_H__
