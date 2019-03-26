import voodoodefs
import functiondecomposition

class VoodooMock:
    def __init__(   self,
                    identifier,
                    inherits,
                    construct,
                    fullIdentifier,
                    code,
                    perFileSettings,
                    templatePrefix,
                    templateParametersList ):
        self._identifier = identifier
        self._inherits = perFileSettings.filterInherits( inherits )
        self._construct = construct
        self._fullIdentifier = fullIdentifier
        self._code = code
        self._perFileSettings = perFileSettings
        self._templatePrefix = templatePrefix
        if len( templatePrefix ) > 0:
            self._templatePrefix += "\n"
        self._templateParametersList = templateParametersList
        self._mockClass = voodoodefs.mockClass( identifier )
        self._fullMockClass = fullIdentifier[ : - len( identifier ) ] + self._mockClass
        self._constructorCount = 0
        self._perFileSettings = perFileSettings

    def _isCopyConstructor( self, decomposition ):
        if len( decomposition.parameters ) != 1:
            return False
        return decomposition.parametersFullSpec() == \
                    "const %s & %s" % ( self._identifier, decomposition.parameters[ 0 ][ 'name' ] )

    def _isMoveSemantics( self, decomposition ):
        if len( decomposition.parameters ) != 1:
            return False
        return decomposition.parametersFullSpec() == \
                    "%s && %s" % ( self._identifier, decomposition.parameters[ 0 ][ 'name' ] )

    def _mockInherits( self ):
        return [ i for i in self._inherits if i not in
                                self._perFileSettings.NO_MOCK_DERIVE_AND_USE_DEFAULT_CONSTRUCTOR ]

    def implementConstructor( self, decomposition ):
        if ( self._isCopyConstructor( decomposition ) or self._isMoveSemantics( decomposition ) ):
            return
        self._constructorCount += 1
        inherits = ""
        construct = "( __VoodooRedirectorConstruction() )"
        if len( self._mockInherits() ) > 0:
            inherits = " :\n\t\t" + ( construct + ",\n\t\t" ).join( self._mockInherits() ) + \
                        construct
        self._code.lineOut( "%s( %s )%s" % (    self._identifier,
                                                decomposition.parametersFullSpec(),
                                                inherits ) )
        self._code.lineOut( "{" )
        self._code.lineOut( "\t__voodooMockName = 0;" )
        self._code.lineOut( "\t__voodooNext = 0;" )
        self._code.lineOut( "\t__voodooPrevious = 0;" )
        self._code.lineOut( "\t__voodooRedirectee = 0;" )
        self._code.lineOut( "\tfor ( %s * i = __voodooTop() ;" % self._identifier )
        self._code.lineOut( "\t   i ;" )
        self._code.lineOut( "\t   i = i->__voodooNext ) {" )
        self._code.lineOut( "\t\ti->__voodooLastRedirector = this;" );
        self._code.lineOut( "\t\tif( i->%s_Constructor( %s ) ) {" %
                                (   self._identifier,
                                    decomposition.parametersForwardingList() ) )
        self._code.lineOut( "\t\t\t__voodooSetRedirectee( i );" )
        self._code.lineOut( "\t\t\treturn;" )
        self._code.lineOut( "\t\t}" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "\tif ( __voodooTop() ) {" )
        self._code.lineOut( '\t\tVOODOO_FAIL_TEST( "Can not construct object of type "' )
        self._code.lineOut( '\t\t\t"\'%s\', "' % self._fullIdentifier )
        self._code.lineOut( '\t\t\t"No mock object of type "' )
        self._code.lineOut( '\t\t\t"\'%s\' "' % self._fullMockClass )
        self._code.lineOut( '\t\t\t"accepted construction!" );' )
        self._code.lineOut( "\t} else {" )
        self._code.lineOut( '\t\tVOODOO_FAIL_TEST( "Can not construct object of type "' )
        self._code.lineOut( '\t\t\t"\'%s\', "' % self._fullIdentifier )
        self._code.lineOut( '\t\t\t"No mock object of type "' )
        self._code.lineOut( '\t\t\t"\'%s\' "' % self._fullMockClass )
        self._code.lineOut( '\t\t\t"exists!" );' )
        self._code.lineOut( "\t}" )
        self._code.lineOut( '\tVOODOO_FAIL_TEST( "VOODOO_FAIL_TEST did not throw "' )
        self._code.lineOut( '\t\t"and mock constructor for class \'%s\'"' % self._identifier )
        self._code.lineOut( '\t\t"must select a redirectee! your test suite "' )
        self._code.lineOut( '\t\t"will segfault now..." );' )
        self._code.lineOut( '\t( (%s *) 0 )->~%s();' % ( self._identifier, self._identifier ) )
        self._code.lineOut( "}" )
        self._code.lineOut( "" )
        self._code.lineOut( "virtual bool %s_Constructor( %s )" % ( self._identifier,
                                                decomposition.parametersFullSpec() ) )
        self._code.lineOut( "{" )
        self._code.lineOut( "\treturn false;" )
        self._code.lineOut( "}" )
        self._code.lineOut( "" )

    def implementMethod( self, decomposition ):
        parametersForwardingList = decomposition.parametersForwardingList()
        if self._isMoveSemantics( decomposition ):
            parametersForwardingList = "std::move( %s )" % parametersForwardingList

        const = ""
        if decomposition.const:
            const = " const"
        self._code.lineOut( "virtual %s %s( %s )%s" % (
                                            decomposition.returnType,
                                            decomposition.name,
                                            decomposition.parametersFullSpec(),
                                            const ) )
        self._code.lineOut( "{" )
        self._code.lineOut( "\tif ( __voodooRedirectee ) {" )
        self._code.lineOut( "\t\t%s( (%s %s *) __voodooRedirectee )->%s( %s );" % (
                                        voodoodefs.returnIfNotVoid( decomposition ),
                                        const,
                                        self._identifier,
                                        decomposition.name,
                                        parametersForwardingList ) )
        self._code.lineOut( "\t} else {" )
        self._code.lineOut( "\t\t__VoodooGrowingString message;" )
        self._code.lineOut( "\t\tmessage.append( \"Method \" " )

        fullSpec = self._fullIdentifier + "::" + decomposition.name + \
                    "(" + decomposition.parametersFullSpec() + ")" + const
        self._code.lineOut( '\t\t\t"\'%s\' "' % fullSpec )
        self._code.lineOut( '\t\t\t"is not implemented by mock class \'" );' )
        self._code.lineOut( '\t\tmessage.append( __voodooMockName );' )
        self._code.lineOut( '\t\tmessage.append( "\'" );' )
        self._code.lineOut( '\t\tVOODOO_FAIL_TEST( message.result() );' )
        self._code.lineOut( '\t\t__VoodooGrowingString message2;' )
        self._code.lineOut( '\t\tmessage2.append( "VOODOO_FAIL_TEST did not throw, "' )
        self._code.lineOut( '\t\t\t" and Method \'%s\' is not implemented in \'" );' % fullSpec )
        self._code.lineOut( '\t\tmessage2.append( __voodooMockName );' )
        self._code.lineOut( '\t\tmessage2.append( "\', but still must return a value. "' )
        self._code.lineOut( '\t\t\t"Your test suite will seg fault now..." );' )
        self._code.lineOut( '\t\tVOODOO_FAIL_TEST( message2.result() );' )
        self._code.lineOut( "\t\t%s( (%s %s *) __voodooRedirectee )->%s( %s );" % (
                                        voodoodefs.returnIfNotVoid( decomposition ),
                                        const,
                                        self._identifier,
                                        decomposition.name,
                                        parametersForwardingList ) )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "}" )
        self._code.lineOut( "" )

    def implementRedirectorClassHeader( self ):
        inherits = ""
        if len( self._inherits ) > 0:
            inherits = " :\n\t\tpublic " + ",\n\t\tpublic ".join( self._inherits ) + "\n"
        self._code.lineOut( "%s%s %s%s" % ( self._templatePrefix, self._construct,
                                    self._identifier, inherits ) )
        self._code.lineOut( "{" )
        self._code.increaseIndent()

    def implementRedirectorClassFooter( self ):
        self._code.decreaseIndent()
        self._code.lineOut( "public:" )
        self._code.lineOut( "\tvirtual ~%s()" % self._identifier )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\tif ( __voodooRedirectee ) {" )
        self._code.lineOut( "\t\t\t__voodooRedirectee->%s_Destructor();" % self._identifier )
        self._code.lineOut( "\t\t} else {" )
        self._code.lineOut( "\t\t\tif ( __voodooPrevious )" )
        self._code.lineOut( "\t\t\t\t* __voodooPrevious = __voodooNext;" )
        self._code.lineOut( "\t\t\tif ( __voodooNext )" )
        self._code.lineOut( "\t\t\t\t__voodooNext->__voodooPrevious = __voodooPrevious;" )
        self._code.lineOut( "\t\t}" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\tbool voodooSameMockObject( const %s & other ) const" %
                                                                    self._identifier )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\tif ( __voodooRedirectee && other.__voodooRedirectee )" )
        self._code.lineOut( "\t\t\treturn __voodooRedirectee == other.__voodooRedirectee;" )
        self._code.lineOut( "\t\tif ( __voodooRedirectee && ! other.__voodooRedirectee )" )
        self._code.lineOut( "\t\t\treturn __voodooRedirectee == & other;" )
        self._code.lineOut( "\t\tif ( ! __voodooRedirectee && other.__voodooRedirectee )" )
        self._code.lineOut( "\t\t\treturn this == other.__voodooRedirectee;" )
        self._code.lineOut( "\t\tif ( ! __voodooRedirectee && ! other.__voodooRedirectee )" )
        self._code.lineOut( "\t\t\treturn this == & other;" )
        self._code.lineOut( "" )
        self._code.lineOut( "\t\treturn false;" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\t%s * voodooLastRedirector() const" % self._identifier )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\treturn __voodooLastRedirector;" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        if self._constructorCount == 0:
            self._code.increaseIndent()
            decomposition = functiondecomposition.FunctionDecomposition( name = self._identifier, parameters = [],
                            text = self._identifier, returnRValue = False, returnType = None, static = False, const = False )
            self.implementConstructor( decomposition )
            self._code.decreaseIndent()
        inherits = ""
        construct = "( __VoodooRedirectorConstruction() )"
        if len( self._mockInherits() ) > 0:
            inherits = " :\n\t\t" + ( construct + ",\n\t\t" ).join( self._mockInherits() ) + \
                        construct + "\n"
        self._code.lineOut( "\t%s( const %s & other )%s" % (    self._identifier,
                                                                self._identifier,
                                                                inherits ) )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\t%s * redirectee = other.__voodooRedirectee;" %
                                self._identifier )
        self._code.lineOut( "\t\tif ( redirectee == 0 )" )
        self._code.lineOut( "\t\t\tredirectee = (%s *) & other;" % self._identifier )
        self._code.lineOut( "\t\t__voodooSetRedirectee( redirectee );" )
        self._code.lineOut( "\t\tif ( other.__voodooRedirectee )" )
        self._code.lineOut( "\t\t\t__voodooRedirectee->%s_CopyConstructor( other );" %
                                                                    self._identifier )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "protected:" )
        self._code.lineOut( "\t%s( __VoodooRedirectorConstruction ) :" %
                                    self._identifier )
        for base in self._mockInherits():
            self._code.lineOut( "\t\t\t%s( __VoodooRedirectorConstruction() )," % base )
        self._code.lineOut( "\t\t\t__voodooMockName( 0 )" )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\t__voodooNext = 0;" )
        self._code.lineOut( "\t\t__voodooPrevious = 0;" )
        self._code.lineOut( "\t\t__voodooRedirectee = 0;" )
        self._code.lineOut( "\t\t__voodooLastRedirector = 0;" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\t%s( __VoodooMockConstruction, const char * mockName ) :" %
                                    self._identifier )
        for base in self._mockInherits():
            self._code.lineOut( "\t\t\t%s( __VoodooMockConstruction(), mockName )," % base )
        self._code.lineOut( "\t\t\t__voodooMockName( mockName )" )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\t__voodooNext = __voodooTop();" )
        self._code.lineOut( "\t\tif ( __voodooNext )" )
        self._code.lineOut( "\t\t\t__voodooNext->__voodooPrevious = & __voodooNext;" )
        self._code.lineOut( "\t\t__voodooPrevious = & __voodooTop();" )
        self._code.lineOut( "\t\t__voodooTop() = this;" )
        self._code.lineOut( "\t\t__voodooRedirectee = 0;" )
        self._code.lineOut( "\t\t__voodooLastRedirector = 0;" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\tvirtual void %s_Destructor()" % self._identifier )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\tvirtual void %s_CopyConstructor( const %s & )" % (
                                            self._identifier,
                                            self._identifier ) )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\tvoid __voodooSetRedirectee( %s * redirectee )" %
                                        self._identifier )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\t__voodooMockName = 0;" )
        self._code.lineOut( "\t\t__voodooRedirectee = redirectee;" )
        self._code.lineOut( "\t\tredirectee->__voodooLastRedirector = this;" )
        for base in self._mockInherits():
            self._code.lineOut( "\t\t%s::__voodooSetRedirectee( redirectee );" % base )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "private:" )
        self._code.lineOut( "\t%s * __voodooNext;" % self._identifier )
        self._code.lineOut( "\t%s * * __voodooPrevious;" % self._identifier )
        self._code.lineOut( "\t%s * __voodooRedirectee;" % self._identifier )
        self._code.lineOut( "\t%s * __voodooLastRedirector;" % self._identifier )
        self._code.lineOut( "\tconst char * __voodooMockName;" )
        self._code.lineOut( "" )
        self._code.lineOut( "\tstatic %s * & __voodooTop()" % self._identifier )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\tstatic %s * value = 0;" % self._identifier )
        self._code.lineOut( "\t\treturn value;" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "}; // %s %s" % ( self._construct, self._identifier ) )
        self._code.lineOut( "" )

    def _templatedIdentifier( self ):
        if len( self._templatePrefix ) == 0:
            return self._identifier
        return self._identifier + "< " + ', '.join( self._templateParametersList ) + " >"

    def implementMockClass( self ):
        self._code.lineOut( "%sclass %s : public %s" % (    self._templatePrefix,
                                                            self._mockClass,
                                                            self._templatedIdentifier() ) )
        self._code.lineOut( "{" )
        self._code.lineOut( "protected:" )
        self._code.lineOut( "\t%s( const char * mockName = \"%s decendant\" ) :" %
                                ( self._mockClass, self._mockClass ) )
        self._code.lineOut( "\t\t\t%s( __VoodooMockConstruction(), mockName )" %
                                    self._templatedIdentifier() )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "}; // class %s" % self._mockClass )
        self._code.lineOut( "" )
