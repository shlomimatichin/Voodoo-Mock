#simple cxxtestgen version. No world/fixtures/suite context.
#No agregation of several tests files into one executable
#output main function supports command line specification of
#which test to run.

import argparse
import re
import subprocess

def getCodeLines( filename ):
    #removes comments
    preprocessed = subprocess.check_output( [ 'cpp', '-fpreprocessed', filename ] )
    return preprocessed.split( '\n' )

def findTestClass( lines ):
    index = 0
    while index < len( lines ) and not lines[ index ].startswith( 'class Test' ):
        index += 1
    if index == len( lines ):
        raise Exception( "a line that starts with 'class Test' was not found in the input line" )
    return index, re.match( r'class (Test[a-zA-Z0-9_]*)', lines[ index ] ).group( 1 )

def findTests( lines, firstLine ):
    assert firstLine < len( lines )
    index = firstLine
    tests = []
    testMethod = re.compile( r'^\s+void (test_[a-zA-Z0-9_]+)' )
    while index < len( lines ):
        match = testMethod.match( lines[ index ] )
        if match is not None:
            tests.append( ( match.group( 1 ), index + 1 ) )
        index += 1
    return tests

parser = argparse.ArgumentParser()
parser.add_argument( "--input", required = True )
parser.add_argument( "--output", required = True )
args = parser.parse_args()

lines = getCodeLines( args.input )
testClassLine, testClassName = findTestClass( lines )
tests = findTests( lines, testClassLine )
if len( tests ) == 0:
    raise Exception( "no tests found" )

RUN_TEST_TEMPLATE = r"""
 static class TestDescription_%(testName)s : public CxxTest::RealTestDescription {
 public:
  TestDescription_%(testName)s() : CxxTest::RealTestDescription( tests, suiteDescription, %(testLine)s, "%(testName)s" ) {}
  void runTest() { theSuite.%(testName)s(); }
 } * testDescription_%(testName)s = 0;
 if ( ( specificTest && testName == "%(testName)s" ) || ! specificTest )
  testDescription_%(testName)s = new TestDescription_%(testName)s;
"""

DELETE_TEMPLATE = r"""
 if ( testDescription_%(testName)s != 0 )
  delete testDescription_%(testName)s;
"""

TEMPLATE = r"""
#ifndef CXXTEST_RUNNING
#define CXXTEST_RUNNING
#endif

#define _CXXTEST_HAVE_STD
#define _CXXTEST_HAVE_EH
#define _CXXTEST_ABORT_TEST_ON_FAIL
#define _CXXTEST_LONGLONG long long
#include <iostream>
#include <cxxtest/StdValueTraits.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/RealDescriptions.h>
#include <cxxtest/VerboseListener.h>
#include <cxxtest/Root.cpp>

#include "%(testFile)s"

static %(testClass)s theSuite;
static CxxTest::List tests = { 0, 0 };
CxxTest::StaticSuiteDescription suiteDescription( "%(testFile)s", 1, "Test", theSuite, tests );

int main( int argc, const char * argv[] ) {
 bool specificTest = argc == 2;
 std::string testName = specificTest ? argv[ 1 ] : "";
 CxxTest::setAbortTestOnFail( true );
%(code)s
 int result = CxxTest::VerboseListener().run();
%(deleteCode)s
 return result;
}
"""

testsCode = "\n".join( RUN_TEST_TEMPLATE % dict(
            location = "%s:%d" % ( args.input, testLine ),
            testLine = testLine,
            testName = testName )
        for testName, testLine in tests )
deleteCode = "\n".join( DELETE_TEMPLATE % dict( testName = testName ) for testName, testLine in tests )
code = TEMPLATE % dict( code = testsCode,
                        testClass = testClassName,
                        location = "%s:1" % args.input,
                        testFile = args.input,
                        deleteCode = deleteCode )
with open( args.output, "w" ) as f:
    f.write( code )
