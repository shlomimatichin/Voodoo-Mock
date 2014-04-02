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
            tests.append( ( match.group( 1 ), index ) )
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
if ( ( specificTest && testName == "%(testName)s" ) || ! specificTest ) {
 std::cout << "\nTEST '%(testName)s'\n";
 try {
  testClass->setUp();
 } catch ( std::exception & e ) {
  std::cout << "\n%(location)s: Exception '" << e.what() << "' thrown from setUp (for test %(testName)s)\n";
  allPassed = false;
 } catch ( ... ) {
  std::cout << "\n%(location)s: Exception thrown from setUp (for test %(testName)s)\n";
  allPassed = false;
 }
 try {
  testClass->%(testName)s();
 } catch ( std::exception & e ) {
  std::cout << "\n%(location)s: Exception '" << e.what() << "' thrown from test %(testName)s\n";
  allPassed = false;
 } catch ( ... ) {
  std::cout << "\n%(location)s: Exception thrown from test %(testName)s\n";
  allPassed = false;
 }
 try {
  testClass->tearDown();
 } catch ( std::exception & e ) {
  std::cout << "\n%(location)s: Exception '" << e.what() << "' thrown from tearDown for test %(testName)s\n";
  allPassed = false;
 } catch ( ... ) {
  std::cout << "\n%(location)s: Exception thrown from tearDown for test %(testName)s\n";
  allPassed = false;
 }
}
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
#include <cxxtest/Root.cpp>
#include "%(testFile)s"

int main( int argc, const char * argv[] ) {
 bool allPassed = true;
 bool specificTest = argc == 2;
 std::string testName = specificTest ? argv[ 1 ] : "";
 %(testClass)s * testClass;
 CxxTest::setAbortTestOnFail( true );

 try {
  testClass = new %(testClass)s;
 } catch ( std::exception & e ) {
  std::cout << "\n%(location)s: Exception '" << e.what() << "' thrown from constructor of %(testClass)s\n";
  allPassed = false;
 } catch ( ... ) {
  std::cout << "\n%(location)s: Exception thrown from constructor of %(testClass)s\n";
  allPassed = false;
 }

 %(code)s

 delete testClass;
 return allPassed ? 0 : 1;
}
"""

testsCode = "\n".join( RUN_TEST_TEMPLATE % dict(
            location = "%s:%d" % ( args.input, testLine ),
            testName = testName )
        for testName, testLine in tests )
code = TEMPLATE % dict( code = testsCode,
                        testClass = testClassName,
                        location = "%s:1" % args.input,
                        testFile = args.input )
with open( args.output, "w" ) as f:
    f.write( code )
