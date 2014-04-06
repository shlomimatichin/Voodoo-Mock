import parsecppfunctionsignature
import re
import tab
import formatcolums
import parsecppmemberlist

class ConstructorReferenceArgumentsCPP:
    def __init__( self, input, args ):
        self._input = input
        self._args = args
        self._tab = tab.Tab( args )
        self._parse = parsecppfunctionsignature.ParseCPPFunctionSignature( input )

    def format( self ):
        return self._input + \
                self._formatInitializationList() + \
                self._indentation() + '{}\n\n' + \
                "private:\n" + \
                self._formatMembers()

    def _formatMembers( self ):
        membersRaw = self._tab.produce( self._args.tabSize ) + ";\n".join( r[ 0 ] + ' ' + r[ 1 ] for r in self._parse.argumentsTwoColumTable() ) + ";\n"
        parse = parsecppmemberlist.ParseCPPMemberList( membersRaw );
        return formatcolums.FormatColums( parse, self._args ).format()

    def _indentation( self, add = "" ):
        spacePrefix = re.match( r"\s*", self._input ).group( 0 )
        size = self._tab.roundUp( self._tab.countChars( spacePrefix + add ) )
        return self._tab.produce( size )

    def _formatInitializationList( self ):
        return ",\n".join( self._indentation( '\t\t' ) + "_%s( %s )" % ( p, p ) for p in self._parameters() ) + '\n'

    def _parameters( self ):
        return [ re.search( r"\w+", r[ 1 ] ).group( 0 ) for r in self._parse.rows() ]
