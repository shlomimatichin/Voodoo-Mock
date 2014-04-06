import parsecpp
import re

class ParseCPPMemberList:
    def __init__( self, input ):
        self._input = input

    def lead( self ):
        return self._spaceBeforeFirstMember()

    def rows( self ):
        colums = self.memberTwoColumTable()
        addSemicolon = [ m[ : -1 ] + ( m[ -1 ] + ';', ) for m in colums ]
        return addSemicolon

    def tail( self ):
        return ""

    def memberTwoColumTable( self ):
        members = self._memberExpressions()
        colums = [ parsecpp.VariableDeclaration( m ).colums() for m in members ]
        return colums

    def _memberExpressions( self ):
        members = [ m.strip() for m in self._input.split( ';' ) ]
        assert len( members ) > 0
        if members[ -1 ] == "":
            members.pop()
        return members

    def _spaceBeforeFirstMember( self ):
        return re.search( r"^(\s*)" , self._input ).groups()[ 0 ]
