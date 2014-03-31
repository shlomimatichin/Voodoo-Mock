#include <cxxtest/TestSuite.h>

#define VOODOO_EXPECT_File_h

#include "Map.h"

using namespace VoodooCommon::Expect;
using namespace VoodooCommon::Expect::Parameter;

class Test_Map: public CxxTest::TestSuite
{
public:
	void test_Read()
	{
		Map tested( "The Map Name" );

		Scenario scenario;
		scenario <<
			new Construction< File >( "Fake file" ) <<
				new EqualsValue< std::string >( "/tmp/map_The Map Name_The Key Name.dat" ) <<
			new CallReturnValue< std::string >( "Fake file::read", "The Expected Value" ) <<
			new Destruction( "Fake file" );
		std::string result = tested.get( "The Key Name" );
		scenario.assertFinished();
		TS_ASSERT_EQUALS( result, "The Expected Value" );
	}

	void test_Write()
	{
		Map tested( "The Map Name" );

		Scenario scenario;
		scenario <<
			new Construction< File >( "Fake file" ) <<
				new EqualsValue< std::string >( "/tmp/map_The Map Name_The Key Name.dat" ) <<
			new CallReturnVoid( "Fake file::write" ) <<
				new EqualsValue< std::string >( "The Written Value" ) <<
			new Destruction( "Fake file" );
		tested.set( "The Key Name", "The Written Value" );
		scenario.assertFinished();
	}
};
