#ifndef __EXAMPLE_SOME_INTERFACE_H_
#define __EXAMPLE_SOME_INTERFACE_H_

namespace Example
{

class SomeInterface
{
public:
	virtual ~SomeInterface(){}

	virtual void doSomething( int i ) = 0;
};

} // namespace Example

#endif // __EXAMPLE_SOME_INTERFACE_H_
// FILE_EXEMPT_FROM_CODE_COVERAGE
