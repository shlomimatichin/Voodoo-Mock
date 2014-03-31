#ifndef __MOCKED_H__
#define __MOCKED_H__

#include <exception>

class MockedClass
{
public:
	static unsigned & staticMethod();
	char method();
};

void globalFunction();
namespace MockedNamespace { double globalNamespacedFunction(); }

void makeRunTimeError();

class File
{
public:
	File( const char * );
	void writeString( const char * );
};

#endif // __MOCKED_H__
