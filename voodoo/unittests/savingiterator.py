import iterateapi

class SavingIterator( iterateapi.IterateAPI ):
    def __init__( self ):
        iterateapi.IterateAPI.__init__( self )
        self.printErrors = True
        self.saved = []
        self._addSaver( 'structForwardDeclaration' )
        self._addSaver( 'enterStruct' )
        self._addSaver( 'leaveStruct' )
        self._addSaver( 'enterClass' )
        self._addSaver( 'leaveClass' )
        self._addSaver( 'variableDeclaration' )
        self._addSaver( 'fieldDeclaration' )
        self._addSaver( 'typedef' )
        self._addSaver( 'union' )
        self._addSaver( 'enum' )
        self._addDecompositionSaver( 'functionForwardDeclaration' )
        self._addDecompositionSaver( 'functionDefinition' )
        self._addDecompositionSaver( 'constructorDefinition' )
        self._addDecompositionSaver( 'method' )
        self._addSaver( 'enterNamespace' )
        self._addSaver( 'leaveNamespace' )
        self._addSaver( 'accessSpec' )

    def _addSaver( self, callName ):
        setattr( self, callName, lambda ** kwargs: self._save( callName, ** kwargs ) )

    def _addDecompositionSaver( self, callName ):
        setattr( self, callName, lambda decomposition: self._save( callName, ** decomposition.__dict__ ) )

    def _save( self, callbackName, fullText = None, ** kwargs ):
        if fullText is not None:
            kwargs[ 'fullTextNaked' ] = fullText.strip( ';' ).replace( " ", "" ).replace( "\t", "" ).replace( '\n', '' )
        self.saved.append( dict( callbackName = callbackName, ** kwargs ) )

    def handleError( self, severity, location, spelling, ranges, fixits ):
        if self.printErrors:
            print "X"*80
            print severity
            print location
            print spelling
            print ranges
            print fixits
        raise Exception( "error parsing" )
