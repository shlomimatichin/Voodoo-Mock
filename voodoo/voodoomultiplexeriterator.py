from voodooiterator import VoodooIterator
from voodooexpectiterator import VoodooExpectIterator
import iterateapi
from voodoodbiterator import VoodooDBIterator

class VoodooMultiplexerIterator( iterateapi.IterateAPI ):
    def __init__( self, perFileSettings, dbFilename ):
        self._iter = VoodooIterator( perFileSettings )
        self._expect = VoodooExpectIterator( perFileSettings )
        self._db = VoodooDBIterator( perFileSettings, dbFilename )
        iterateapi.IterateAPI.__init__( self )
        self._multiplex()

    def handleError( self, severity, location, spelling, ranges, fixits ):
        SEVERITY_TO_TEXT = { 0: 'Ignored', 1: 'Note', 2: 'Warning', 3: 'Error', 4: 'Fatal' }
        rangesText = "\nRange: ".join( [ str( r ) for r in ranges ] )
        fixitsText = "\nFixit: ".join( [ str( f ) for f in fixits ] )
        raise Exception( "%s: at '%s': '%s'\nRange: %s\nFixit: %s" % ( SEVERITY_TO_TEXT[ severity ], location, spelling, rangesText, fixitsText ) )

    def _multiplex( self ):
        class MethodMultiplexer:
            def __init__( self, multiplexer, name ):
                self._multiplexer = multiplexer
                self._name = name

            def __call__( self, * args, ** kwargs ):
                getattr( self._multiplexer._iter, self._name )( * args, ** kwargs )
                getattr( self._multiplexer._expect, self._name )( * args, ** kwargs )
                getattr( self._multiplexer._db, self._name )( * args, ** kwargs )
        self.structForwardDeclaration = MethodMultiplexer( self, "structForwardDeclaration" )
        self.classForwardDeclaration = MethodMultiplexer( self, "classForwardDeclaration" )
        self.enterStruct = MethodMultiplexer( self, "enterStruct" )
        self.leaveStruct = MethodMultiplexer( self, "leaveStruct" )
        self.enterClass = MethodMultiplexer( self, "enterClass" )
        self.leaveClass = MethodMultiplexer( self, "leaveClass" )
        self.variableDeclaration = MethodMultiplexer( self, "variableDeclaration" )
        self.typedef = MethodMultiplexer( self, "typedef" )
        self.enum = MethodMultiplexer( self, "enum" )
        self.functionForwardDeclaration = MethodMultiplexer( self, "functionForwardDeclaration" )
        self.functionDefinition = MethodMultiplexer( self, "functionDefinition" )
        self.constructorDefinition = MethodMultiplexer( self, "constructorDefinition" )
        self.method = MethodMultiplexer( self, "method" )
        self.fieldDeclaration = MethodMultiplexer( self, "fieldDeclaration" )
        self.enterNamespace = MethodMultiplexer( self, "enterNamespace" )
        self.leaveNamespace = MethodMultiplexer( self, "leaveNamespace" )
        self.accessSpec = MethodMultiplexer( self, "accessSpec" )
        self.using = MethodMultiplexer( self, "using" )

    def iter( self ):
        return self._iter.out()

    def expect( self ):
        return self._expect.out()
