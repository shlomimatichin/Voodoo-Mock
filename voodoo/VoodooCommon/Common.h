#ifndef __VOODOO_COMMON
#define __VOODOO_COMMON

#include "VoodooConfiguration.h"
#include <string.h>

class __VoodooMockConstruction {};

#define __VoodooRedirectorConstruction __Voodoo_Error_You_Must_Enable_Voodoo_For_This_Derived_Class_Too
class __VoodooRedirectorConstruction {};

#ifndef VOODOO_MAX_MESSAGE
#define VOODOO_MAX_MESSAGE 4096
#endif // VOODOO_MAX_MESSAGE

#define __VOODOO_QUOTE( x ) #x

class __VoodooGrowingString
{
public:
	__VoodooGrowingString()
	{
		_result[ 0 ] = '\0';
		_result[ VOODOO_MAX_MESSAGE - 1 ] = '\0' ;
		_result[ VOODOO_MAX_MESSAGE ] = '\0' ;
	}

	void append( const char * source )
	{
		unsigned length = strlen( _result );
		strncat( _result , source , VOODOO_MAX_MESSAGE - length );
	}

	const char * result()
	{
		if ( _result[ VOODOO_MAX_MESSAGE - 1 ] != '\0' ) {
			VOODOO_FAIL_TEST( "Please #define VOODOO_MAX_MESSAGE to a value " 
						"larger than " __VOODOO_QUOTE( VOODOO_MAX_MESSAGE ) );
		}
		return _result;
	}

private:
	char _result[ VOODOO_MAX_MESSAGE + 1 ];
};

#endif // __VOODOO_COMMON
