import unittest
import parsecpp
import parsecppmemberlist
import parsecppfunctionsignature
import parsesimplecall
import tokenize
import formatcolums

class FakeParse:
    pass

class FakeArgs:
    asterixInFirstColum = False
    indentWithTabs = True
    alwaysNewLineForFirstParameter = False
    noSpaceBeforeClosingParenthesis = False
    tabSize = 4
    minimumSpaceBetweenColumns = 2
    optimizeForMaximumLineLength = 80

class Test( unittest.TestCase ):
    def test_trivialSplit( self ):
        tested = parsecpp.VariableDeclaration( 'int a' )
        self.assertEquals( tested.colums()[ 0 ], 'int' )
        self.assertEquals( tested.colums()[ 1 ], 'a' )

    def test_array( self ):
        tested = parsecpp.VariableDeclaration( 'int a[ kuki ]' )
        self.assertEquals( tested.colums()[ 0 ], 'int' )
        self.assertEquals( tested.colums()[ 1 ], 'a[ kuki ]' )

    def test_default( self ):
        tested = parsecpp.VariableDeclaration( 'int a = 3' )
        self.assertEquals( tested.colums()[ 0 ], 'int' )
        self.assertEquals( tested.colums()[ 1 ], 'a = 3' )

    def test_pointer( self ):
        tested = parsecpp.VariableDeclaration( 'int * a' )
        self.assertEquals( tested.colums()[ 0 ], 'int *' )
        self.assertEquals( tested.colums()[ 1 ], 'a' )

    def test_reference( self ):
        tested = parsecpp.VariableDeclaration( 'int & a' )
        self.assertEquals( tested.colums()[ 0 ], 'int &' )
        self.assertEquals( tested.colums()[ 1 ], 'a' )

    def test_pointerKernelStyle( self ):
        tested = parsecpp.VariableDeclaration( 'int * a', asterixInFirstColum = False )
        self.assertEquals( tested.colums()[ 0 ], 'int' )
        self.assertEquals( tested.colums()[ 1 ], '* a' )

    def test_memberList( self ):
        tested = parsecppmemberlist.ParseCPPMemberList( '  int a;\nint b;\nint c;\n' )
        self.assertEquals( tested.lead(), '  ' )
        self.assertEquals( tested.rows(), [ ( 'int', 'a;' ), ( 'int', 'b;' ), ( 'int', 'c;' ) ] )
        self.assertEquals( tested.tail(), '' )

    def test_parenthesis( self ):
        tested = tokenize.Tokenize( 'void func();' )
        self.assertEquals( tested.splitByParenthesis()[ 0 ], 'void func(' )
        self.assertEquals( tested.splitByParenthesis()[ 1 ], '' )
        self.assertEquals( tested.splitByParenthesis()[ 2 ], ');' )

    def test_parenthesisComplicated( self ):
        tested = tokenize.Tokenize( 'void func( int a[], std::function< void () > drek ) override' )
        self.assertEquals( tested.splitByParenthesis()[ 0 ], 'void func(' )
        self.assertEquals( tested.splitByParenthesis()[ 1 ], 'int a[], std::function< void () > drek' )
        self.assertEquals( tested.splitByParenthesis()[ 2 ], ') override' )

    def test_splitByCommasWithZeroLevelParenthesis( self ):
        tested = tokenize.Tokenize( 'int a[], std::function< void () > drek' )
        self.assertEquals( tested.splitByZeroParenLevel()[ 0 ], 'int a[]' )
        self.assertEquals( tested.splitByZeroParenLevel()[ 1 ], 'std::function< void () > drek' )

    def test_splitByCommasWithZeroLevelParenthesis_Complicated( self ):
        tested = tokenize.Tokenize( 'int a[,], std::function< , void ( , ) > drek' )
        self.assertEquals( tested.splitByZeroParenLevel()[ 0 ], 'int a[,]' )
        self.assertEquals( tested.splitByZeroParenLevel()[ 1 ], 'std::function< , void ( , ) > drek' )

    def test_parseFunctionDeclaration( self ):
        tested = parsecppfunctionsignature.ParseCPPFunctionSignature(
                'void func( int a[], std::function< void () > drek ) override' )
        self.assertEquals( tested.lead(), 'void func(' )
        self.assertEquals( tested.tail(), ') override' )
        self.assertEquals( tested.rows()[ 0 ], ( 'int', 'a[],' ) )
        self.assertEquals( tested.rows()[ 1 ], ( 'std::function< void () >', 'drek' ) )

    def test_parseFunctionCall( self ):
        tested = parsesimplecall.ParseSimpleCall( 'a = b( c, d, & e, (cast) & d );' )
        self.assertEquals( tested.lead(), 'a = b(' )
        self.assertEquals( tested.tail(), ');' )
        self.assertEquals( tested.rows()[ 0 ], ( 'c,', ) )
        self.assertEquals( tested.rows()[ 1 ], ( 'd,', ) )
        self.assertEquals( tested.rows()[ 2 ], ( '& e,', ) )
        self.assertEquals( tested.rows()[ 3 ], ( '(cast) & d', ) )

    def test_parsePythonFunction( self ):
        tested = parsesimplecall.ParseSimpleCall( '    def __init__( a, b, c = 3 ):' )
        self.assertEquals( tested.lead(), '    def __init__(' )
        self.assertEquals( tested.tail(), '):' )
        self.assertEquals( tested.rows()[ 0 ], ( 'a,', ) )
        self.assertEquals( tested.rows()[ 1 ], ( 'b,', ) )
        self.assertEquals( tested.rows()[ 2 ], ( 'c = 3', ) )

    def test_formatSimple( self ):
        parse = FakeParse()
        parse.lead = lambda: "\t\tConstructor("
        parse.rows = lambda: [ ( 'int', 'a,' ), ( 'const unsigned long', 'b' ) ]
        parse.tail = lambda: "):"
        tested = formatcolums.FormatColums( parse, FakeArgs() )
        self.assertEquals( tested.format(), '\t\tConstructor(    int                  a,\n\t\t\t\t\t\tconst unsigned long  b ):' )

if __name__ == '__main__':
    unittest.main()
