class Tab:
    def __init__( self, args ):
        self._args = args

    def roundUp( self, value ):
        reminder = value % self._args.tabSize
        if reminder == 0:
            return value
        return value + self._args.tabSize - reminder

    def countChars( self, string ):
        result = 0
        string = [ c for c in string ]
        while len( string ) > 0:
            char = string.pop( 0 )
            if char == '\t':
                result = self.roundUp( result + 1 )
            else:
                result += 1
        return result

    def produce( self, size ):
        assert size % self._args.tabSize == 0
        if self._args.indentWithTabs:
            return '\t' * ( size / self._args.tabSize )
        else:
            return ' ' * size
