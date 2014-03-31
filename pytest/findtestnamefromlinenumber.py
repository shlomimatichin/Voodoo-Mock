import sys
import re

filename = sys.argv[ 1 ]
lineNumber = int( sys.argv[ 2 ] ) - 1

lines = open( filename ).readlines()
assert lineNumber < len( lines ), "Line number must be inside file length"

PYTHON_TEST_METHOD_DEFINITION = re.compile( "\s+def\s+(test_\w+)\(" )
CPP_TEST_METHOD_DEFINITION = re.compile( "\s+void\s+(test_\w+)\(" )

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
sys.exit( 1 )
