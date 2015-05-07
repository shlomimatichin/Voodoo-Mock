import sys
import os.path
import os
import stat
import re
import voodoo
import multiprocessing
import preprocessor
import argparse
import traceback

INCLUDE = [ r"\.h$", r"\.hh$", r"\.H$", r"\.HH$", r"\.hxx$", r"\.HXX$", r"\.hpp$", r"\.HPP$" ]

parser = argparse.ArgumentParser()
parser.add_argument( "--inputPath", action = "append", default = [], help = "The directory to walk for header files. Can be specified more than once" )
parser.add_argument( "--outputPath", required = True, help = "Output directory to generate mirror tree under" )
parser.add_argument( "--excludeFilesPattern", action = "append", default = [], help = "python regular expression for file names (relative path) to ignore. Can be specified more than once. Example: '--exclude=\\btests\\b'" )
parser.add_argument( "--onlyIfNew", action = "store_true", help = "Only generate files if origin file modification date is newer (like make does). This helps to integrate with build systems" )
parser.add_argument( "--concurrent", action = "store_true", help = "Detect CPU count, and parse files concurrently" )
parser.add_argument( "--voodooDB", default = "/tmp/voodoodb.tmp", help = "where to store the database used for the voodoohint script. The voodoohint script allows editor integration to generate scenario code semi-automatically. You probably want to leave it at the default, or disabling it by passing '--voodooDB='" )
parser.add_argument( "--includePath", action = "append", default = [], help = "an include path to pass into the CLang compiler. translates into a -I switch. Can be provided more than once. Since full compilation is performed to extract the API, all includes libraries the code under tests is using should be provided" )
parser.add_argument( "--define", action = "append", default = [], help = "a compiler macro to pass into the CLang compiler. translates into a -D switch. Can be provided more than once. Since full compilation is performed to extract the API, all macros required by the code under test must be provided, either from command line using this switch, or by using the '--preInclude' switch" )
parser.add_argument( "--preInclude", action = "append", default = [], help = "preinclude this file before all others - to fix issues with clang or the unittest framework. Since full compilation is performed to extract the API, all macros required by the code under test must be provided, either from this preincluded file, or by using the '--define' switch" )
args = parser.parse_args()

assert len( args.inputPath ) > 0, "please specify at least one --inputPath argument"
for inputPath in args.inputPath:
    assert os.path.isdir( inputPath ), "--inputPath must be an existing directory"
try:
    os.makedirs( args.outputPath )
except:
    pass
assert os.path.isdir( args.outputPath ), "--outputPath must be a directory"

def isInput( fullName ):
    match = False
    for include in INCLUDE:
        if re.search( include, fullName ) is not None:
            match = True
            break
    if not match:
        return False
    for exclude in args.excludeFilesPattern:
        if re.search( exclude, fullName ) is not None:
            return False
    return True

def mtime( fullName ):
    return os.stat( fullName )[ stat.ST_MTIME ]

def fullOutputName( fullName, inputPath ):
    return os.path.join( args.outputPath, fullName[ len( inputPath ) : ].strip( os.sep ) )

def inputList():
    fileList = []
    for inputPath in args.inputPath:
        for dir, dirNames, fileNames in os.walk( inputPath ):
            for fileName in fileNames:
                fullName = os.path.join( dir, fileName )
                if isInput( fullName ):
                    fullOutput = fullOutputName( fullName, inputPath )
                    if args.onlyIfNew and os.path.exists( fullOutput ):
                        if mtime( fullOutput ) > mtime( fullName ):
                            continue
                    fileList.append( ( fullName, inputPath ) )
    return fileList

def mkdirOf( fullName ):
    outputdir = os.path.dirname( fullName )
    try:
        os.makedirs( outputdir )
    except:
        pass

def voodooOneFile( fullName, inputPath, fileList ):
    fullOutput = fullOutputName( fullName, inputPath )
    mkdirOf( fullOutput )
    output = ''
    try:
        output += voodoo.voodoo(    input = fullName,
                                    output = fullOutput,
                                    pathToRemoveFromIdentifier = inputPath,
                                    voodooDBFile = args.voodooDB,
                                    includes = args.includePath,
                                    defines = args.define,
                                    trace = False,
                                    preIncludes = args.preInclude )
        state = "V"
    except Exception, e:
        if str(e).find( "all argume" ) != -1:
            raise
        inputLines = voodoo._readLinesOfFile( fullName )
        prepro = preprocessor.Preprocessor( fullName, fullOutput, inputLines, inputPath )
        output += prepro.intercepter()
        output += "\n/* The error that forced interception:\n" + \
                    str( e ).replace( "*/", "* /" ) + "\n"
        output += "\n"
        output += "Voodoo stack trace:\n" + traceback.format_exc()
        output += "*/\n"
        output += "\n"
        state = "I"
    f = file( fullOutput, "w" )
    f.write( output )
    f.flush()
    f.close()
    sys.stdout.write( "  <%d/%d> %s  %s\n" % (    1 + fileList.index( ( fullName, inputPath ) ),
                                                len( fileList ),
                                                state, fullOutput ) )

def cores():
    return multiprocessing.cpu_count();

def voodooFilesInList( fileList ):
    if args.concurrent:
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor( max_workers = cores() ) as executor:
            futures = [ executor.submit( voodooOneFile, fullName, inputPath, fileList ) for fullName, inputPath in fileList ]
            for future in concurrent.futures.as_completed( futures ):
                future.result()
    else:
        for fullName, inputPath in fileList:
            voodooOneFile( fullName, inputPath, fileList )

voodooFilesInList( inputList() )
