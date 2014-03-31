#ifndef __MOCKED_H__
#define __MOCKED_H__

#include "Data.h"

class Spreadsheet {};
void clear( Spreadsheet & );
void setInterval( unsigned );
void logMessage( const char * );
void giveData( struct Data & data );
void setCallback( DoItInterface & interface );
void setCallback( DoItInterface * interface );
void returnValueByReferenceOutParamter( unsigned & out );
void returnValueByPointerOutParamter( unsigned * out );

#endif // __MOCKED_H__
