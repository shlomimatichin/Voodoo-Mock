#include <cxxtest/TestSuite.h>

#if !defined(_WIN32) && defined( __GNUG__ )

#include <execinfo.h>

#	define VOODOO_FAIL_TEST( s ) do { \
		try { \
			TS_FAIL( s ); \
		} catch( ... ) { \
			void * bt[ 64 ]; \
			int result = backtrace( bt, 64 ); \
			backtrace_symbols_fd( bt, result, 1 ); \
			throw; \
		} \
	} while ( 0 )

#else // __GNUC__

#	define VOODOO_FAIL_TEST( s ) TS_FAIL( s )

#endif // __GNUC__

#define VOODOO_FAIL_TEST_NO_THROW( s ) do { \
        try { \
            VOODOO_FAIL_TEST( s ); \
        } catch( CxxTest::AbortTest & ) {} \
    } while ( false )

#define VOODOO_WARNING( x ) TS_WARN( x )

#define VOODOO_TO_STRING( x ) TS_AS_STRING( x )
