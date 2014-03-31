#ifndef __TESTED_H__
#define __TESTED_H__

#include "Mocked.h"

static inline void callGlobalFunction()
{
	globalFunction();
}

static inline double callGlobalNamespacedFunction()
{
	using namespace MockedNamespace;
	return globalNamespacedFunction();
}

static inline unsigned & callStaticMethod()
{
	return MockedClass::staticMethod();
}

static inline char constructClassToCallMethod()
{
	return MockedClass().method();
}

static inline void catchRunTimeError()
{
	try {
		makeRunTimeError();
	} catch ( ... ) {}
}

static inline void logMessage( const char * message )
{
	try {
		File( "C:\\log.txt" ).writeString( message );
	} catch ( ... ) {}
}

#endif // __TESTED_H__
