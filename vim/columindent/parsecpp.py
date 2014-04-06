import tokenize

class VariableDeclaration:
    #input: 'int a'
    #output: ( 'int', 'a' )
    def __init__( self, declaration, asterixInFirstColum = True ):
        tokens = tokenize.Tokenize( declaration.strip() ).tokens()
        splitPoint = len( tokens )
        if '[' in tokens and tokens.index( '[' ) < splitPoint:
            splitPoint = tokens.index( '[' )
        if '=' in tokens and tokens.index( '=' ) < splitPoint:
            splitPoint = tokens.index( '=' )
        self._firstColum = tokens[ : splitPoint ]
        self._secondColum = tokens[ splitPoint : ]
        self._moveSpacesFromFirstColumToSecondColum()
        if len( self._firstColum ) == 0:
            self._firstColum = self._secondColum
            self._secondColum = []
            return
        self._moveTokenFromFirstColumToSecondColum() #eat variable name

        if not asterixInFirstColum:
            self._moveAsterixesFromFirstColumToSecondColum()

    def colums( self ):
        return "".join( self._firstColum ).strip(), "".join( self._secondColum ).strip()

    def _moveTokenFromFirstColumToSecondColum( self ):
        assert len( self._firstColum ) > 0
        self._secondColum.insert( 0, self._firstColum[ -1 ] )
        self._firstColum.pop()

    def _moveTokensFromFirstColumsToSecondColum( self, matching ):
        while len( self._firstColum ) > 0 and matching( self._firstColum[ -1 ] ):
            self._moveTokenFromFirstColumToSecondColum()

    def _moveSpacesFromFirstColumToSecondColum( self ):
        self._moveTokensFromFirstColumsToSecondColum( lambda x: x.isspace() )

    def _moveAsterixesFromFirstColumToSecondColum( self ):
        self._moveTokensFromFirstColumsToSecondColum( lambda x: x.isspace() or x == '*' )

class Classification:
    def __init__( self, string ):
        self._string = string
        self._lines = string.strip().split( "\n" )

    def memberList( self ):
        return not self._looksLikeACallOrFunctionDeclaration()

    def _looksLikeACallOrFunctionDeclaration( self ):
        return '(' in self._lines[ 0 ] and ')' in self._lines[ -1 ]
