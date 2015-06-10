from voodooiterator import VoodooIterator
from voodooexpectfunction import VoodooExpectFunction
from voodooexpect import VoodooExpect

class VoodooExpectIterator( VoodooIterator ):
    def __init__( self, perFileSettings ):
        self._perFileSettings = perFileSettings
        VoodooIterator.__init__( self, perFileSettings )
        self._expect = []

    def functionForwardDeclaration( self, decomposition ):
        if self.protectionIgnoring().ignore():
            return
        if decomposition.name in self._perFileSettings.SKIP:
            return
        self._function( decomposition )

    def functionDefinition( self, decomposition ):
        if self.protectionIgnoring().ignore():
            return
        if decomposition.name in self._perFileSettings.SKIP:
            return
        self._function( decomposition )

    def constructorDefinition( self, decomposition ):
        if self.protectionIgnoring().ignore():
            return
        self._expect[ -1 ].constructor( decomposition )

    def method( self, decomposition ):
        if self.protectionIgnoring().ignore():
            return
        if decomposition.static:
            self._function( decomposition )
        else:
            self._expect[ -1 ].method( decomposition )

    def enterStruct( self, name, inheritance, templatePrefix, templateParametersList, fullText ):
        self._enterConstruct( name, inheritance, templatePrefix, templateParametersList, fullText, 'struct', 'public' )
    def leaveStruct( self ):
        self._leaveConstruct()
    def enterClass( self, name, inheritance, templatePrefix, templateParametersList, fullText ):
        self._enterConstruct( name, inheritance, templatePrefix, templateParametersList, fullText, 'class', 'private' )
    def leaveClass( self ):
        self._leaveConstruct()

    def _enterConstruct( self, name, inheritance, templatePrefix, templateParametersList, fullText, construct, defaultProtection ):
        if not self.shouldImplementEnterConstruct( name, fullText, defaultProtection ):
            return
        expect = VoodooExpect(  code = self.code(),
                                identifier = name,
                                fullIdentifier = self.fullIdentifier( name ),
                                construct = construct,
                                inherits = [ identifier for protection, identifier in inheritance ],
                                perFileSettings = self._perFileSettings,
                                templatePrefix = templatePrefix,
                                templateParametersList = templateParametersList )
        expect.implementExpectingClassHeader()
        self._expect.append( expect )
        self.inClass.append( name )

    def _leaveConstruct( self ):
        if not self.shouldImplementLeaveConstruct():
            return
        expect = self._expect.pop()
        expect.implementExpectingClassFooter()
        expect.implementFakeClass( expect.fullIdentifier() )
        expect.implementFakeNDClass( expect.fullIdentifier() )
        self.inClass.pop()

    def _function( self, decomposition ):
        VoodooExpectFunction( self.code() ).function( decomposition )
