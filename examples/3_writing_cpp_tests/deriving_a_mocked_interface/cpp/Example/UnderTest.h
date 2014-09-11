#ifndef __EXAMPLE_UNDER_TEST_H__
#define __EXAMPLE_UNDER_TEST_H__

#include "Example/SomeInterface.h"

namespace Example
{

class UnderTest : public SomeInterface
{
public:
	UnderTest( SomeInterface * ptr ) : _ptr( ptr ) {}

	void doSomething( int i ) override
	{
		_ptr->doSomething( i + 1 );
	}

private:

	UnderTest( const UnderTest & rhs ) = delete;
	UnderTest & operator= ( const UnderTest & rhs ) = delete;

	SomeInterface * _ptr;
};

} // namespace Example

#endif // __EXAMPLE_UNDER_TEST_H__
