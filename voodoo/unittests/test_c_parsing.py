import unittest
import savingiterator
import tempfile
import pprint
import os
import platform

class TestCParsing( unittest.TestCase ):
    def setUp( self ):
        self.maxDiff = None

    def _tempfile( self, contents ):
        #
        # From the python documentation:
        # Whether the name can be used to open the file a second time, while the
        # named temporary file is still open, varies across platforms (it can be 
        # so used on Unix; it cannot  on Windows NT or later).
        # 
        if platform.system() == "Windows":
            t = tempfile.NamedTemporaryFile( suffix = ".h", delete=False )
        else:
            t = tempfile.NamedTemporaryFile( suffix = ".h" )
        t.write( contents )
        t.flush()
        if platform.system() == "Windows":
          t.close()
        return t

    def _simpleTest( self, contents, expected ):
        tested = savingiterator.SavingIterator()
        contentsFile = self._tempfile( contents )
        tested.process( contentsFile.name )
        if tested.saved != expected:
            pprint.pprint( tested.saved )
            pprint.pprint( expected )
        self.assertEquals( tested.saved, expected )
        if platform.system() == "Windows":
          os.remove( contentsFile.name )

    def test_structDeclaration( self ):
        self._simpleTest( "struct name_of_struct;", [ dict( callbackName = "structForwardDeclaration", name = "name_of_struct" ) ] )

    def test_emptyStructDefinition( self ):
        self._simpleTest( "struct name_of_struct {};", [
            dict( callbackName = "enterStruct", name = "name_of_struct", fullTextNaked = "structname_of_struct{}", inheritance = [] ),
            dict( callbackName = "leaveStruct" ),
        ] )

    def test_globalInteger( self ):
        self._simpleTest( "int global;", [
            dict( callbackName = "variableDeclaration", name = "global", text = "int global" ),
        ] )

    def test_globalPointer( self ):
        self._simpleTest( "char * global;", [
            dict( callbackName = "variableDeclaration", name = "global", text = "char * global" ),
        ] )

    def test_globalConstPointer( self ):
        self._simpleTest( "const char * global;", [
            dict( callbackName = "variableDeclaration", name = "global", text = "const char * global" ),
        ] )

    def test_globalTypedef( self ):
        self._simpleTest( "typedef const char * stringTypedef;", [
            dict( callbackName = "typedef", name = "stringTypedef", text = "typedef const char * stringTypedef" ),
        ] )

    def test_globalVoidFunctionForwardDeclaration( self ):
        self._simpleTest( "void aFunction();", [
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "aFunction", parameters = [],
                text = "void aFunction", returnRValue = False, returnType = "void", static = False, const = False, virtual = False ),
        ] )

    def test_globalIntFunctionForwardDeclaration( self ):
        self._simpleTest( "int aFunction();", [
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "aFunction", parameters = [],
                text = "int aFunction", returnRValue = False, returnType = "int", static = False, const = False, virtual = False ),
        ] )

    def test_globalConstIntFunctionForwardDeclaration( self ):
        self._simpleTest( "const int aFunction();", [
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "aFunction", parameters = [],
                text = "const int aFunction", returnRValue = False, returnType = "const int", static = False, const = False, virtual = False ),
        ] )

    def test_globalConstCharPFunctionForwardDeclaration( self ):
        self._simpleTest( "const char * aFunction();", [
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "aFunction", parameters = [],
                text = "const char * aFunction", returnRValue = False, returnType = "const char *", static = False, const = False, virtual = False ),
        ] )

    def test_globalConstCharPConstFunctionForwardDeclaration( self ):
        self._simpleTest( "const char * const aFunction();", [
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "aFunction", parameters = [],
                text = "const char * const aFunction", returnRValue = False, returnType = "const char * const", static = False, const = False, virtual = False ),
        ] )

    def test_globalUnsignedLongLongFunctionForwardDeclaration( self ):
        self._simpleTest( "unsigned long long aFunction();", [
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "aFunction", parameters = [],
                text = "unsigned long long aFunction", returnRValue = False, returnType = "unsigned long long", static = False, const = False, virtual = False ),
        ] )

    def test_globalVoidFunctionForwardDeclarationIntParameter( self ):
        self._simpleTest( "void aFunction( int a );", [
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "aFunction",
                text = "void aFunction", returnRValue = False, returnType = "void", static = False, const = False, virtual = False, parameters = [
                    dict( name = "a", text = "int a", isParameterPack = False ) ] ),
        ] )

    def test_globalVoidFunctionForwardDeclarationIntConstCharPParameter( self ):
        self._simpleTest( "void aFunction( int a, const char * p );", [
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "aFunction",
                text = "void aFunction", returnRValue = False, returnType = "void", static = False, const = False, virtual = False, parameters = [
                dict( name = "a", text = "int a", isParameterPack = False ),
                dict( name = "p", text = "const char * p", isParameterPack = False ), ] ),
        ] )

    def test_VoidFunctionPointerDefinition( self ):
        self._simpleTest( "void (*aFunction)();", [
            dict( callbackName = "variableDeclaration", name = "aFunction", text = "void ( * aFunction ) ( )" ),
        ] )

    def test_TypedefVoidFunctionPointerDefinition( self ):
        self._simpleTest( "typedef void (*aFunction)();", [
            dict( callbackName = "typedef", name = "aFunction", text = "typedef void ( * aFunction ) ( )" ),
        ] )

    def test_Enum( self ):
        self._simpleTest( "enum EnumName { A = 1, B, C = 2 };", [
            dict( callbackName = "enum", name = "EnumName", text = "enum EnumName { A = 1 , B , C = 2 }" ),
        ] )

    def test_globalVoidFunctionDefinition( self ):
        self._simpleTest( "void aFunction() {}", [
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "aFunction", parameters = [],
                text = "void aFunction", returnRValue = False, returnType = "void", static = False, const = False, virtual = False ),
        ] )

    def test_globalVoidFunctionDefinitionWithInts( self ):
        self._simpleTest( "int aFunction( int a ) { return a; }", [
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "aFunction", text = "int aFunction",
                returnRValue = False, returnType = "int", static = False, const = False, virtual = False, parameters = [
                dict( name = "a", text = "int a", isParameterPack = False ) ] ),
        ] )

    def test_globalVoidFunctionDefinitionStatic( self ):
        self._simpleTest( "static void aFunction() {}", [
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "aFunction", parameters = [],
                text = "void aFunction", returnRValue = False, returnType = "void", static = False, const = False, virtual = False ),
        ] )

    def test_globalVoidFunctionDefinitionInline( self ):
        self._simpleTest( "inline void aFunction() {}", [
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "aFunction", parameters = [],
                text = "void aFunction", returnRValue = False, returnType = "void", static = False, const = False, virtual = False ),
        ] )

    def test_globalVoidFunctionDefinitionStaticInline( self ):
        self._simpleTest( "static inline void aFunction() {}", [
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "aFunction", parameters = [],
                text = "void aFunction", returnRValue = False, returnType = "void", static = False, const = False, virtual = False ),
        ] )

    def test_nonEmptyStructDefinition( self ):
        self._simpleTest( "struct name_of_struct { int a; const char * b; };", [
            dict( callbackName = "enterStruct", name = "name_of_struct", inheritance = [], fullTextNaked = "structname_of_struct{inta;constchar*b;}" ),
            dict( callbackName = "fieldDeclaration", name = "a", text = "int a" ),
            dict( callbackName = "fieldDeclaration", name = "b", text = "const char * b" ),
            dict( callbackName = "leaveStruct" ),
        ] )

    def test_globalVoidFunctionDefinitionWithStructPointers( self ):
        self._simpleTest( "const struct S * aFunction( const struct S * s ) { return 0; }", [
            dict( callbackName = 'structForwardDeclaration', name = 'S' ),
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "aFunction",
                text = "const struct S * aFunction", returnRValue = False, returnType = "const struct S *", static = False, const = False, virtual = False, parameters = [
                dict( name = "s", text = "const struct S * s", isParameterPack = False ) ] ),
        ] )

    def test_nonEmptyStructTypdefDefinition( self ):
        self._simpleTest( "typedef struct name_of_struct { int a; const char * b; } struct_t;", [
            dict( callbackName = "enterStruct", name = "name_of_struct", inheritance = [], fullTextNaked = "structname_of_struct{inta;constchar*b;}" ),
            dict( callbackName = "fieldDeclaration", name = "a", text = "int a" ),
            dict( callbackName = "fieldDeclaration", name = "b", text = "const char * b" ),
            dict( callbackName = "leaveStruct" ),
            dict( callbackName = "typedef", name = "struct_t", text = "typedef struct name_of_struct struct_t" )
        ] )

    def test_useTypedef( self ):
        self._simpleTest( "typedef int Int;\nInt i;", [
            dict( callbackName = "typedef", name = "Int", text = "typedef int Int" ),
            dict( callbackName = "variableDeclaration", name = "i", text = "Int i" ),
        ] )

    def _parseError( self, contents ):
        tested = savingiterator.SavingIterator()
        tested.printErrors = False
        contentsFile = self._tempfile( contents )
        try:
            tested.process( contentsFile.name )
        except:
            return
        else:
            raise Exception( "Expected parsing to fail" )

    def test_unknownType( self ):
        self._parseError( "Int i;" )

    def _testInclude( self, contents1, contents2, expected ):
        tested = savingiterator.SavingIterator()
        contentsFile1 = self._tempfile( contents1 )
        contentsFile2 = self._tempfile( '#include "%s"\n%s' % ( contentsFile1.name, contents2 ) )
        tested.process( contentsFile2.name )
        if tested.saved != expected:
            pprint.pprint( tested.saved )
            pprint.pprint( expected )
        self.assertEquals( tested.saved, expected )

    def test_includeScenario( self ):
        self._testInclude( "typedef int Int;", "Int i;", [
            dict( callbackName = "variableDeclaration", name = "i", text = "Int i" ),
        ] )

    def test_realCase( self ):
        self._simpleTest( """
struct net_device {};
struct net {};
extern struct net init_net;
extern struct net_device * dev_get_by_name(struct net *net, const char *name);
extern void dev_put(struct net_device *dev);
        """, [
            dict( callbackName = "enterStruct", name = 'net_device', inheritance = [], fullTextNaked = "structnet_device{}" ),
            dict( callbackName = "leaveStruct" ),
            dict( callbackName = "enterStruct", name = 'net', inheritance = [], fullTextNaked = "structnet{}" ),
            dict( callbackName = "leaveStruct" ),
            dict( callbackName = "variableDeclaration", name = "init_net", text = "extern struct net init_net" ),
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "dev_get_by_name", text = "struct net_device * dev_get_by_name",
                returnRValue = False, returnType = "struct net_device *", static = False, const = False, virtual = False, parameters = [
                dict( name = "net", text = "struct net * net", isParameterPack = False ),
                dict( name = "name", text = "const char * name", isParameterPack = False ) ] ),
            dict( callbackName = 'functionForwardDeclaration', name = 'dev_put',
		    parameters = [ dict( name = 'dev', text = 'struct net_device * dev', isParameterPack = False ) ],
                  returnRValue = False, returnType = 'void', static = False, templatePrefix = '', text = 'void dev_put', const = False, virtual = False )
        ] )

    def test_defines( self ):
        contents = "DEFINESTRUCT name_of_struct;"
        tested = savingiterator.SavingIterator()
        contentsFile = self._tempfile( contents )
        tested.process( contentsFile.name, defines = [ "DEFINESTRUCT=struct" ] )
        expected = [ dict( callbackName = "structForwardDeclaration", name = "name_of_struct" ) ]
        if tested.saved != expected:
            pprint.pprint( tested.saved )
            pprint.pprint( expected )
        self.assertEquals( tested.saved, expected )

    # If the purpose of this test is to validate the redefinition of size_t, it fails with
	# a 64 bits version of gcc on windows (x86_64-w64-mingw32-c++.exe) with the following error:
	#   <SourceLocation file 'c:\\cygwin\\distcc\\tmp\\tmpgykt8v.h', line 1, column 23>
	#   typedef redefinition with different types ('unsigned long' vs 'unsigned int')
	#   <clang.cindex.RangeIterator instance at 0x0212EC60>
	#   <clang.cindex.FixItIterator instance at 0x0212EC88>
	#
	# If the purpose of this test is to validate that a function can use a typedef'ed type,
	# size_t can be renamed to eliminate the collision with the system declaration.
	#
	# The second possibility is considered the right one as it is easier to address :)
	# 
    def test_BugfixTypedef1( self ):
        self._simpleTest( "typedef unsigned long a_size_t; a_size_t defunc();", [
            dict( callbackName = "typedef", name = "a_size_t", text = "typedef unsigned long a_size_t" ),
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "defunc", text = "a_size_t defunc",
                returnRValue = False, returnType = "a_size_t", static = False, parameters = [], const = False, virtual = False ),
        ] )

    def test_StaticVariableShouldNotRemainStaticToAvoidCompilationError( self ):
        self._simpleTest( "static int i;", [
            dict( callbackName = "variableDeclaration", name = "i", text = "int i" ) ] )

    def test_BugfixRecursiveBraces( self ):
        self._simpleTest( "int func() { if ( 1 ) { return 1; } else { return 0; } }", [
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "func",
                text = "int func",
                returnRValue = False, returnType = "int", static = False, parameters = [], const = False, virtual = False ),
        ] )

    def test_BugfixHashPoundParsedIntoFunctionDeclarationSyntaticUnit( self ):
        self._simpleTest( "#if 1\nint func() { return 0; }\n#endif", [
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "func",
                text = "int func",
                returnRValue = False, returnType = "int", static = False, parameters = [], const = False, virtual = False ),
        ] )

    def test_unionDeclaration( self ):
        self._simpleTest( "union a { int b; int c; };", [
            dict( callbackName = "union", name = "a", text = "union a { int b ; int c ; }" ),
        ] )

    def test_anonymousUnionMember( self ):
        self._simpleTest( "struct a { union { int b; int c; } d; };", [
            dict( callbackName = "enterStruct", name = "a", fullTextNaked = "structa{union{intb;intc;}d;}", inheritance = [] ),
            dict( callbackName = "fieldDeclaration", name = "d", text = "union { int b ; int c ; } d" ),
            dict( callbackName = "leaveStruct" ),
        ] )

    def test_justADefine( self ):
        self._simpleTest( "#define nothing nada\n", [] )
        self._simpleTest( "#define nothing\n\nnothing", [] )
        self._simpleTest( "#define nothing\n\nnothing int a;", [
            dict( callbackName = "variableDeclaration", name = "a", text = "int a" ),
        ] )
        self._simpleTest( "#define a b\n\nint a;", [
            dict( callbackName = "variableDeclaration", name = "b", text = "int a" ),
        ] )

    def notest_KnownIssue_DefiningIntBoolOrBuiltinTypes( self ):
        self._simpleTest( "#define int int\n\rbool b;\nint a;", [
            dict( callbackName = "variableDeclaration", name = "b", text = "bool b" ),
            dict( callbackName = "variableDeclaration", name = "a", text = "int a" ),
        ] )

if __name__ == '__main__':
    unittest.main()
