#define VOODOO_cpp_Example_Mocked_h
#include <cxxtest/TestSuite.h>

#include "Example/UnderTest.h"
#include <iostream>

//using namespace VoodooCommon::Expect;
//using namespace VoodooCommon::Expect::Parameter;

class MockSomeClass : public Mock_SomeClass
{
public:
	bool SomeClass_Constructor()
	{
		return true;
	}

	void setValue( int n )
	{
		_n = n;
	}

	int generateValue()
	{
		return _n;
	}

private:
	int _n;
};

class Test_Example: public CxxTest::TestSuite
{
public:
	std::unique_ptr< MockSomeClass > _mockedSomeClass;

	void setUp()
	{
		_mockedSomeClass.reset( new MockSomeClass );
	}

	void tearDown()
	{
	}

	void test_ZeroValue()
	{
		ToBeTested tested;

		_mockedSomeClass->setValue( 0 );
		TS_ASSERT_EQUALS( 0, tested.getValue() );
	}

	void test_PositiveValue()
	{
		ToBeTested tested;

		_mockedSomeClass->setValue( 1 );
		tested.getValue( );
		TS_ASSERT_EQUALS( 10, tested.getValue() );
	}

	void test_NegativeValue()
	{
		ToBeTested tested;

		_mockedSomeClass->setValue( -1 );
		TS_ASSERT_EQUALS( -10, tested.getValue() );
	}

};
