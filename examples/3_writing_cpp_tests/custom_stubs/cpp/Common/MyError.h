#ifndef __COMMON_MY_ERROR_H__
#define __COMMON_MY_ERROR_H__

#include <string>
#include <stdexcept>

class MyError : public std::runtime_error
{
public:
	MyError( const std::string & what, const char * filename, unsigned line ) :
		std::runtime_error( what ),
		filename( filename ),
		line( line )
	{}

	const char * const filename;
	const unsigned line;
};

#define EXCEPTION_SUBCLASS( name, superclass ) \
	class name : public superclass \
	{ \
	public: \
		using ::MyError::MyError; \
	}

#define EXCEPTION_CLASS( name ) EXCEPTION_SUBCLASS( name, ::MyError )

#define THROW( name, serialize ) do { \
		std::ostringstream __seralize; \
		__seralize << serialize << \
			" (" << __FILE__ << ':' << __LINE__ << ':' << \
				__FUNCTION__ << ')'; \
		throw name( __seralize.str(), __FILE__, __LINE__ ); \
	} while( 0 )

#endif // __COMMON_MY_ERROR_H__
//FILE_EXEMPT_FROM_CODE_COVERAGE
