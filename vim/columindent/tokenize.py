import re

class Tokenize:
    def __init__( self, string, templateParens = True ):
        self._string = string
        self._matching = { '(': ')', '[': ']', '{': '}' }
        if templateParens:
            self._matching[ '<' ] = '>'
        self._tokens = [ t for t in re.split( r'(\W)' , string ) if len( t ) > 0 ]
        self._assertBalancedParenthesis()

    def tokens( self ):
        return list( self._tokens )

    def splitByParenthesis( self ):
        tokens = list( self._tokens )
        upToParenthesis = "".join( tokens[ : tokens.index( '(' ) + 1 ] )
        tokens.reverse()
        afterParenthesisList = tokens[ : tokens.index( ')' ) + 1 ]
        afterParenthesisList.reverse()
        afterParenthesis = "".join( afterParenthesisList )
        insideParenthesis = self._string[ len( upToParenthesis ) : - len( afterParenthesis ) ]
        return upToParenthesis, insideParenthesis.strip(), afterParenthesis

    def splitByZeroParenLevel( self, splitToken = ',' ):
        opening = set( self._matching.keys() )
        closing = set( self._matching.values() )
        tokens = list( self._tokens )
        parts = [[]]
        parenLevel = 0
        while len( tokens ) > 0:
            token = tokens.pop( 0 )
            if token in opening:
                parenLevel += 1
            elif token in closing:
                parenLevel -= 1
            elif token == "'" or token == '"':
                parts[ -1 ] += self._stringLiteralFromTokens( tokens , token )
                continue
            elif token == splitToken and parenLevel == 0:
                parts.append( [] )
                continue
            parts[ -1 ].append( token )
        return [ "".join( p ).strip() for p in parts ]

    def _assertBalancedParenthesis( self ):
        opening = set( self._matching.keys() )
        closing = set( self._matching.values() )
        opened = []
        for i in xrange( len( self._tokens ) ):
            c = self._tokens[ i ]
            if c in opening:
                opened.append( c )
            if c in closing:
                if len( opened ) == 0 or self._matching[ opened[ -1 ] ] != c:
                    charIndex = len( "".join( self._tokens[ : i ] ) )
                    raise Exception( "()[]{}<> parenthesis are not balanced in "
                            "the input: '%s' at char %d:\n%s\n%s^\n%s" % (
                                self._string, charIndex,
                                self._string, " " * charIndex,
                                opened ) )
                opened.pop()

    @staticmethod
    def _stringLiteralFromTokens( tokens, firstChar ):
        result = [ firstChar ]
        ignoreNext = False
        while len( tokens ) > 0:
            token = tokens.pop( 0 )
            result.append( token )
            if ( token == firstChar and not ignoreNext ):
                break
            ignoreNext = token == '\\'
        return "".join( result )
