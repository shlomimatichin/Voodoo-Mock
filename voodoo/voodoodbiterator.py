import shelve
import iterateapi
import atexit
import filelock

class VoodooDBIterator( iterateapi.IterateAPI ):
    def __init__( self, perFileSettingsNotUsed, dbFilename ):
        self._dbFilename = dbFilename
        iterateapi.IterateAPI.__init__( self )
        self._db = {}
        atexit.register( self._atExit )

    def _atExit( self ):
        if not self._dbFilename:
            return
        with filelock.FileLock( self._dbFilename, timeout = 2 ) as lock:
            db = shelve.open( self._dbFilename, "c" )
            db.update( self._db )
            db.close()

    def structForwardDeclaration( self, ** kwargs ): pass
    def enterStruct( self, ** kwargs ): pass
    def leaveStruct( self, ** kwargs ): pass
    def enterClass( self, ** kwargs ): pass
    def leaveClass( self, ** kwargs ): pass
    def variableDeclaration( self, ** kwargs ): pass
    def typedef( self, ** kwargs ): pass
    def enum( self, ** kwargs ): pass
    def fieldDeclaration( self, ** kwargs ): pass
    def enterNamespace( self, ** kwargs ): pass
    def leaveNamespace( self, ** kwargs ): pass
    def accessSpec( self, ** kwargs ): pass
    def using( self, ** kwargs ): pass

    def functionForwardDeclaration( self, decomposition ):
        self._db[ self._fullIdentifier( decomposition.name ) ] = decomposition
    def functionDefinition( self, decomposition ):
        self._db[ self._fullIdentifier( decomposition.name ) ] = decomposition
    def constructorDefinition( self, decomposition ):
        self._db[ self._fullIdentifier( decomposition.name ) ] = decomposition
    def method( self, decomposition ):
        self._db[ self._fullIdentifier( decomposition.name ) ] = decomposition

    def _fullIdentifier( self, identifier ):
        return "::".join( [ identifier ] )
