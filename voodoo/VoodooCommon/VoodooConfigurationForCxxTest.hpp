#include <cxxtest/TestSuite.h>

#define VOODOO_FAIL_TEST( s ) TS_FAIL( s )

#define VOODOO_FAIL_TEST_NO_THROW( s ) do { \
        try { \
            VOODOO_FAIL_TEST( s ); \
        } catch( CxxTest::AbortTest & ) {} \
    } while ( false ) 

#define VOODOO_WARNING( x ) TS_WARN( stderr , "%s\n" , x );

#define VOODOO_TO_STRING( x ) TS_AS_STRING( x )
