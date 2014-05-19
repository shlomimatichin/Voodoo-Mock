import parsecpp
import parsecppmemberlist
import parsecppfunctionsignature
import parsesimplecall
import formatcolums
import sys
import constructorreferenceargumentscpp
import constructorreferenceargumentspy

def main( args ):
    input = sys.stdin.read().rstrip()
    if "" in input.split( "\n" ):
        sys.stdout.write( "ERROR: Empty lines are not allowed in input" )
        exit( 1 )

    if args.filename.endswith( ".py" ):
        if args.cmd == "indent":
            parse = parsesimplecall.ParseSimpleCall( input )
            print formatcolums.FormatColums( parse, args ).format()
        elif args.cmd == "indentCPPDeclaration":
            assert False, "Command 'indentCPPDeclaration' not valid for .py files"
        elif args.cmd == "constructorReferenceArguments":
            print constructorreferenceargumentspy.ConstructorReferenceArgumentsPy( input, args ).format()
        else:
            assert False
    elif args.filename.endswith( ".cpp" ) or args.filename.endswith( ".h" ) or args.filename.endswith( ".c" ):
        if args.cmd == "indent":
            classify = parsecpp.Classification( input )
            if classify.memberList():
                parse = parsecppmemberlist.ParseCPPMemberList( input )
            elif input.rstrip().endswith( ';' ):
                #guess: ends with ; is a call, not a declaration
                parse = parsesimplecall.ParseSimpleCall( input )
            else:
                parse = parsecppfunctionsignature.ParseCPPFunctionSignature( input )
            print formatcolums.FormatColums( parse, args ).format()
        elif args.cmd == "indentCPPDeclaration":
            parse = parsecppfunctionsignature.ParseCPPFunctionSignature( input )
            print formatcolums.FormatColums( parse, args ).format()
        elif args.cmd == "constructorReferenceArguments":
            print constructorreferenceargumentscpp.ConstructorReferenceArgumentsCPP( input, args ).format()
        else:
            assert False
    else:
        raise Exception( "Unfamiliar with extension of file '%s'" % args.filename )

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument( "filename" )
    parser.add_argument( "cmd", choices = [ 'indent', 'indentCPPDeclaration', 'constructorReferenceArguments' ] )
    parser.add_argument( "--asterixInFirstColum", action = "store_true" )
    parser.add_argument( "--indentWithTabs", action = "store_true", help = "otherwise use space" )
    parser.add_argument( "--optimizeForMaximumLineLength", default = 116, type = int )
    parser.add_argument( "--tabSize", default = 4, type = int )
    parser.add_argument( "--alwaysNewLineForFirstParameter", action = "store_true", help = "helps with kernel coding conventions" )
    parser.add_argument( "--minimumSpaceBetweenColumns", default = 2, type = int )
    parser.add_argument( "--noSpaceBeforeClosingParenthesis", action = "store_true" )
    args = parser.parse_args()
    main( args )

