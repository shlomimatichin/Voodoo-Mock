import sys
import os.path
import voodoo
import argparse

parser = argparse.ArgumentParser()
parser.add_argument( "--input", required = True, help = "file to parse" )
parser.add_argument( "--output", required = True, help = "output location (if directory, input's subdirs will be recreated)" )
parser.add_argument( "--pathToRemoveFromIdentifier", default = "", help = "shorten the VOODOO_* and VOODOO_EXPECT_* macros by using less components of the file path. Example: if running 'python single.py --input=c/namespace/file.h --output=voodoo', the macro 'VOODOO_c_namespace_file_h' will be generated. Adding '--pathTo=c' will cause the macro 'VOODOO_namespace_file_h' to be used instead" )
parser.add_argument( "--voodooDB", default = "/tmp/voodoodb.tmp", help = "where to store the database used for the voodoohint script. The voodoohint script allows editor integration to generate scenario code semi-automatically. You probably want to leave it at the default, or disabling it by passing '--voodooDB='" )
parser.add_argument( "--includePath", action = "append", default = [], help = "an include path to pass into the CLang compiler. translates into a -I switch. Can be provided more than once. Since full compilation is performed to extract the API, all includes libraries the code under tests is using should be provided" )
parser.add_argument( "--define", action = "append", default = [], help = "a compiler macro to pass into the CLang compiler. translates into a -D switch. Can be provided more than once. Since full compilation is performed to extract the API, all macros required by the code under test must be provided, either from command line using this switch, or by using the '--preInclude' switch" )
parser.add_argument( "--preInclude", action = "append", default = [], help = "preinclude this file before all others - to fix issues with clang or the unittest framework. Since full compilation is performed to extract the API, all macros required by the code under test must be provided, either from this preincluded file, or by using the '--define' switch" )
parser.add_argument( "--trace", action = "store_true", help = "trace more for debugging voodoo itself" )
args = parser.parse_args()

if not os.path.isfile( args.input ):
    raise Exception( "'%s' is not a file" % args.input )
output = args.output
if os.path.isdir( output ):
    output = os.path.join( output, args.input )
outputdir = os.path.dirname( output )
try:
	os.makedirs( os.path.dirname( output ) )
except:
	pass

content = voodoo.voodoo(	input = args.input,
							output = output,
							pathToRemoveFromIdentifier = args.pathToRemoveFromIdentifier,
							trace = args.trace,
							voodooDBFile = args.voodooDB,
							includes = args.includePath,
							defines = args.define,
                            preIncludes = args.preInclude )
f = file( output , "w" )
f.write( content )
f.close()
