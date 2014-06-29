#TODO: virtual detection
class FunctionDecomposition:
    def __init__( self, name, parameters, text, returnType, static, const, templatePrefix = "" ):
        self.name = name
        self.parameters = parameters
        self.text = text
        self.returnType = returnType
        self.static = static
        self.templatePrefix = templatePrefix
        self.const = const
        self.virtual = False

    def parametersFullSpec( self ):
        return ", ".join( [ p[ 'text' ] for p in self.parameters ] )

    def parametersForwardingList( self ):
        return ", ".join( [ p[ 'name' ] for p in self.parameters ] )

    def returnTypeIsVoid( self ):
        return self.returnType == "void"

    def stringReturnIfNotVoid( self ):
        return "" if self.returnTypeIsVoid() else "return "

    def stringStaticIfStatic( self ):
        return "static " if self.static else ""

    def stringStaticInlineIfStatic( self ):
        return "static inline " if self.static else ""
