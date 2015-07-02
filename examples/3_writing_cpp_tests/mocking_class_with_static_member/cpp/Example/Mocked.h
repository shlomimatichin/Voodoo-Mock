#ifndef __MOCKED_H__
#define __MOCKED_H__

#include <stdio.h>

class FooWithStatic
{
public:
	FooWithStatic()
	{
		++_publicInstanceCounter;
		++_privateInstanceCounter;
	}
	void print()
	{
		printf( "_publicInstanceCounter: %d, _privateInstanceCounter: %d\n",
				_publicInstanceCounter, _privateInstanceCounter );
	}

	static int _publicInstanceCounter;
private:
	static int _privateInstanceCounter;
};

int FooWithStatic::_publicInstanceCounter;
int FooWithStatic::_privateInstanceCounter;

#endif // __MOCKED_H__
// FILE_EXEMPT_FROM_CODE_COVERAGE
