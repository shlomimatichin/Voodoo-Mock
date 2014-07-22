#ifndef __EXAMPLE_UNDER_TEST_H__
#define __EXAMPLE_UNDER_TEST_H__

#include "Example/MockMe.h"

namespace Example
{

class UnderTest
{
public:
	UnderTest(){}

	void underTest()
	{
		MockMe< int > mockMe;
		int result = mockMe.mockMe( 3 );
		(void) result;
	}

private:

	UnderTest( const UnderTest & rhs ) = delete;
	UnderTest & operator= ( const UnderTest & rhs ) = delete;
};

} // namespace Example

#endif // __EXAMPLE_UNDER_TEST_H__
