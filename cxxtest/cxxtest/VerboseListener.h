#ifndef __cxxtest__VerboseListener_h__
#define __cxxtest__VerboseListener_h__

#include <cxxtest/ErrorPrinter.h>

namespace CxxTest
{
    class VerboseListener : public ErrorPrinter
    {
	private:
        void enterWorld( const WorldDescription & desc )
		{
			* outputStream() << "\nCOUNT " << desc.numTotalTests() << "\n";
			outputStream()->flush();
		}
        void enterSuite( const SuiteDescription & desc )
		{
			* outputStream() << "\nSUITE '" << desc.suiteName() << "'\n";
			outputStream()->flush();
		}
        void enterTest( const TestDescription & desc )
		{
			* outputStream() << "\nTEST '" << desc.testName() << "'\n";
			outputStream()->flush();
		}
        void leaveWorld( const WorldDescription &desc ) {}
        void leaveTest( const TestDescription & ) {}
    };
}

#endif // __cxxtest__VerboseListener_h__
