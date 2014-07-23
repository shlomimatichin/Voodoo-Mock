#ifndef __EXAMPLE_MOCK_ME_H__
#define __EXAMPLE_MOCK_ME_H__

namespace Example
{

class MockMe
{
public:
	MockMe(){}

	this class does not pass through the voodoo parser:
	1. maybe its way too complicated to parse (for example, a boost header file)
	2. maybe you are building the stub before writing the code
	3. maybe you just want something very custom in your test

private:

	MockMe( const MockMe & rhs ) = delete;
	MockMe & operator= ( const MockMe & rhs ) = delete;
};

} // namespace Example

#endif // __EXAMPLE_MOCK_ME_H__
//FILE_EXEMPT_FROM_CODE_COVERAGE
