import inspect

def stackTrace( ** kwargs ):
	if 'removeFrames' not in kwargs:
		kwargs[ 'removeFrames' ] = 0
	if 'stack' not in kwargs:
		kwargs[ 'stack' ] = inspect.stack()
	stack = kwargs[ 'stack' ][ 1 + kwargs[ 'removeFrames' ] : ]
	result = "STACK TRACE:\n"
	for frame in stack:
		result += "%s:%d: from Here\n" % ( frame[ 1 ] , frame[ 2 ] )
	result += "STACK TRACE END\n"
	return result
