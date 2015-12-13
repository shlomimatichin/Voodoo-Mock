#ifndef __EXAMPLE_MOCK_ME_H__
#define __EXAMPLE_MOCK_ME_H__

namespace Example
{

template < typename T >
class Mockme;

template < typename T >
class MockMe
{
public:
	MockMe(){}

	T mockMe( T argument )
	{
		return argument + argument;
	}

private:

	MockMe( const MockMe & rhs ) = delete;
	MockMe & operator= ( const MockMe & rhs ) = delete;
};

} // namespace Example

#endif // __EXAMPLE_MOCK_ME_H__
//FILE_EXEMPT_FROM_CODE_COVERAGE
