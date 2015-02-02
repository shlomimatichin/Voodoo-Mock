#ifndef __UNDERTEST_H_
#define __UNDERTEST_H_

#include "Mocked.h"
#include <memory>

void setDefaultInterval()
{
	setInterval( 4 );
}

void setHighInterval()
{
	setInterval( 10 );
}

void doSomething( AMockedStruct & s)
{
	operateOnStruct( s );
}

void doSomethingOnUniquePtr( std::unique_ptr< AMockedStruct > s)
{
	operateOnStructUniquePtr( std::move( s ) );
}

void doSomethingOnPtr( AMockedStruct * s)
{
	operateOnStructPtr( s );
}

void doSomethingOnIgnoredParameterPack( int n, float f, const char * str )
{
	ClassWithIgnoredParameterPack c { f, n, str };
	c.someOperation( n, f, str );
}

void doSomethingOnParameterPack( int n, float f, const char * str )
{
	ClassWithParameterPack c { f, n, str };
	c.someOperation( n, f, str );
}

void doubleClear( Data & data )
{
	clear( data );
	clear( data );
}

void copyAndClear( Data & data )
{
	Data copy( data );
	clear( copy );
}

void giveDataSwitched( struct Data data )
{
	unsigned temp = data.a;
	data.a = data.b;
	data.b = temp;
	giveData( data );
}

template < typename T >
void moveData( T data )
{
	doMoveData( std::move( data ) );
}

void setCallbackByReference()
{
	class DoIt : public DoItInterface
	{
	public:
		void doIt() { setInterval( 0 ); }
	};

	static DoIt it;
	setCallback( it );
}

void setCallbackByPointer()
{
	class DoIt : public DoItInterface
	{
	public:
		void doIt() { setInterval( 1 ); }
	};

	static DoIt it;
	setCallback( & it );
}

unsigned outParameterToReturnValue()
{
	unsigned result;
	returnValueByReferenceOutParamter( result );
	return result;
}

unsigned outPointerParameterToReturnValue()
{
	unsigned result;
	returnValueByPointerOutParamter( & result );
	return result;
}

void markLog()
{
	logMessage( "MARK" );
}

void createWithTemplateConstructor( int n )
{
	StructWithTemplateConstructor c { n };
}

#endif // __UNDERTEST_H_
// FILE_EXEMPT_FROM_CODE_COVERAGE
