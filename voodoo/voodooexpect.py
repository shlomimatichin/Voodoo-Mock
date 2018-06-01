import voodoodefs
from voodooexpectfunction import VoodooExpectFunction
import functiondecomposition

class VoodooExpect:
    def __init__( self, code, identifier, fullIdentifier, construct, inherits, templatePrefix,
                    templateParametersList, perFileSettings ):
        self._code = code
        self._identifier = identifier
        self._fullIdentifier = fullIdentifier
        self._construct = construct
        self._inherits = perFileSettings.filterInherits( inherits )
        self._templatePrefix = templatePrefix
        self._templateParametersList = templateParametersList
        self._perFileSettings = perFileSettings
        self._constructorCount = 0
        self._implicitAssignmentOperator = True

    def identifier( self ):
        return self._identifier

    def fullIdentifier( self ):
        return self._fullIdentifier

    def _implementParametersHandeling( self, decomposition ):
        shouldIgnoreParameterPack = False
        if  "::".join( [ self._fullIdentifier, decomposition.name ] ) in self._perFileSettings.IGNORE_PARAMETER_PACK:
                shouldIgnoreParameterPack = True

        VoodooExpectFunction( self._code )._implementParametersHandeling( decomposition, shouldIgnoreParameterPack = shouldIgnoreParameterPack )

    def _implementReturnValue( self, decomposition ):
        VoodooExpectFunction( self._code )._implementReturnValue( decomposition )

    def _instanceOfFunction( self, decomposition ):
        if decomposition.templatePrefix == "":
            return '"' + decomposition.name + '"'
        else:
            return '_VOODOO_TEMPLATE_INSTANCE_OF_THIS_FUNCTION( "' + \
                        decomposition.name + '" )'

    def method( self, decomposition ):
        if decomposition.name == "operator=":
            self._implicitAssignmentOperator = False
#todo: is operator = still named like this?
        if decomposition.const:
            const = " const"
        else:
            const = ""
        if decomposition.virtual:
            virtual = "virtual "
        else:
            virtual = ""
        self._code.lineOut( "%s%s%s %s( %s )%s" % ( virtual,
                        voodoodefs.templateLine( decomposition.templatePrefix ),
                        decomposition.returnType,
                        decomposition.name,
                        decomposition.parametersFullSpec(),
                        const ) )
        self._code.lineOut( "{" )
        VoodooExpectFunction( self._code )._try()
        self._code.lineOut( '\t__VoodooGrowingString growingString;' )
        self._code.lineOut( '\tgrowingString.append( "Call to " );' )
        self._code.lineOut( '\tgrowingString.append( __voodooInstanceName );' )
        self._code.lineOut( '\tgrowingString.append( "::" );' )
        self._code.lineOut( '\tgrowingString.append( %s );' %
                            self._instanceOfFunction( decomposition ) )
        self._code.lineOut( '\tVoodooCommon::Expect::Multiplexer multiplexer( ' +
                    'growingString.result() );' )
        self._implementParametersHandeling( decomposition )
        self._implementReturnValue( decomposition )
        VoodooExpectFunction( self._code )._catchVoodooErrorMessages()
        self._code.lineOut( "}" )
        self._code.lineOut( "" )

    def _isCopyConstructor( self, decomposition ):
        if len( decomposition.parameters ) != 1:
            return False
        return decomposition.parametersFullSpec() == \
                    "const %s & %s" % ( self._identifier, decomposition.parameters[ 0 ][ 'name' ] )

    def constructor( self, decomposition ):
        if ( self._isCopyConstructor( decomposition ) ):
            return
        self._constructorCount += 1
        self._code.lineOut( "%s%s( %s )%s" % (
                        voodoodefs.templateLine( decomposition.templatePrefix ),
                        self._identifier,
                        decomposition.parametersFullSpec(),
                        self._constructHeritage() ) )
        self._code.lineOut( "{" )
        VoodooExpectFunction( self._code )._try()
        self._code.lineOut( '\t__VoodooGrowingString growingString;' )
        self._code.lineOut( '\tgrowingString.append( "Construction of " );' )
        self._code.lineOut( '\tgrowingString.append( ' +
            'VoodooCommon::PointerTypeString( this ).typeString() );' )
        self._code.lineOut( '\t__voodooConstructingInstance() = this;' )
        self._code.lineOut( '\tVoodooCommon::Expect::Multiplexer multiplexer( ' +
                            'growingString.result() );' )
        self._implementParametersHandeling( decomposition )
        self._code.lineOut( '\t__voodooSetInstanceName( "" );' )
        self._code.lineOut( "\tconst void * instanceNameAsVoid;" )
        self._code.lineOut( '\tmultiplexer.returnValue( "const char *", instanceNameAsVoid );' )
        self._code.lineOut( "\tconst char * instanceName = (const char *) instanceNameAsVoid;" )
        self._code.lineOut( '\t__voodooSetInstanceName( instanceName );' )
        self._code.lineOut( '\t__voodooInsertToInstanceList();' )
        self._code.lineOut( '\t__voodooConstructingInstance() = NULL;' )
        VoodooExpectFunction( self._code )._catchVoodooErrorMessages()
        self._code.lineOut( "}" )
        self._code.lineOut( "" )

    def implementExpectingClassHeader( self ):
        if len( self._inherits ) > 0:
            inherits = " :\n\t\tpublic " + ",\n\t\tpublic ".join( self._inherits ) + "\n"
        else:
            inherits = ""
        self._code.lineOut( "%s%s %s%s" % (
                                voodoodefs.templateLine( self._templatePrefix ),
                                self._construct,
                                self._identifier,
                                inherits ) )
        self._code.lineOut( "{" )
        self._code.increaseIndent()

    def _mockInherits( self ):
        return [ i for i in self._inherits if i not in
                                self._perFileSettings.NO_MOCK_DERIVE_AND_USE_DEFAULT_CONSTRUCTOR ]

    def _constructHeritage( self ):
        if len( self._mockInherits() ) == 0:
            return ""
        construct = "( __VoodooRedirectorConstruction() )"
        return " :\n\t\t" + \
                    ( construct + ",\n\t\t" ).join( self._mockInherits() ) + \
                    construct + "\n"

    def implementExpectingClassFooter( self ):
        self._code.decreaseIndent()
        self._code.lineOut( "public:" )
        self._code.lineOut( "\tvirtual ~%s()" % self._identifier )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\t__voodooRemoveFromInstanceList();" )
        self._code.lineOut( '\t\tif ( __voodooInstanceName[ 0 ] != \'\\0\' ) {' );
        VoodooExpectFunction( self._code )._try( "\t\t" )
        self._code.lineOut( '\t\t\t__VoodooGrowingString growingString;' )
        self._code.lineOut( '\t\t\tgrowingString.append( "Destruction of " );' )
        self._code.lineOut( '\t\t\tgrowingString.append( __voodooInstanceName );' )
        self._code.lineOut( '\t\t\tVoodooCommon::Expect::Multiplexer multiplexer(' +
                        ' growingString.result() );' )
        self._code.lineOut( '\t\t\tconst void * unusedReturnValue = 0;' )
        self._code.lineOut( '\t\t\tmultiplexer.returnValue( 0, unusedReturnValue );' )
        VoodooExpectFunction( self._code )._catchVoodooErrorMessages( "\t\t", noThrow = True )
        self._code.lineOut( '\t\t\t__voodooSetInstanceName( "" );' )
        self._code.lineOut( "\t\t}" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        if self._constructorCount == 0:
            self._code.increaseIndent()
            decomposition = functiondecomposition.FunctionDecomposition( name = self._identifier, parameters = [],
                            text = self._identifier, returnRValue = False, returnType = None, static = False, const = False )
            self.constructor( decomposition )
            self._code.decreaseIndent()
        if self._implicitAssignmentOperator:
            self._code.increaseIndent()
            decomposition = functiondecomposition.FunctionDecomposition(
                            name = "operator=",
                            parameters = [ dict( name = "other", text = "const %s & other" % self._identifier ) ],
                            text = "%s & operator=" % self._identifier,
                            returnType = "%s &" % self._identifier,
                             returnRValue = False,
                            static = False,
                            const = False )
            self.method( decomposition )
            self._code.decreaseIndent()
        self._code.lineOut( "\t%s( const %s & other )%s" % (
                    self._identifier, self._identifier,
                    self._constructHeritage() ) )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\t__VoodooGrowingString growingString;" )
        self._code.lineOut( '\t\tgrowingString.append( "Copy of " );' )
        self._code.lineOut( '\t\tgrowingString.append( other.__voodooInstanceName );' )
        self._code.lineOut( "\t\t__voodooSetInstanceName( growingString.result() );" )
        self._code.lineOut( "\t\t__voodooInsertToInstanceList();" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\tconst char * voodooInstanceName() const" )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\treturn __voodooInstanceName;" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\tstatic %s * voodooInstanceByName( const char * name )" % self._identifier )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\tfor ( %s * i = __voodooHeadInstance(); i != 0 ; i = i->__voodooNextInstance )" % self._identifier )
        self._code.lineOut( "\t\t\tif ( strcmp( i->__voodooInstanceName, name ) == 0 )" )
        self._code.lineOut( "\t\t\t\treturn i;" )
        self._code.lineOut( "\t\treturn 0;" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\tstatic %s & voodooConstructingInstance()" % self._identifier )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\tif ( __voodooConstructingInstance() == 0 ) {" )
        self._code.lineOut( '\t\t\tVOODOO_FAIL_TEST( "You called %s::voodooConstructingInstance() "' % self._identifier )
        self._code.lineOut( '\t\t\t\t\t"outside of constructor callback" );' )
        self._code.lineOut( '\t\t}' )
        self._code.lineOut( "\t\treturn * __voodooConstructingInstance();" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "protected:" )
        self._code.lineOut( "\t%s( __VoodooRedirectorConstruction )%s" %
                                ( self._identifier, self._constructHeritage() ) )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\t__voodooInsertToInstanceList();" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\tvoid __voodooSetInstanceName( const char * instanceName )" )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\tstrncpy( __voodooInstanceName, instanceName, VOODOO_EXPECT_MAX_INSTANCE_NAME );" )
        for base in self._mockInherits():
            self._code.lineOut( "\t\t%s::__voodooSetInstanceName( instanceName );" % base )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "private:" )
        self._code.lineOut( "\tchar __voodooInstanceName[ VOODOO_EXPECT_MAX_INSTANCE_NAME + sizeof( '\\0' ) ];" )
        self._code.lineOut( "\t%s * * __voodooPreviousInstance;" % self._identifier )
        self._code.lineOut( "\t%s * __voodooNextInstance;" % self._identifier )
        self._code.lineOut( "" )
        self._code.lineOut( "\tstatic %s * & __voodooHeadInstance()" % self._identifier )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\tstatic %s * head = 0;" % self._identifier )
        self._code.lineOut( "\t\treturn head;" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\tstatic %s * & __voodooConstructingInstance()" % self._identifier )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\tstatic %s * instance = 0;" % self._identifier )
        self._code.lineOut( "\t\treturn instance;" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\tvoid __voodooInsertToInstanceList()" )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\t__voodooNextInstance = __voodooHeadInstance();" )
        self._code.lineOut( "\t\tif ( __voodooNextInstance != 0 )" )
        self._code.lineOut( "\t\t\t__voodooNextInstance->__voodooPreviousInstance = & __voodooNextInstance;" )
        self._code.lineOut( "\t\t__voodooPreviousInstance = & __voodooHeadInstance();" )
        self._code.lineOut( "\t\t__voodooHeadInstance() = this;" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\tvoid __voodooRemoveFromInstanceList()" )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\tif ( __voodooPreviousInstance != 0 ) {" )
        self._code.lineOut( "\t\t\t* __voodooPreviousInstance = __voodooNextInstance;" )
        self._code.lineOut( "\t\t\tif ( __voodooNextInstance != 0 )" )
        self._code.lineOut( "\t\t\t\t__voodooNextInstance->__voodooPreviousInstance = __voodooPreviousInstance;" )
        self._code.lineOut( "\t\t}" )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "}; // %s %s" % ( self._construct, self._identifier ) )
        self._code.lineOut( "" )

    def implementFakeClass( self, fullIdentifier ):
        fakeClass = voodoodefs.fakeClass( self._identifier )
        self._code.lineOut( "%sclass %s : public %s%s" % (
                                voodoodefs.templateLine( self._templatePrefix ),
                                fakeClass,
                                self._identifier,
                                self._passTemplateParameters() ) )
        self._code.lineOut( "{" )
        self._code.lineOut( "public:" )
        self._code.lineOut( "\t%s( const char * instanceName = \"Fake %s\" ) :" %
                                ( fakeClass, fullIdentifier ) )
        self._code.lineOut( "\t\t\t%s%s( __VoodooRedirectorConstruction() )" %
                                    ( self._identifier, self._passTemplateParameters() ) )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\t%s%s::__voodooSetInstanceName( instanceName );" %
                                    ( self._identifier, self._passTemplateParameters() ) )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "}; // class %s" % fakeClass )
        self._code.lineOut( "" )

    def implementFakeNDClass( self, fullIdentifier ):
        fakeNDClass = voodoodefs.fakeNDClass( self._identifier )
        self._code.lineOut( "%sclass %s : public %s%s" % (
                                voodoodefs.templateLine( self._templatePrefix ),
                                fakeNDClass,
                                self._identifier,
                                self._passTemplateParameters() ) )
        self._code.lineOut( "{" )
        self._code.lineOut( "public:" )
        self._code.lineOut( "\t%s( const char * instanceName = \"Fake %s\" ) :" %
                                ( fakeNDClass, fullIdentifier ) )
        self._code.lineOut( "\t\t\t%s%s( __VoodooRedirectorConstruction() )" %
                                    ( self._identifier, self._passTemplateParameters() ) )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\t%s%s::__voodooSetInstanceName( instanceName );" %
                                    ( self._identifier, self._passTemplateParameters() ) )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "" )
        self._code.lineOut( "\t~%s() " % fakeNDClass )
        self._code.lineOut( "\t{" )
        self._code.lineOut( "\t\t%s%s::__voodooSetInstanceName( \"\" );" %
                                    ( self._identifier, self._passTemplateParameters() ) )
        self._code.lineOut( "\t}" )
        self._code.lineOut( "}; // class %s" % fakeNDClass )
        self._code.lineOut( "" )

    def _passTemplateParameters( self ):
        if self._templateParametersList:
            return "< " + ", ".join( self._templateParametersList ) + " >"
        else:
            return ""
