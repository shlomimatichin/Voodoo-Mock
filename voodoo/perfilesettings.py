import traceback
import re

class PerFileSettings:
    _EXPRESSION1 = re.compile( r"//\s*VOODOO_PERFILESETTINGS\s*(.*)" )
    _EXPRESSION2 = re.compile( r"/\*\s*VOODOO_PERFILESETTINGS\s*(.*)\*/" )
    _EXPRESSIONS = [ _EXPRESSION1, _EXPRESSION2 ]

    def __init__( self, inputLines ):
        self._defaults()

        relevant = self._relevantLines( inputLines )
        if relevant == "":
            return
        try:
            exec relevant in dict(), self.__dict__
        except:
            traceback.print_exc()
            print "Python syntax error in: '%s'" % relevant

    def filterInherits( self, inherits ):
        return [ inherit for inherit in inherits if inherit not in self.NO_INHERITS ]

    def _relevantLines( self, inputLines ):
        relevantLines = []
        for line in inputLines:
            for exp in self._EXPRESSIONS:
                match = exp.search( line )
                if match is not None:
                    relevantLines.append( match.group( 1 ) )
                    continue
        return "\n".join( relevantLines )

    def _defaults( self ):
        self.NO_MOCK_DERIVE_AND_USE_DEFAULT_CONSTRUCTOR = []
        self.SKIP = []
        self.NO_MOCK = []
        self.NO_INHERITS = []
