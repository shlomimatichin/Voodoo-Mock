import voodoodefs

class VoodooExpectFunction:
    def __init__( self, code ):
        self._code = code

    def function( self, decomposition ):
        self._code.lineOut( "%s%s%s%s %s( %s )" % (
                    decomposition.templatePrefix,
                    decomposition.stringStaticInlineIfStatic(),
                    decomposition.stringVirtualIfVirtual(),
                    decomposition.returnType,
                    decomposition.name,
                    decomposition.parametersFullSpec() ) )
        self._code.lineOut( "{" )
        self._try()
        self._code.lineOut( '\t__VoodooGrowingString growingString;' )
        self._code.lineOut( '\tgrowingString.append( "Call to " );' )
        self._code.lineOut( '\tgrowingString.append( __FUNCTION__ );' )
        self._code.lineOut( '\tVoodooCommon::Expect::Multiplexer multiplexer( growingString.result() );' )
        self._implementParametersHandeling( decomposition )
        self._implementReturnValue( decomposition )
        self._catchVoodooErrorMessages()
        self._code.lineOut( "}" )
        self._code.lineOut( "" )

    def _implementParametersHandeling( self, decomposition, shouldIgnoreParameterPack = False ):
        for index in xrange( len( decomposition.parameters ) ):
            parameter = decomposition.parameters[ index ]
            if not parameter.get( 'isParameterPack', False ):
                self._code.lineOut( '\tmultiplexer.check' +
                    '( %d, ' % index +
                    'VoodooCommon::PointerTypeString( & %s ).typeString(), ' % parameter[ 'name' ] +
                    '& %s );' % parameter[ 'name' ] )
            elif not shouldIgnoreParameterPack:
                self._code.lineOut( '\tmultiplexer.checkParameterPack( %s, ' % index +
                        '%s... ); ' % parameter[ 'name' ] )
        for index in xrange( len( decomposition.parameters ) ):
            parameter = decomposition.parameters[ index ]
            if not parameter.get( 'isParameterPack', False ):
                self._code.lineOut( '\tmultiplexer.effect' +
                    '( %d, ' % index +
                    'VoodooCommon::PointerTypeString( & %s ).typeString(), ' % parameter[ 'name' ] +
                    '& %s );' % parameter[ 'name' ] )
            elif not shouldIgnoreParameterPack:
                self._code.lineOut( '\tmultiplexer.effectParameterPack( %s, ' % index +
                        '%s... ); ' % parameter[ 'name' ] )

    def _implementReturnValue( self, decomposition ):
        nonReferenceType = self._nonReferenceType( decomposition )
        self._code.lineOut( '\tconst void * returnValueAsVoid = 0;' )
        self._code.lineOut( '\t%s * returnValueUnused = 0;' % nonReferenceType )
        self._code.lineOut( '\tmultiplexer.returnValue(' +
                'VoodooCommon::PointerTypeString( returnValueUnused ).typeString(), returnValueAsVoid );' )
        if not decomposition.returnTypeIsVoid():
            if decomposition.returnRValue:
                self._code.lineOut( '\treturn std::move( * (%s *) returnValueAsVoid );' % nonReferenceType )
            else:
                self._code.lineOut( '\treturn * (%s *) returnValueAsVoid;' % nonReferenceType )

    def _nonReferenceType( self, decomposition ):
        return decomposition.returnType.rstrip( '& \t' )

    def _try( self, tabs = "" ):
        self._code.increaseIndent()
        self._code.lineOut( tabs + 'try {' )

    def _catchVoodooErrorMessages( self, tabs = "", noThrow = False ):
        self._code.lineOut( tabs + '} catch ( VoodooCommon::ErrorMessage & e ) {' )
        self._code.lineOut( tabs + '\tVoodooCommon::ErrorMessage error;' )
        self._code.lineOut( tabs + '\terror.append( "From " );' )
        self._code.lineOut( tabs + '\terror.append( __FUNCTION__ );' )
        self._code.lineOut( tabs + '\terror.append( ": " );' )
        self._code.lineOut( tabs + '\terror.append( e.result() );' )
        if noThrow:
            self._code.lineOut( tabs + '\tVOODOO_FAIL_TEST_NO_THROW( error.result() );' )
        else:
            self._code.lineOut( tabs + '\tVOODOO_FAIL_TEST( error.result() );' )
            self._code.lineOut( tabs + '\tthrow "VOODOO_FAIL_TEST must throw";' )
        self._code.lineOut( tabs + '}' )
        self._code.decreaseIndent()
