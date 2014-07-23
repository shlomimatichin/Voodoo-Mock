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
		int what = 8;
		MockMe mockMe( what );
		int first = 1;
		const char * second = "yada";
		mockMe.justASimpleVoidMethod( first, second );
		int result = mockMe.returnsAnInt();
		(void) result;
		std::unique_ptr< int > result2 = mockMe.returnsAUniquePtr();
		(void) result2;

		globalFunction( second );
	}

private:

	UnderTest( const UnderTest & rhs ) = delete;
	UnderTest & operator= ( const UnderTest & rhs ) = delete;
};

} // namespace Example

#endif // __EXAMPLE_UNDER_TEST_H__
