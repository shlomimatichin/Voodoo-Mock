from pytestsuite import *
from pyvoodoo.scenario import lookupExpectationsInScenario, completeExpectation
from pyvoodoo.voodooexception import VoodooException

class UltimateObject:
	def __init__( self, path, ** attributes ):
		self.__dict__[ "_voodooPath" ] = path
		for k, v in attributes.iteritems():
			self.__dict__[ k ] = v

	def voodooPath( self ):
		return self.__dict__[ '_voodooPath' ]

	def voodooAddAttribute( self , name , value ):
		self.__dict__[ name ] = value

	def __hash__( self ):
		return id( self ).__hash__()

	def __str__( self ):
		return "<UltimateObject '%s'>" % self.voodooPath()

	def __repr__( self ):
		return "<UltimateObject '%s'>" % self.voodooPath()

	def __getattr__( self , name ):
		if name == "__path__":
			return "UltimateObject module"
		voodooPath = self.__dict__[ "_voodooPath" ]
		return UltimateObject( voodooPath + "." + name )

	def __setattr__( self , name , value ):
		voodooPath = self.__dict__[ "_voodooPath" ]
		expectation = lookupExpectationsInScenario( voodooPath + "." + name )[ 0 ]
		TS_ASSERT( expectation._voodooExpectationType.startsWith(
															"SetAttr" ) );
		expectation.compare( value )
		completeExpectation( expectation )

	def __call__( self , * args , ** kwargs ):
		voodooPath = self.__dict__[ "_voodooPath" ]
		expectations = lookupExpectationsInScenario( voodooPath )
		TS_ASSERT_LESS_THAN( 0 , expectations )
		exceptions = []
		for expectation in expectations:
			try:
				expectation.compare( args , kwargs )
				completeExpectation( expectation )
				return expectation.returnValue()
			except VoodooException, e:
				exceptions.append( e )
		try:
			paramsRepr = str( ( args , kwargs ) )
		except:
			paramsRepr = "<Params unreprable>"
		TS_FAIL( "No expectation matched '%s( %s )'; Errors; %s" % (
					self._voodooPath ,
					paramsRepr ,
					"\n".join( [ str( e ) for e in exceptions ] ) ) )
