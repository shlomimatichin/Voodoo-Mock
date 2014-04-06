import os
import argparse
import main

def underDirectory( filename, directory ):
    return directory in filename.split( os.path.sep )

parser = argparse.ArgumentParser()
parser.add_argument( "filename" )
parser.add_argument( "cmd", choices = [ 'indent', 'indentCPPDeclaration', 'constructorReferenceArguments' ] )
parser.add_argument( "--optimizeForMaximumLineLength", default = 116, type = int )
parser.add_argument( "--minimumSpaceBetweenColumns", default = 2, type = int )

args = parser.parse_args()
if args.filename.endswith( ".py" ):
    args.asterixInFirstColum = False
    args.indentWithTabs = False
    args.alwaysNewLineForFirstParameter = False
    args.noSpaceBeforeClosingParenthesis = False
    args.tabSize = 4
elif underDirectory( args.filename, 'c' ) and not underDirectory( args.filename, 'tests' ):
    args.asterixInFirstColum = True
    args.indentWithTabs = True
    args.alwaysNewLineForFirstParameter = True
    args.noSpaceBeforeClosingParenthesis = True
    args.tabSize = 8
else:
    args.asterixInFirstColum = False
    args.indentWithTabs = True
    args.alwaysNewLineForFirstParameter = False
    args.noSpaceBeforeClosingParenthesis = False
    args.tabSize = 8
main.main( args )
