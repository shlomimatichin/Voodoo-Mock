#ifndef __UNDERTEST_H_
#define __UNDERTEST_H_

#include "Mocked.h"
#include <memory>

void printFoo()
{
	FooWithStatic f;
	f.print();
}

#endif // __UNDERTEST_H_
// FILE_EXEMPT_FROM_CODE_COVERAGE
