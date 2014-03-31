from pyvoodoo.ultimateobject import UltimateObject
from pyvoodoo.scenario import lookupExpectationsInScenario, completeExpectation

class _UltimateClass( UltimateObject ):
	def __init__( self , * args , ** kwargs ):
		expectation = lookupExpectationsInScenario( self._VOODOO_PATH )[ 0 ]
		expectation.compare( args, kwargs )
		completeExpectation( expectation )
		self.__dict__[ '_voodooPath' ] = expectation.voodooPath()
		self.voodooObjects.append( self )
		expectation.returnValue()

	def __setattr__( self , name , value ):
		self.__dict__[ name ] = value

def UltimateClass( voodooPath ):
	class NewCopy( _UltimateClass ):
		pass
	NewCopy._VOODOO_PATH = voodooPath
	NewCopy.voodooObjects = []
	return NewCopy
