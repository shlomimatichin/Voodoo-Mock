import voodoodefs

class VoodooChain:
    def __init__( self, identifier, fullIdentifier, growCode, cache ):
        self._identifier = identifier
        self._fullIdentifier = fullIdentifier
        self._code = growCode
        self._identifierToSnippets = cache
        if self._identifierToSnippets is None:
            self._identifierToSnippets = {}
        self._mockClass = voodoodefs.mockClass( identifier )
        self._fullMockClass = fullIdentifier[ : - len( identifier ) ] + self._mockClass
        self._voodooCalls, self._implementation = self._snippets()

    def cache( self ):
        return self._identifierToSnippets

    def isFirst( self ):
        return self._isFirst

    def overload( self, decomposition ):
        self._implementOverload( decomposition )
        self._implementVoodooCall( decomposition )
        self._implementChain( decomposition )

    def _snippets( self ):
        self._isFirst = not self._identifierToSnippets.has_key(
                                        self._fullIdentifier )
        if self._isFirst:
            self._identifierToSnippets[ self._fullIdentifier ] = \
                        self._defineChainClass()
        return self._identifierToSnippets[ self._fullIdentifier ]

    def _defineChainClass( self ):
        self._code.lineOut( "class %s" % self._mockClass )
        self._code.lineOut( "{" )
        self._code.lineOut( "public:" )
        self._code.increaseIndent()
        voodooCalls = self._code.newSnippet()
        self._code.lineOut( "" )
        self._code.decreaseIndent()
        self._code.lineOut( "protected:" )
        self._code.increaseIndent()
        implementation = self._code.newSnippet()
        self._code.lineOut( "%s()" % self._mockClass )
        self._code.lineOut( "{" )
        self._code.lineOut( "\t__voodooNext = __voodooTop();" )
        self._code.lineOut( "\tif ( __voodooNext )" )
        self._code.lineOut( "\t\t__voodooNext->__voodooPrevious = & __voodooNext;" )
        self._code.lineOut( "\t__voodooPrevious = & __voodooTop();" )
        self._code.lineOut( "\t__voodooTop() = this;" )
        self._code.lineOut( "}" )
        self._code.lineOut( "" )
        self._code.lineOut( "virtual ~%s()" % self._mockClass )
        self._code.lineOut( "{" )
        self._code.lineOut( "\t* __voodooPrevious = __voodooNext;" )
        self._code.lineOut( "\tif ( __voodooNext )" )
        self._code.lineOut( "\t\t__voodooNext->__voodooPrevious = __voodooPrevious;" )
        self._code.lineOut( "}" )
        self._code.lineOut( "" )
        self._code.decreaseIndent()
        self._code.lineOut( "private:" )
        self._code.lineOut( "\t%s * __voodooNext;" % self._mockClass )
        self._code.lineOut( "\t%s * * __voodooPrevious;" % self._mockClass )
        self._code.lineOut( "" )
        self._code.lineOut( "\tstatic %s * & __voodooTop()" % self._mockClass )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\tstatic %s * value = 0;" % self._mockClass )
        self._code.lineOut( "\t\treturn value;" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "}; // class %s" % self._mockClass )
        self._code.lineOut( "" )
        return voodooCalls, implementation

    def _implementOverload( self, decomposition ):
        self._code.lineOut( "%s%s %s( %s )" % ( decomposition.stringStaticInlineIfStatic(),
                                                decomposition.returnType,
                                                self._identifier,
                                                decomposition.parametersFullSpec() ) )
        self._code.lineOut( "{" )
        self._code.lineOut( "\t%s%s::%s( %s );" % (
                                    decomposition.stringReturnIfNotVoid(),
                                    self._mockClass,
                                    voodoodefs.VOODOO_CALL,
                                    decomposition.parametersForwardingList() ) )
        self._code.lineOut( "}" )
        self._code.lineOut( "" )

    def _implementVoodooCall( self, decomposition ):
        self._code.lineOut( "static %s %s( %s )" % (
                                    decomposition.returnType,
                                    voodoodefs.VOODOO_CALL,
                                    decomposition.parametersFullSpec() ),
                            self._voodooCalls )
        self._code.lineOut( "{", self._voodooCalls )
        self._code.lineOut( "\tif ( ! __voodooTop() ) {", self._voodooCalls )
        self._code.lineOut( '\t\tVOODOO_FAIL_TEST( "No implementation "', self._voodooCalls )
        self._code.lineOut( '\t\t\t"for chain (or static method) "', self._voodooCalls )
        self._code.lineOut( '\t\t\t"\'%s\', "' % self._fullIdentifier, self._voodooCalls )
        self._code.lineOut( '\t\t\t"Because no object of class "', self._voodooCalls )
        self._code.lineOut( '\t\t\t"\'%s\' "' % self._fullMockClass, self._voodooCalls )
        self._code.lineOut( '\t\t\t"exists!" );', self._voodooCalls )
        if decomposition.returnTypeIsVoid():
            self._code.lineOut( "\t\treturn;", self._voodooCalls )
        else:
            self._code.lineOut( '\t\tVOODOO_FAIL_TEST(', self._voodooCalls )
            self._code.lineOut( '\t\t\t"VOODOO_FAIL_TEST did not "', self._voodooCalls )
            self._code.lineOut( '\t\t\t"throw, and chain (or static "', self._voodooCalls )
            self._code.lineOut( '\t\t\t"member) "', self._voodooCalls )
            self._code.lineOut( '\t\t\t"\'%s\', "' % self._fullIdentifier, self._voodooCalls )
            self._code.lineOut( '\t\t\t"implemented by redirector class "', self._voodooCalls )
            self._code.lineOut( '\t\t\t"\'%s\' "' % self._fullMockClass, self._voodooCalls )
            self._code.lineOut( '\t\t\t"must return a value: "', self._voodooCalls )
            self._code.lineOut( '\t\t\t"your test suite will "', self._voodooCalls )
            self._code.lineOut( '\t\t\t"segfault now..." );', self._voodooCalls )
        self._code.lineOut( "\t}", self._voodooCalls )
        self._code.lineOut( "\t%s__voodooTop()->%s( %s );" % (
                                    decomposition.stringReturnIfNotVoid(),
                                    self._identifier,
                                    decomposition.parametersForwardingList() ),
                            self._voodooCalls )
        self._code.lineOut( "}", self._voodooCalls )
        self._code.lineOut( "", self._voodooCalls )

    def _implementChain( self, decomposition ):
        self._code.lineOut( "virtual %s %s( %s )" % (
                                                decomposition.returnType,
                                                self._identifier,
                                                decomposition.parametersFullSpec() ),
                            self._implementation )
        self._code.lineOut( "{", self._implementation )
        self._code.lineOut( '\tif ( ! __voodooNext ) {', self._implementation )
        self._code.lineOut( '\t\tVOODOO_FAIL_TEST( ', self._implementation )
        self._code.lineOut( '\t\t\t"No implementation for chain "', self._implementation )
        self._code.lineOut( '\t\t\t"(or static method) "', self._implementation )
        self._code.lineOut( '\t\t\t"\'%s\', "' % self._fullIdentifier , self._implementation )
        self._code.lineOut( '\t\t\t"Because non of the existing "', self._implementation )
        self._code.lineOut( '\t\t\t"objects of class "', self._implementation )
        self._code.lineOut( '\t\t\t"\'%s\' "' % self._fullMockClass, self._implementation )
        self._code.lineOut( '\t\t\t"implement it!" );', self._implementation )
        if decomposition.returnTypeIsVoid():
            self._code.lineOut( "\t\treturn;", self._implementation );
        else:
            self._code.lineOut( "\t\tVOODOO_FAIL_TEST( ", self._implementation )
            self._code.lineOut( '\t\t\t"VOODOO_FAIL_TEST did "', self._implementation )
            self._code.lineOut( '\t\t\t"not throw, and chain "', self._implementation )
            self._code.lineOut( '\t\t\t"(or static method) "', self._implementation )
            self._code.lineOut( '\t\t\t"\'%s\', "' % self._fullIdentifier,
                                self._implementation )
            self._code.lineOut( '\t\t\t"implemented by "', self._implementation )
            self._code.lineOut( '\t\t\t"redirector class "', self._implementation )
            self._code.lineOut( '\t\t\t"\'%s\' "' % self._fullMockClass, self._implementation )
            self._code.lineOut( '\t\t\t"must return a value: "', self._implementation )
            self._code.lineOut( '\t\t\t"your test suite will "', self._implementation )
            self._code.lineOut( '\t\t\t"segfault now..." );', self._implementation )
        self._code.lineOut( "\t}", self._implementation )
        self._code.lineOut( "\t%s__voodooNext->%s( %s );" % (
                                                decomposition.stringReturnIfNotVoid(),
                                                self._identifier,
                                                decomposition.parametersForwardingList() ),
                            self._implementation )
        self._code.lineOut( "}", self._implementation )
        self._code.lineOut( "", self._implementation )
