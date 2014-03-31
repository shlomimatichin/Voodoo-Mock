#if ! defined(__VOODOO_COMMON_SPRINTF_H__)
#define __VOODOO_COMMON_SPRINTF_H__

#include <stdarg.h>
#include <stdio.h>
#include <string>

namespace VoodooCommon
{

class Sprintf
{
public:
	Sprintf( const char * format, ... )
	{
		va_list args;
		va_start( args, format );
		vsnprintf( buffer, sizeof( buffer ), format, args );
		buffer[ sizeof( buffer ) - 1 ] = '\0';
		va_end( args );
	}

	operator const char * () const { return buffer; }
	operator std::string () const { return buffer; }

private:
	char buffer[ 512 ];
};

}

#endif // __VOODOO_COMMON_SPRINTF_H__
