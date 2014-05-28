import re
import tab

class FormatColums:
    def __init__( self, parse, args ):
        self._parse = parse
        self._args = args
        self._tab = tab.Tab( args )
        self._lines = self._toLines( parse.rows() )
        self._lead = parse.lead()
        if self._lead.isspace():
            self._indentationCharacters = self._tab.countChars( self._lead )
        else:
            self._indentationCharacters = self._tab.countChars( self._lead + '\t' )
            mustAddNewLine = self._args.alwaysNewLineForFirstParameter
            if self._indentationCharacters + self._longestLine() > args.optimizeForMaximumLineLength:
                mustAddNewLine = True
                self._indentationCharacters = args.optimizeForMaximumLineLength - self._tab.roundUp( self._longestLine )
                if self._indentationCharacters < self._minimumIndentation():
                    self._indentationCharacters = self._minimumIndentation()
            if mustAddNewLine:
                self._lead + '\n' + self._indentation()
            else:
                assert self._indentationCharacters > self._tab.countChars( self._lead )
                self._lead += ' ' * ( self._indentationCharacters - self._tab.countChars( self._lead ) )

    def format( self ):
        return self._lead + ( '\n' + self._indentation() ).join( self._lines ) + self._tail()

    def _minimumIndentation( self ):
        assert not self._lead.isspace()
        spacePrefix = re.match( r'(\s*)', self._lead ).group( 0 )
        return self._tab.countChars( spacePrefix + '\t' )

    def _tail( self ):
        tail = self._parse.tail()
        if len( tail ) > 0 and not tail.isspace():
            if self._args.noSpaceBeforeClosingParenthesis:
                return tail
            return ' ' + tail
        else:
            return tail

    def _indentation( self ):
        return self._tab.produce( self._indentationCharacters )

    def _longestLine( self ):
        return max( len( l ) for l in self._lines )

    def _toLines( self, rows ):
        if len( rows[ 0 ] ) == 1:
            return [ r[ 0 ] for r in rows ]
        else:
            return self._twoColumnsToLines( rows )

    def _twoColumnsToLines( self, rows ):
        assert len( rows[ 0 ] ) == 2
        maxLengthFirstColumn = max( len( r[ 0 ] ) for r in rows )
        firstColumSize = maxLengthFirstColumn + self._args.minimumSpaceBetweenColumns
        return [ r[ 0 ] + ' ' * ( firstColumSize - len( r[ 0 ] ) ) + r[ 1 ] for r in rows ]
