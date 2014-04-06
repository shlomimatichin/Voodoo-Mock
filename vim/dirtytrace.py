import re
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument( "filename" )
args = parser.parse_args()

inputLines = sys.stdin.readlines()
indent = re.match( r"(\s*)\S", inputLines[ 0 ] ).group( 1 )
input = "".join( inputLines )

if args.filename.endswith( ".py" ):
    sys.stdout.write( "### DIRTY TRACE\n" +
                        indent + "print 'X'*100\n" +
                        "### DIRTY TRACE END\n" +
                        input )
elif args.filename.endswith( ".cpp" ) or args.filename.endswith( ".h" ):
    sys.stdout.write( "/// DIRTY TRACE\n" +
                        '''std::cerr << __FILE__ << ':' << __LINE__ << ": XXXX " << std::endl;\n''' +
                        "/// DIRTY TRACE END\n" +
                        input )
else:
    assert False, "Not implemented for this file type"
