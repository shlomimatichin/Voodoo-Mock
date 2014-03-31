import os
import stat
import sys
import re
import argparse
import shelve
import traceback

parser = argparse.ArgumentParser()
parser.add_argument( "--dumpDB", action = "store_true" )
parser.add_argument( "--hintLine", type = int )
parser.add_argument( "--db", default = "/tmp/voodoodb.tmp" )
args = parser.parse_args()
assert args.hintLine or args.dumpDB, "Please specify at least one of --hintLine or --dumpDB"

def typeWithoutReference( type ):
    return type.replace( " :: ", "::" ).replace( ":: ", "::" ).strip().rstrip( '&' ).strip()

def parameterType( parametersListPair ):
    found = parametersListPair[ 0 ].rfind( parametersListPair[ 1 ] )
    result = parametersListPair[ 0 ][ : found ] + \
            parametersListPair[ 0 ][ found + len( parametersListPair[ 1 ] ) : ]
    return typeWithoutReference( result )

def parametersLines( input, decomposition ):
    result = []
    for p in decomposition.parameters:
         result.append( "new EXPECTATION < %s >( PARAMETER ) <<" % p[ 'text' ] )
#        unnamespacedType = p.type.split( "::" )[ -1 ]
#        allExpectConstructions = re.findall( r'Construction\s*\<\s*(.*?%s)\s*\>\s*\(\s*\"(.*?)\"\s*\)' % type, input )
#        allFakeConstructions = re.findall( r'Fake(ND)?_%s\s*\(\s*\"(.*?)\"\s*\)' % unnamespacedType, input )
#        if len( allExpectConstructions ) == 1 and len( allFakeConstructions ) == 0:
#            result.append( 'new Named< %s >( "%s" ) <<' % (
#                    allExpectConstructions[ 0 ][ 0 ], allExpectConstructions[ 0 ][ 1 ] ) )
#        elif len( allExpectConstructions ) == 0 and len( allFakeConstructions ) == 1:
#            raise Exception( "not implememnted yet!" )
#        else:
#            result.append( "new EXPECTATION < %s >( PARAMETER ) <<" % p.type )
    return result

def typeOfNamedObject( input, object ):
    exp = r'Construction\s*\<\s*(.*)\s*\>\s*\(\s*\"%s\"\s*\)' % object
    match = re.search( exp, input )
    exp = r'\b([\S:]*)Fake(ND)?_(\S*)\s+.*\(\s*\"%s\"\s*\)' % object
    match2 = re.search( exp, input )
    if match is not None:
        return match.group( 1 ).strip()
    if match2 is not None:
        return ( match2.group( 1 ) + match2.group( 3 ) ).strip()
    raise Exception( 'Unable to find Construction< ? >( "%s" ) or Fake[ND]_?( "%s" )' % (
                object, object ) )

def splitLineToTabFullNamespaceFunction( line ):
    tab, full = re.match( r'(\s*)(\S.*\S)\s*$', line ).groups()
    match = re.match( r'(.*)::([^:]*)', full )
    if match is None:
        namespace = ""
        function = full
    else:
        namespace, function = match.groups()
    return tab, full, namespace, function

def findDecompositionInCache( cache, name ):
    for key in cache.keys():
        if key.endswith( name ):
            return cache[ key ]
    raise Exception( "Entity name '%s' not found in Database!" % name )

def functionFirstLine( decomposition, function ):
    if decomposition.returnType == 'void':
        return 'new CallReturnVoid( "%s" ) <<' % function
    elif decomposition.returnType == 'bool':
        return 'new CallReturnValue< bool >( "%s", true ) <<' % function
    elif decomposition.returnType == 'int':
        return 'new CallReturnValue< int >( "%s", 0 ) <<' % function
    elif decomposition.returnType.endswith( ' *' ):
        return 'new CallReturnValue< %s >( "%s", nullptr ) <<' % ( decomposition.returnType, function )
    else:
        return 'new CallReturn RETURNTYPE < %s >( "%s", RESULT ) <<' % (
                    typeWithoutReference( decomposition.returnType ), function )

def hintFunctionCall( cache, inputLines, input, hintLine ):
    tab, function = splitLineToTabFullNamespaceFunction( hintLine )[ : 2 ]
    decomposition = findDecompositionInCache( cache, function )
    firstLine = functionFirstLine( decomposition, function )
    paramsLines = parametersLines( input, decomposition )
    replacement = tab + ( "\n%s\t" % tab ).join( [ firstLine ] + paramsLines ) + "\n"
    return replacement

def hintMethodCall( cache, inputLines, input, hintLine ):
    tab, function, object, functionName = splitLineToTabFullNamespaceFunction( hintLine )
    className = typeOfNamedObject( input, object )
    functionName = className + "::" + functionName
    decomposition = findDecompositionInCache( cache, functionName )
    firstLine = functionFirstLine( decomposition, function )
    paramsLines = parametersLines( input, decomposition )
    replacement = tab + ( "\n%s\t" % tab ).join( [ firstLine ] + paramsLines ) + "\n"
    return replacement

def hintConstruction( cache, inputLines, input, hintLine ):
    tab, fullClassName, namespace, className = splitLineToTabFullNamespaceFunction( hintLine )
    constructorName = fullClassName + "::" + className
    decomposition = findDecompositionInCache( cache, constructorName )
    firstLine = 'new Construction< %s >( "%s" ) <<' % ( fullClassName, className )
    paramsLines = parametersLines( input, decomposition )
    replacement = tab + ( "\n%s\t" % tab ).join( [ firstLine ] + paramsLines ) + "\n"
    return replacement

def hintNewHook( cache, inputLines, input, hintLine ):
    tab = re.match( r"(\s*)NewHook(\s*)$", hintLine ).group( 1 )
    return "%sclass ? { public: void operator () () {\n\n%s} };\n" % ( tab, tab )

cache = shelve.open( args.db, "r" )
if args.hintLine:
    inputLines = sys.stdin.readlines()
    input = "".join( inputLines )
    outputLines = inputLines
    hintLine = inputLines[ args.hintLine - 1 ]
    replacement = ""
    for hint in [ hintFunctionCall, hintMethodCall, hintConstruction, hintNewHook ]:
        try:
            replacement = hint( cache, inputLines, input, hintLine )
            break
        except Exception, e:
            replacement += "%s did not work, trace:\n%s\n" % ( hint, traceback.format_exc() )
    outputLines[ args.hintLine - 1 ] = replacement
    sys.stdout.write( "".join( outputLines ) )
elif args.dumpDB:
    import pprint
    pprint.pprint( sorted( cache.keys() ) )
