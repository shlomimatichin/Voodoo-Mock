#ifndef __EXAMPLE_MOCK_ME_H__
#define __EXAMPLE_MOCK_ME_H__

#include <memory>

namespace Example
{

class MockMe
{
public:
	MockMe(){}

	template < typename T >
	void mockMe( std::unique_ptr< T > & argument )
	{
	}

private:

	MockMe( const MockMe & rhs ) = delete;
	MockMe & operator= ( const MockMe & rhs ) = delete;
};

} // namespace Example

#endif // __EXAMPLE_MOCK_ME_H__
//FILE_EXEMPT_FROM_CODE_COVERAGE
