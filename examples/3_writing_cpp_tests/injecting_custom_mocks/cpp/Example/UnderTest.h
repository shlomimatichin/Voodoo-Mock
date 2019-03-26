#ifndef __UNDERTEST_H_
#define __UNDERTEST_H_

#include "Example/Mocked.h"
#include <memory>

class ToBeTested
{
public:
	ToBeTested() = default;

	int getValue( )
	{
		return _foo.generateValue() * 10;
	}
private:
	SomeClass _foo;
};

#endif // __UNDERTEST_H_
// FILE_EXEMPT_FROM_CODE_COVERAGE
