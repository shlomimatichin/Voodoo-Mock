#ifndef __TESTED_H__
#define __TESTED_H__

#include "Mocked.h"

void setDefaultInterval()
{
	setInterval( 4 );
}

void setHighInterval()
{
	setInterval( 10 );
}

void doubleClear( Spreadsheet & spreadsheet )
{
	clear( spreadsheet );
	clear( spreadsheet );
}

void copyAndClear( Spreadsheet & spreadsheet )
{
	Spreadsheet copy( spreadsheet );
	clear( copy );
}

void giveDataSwitched( struct Data data )
{
	unsigned temp = data.a;
	data.a = data.b;
	data.b = temp;
	giveData( data );
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

#endif // __TESTED_H__
