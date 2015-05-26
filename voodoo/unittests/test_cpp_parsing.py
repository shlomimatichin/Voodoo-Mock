import unittest
import savingiterator
import tools
import pprint
import subprocess
import os

class TestCPPParsing( unittest.TestCase ):
    def setUp( self ):
        self.maxDiff = None

    def _simpleTest( self, contents, expected ):
        tested = savingiterator.SavingIterator()
        with tools.temporaryFile( contents ) as contentsFile:
            tested.process( contentsFile )
        if tested.saved != expected:
            pprint.pprint( tested.saved )
            pprint.pprint( expected )
        self.assertEquals( tested.saved, expected )

    def _testWithHeaders( self, headersContents, contents, expected ):
        tested = savingiterator.SavingIterator()
        with tools.temporaryFile( headersContents ) as headersContentsFile:
            fullContents = ( '#include "%s"\n' % headersContentsFile ) + contents
            with tools.temporaryFile( fullContents ) as contentsFile:
                tested.process( contentsFile )
        if tested.saved != expected:
            pprint.pprint( tested.saved )
            pprint.pprint( expected )
        self.assertEquals( tested.saved, expected )

    def test_classDeclaration( self ):
        self._simpleTest( "class SuperDuper { int y; public: int x; private: int z; };", [
            dict( callbackName = "enterClass", name = "SuperDuper", inheritance = [],
                templatePrefix = "", templateParametersList = None, fullTextNaked = "classSuperDuper{inty;public:intx;private:intz;}" ),
            dict( callbackName = "fieldDeclaration", name = "y", text = "int y" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "fieldDeclaration", name = "x", text = "int x" ),
            dict( callbackName = "accessSpec", access = "private" ),
            dict( callbackName = "fieldDeclaration", name = "z", text = "int z" ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_namespace( self ):
        self._simpleTest( "namespace A { namespace B { int b; } namespace C { int c; } int a; }", [
            dict( callbackName = "enterNamespace", name = "A" ),
            dict( callbackName = "enterNamespace", name = "B" ),
            dict( callbackName = "variableDeclaration", name = "b", text = "int b" ),
            dict( callbackName = "leaveNamespace" ),
            dict( callbackName = "enterNamespace", name = "C" ),
            dict( callbackName = "variableDeclaration", name = "c", text = "int c" ),
            dict( callbackName = "leaveNamespace" ),
            dict( callbackName = "variableDeclaration", name = "a", text = "int a" ),
            dict( callbackName = "leaveNamespace" ),
        ] )

    def test_namespaceAlias( self ):
        self._simpleTest( "namespace A { namespace B { int b; } namespace C { int c; } int a; } namespace D = A::B;", [
            dict( callbackName = "enterNamespace", name = "A" ),
            dict( callbackName = "enterNamespace", name = "B" ),
            dict( callbackName = "variableDeclaration", name = "b", text = "int b" ),
            dict( callbackName = "leaveNamespace" ),
            dict( callbackName = "enterNamespace", name = "C" ),
            dict( callbackName = "variableDeclaration", name = "c", text = "int c" ),
            dict( callbackName = "leaveNamespace" ),
            dict( callbackName = "variableDeclaration", name = "a", text = "int a" ),
            dict( callbackName = "leaveNamespace" ),
        dict( callbackName = "using", text = "namespace D = A :: B" ),
        ] )

    def test_constructor( self ):
        self._simpleTest( "class SuperDuper { public: \nSuperDuper( int a, const char * b ) {}\n int c; };", [
            dict( callbackName = "enterClass", name = "SuperDuper", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classSuperDuper{public:SuperDuper(inta,constchar*b){}intc;}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "constructorDefinition", templatePrefix = "", name = "SuperDuper", text = "SuperDuper",
                returnRValue = False, returnType = None, static = None, virtual = False, const = False, parameters = [
                dict( name = "a", text = "int a", isParameterPack = False ),
                dict( name = "b", text = "const char * b", isParameterPack = False ), ] ),
            dict( callbackName = "fieldDeclaration", name = "c", text = "int c" ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_variadicConstructor( self ):
        self._simpleTest( "class SuperDuper { public: \ntemplate< typename T, typename... ARGS >\nSuperDuper( T a, ARGS... b ) {}\n int c; };", [
            dict( callbackName = "enterClass", name = "SuperDuper", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classSuperDuper{public:template<typenameT,typename...ARGS>SuperDuper(Ta,ARGS...b){}intc;}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "constructorDefinition", templatePrefix = "template < typename T , typename ... ARGS >", name = "SuperDuper", text = "SuperDuper",
                returnRValue = False, returnType = None, static = None, virtual = False, const = False, parameters = [
                dict( name = "a", text = "T a", isParameterPack = False ),
                dict( name = "b", text = "ARGS ... b", isParameterPack = True ), ] ),
            dict( callbackName = "fieldDeclaration", name = "c", text = "int c" ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_templateConstructor( self ):
        self._simpleTest( "class SuperDuper { public: \ntemplate< typename T >\nSuperDuper( T a, const char * b ) {}\n int c; };", [
            dict( callbackName = "enterClass", name = "SuperDuper", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classSuperDuper{public:template<typenameT>SuperDuper(Ta,constchar*b){}intc;}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "constructorDefinition", templatePrefix = "template < typename T >", name = "SuperDuper", text = "SuperDuper",
                returnRValue = False, returnType = None, static = None, virtual = False, const = False, parameters = [
                dict( name = "a", text = "T a", isParameterPack = False ),
                dict( name = "b", text = "const char * b", isParameterPack = False ), ] ),
            dict( callbackName = "fieldDeclaration", name = "c", text = "int c" ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_inheritance( self ):
        self._simpleTest( "class Yuvu {}; class Mushu {}; class Udu {}; class SuperDuper : Yuvu, public Mushu, protected Udu {};", [
            dict( callbackName = "enterClass", name = "Yuvu", inheritance = [],
                templatePrefix = "", templateParametersList = None, fullTextNaked = "classYuvu{}" ),
            dict( callbackName = "leaveClass" ),
            dict( callbackName = "enterClass", name = "Mushu", inheritance = [],
                templatePrefix = "", templateParametersList = None, fullTextNaked = "classMushu{}" ),
            dict( callbackName = "leaveClass" ),
            dict( callbackName = "enterClass", name = "Udu", inheritance = [],
                templatePrefix = "", templateParametersList = None, fullTextNaked = "classUdu{}" ),
            dict( callbackName = "leaveClass" ),
            dict( callbackName = "enterClass", name = "SuperDuper",
                inheritance = [ ( 'public', 'Mushu' ), ( 'protected', 'Udu' ) ],
                templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classSuperDuper:Yuvu,publicMushu,protectedUdu{}" ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_methodDefinition( self ):
        self._simpleTest( "class SuperDuper { public: \nint aFunction( int a ) { return 0; }\n int c; };", [
            dict( callbackName = "enterClass", name = "SuperDuper", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classSuperDuper{public:intaFunction(inta){return0;}intc;}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "method", templatePrefix = "", name = "aFunction", text = "aFunction",
                returnRValue = False, returnType = "int", static = False, virtual = False, const = False, parameters = [
                dict( name = "a", text = "int a", isParameterPack = False ) ] ),
            dict( callbackName = "fieldDeclaration", name = "c", text = "int c" ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_methodDeclaration( self ):
        self._simpleTest( "class SuperDuper { public: \nint aFunction( int a );\n int c; };", [
            dict( callbackName = "enterClass", name = "SuperDuper", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classSuperDuper{public:intaFunction(inta);intc;}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "method", templatePrefix = "", name = "aFunction", text = "aFunction",
                returnRValue = False, returnType = "int", static = False, virtual = False, const = False, parameters = [
                dict( name = "a", text = "int a", isParameterPack = False ) ] ),
            dict( callbackName = "fieldDeclaration", name = "c", text = "int c" ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_staticmethod( self ):
        self._simpleTest( "class SuperDuper { public: \nstatic int aFunction( int a );\n int c; };", [
            dict( callbackName = "enterClass", name = "SuperDuper", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classSuperDuper{public:staticintaFunction(inta);intc;}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "method", templatePrefix = "", name = "aFunction", text = "aFunction",
                returnRValue = False, returnType = "int", static = True, virtual = False, const = False, parameters = [
                dict( name = "a", text = "int a", isParameterPack = False ) ] ),
            dict( callbackName = "fieldDeclaration", name = "c", text = "int c" ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_constMethodDeclaration( self ):
        self._simpleTest( "class SuperDuper { public: \nint aFunction( int a ) const;\n int c; };", [
            dict( callbackName = "enterClass", name = "SuperDuper", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classSuperDuper{public:intaFunction(inta)const;intc;}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "method", templatePrefix = "", name = "aFunction", text = "aFunction",
                returnRValue = False, returnType = "int", static = False, virtual = False, const = True, parameters = [
                dict( name = "a", text = "int a", isParameterPack = False ) ] ),
            dict( callbackName = "fieldDeclaration", name = "c", text = "int c" ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_functionReturningStdString( self ):
        self._simpleTest( "#include <string>\nstd::string theString();", [
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "theString", text = "std :: string theString",
                returnRValue = True, returnType = "std :: string", static = False, virtual = False, const = False, parameters = [] ),
        ] )

    def test_ClassInheritance( self ):
        self._simpleTest( "class AInterface {};\nclass B : public AInterface {};", [
            dict( callbackName = "enterClass", name = "AInterface", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classAInterface{}" ),
            dict( callbackName = "leaveClass" ),
            dict( callbackName = "enterClass", name = "B", inheritance = [ ( 'public', 'AInterface' ) ],
                templatePrefix = "", templateParametersList = None, fullTextNaked = "classB:publicAInterface{}" ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_ClassPrivateInheritance( self ):
        self._simpleTest( "class AInterface {};\nclass B : private AInterface {};", [
            dict( callbackName = "enterClass", name = "AInterface", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classAInterface{}" ),
            dict( callbackName = "leaveClass" ),
            dict( callbackName = "enterClass", name = "B", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classB:privateAInterface{}" ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_LValueReference( self ):
        self._simpleTest( "class Result {};\nResult globalResult;\nResult & getResult() { return globalResult; }", [
            dict( callbackName = "enterClass", name = "Result", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classResult{}" ),
            dict( callbackName = "leaveClass" ),
            dict( callbackName = "variableDeclaration", name = "globalResult", text = "Result globalResult" ),
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "getResult", text = "Result & getResult",
                returnRValue = False, returnType = "Result &", static = False, virtual = False, const = False, parameters = [] ),
        ] )

    def test_ConstLValueReference( self ):
        self._simpleTest( "class Result {};\nResult globalResult;\nconst Result & getResult() { return globalResult; }", [
            dict( callbackName = "enterClass", name = "Result", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classResult{}" ),
            dict( callbackName = "leaveClass" ),
            dict( callbackName = "variableDeclaration", name = "globalResult", text = "Result globalResult" ),
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "getResult", text = "const Result & getResult",
                returnRValue = False, returnType = "const Result &", static = False, virtual = False, const = False, parameters = [] ),
        ] )

    def test_ReturningPointer( self ):
        self._simpleTest( "class Result {};\nResult globalResult;\nResult * getResult() { return & globalResult; }", [
            dict( callbackName = "enterClass", name = "Result", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classResult{}" ),
            dict( callbackName = "leaveClass" ),
            dict( callbackName = "variableDeclaration", name = "globalResult", text = "Result globalResult" ),
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "getResult", text = "Result * getResult",
                returnRValue = False, returnType = "Result *", static = False, virtual = False, const = False, parameters = [] ),
        ] )

    def test_ReturnTypeIsSharedPtr( self ):
        self._testWithHeaders( "template < typename T > class sharedptr {};", "sharedptr< int > func();", [
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "func", text = "sharedptr < int > func",
                returnRValue = True, returnType = "sharedptr < int >", static = False, virtual = False, const = False, parameters = [] ),
        ] )

    def test_ReturnTypeIsSharedPtr_FunctionDefinition( self ):
        self._testWithHeaders( "template < typename T > class sharedptr {};",
                                "sharedptr< int > func() { return sharedptr< int >(); }", [
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "func", text = "sharedptr < int > func",
                returnRValue = True, returnType = "sharedptr < int >", static = False, virtual = False, const = False, parameters = [] ),
        ] )

    def test_ReturnTypeIsSharedPtr_Method( self ):
        self._testWithHeaders( "template < typename T > class sharedptr {};",
                "class A { public: sharedptr< int > func() { return sharedptr< int >(); } };", [
            dict( callbackName = "enterClass", name = "A", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classA{public:sharedptr<int>func(){returnsharedptr<int>();}}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "method", templatePrefix = "", name = "func", text = "func",
                returnRValue = True, returnType = "sharedptr < int >", static = False, virtual = False, const = False, parameters = [] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_ReturnTypeIsSharedPtr_Method_Bugfix( self ):
        self._testWithHeaders( "template < typename T > class sharedptr {};",
                "class A { public: const sharedptr< int > func() const { return sharedptr< int >(); } };", [
            dict( callbackName = "enterClass", name = "A", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classA{public:constsharedptr<int>func()const{returnsharedptr<int>();}}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "method", templatePrefix = "", name = "func", text = "func",
                returnRValue = True, returnType = "const sharedptr < int >", static = False, virtual = False, const = True, parameters = [] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_ReturnTypeIsSharedPtr_Method_BugfixOperatorSpace( self ):
        self._simpleTest( "class A { public: bool operator==( int other ) { return true; } };", [
            dict( callbackName = "enterClass", name = "A", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classA{public:booloperator==(intother){returntrue;}}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "method", templatePrefix = "", name = "operator==", text = "operator==",
                returnRValue = False, returnType = "bool", static = False, virtual = False, const = False, parameters = [
                    dict( name = "other", text = "int other", isParameterPack = False ) ] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_MethodDeclerationBeforeDtor_Bugfix( self ):
        self._simpleTest( "class File { public: File & operator=( File && rhs ); ~File(); };", [
            dict( callbackName = "enterClass", name = "File", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classFile{public:File&operator=(File&&rhs);~File();}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "method", templatePrefix = "", name = "operator=", text = "operator=",
                returnRValue = False, returnType = "File &", static = False, virtual = False, const = False, parameters = [
                    dict( name = "rhs", text = "File && rhs", isParameterPack = False ) ] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_MethodDefinitionBeforeDtor_Bugfix( self ):
        self._simpleTest( "class File { public: File & operator=( File && rhs ) { return *this; } ~File() {} };", [
            dict( callbackName = "enterClass", name = "File", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classFile{public:File&operator=(File&&rhs){return*this;}~File(){}}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "method", templatePrefix = "", name = "operator=", text = "operator=",
                returnRValue = False, returnType = "File &", static = False, virtual = False, const = False, parameters = [
                    dict( name = "rhs", text = "File && rhs", isParameterPack = False ) ] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_Bugfix_ExplicilyRemoveCommentTokens( self ):
        self._simpleTest( "void /*hello*/ func() /* bye */ {}", [
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "func", text = "void func",
                returnRValue = False, returnType = "void", static = False, virtual = False, const = False, parameters = [] ),
        ] )

    def test_Bugfix_TrailingStaticKeywordInFunctionDefinition( self ):
        self._simpleTest( "void func() {} static void func2() {}", [
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "func", text = "void func",
                returnRValue = False, returnType = "void", static = False, virtual = False, const = False, parameters = [] ),
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "func2", text = "void func2",
                returnRValue = False, returnType = "void", static = False, virtual = False, const = False, parameters = [] ),
        ] )

    def test_Bugfix_PureVirtualNotParsedCorrectly( self ):
        self._simpleTest( "class SuperDuper { virtual void aFunction() = 0;};", [
            dict( callbackName = "enterClass", name = "SuperDuper", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classSuperDuper{virtualvoidaFunction()=0;}" ),
            dict( callbackName = "method", templatePrefix = "", name = "aFunction", text = "aFunction",
                returnRValue = False, returnType = "void", static = False, virtual = True, const = False, parameters = [] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_Bugfix_PureVirtualConstMethodDefinition( self ):
        self._simpleTest( "class SuperDuper { virtual void aFunction() const = 0;};", [
            dict( callbackName = "enterClass", name = "SuperDuper", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classSuperDuper{virtualvoidaFunction()const=0;}" ),
            dict( callbackName = "method", templatePrefix = "", name = "aFunction", text = "aFunction",
                returnRValue = False, returnType = "void", static = False, virtual = True, const = True, parameters = [] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_ClassInheritanceOverrideConstMethod( self ):
        self._simpleTest( "class AInterface { virtual int f() const = 0; static int a;};\nclass B : public AInterface { int f() const override { return 0; }};", [
            dict( callbackName = "enterClass", name = "AInterface", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classAInterface{virtualintf()const=0;staticinta;}" ),
            dict( callbackName = "method", templatePrefix = "", name = "f", text = "f",
                returnRValue = False, returnType = "int", static = False, virtual = True, const = True, parameters = [] ),
            dict( callbackName = "variableDeclaration", name = "a", text = "int a" ),
            dict( callbackName = "leaveClass" ),
            dict( callbackName = "enterClass", name = "B", inheritance = [ ( 'public', 'AInterface' ) ],
                templatePrefix = "", templateParametersList = None, fullTextNaked = "classB:publicAInterface{intf()constoverride{return0;}}" ),
            dict( callbackName = "method", templatePrefix = "", name = "f", text = "f",
                returnRValue = False, returnType = "int", static = False, virtual = False, const = True, parameters = [] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_NoExcept( self ):
        self._simpleTest( "int f() noexcept { return 0; } int g() noexcept;"
                "class A { public: A() noexcept; ~A() noexcept; void method() noexcept;};", [
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "f", text = "int f",
                returnRValue = False, returnType = "int", static = False, virtual = False, const = False, parameters = [] ),
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "g", text = "int g",
                returnRValue = False, returnType = "int", static = False, virtual = False, const = False, parameters = [] ),
            dict( callbackName = "enterClass", name = "A", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classA{public:A()noexcept;~A()noexcept;voidmethod()noexcept;}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "constructorDefinition", templatePrefix = "", name = "A", text = "A",
                returnRValue = False, returnType = None, static = None, virtual = False, const = False, parameters = [] ),
            dict( callbackName = "method", templatePrefix = "", name = "method", text = "method",
                returnRValue = False, returnType = "void", static = False, virtual = False, const = False, parameters = [] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_ExternC( self ):
        self._simpleTest( 'extern "C" { int a; }\nextern "C" void f();', [
            dict( callbackName = "variableDeclaration", name = "a", text = "int a" ),
            dict( callbackName = "functionForwardDeclaration", templatePrefix = "", name = "f", text = "void f",
                returnRValue = False, returnType = "void", static = False, virtual = False, const = False, parameters = [] ),
        ] )

    def test_ExplicitConversionOperator( self ):
        self._simpleTest( 'class A { public: explicit operator int () { return 0; } };', [
            dict( callbackName = "enterClass", name = "A", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classA{public:explicitoperatorint(){return0;}}" ),
            dict( callbackName = "accessSpec", access = "public" ),
            dict( callbackName = "conversionFunction", conversionType = "int", const = False ),
            dict( callbackName = "leaveClass" ),
        ] )

#    def test_CodeInMacro( self ):
#        self._simpleTest( "#define X class SuperDuper { public: int aFunction( int a ) { return 0; } int c; }\nint c; X;", [
#            dict( callbackName = "variableDeclaration", name = "c", text = "int c" ),
#            dict( callbackName = "enterClass", name = "SuperDuper", inheritance = [], templatePrefix = "", templateParametersList = None,
#                fullTextNaked = "classSuperDuper{public:intaFunction(inta){return0;}intc;}" ),
#            dict( callbackName = "accessSpec", access = "public" ),
#            dict( callbackName = "method", templatePrefix = "", name = "aFunction", text = "aFunction",
#                returnRValue = False, returnType = "int", static = False, virtual = False, const = False, parameters = [
#                dict( name = "a", text = "int a" ) ] ),
#            dict( callbackName = "fieldDeclaration", name = "c", text = "int c" ),
#            dict( callbackName = "leaveClass" ),
#        ] )

    def test_usingNamespace( self ):
        self._simpleTest( "namespace A {} using namespace A;", [
            dict( callbackName = "enterNamespace", name = "A" ),
            dict( callbackName = "leaveNamespace" ),
            dict( callbackName = "using", text = "using namespace A" )
        ] )

    def test_templateMethod( self ):
        self._simpleTest( "class A {template < typename T > int aFunction( T a ) { return 0; }};", [
            dict( callbackName = "enterClass", name = "A", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classA{template<typenameT>intaFunction(Ta){return0;}}" ),
            dict( callbackName = "method", templatePrefix = "template < typename T >", name = "aFunction",
                text = "aFunction", returnRValue = False, returnType = "int", static = False, virtual = False, const = False,
                parameters = [ dict( name = "a", text = "T a", isParameterPack = False ) ] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_variadicTemplateMethod( self ):
        self._simpleTest( "class A {template < typename... ARGS > int aFunction( ARGS... a ) { return 0; }};", [
            dict( callbackName = "enterClass", name = "A", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classA{template<typename...ARGS>intaFunction(ARGS...a){return0;}}" ),
            dict( callbackName = "method", templatePrefix = "template < typename ... ARGS >", name = "aFunction",
                text = "aFunction", returnRValue = False, returnType = "int", static = False, virtual = False, const = False,
                parameters = [ dict( name = "a", text = "ARGS ... a", isParameterPack = True ) ] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_ClassInheritanceOverrideFinalMethod( self ):
        self._simpleTest( "class AInterface { virtual int f() = 0; static int a;};\nclass B : public AInterface { int f() override final { return 0; }};", [
            dict( callbackName = "enterClass", name = "AInterface", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classAInterface{virtualintf()=0;staticinta;}" ),
            dict( callbackName = "method", templatePrefix = "", name = "f", text = "f",
                returnRValue = False, returnType = "int", static = False, virtual = True, const = False, parameters = [] ),
            dict( callbackName = "variableDeclaration", name = "a", text = "int a" ),
            dict( callbackName = "leaveClass" ),
            dict( callbackName = "enterClass", name = "B", inheritance = [ ( 'public', 'AInterface' ) ],
                templatePrefix = "", templateParametersList = None, fullTextNaked = "classB:publicAInterface{intf()overridefinal{return0;}}" ),
            dict( callbackName = "method", templatePrefix = "", name = "f", text = "f",
                returnRValue = False, returnType = "int", static = False, virtual = False, const = False, parameters = [] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_usingNotANamespace( self ):
        self._simpleTest( "namespace A { int a; } namespace B { using A::a; }", [
            dict( callbackName = "enterNamespace", name = "A" ),
            dict( callbackName = "variableDeclaration", name = "a", text = "int a" ),
            dict( callbackName = "leaveNamespace" ),
            dict( callbackName = "enterNamespace", name = "B" ),
            dict( callbackName = "using", text = "using A :: a" ),
            dict( callbackName = "leaveNamespace" ),
        ] )

    def test_templateSpecializationWithEnum( self ):
        self._simpleTest( "enum class foo { ONE, TWO };template < foo T > struct A {};template <> struct A<foo::ONE> { typedef int * TheType; };", [
            dict( callbackName = "enum", name = "foo", text = "enum class foo { ONE , TWO }" ),
            dict( callbackName = "enterStruct", name = "A", inheritance = [],
                templatePrefix = "template < foo T >", templateParametersList = [ "T" ],
                fullTextNaked = "template<fooT>structA{}" ),
            dict( callbackName = "leaveStruct" ),
            dict( callbackName = "enterStruct", name = "A<foo::ONE>", inheritance = [],
                templatePrefix = "template <>", templateParametersList = [ "" ],
                fullTextNaked = "template<>structA<foo::ONE>{typedefint*TheType;}" ),
            dict( callbackName = "typedef", name = "TheType", text = "typedef int * TheType" ),
            dict( callbackName = "leaveStruct" ),
        ] )

    def test_templateSpecializationWithType( self ):
        self._simpleTest( "template < typename T > struct A {};template <> struct A<int> { typedef int * TheType; };", [
            dict( callbackName = "enterStruct", name = "A", inheritance = [],
                templatePrefix = "template < typename T >", templateParametersList = [ "T" ],
                fullTextNaked = "template<typenameT>structA{}" ),
            dict( callbackName = "leaveStruct" ),
            dict( callbackName = "enterStruct", name = "A<int>", inheritance = [],
                templatePrefix = "template <>", templateParametersList = [ "" ],
                fullTextNaked = "template<>structA<int>{typedefint*TheType;}" ),
            dict( callbackName = "typedef", name = "TheType", text = "typedef int * TheType" ),
            dict( callbackName = "leaveStruct" ),
        ] )

    def test_templateSpecializationWithIntLiteral( self ):
        self._simpleTest( "template < int T > struct A {};template <> struct A<5> { typedef int * TheType; };", [
            dict( callbackName = "enterStruct", name = "A", inheritance = [],
                templatePrefix = "template < int T >", templateParametersList = [ "T" ],
                fullTextNaked = "template<intT>structA{}" ),
            dict( callbackName = "leaveStruct" ),
            dict( callbackName = "enterStruct", name = "A<5>", inheritance = [],
                templatePrefix = "template <>", templateParametersList = [ "" ],
                fullTextNaked = "template<>structA<5>{typedefint*TheType;}" ),
            dict( callbackName = "typedef", name = "TheType", text = "typedef int * TheType" ),
            dict( callbackName = "leaveStruct" ),
        ] )

    def test_templateClass( self ):
        self._simpleTest( "template < typename T > class A { T aFunction( T a ) { return 0; }};", [
            dict( callbackName = "enterClass", name = "A", inheritance = [],
                templatePrefix = "template < typename T >", templateParametersList = [ "T" ],
                fullTextNaked = "template<typenameT>classA{TaFunction(Ta){return0;}}" ),
            dict( callbackName = "method", templatePrefix = "", name = "aFunction",
                text = "aFunction", returnRValue = False, returnType = "T", static = False, virtual = False, const = False,
                parameters = [ dict( name = "a", text = "T a", isParameterPack = False ) ] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_templateClass_Complex( self ):
        self._simpleTest( "#include <memory>\ntemplate < typename T1, class T2, unsigned long T3 > class A {};", [
            dict( callbackName = "enterClass", name = "A", inheritance = [],
                templatePrefix = "template < typename T1 , class T2 , unsigned long T3 >", templateParametersList = [ "T1", "T2", "T3" ],
                fullTextNaked = "template<typenameT1,classT2,unsignedlongT3>classA{}" ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_templateStruct( self ):
        self._simpleTest( "template < typename T > struct A { T aFunction( T a ) { return 0; }};", [
            dict( callbackName = "enterStruct", name = "A", inheritance = [],
                templatePrefix = "template < typename T >", templateParametersList = [ "T" ],
                fullTextNaked = "template<typenameT>structA{TaFunction(Ta){return0;}}" ),
            dict( callbackName = "method", templatePrefix = "", name = "aFunction",
                text = "aFunction", returnRValue = False, returnType = "T", static = False, virtual = False, const = False,
                parameters = [ dict( name = "a", text = "T a", isParameterPack = False ) ] ),
            dict( callbackName = "leaveStruct" ),
        ] )

    def test_Bugfix_FunctionsThatReturnClassesMightNeedToReturnRvalue( self ):
        self._simpleTest( "#include <memory>\n"
                    "std::unique_ptr< int > func() { \n"
                    "std::unique_ptr< int > res( new int );\n"
                "return std::move( res );}\n", [
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "func",
                text = "std :: unique_ptr < int > func",
                returnType = "std :: unique_ptr < int >", static = False, virtual = False,
                returnRValue = True,
                const = False, parameters = [] ),
        ] )

    def test_Bugfix_FunctionsThatReturnClassesMightNeedToReturnRvalue_TypedefToUniquePTR( self ):
        self._simpleTest( "#include <memory>\n"
                "typedef std::unique_ptr< int > UniqueInt;"
                "UniqueInt func() { \n"
                "UniqueInt res( new int );\n"
                "return std::move( res );}\n", [
            dict( callbackName = 'typedef', name = 'UniqueInt', text = 'typedef std :: unique_ptr < int > UniqueInt' ),
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "func",
                text = "UniqueInt func",
                returnType = "UniqueInt", static = False, virtual = False,
                returnRValue = True,
                const = False, parameters = [] ),
        ] )

    def test_Bugfix_VirtualWithCode( self ):
        self._simpleTest( "class SuperDuper { virtual int aFunction() { return 10; } };", [
            dict( callbackName = "enterClass", name = "SuperDuper", inheritance = [], templatePrefix = "", templateParametersList = None,
                fullTextNaked = "classSuperDuper{virtualintaFunction(){return10;}}" ),
            dict( callbackName = "method", templatePrefix = "", name = "aFunction",
                text = "aFunction",
                returnType = "int", static = False, virtual = True,
                returnRValue = False,
                const = False, parameters = [] ),
            dict( callbackName = "leaveClass" ),
        ] )

    def test_templateFunction( self ):
        self._simpleTest( "template< typename T > int func(); ", [
            dict( callbackName = "functionDefinition", templatePrefix = "", name = "func", text = "template < typename T > int func",
                returnRValue = False, returnType = "template < typename T > int", static = False, virtual = False, const = False, parameters = [] ),
        ] )

if __name__ == '__main__':
    unittest.main()
