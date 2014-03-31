#include <cxxtest/TestSuite.h>

#define VOODOO_FAIL_TEST( s ) TS_FAIL( s )

#define VOODOO_WARNING( x ) TS_WARN( stderr , "%s\n" , x );

#define VOODOO_TO_STRING( x ) TS_AS_STRING( x )
