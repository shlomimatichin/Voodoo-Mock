import tokenize

class ParseSimpleCall:
    def __init__( self, input ):
        self._input = input
        self._lead, self._parameters, self._tail = tokenize.Tokenize( input ).splitByParenthesis()

    def lead( self ): return self._lead
    def rows( self ):
        params = tokenize.Tokenize( self._parameters ).splitByZeroParenLevel()
        withCommas = [ p + "," for p in params[ : -1 ] ] + [ params[ -1 ] ]
        return [ ( p, ) for p in withCommas ]
    def tail( self ): return self._tail
