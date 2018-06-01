import sys
import re

PYTHON_TEST_METHOD_DEFINITION = re.compile( "\s+def\s+(test_\w+)\(" )
CPP_TEST_METHOD_DEFINITION = re.compile( "\s+void\s+(test_\w+)\(" )

filename = sys.argv[ 1 ]
lineNumberOrRegex = sys.argv[ 2 ]

try:
    lineNumber = int( sys.argv[ 2 ] ) - 1
    secondArgumentIsALineNumber = True
except:
    secondArgumentIsALineNumber = False

if secondArgumentIsALineNumber:
    lines = open( filename ).readlines()
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
else:
    content = open( filename ).read()
    for testName in PYTHON_TEST_METHOD_DEFINITION.findall(content) + \
            CPP_TEST_METHOD_DEFINITION.findall(content):
        if re.search(lineNumberOrRegex, testName) is not None:
            print testName
            sys.exit( 0 )
    print "REGEX DOES NOT MATCH TEST METHOD"
sys.exit( 1 )
