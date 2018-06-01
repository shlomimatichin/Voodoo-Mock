#ifndef __VOODOO_CONFIGURATION_H__
#define __VOODOO_CONFIGURATION_H__

#include <stdio.h>
#include <unistd.h>
#include <strstream>

class VoodooTestFailed {};

#define VOODOO_FAIL_TEST( s ) { \
		fprintf( stderr , "%s\n" , s );\
		throw VoodooTestFailed(); \
	}
#define VOODOO_FAIL_TEST_NO_THROW( s ) { \
		fprintf( stderr , "%s\n" , s );\
        _exit(1); \
    }
#define VOODOO_WARNING( x ) fprintf( stderr , "%s\n" , x );

#define VOODOO_TO_STRING( x ) \
	( ( (std::strstream &) (std::strstream() << (x) << '\0') ).str() )

#endif
