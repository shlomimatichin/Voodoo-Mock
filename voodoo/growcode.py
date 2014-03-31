_DEFAULT_SNIPPET = 1000000

class GrowCode:
	def __init__( self ):
		self._snippets = [ "" ]
		self._indents = [ 0 ]
		self._defaultSnippet = 0

	def _snippetOrDefault( self , snippet ):
		if snippet == _DEFAULT_SNIPPET:
			return self._defaultSnippet
		else:
			return snippet

	def lineOut( self , text , snippet = _DEFAULT_SNIPPET ):
		indent = "\t" * self._indents[ self._snippetOrDefault( snippet ) ]
		indented = indent + ( "\n" + indent ).join( text.split( "\n" ) ) + "\n"
		self._snippets[ self._snippetOrDefault( snippet ) ] += indented

	def increaseIndent( self , snippet = _DEFAULT_SNIPPET ):
		self._indents[ self._snippetOrDefault( snippet ) ] += 1

	def decreaseIndent( self , snippet = _DEFAULT_SNIPPET ):
		assert self._indents[ self._snippetOrDefault( snippet ) ] > 0
		self._indents[ self._snippetOrDefault( snippet ) ] -= 1

	def newSnippet( self , snippet = _DEFAULT_SNIPPET ):
		snippet = self._snippetOrDefault( snippet )
		self._snippets.insert( snippet + 1 , "" )
		self._indents.insert( snippet + 1 , self._indents[ snippet ] )
		if self._defaultSnippet >= snippet:
			self._defaultSnippet += 1
		return snippet

	def result( self ):
		return "".join( self._snippets )
