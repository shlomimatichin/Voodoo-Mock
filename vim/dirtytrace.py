import re
import sys

PYTHON_FILE = False
CPP_FILE = False

if len( sys.argv ) == 2 and sys.argv[ 1 ].endswith( ".py" ):
	PYTHON_FILE = True
if len( sys.argv ) == 2 and sys.argv[ 1 ].endswith( ".cpp" ) or sys.argv[ 1 ].endswith( ".h" ):
	CPP_FILE = True

if PYTHON_FILE:
    inputLines = sys.stdin.readlines()
    indent = re.match( r"(\s*)\S", inputLines[ 0 ] ).group( 1 )
    input = "".join( inputLines )

    sys.stdout.write( "### DIRTY TRACE\n" +
                        indent + "print 'X'*100\n" +
                        "### DIRTY TRACE END\n" +
                        input )
elif CPP_FILE:
    inputLines = sys.stdin.readlines()
    indent = re.match( r"(\s*)\S", inputLines[ 0 ] ).group( 1 )
    input = "".join( inputLines )

    sys.stdout.write( "/// DIRTY TRACE\n" +
                        '''std::cerr << __FILE__ << ':' << __LINE__ << ": XXXX " << std::endl;\n''' +
                        "/// DIRTY TRACE END\n" +
                        input )
else:
    assert False, "Not implemented for this file type"
