#ifndef __MOCKED_H__
#define __MOCKED_H__

#include "Data.h"
#include <memory>

struct AMockedStruct {};

struct StructWithTemplateConstructor
{
	template< typename T >
	StructWithTemplateConstructor( T i );
};

void operateOnStruct( AMockedStruct & s );
void operateOnStructPtr( AMockedStruct * s );
void operateOnStructUniquePtr( std::unique_ptr< AMockedStruct > s );
void clear( Data & data );
void setInterval( unsigned interval );
void logMessage( const char * message );
void giveData( struct Data & data );
void doMoveData( MoveableData data );
void doMoveData( MoveableCtorData data );
void setCallback( DoItInterface & interface );
void setCallback( DoItInterface * interface );
void returnValueByReferenceOutParamter( unsigned & out );
void returnValueByPointerOutParamter( unsigned * out );

#endif // __MOCKED_H__
// FILE_EXEMPT_FROM_CODE_COVERAGE
