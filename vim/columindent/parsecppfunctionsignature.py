import parsecpp
import tokenize

class ParseCPPFunctionSignature:
    def __init__( self, input ):
        self._input = input
        self._lead, self._parameters, self._tail = tokenize.Tokenize( input ).splitByParenthesis()

    def lead( self ): return self._lead

    def rows( self ):
        colums = self.argumentsTwoColumTable()
        addComma = [ m[ : -1 ] + ( m[ -1 ] + ',', ) for m in colums[ : -1 ] ] + [ colums[ -1 ] ]
        return addComma

    def tail( self ): return self._tail

    def argumentsTwoColumTable( self ):
        arguments = self._argumentsExpressions()
        colums = [ parsecpp.VariableDeclaration( a ).colums() for a in arguments ]
        return colums

    def _argumentsExpressions( self ):
        return tokenize.Tokenize( self._parameters ).splitByZeroParenLevel()
