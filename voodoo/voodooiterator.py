from growcode import GrowCode
from voodoochain import VoodooChain
from voodoomock import VoodooMock
import protectionignoring
import iterateapi

class VoodooIterator( iterateapi.IterateAPI ):
    def __init__( self, perFileSettings ):
        iterateapi.IterateAPI.__init__( self )
        self._code = GrowCode()
        self._namespace = []
        self.inClass = []
        self._protectionIgnoring = protectionignoring.ProtectionIgnoring()
        self._voodoomocks = []
        self._chainCache = None
        self._perFileSettings = perFileSettings

    def out( self ):
        return self._code.result()

    def code( self ):
        return self._code

    def protectionIgnoring( self ):
        return self._protectionIgnoring

    def fullIdentifier( self , identifier ):
        return "::".join( self._namespace + self.inClass + [ identifier ] )

    def structForwardDeclaration( self, name ):
        if self._protectionIgnoring.ignore():
            return
        if name in self._perFileSettings.SKIP:
            return
        self._code.lineOut( "struct " + name + ";" )
        self._code.lineOut( "" )

    def variableDeclaration( self, name, text ):
        if self._protectionIgnoring.ignore():
            return
        if name in self._perFileSettings.SKIP:
            return
        self._textOut( text )

    def typedef( self, name, text ):
        if self._protectionIgnoring.ignore():
            return
        if name in self._perFileSettings.SKIP:
            return
        self._textOut( text )

    def union( self, name, text ):
        if self._protectionIgnoring.ignore():
            return
        if name in self._perFileSettings.SKIP:
            return
        self._textOut( text )

    def enum( self, name, text ):
        if self._protectionIgnoring.ignore():
            return
        if name in self._perFileSettings.SKIP:
            return
        self._textOut( text )

    def fieldDeclaration( self, name, text ):
        if self._protectionIgnoring.ignore():
            return
        if name in self._perFileSettings.SKIP:
            return
        self._textOut( text )

    def using( self, text ):
        if self._protectionIgnoring.ignore():
            return
        self._textOut( text )

    def functionForwardDeclaration( self, decomposition ):
        if self._protectionIgnoring.ignore():
            return
        if decomposition.name in self._perFileSettings.SKIP:
            return
        self._function( decomposition )

    def functionDefinition( self, decomposition ):
        if self._protectionIgnoring.ignore():
            return
        if decomposition.name in self._perFileSettings.SKIP:
            return
        self._function( decomposition )

    def constructorDefinition( self, decomposition ):
        if self._protectionIgnoring.ignore():
            return
        mock = self._voodoomocks[ -1 ]
        mock.implementConstructor( decomposition )

    def method( self, decomposition ):
        if self._protectionIgnoring.ignore():
            return
        if decomposition.static:
            self._function( decomposition )
        else:
            mock = self._voodoomocks[ -1 ]
            mock.implementMethod( decomposition )

    def enterStruct( self, name, inheritance, templatePrefix, templateParametersList, fullText ):
        self._enterConstruct( name, inheritance, templatePrefix, templateParametersList, fullText, 'struct', 'public' )
    def leaveStruct( self ):
        self._leaveConstruct()
    def enterClass( self, name, inheritance, templatePrefix, templateParametersList, fullText ):
        self._enterConstruct( name, inheritance, templatePrefix, templateParametersList, fullText, 'class', 'private' )
    def leaveClass( self ):
        self._leaveConstruct()

    def enterNamespace( self, name ):
        if self._protectionIgnoring.ignore():
            return
        self._namespace.append( name )
        self._code.lineOut( "namespace %s" % name )
        self._code.lineOut( "{" )
        self._code.increaseIndent()

    def leaveNamespace( self ):
        if self._protectionIgnoring.ignore():
            return
        self._namespace.pop()
        self._code.decreaseIndent()
        self._code.lineOut( "};" )

    def accessSpec( self, access ):
        if access != 'private':
            self._code.decreaseIndent()
            self._code.lineOut( access + ":" )
            self._code.increaseIndent()
        self._protectionIgnoring.change( access )

    def _textOut( self, text ):
        self._code.lineOut( text + ";" )
        self._code.lineOut( "" )

    def _function( self, decomposition ):
        chain = VoodooChain( decomposition.name, self.fullIdentifier( decomposition.name ), self._code, self._chainCache )
        self._chainCache = chain.cache()
        chain.overload( decomposition )

    def shouldImplementEnterConstruct( self, name, fullText, defaultProtection ):
        if name in self._perFileSettings.NO_MOCK:
            self._code.lineOut( fullText + ";" )
            self._code.lineOut( "" )
            self._protectionIgnoring.enterSkipped()
        elif name in self._perFileSettings.SKIP:
            self._protectionIgnoring.enterSkipped()
        else:
            self._protectionIgnoring.enter( defaultProtection )
        return not self._protectionIgnoring.ignoreButLast()

    def _enterConstruct( self, name, inheritance, templatePrefix, templateParametersList, fullText, construct, defaultProtection ):
        if not self.shouldImplementEnterConstruct( name, fullText, defaultProtection ):
            return
        mock = VoodooMock(  construct = construct,
                            identifier = name,
                            inherits = [ identifier for protection, identifier in inheritance ],
                            fullIdentifier = self.fullIdentifier( name ),
                            code = self._code,
                            perFileSettings = self._perFileSettings,
                            templatePrefix = templatePrefix,
                            templateParametersList = templateParametersList )
        mock.implementRedirectorClassHeader()
        self._voodoomocks.append( mock )
        self.inClass.append( name )

    def shouldImplementLeaveConstruct( self ):
        ignore = self._protectionIgnoring.ignoreButLast()
        self._protectionIgnoring.leave()
        return not ignore

    def _leaveConstruct( self ):
        if not self.shouldImplementLeaveConstruct():
            return
        self.inClass.pop()
        mock = self._voodoomocks.pop()
        mock.implementRedirectorClassFooter()
        mock.implementMockClass()
