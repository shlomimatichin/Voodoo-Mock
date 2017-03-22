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

int FooWithStatic::_publicInstanceCounter = 0;
int FooWithStatic::_privateInstanceCounter = 0;

static int someNum;

class Foo
{
public:
	class IndentedFooWithStatic
	{
	public:
		IndentedFooWithStatic()
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
};

int Foo::IndentedFooWithStatic::_publicInstanceCounter = 0;
int Foo::IndentedFooWithStatic::_privateInstanceCounter = 0;

#endif // __MOCKED_H__
// FILE_EXEMPT_FROM_CODE_COVERAGE
