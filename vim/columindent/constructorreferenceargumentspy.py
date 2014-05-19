import parsesimplecall
import re
import tab

class ConstructorReferenceArgumentsPy:
    def __init__( self, input, args ):
        self._input = input
        self._args = args
        self._tab = tab.Tab( args )
        self._parse = parsesimplecall.ParseSimpleCall( input )

    def format( self ):
        return self._input + "\n" + \
                self._formatInitialization()

    def _indentation( self, add = "" ):
        spacePrefix = re.match( r"\s*", self._input ).group( 0 )
        size = self._tab.roundUp( self._tab.countChars( spacePrefix + add ) )
        return self._tab.produce( size )

    def _formatInitialization( self ):
        return "".join( self._indentation( '\t' ) + "self._%s = %s\n" % ( p, p ) for p in self._parameters() )

    def _parameters( self ):
        parameters = [ re.search( r"\w+", r[ 0 ] ).group( 0 ) for r in self._parse.rows() ]
        if parameters[ 0 ] == "self":
            del parameters[ 0 ]
        return parameters
