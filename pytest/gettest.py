import sys
import re

PYTHON_TEST_METHOD_DEFINITION = re.compile( "\s+def\s+(test_\w+)\(" )
CPP_TEST_METHOD_DEFINITION = re.compile( "\s+void\s+(test_\w+)\(" )

filename = sys.argv[ 1 ]
lines = open( filename ).readlines()

try:
    lineNumber = int( sys.argv[ 2 ] ) - 1
    # This flow only apply for the case that second arg is line-number
    assert lineNumber < len(lines), "Line number must be inside file length"

    for line in reversed( lines[ : lineNumber + 1 ] ):
        match = PYTHON_TEST_METHOD_DEFINITION.match( line )
        if match:
            print match.group( 1 )
            sys.exit( 0 )
        match = CPP_TEST_METHOD_DEFINITION.match( line )
        if match:
            print match.group( 1 )
            sys.exit( 0 )
    print "POSITION IN FILE IS NOT INSIDE A TEST METHOD"
except ValueError:
    # This flow only apply for the case that second arg is test's name regex
    testNameRegex = sys.argv[ 2 ]

    for line in lines:
        match = PYTHON_TEST_METHOD_DEFINITION.match( line )
        if match and re.match(testNameRegex,  match.group(1)):
                print match.group( 1 )
                sys.exit( 0 )
        match = CPP_TEST_METHOD_DEFINITION.match( line )
        if match and re.match(testNameRegex, match.group(1)):
                print match.group( 1 )
                sys.exit( 0 )
    print "REGEX DOES NOT MATCH TEST METHOD"
sys.exit( 1 )
