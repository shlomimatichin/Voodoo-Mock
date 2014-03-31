class ProtectionIgnoring:
    def __init__( self ):
        self._protection = [ "public" ]

    def ignore( self ):
        return 'private' in self._protection or 'skip' in self._protection

    def enter( self, protection ):
        assert protection in [ 'private', 'protected', 'public' ]
        self._protection.append( protection )

    def enterSkipped( self ):
        self._protection.append( 'skip' )

    def leave( self ):
        self._protection.pop()

    def change( self, protection ):
        assert protection in [ 'private', 'protected', 'public' ]
        self._protection[ -1 ] = protection

    def ignoreButLast( self ):
        return 'private' in self._protection[ : -1 ] or 'skip' in self._protection
        #note: no [:-1] for 'skip', this is not a bug
