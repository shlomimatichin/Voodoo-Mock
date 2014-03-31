from pytestsuite import *
from pyvoodoo.ultimateobject import UltimateObject
from voodooexception import VoodooException
import pprint

class Call:
	def __init__(	self,
					path,
					paramExpectations,
					returnValue,
					kwargsExpectations = {},
					hook = None,
					bookmark = None ):
		self._voodooHook = hook
		assert isinstance( paramExpectations , list ) or isinstance( paramExpectations , tuple )
		self._voodooPath = path
		self._voodooExpectationType = "Call"
		self._voodooParamExpectations = paramExpectations
		self._voodooKwargsExpectations = kwargsExpectations
		self._voodooReturnValue = returnValue
		self._voodooException = None
		self._voodooBookmark = bookmark

	def formatTrace( self ):
		args = [ p.formatTrace() for p in self._voodooParamExpectations ]
		kwargs = [ str( ( p, self._voodooKwargsExpectations[ p ].formatTrace() ) ) for p in self._voodooKwargsExpectations ]
		return ( "%s: '%s'\n\t" % ( self._voodooExpectationType, self._voodooPath ) +
				"\n\t".join( args + kwargs ) ).strip()

	def voodooFormat( self ):
		return self._voodooPath

	def compare( self , args , kwargs ):
		expectedNumOfParams = len( self._voodooParamExpectations ) + \
												len( self._voodooKwargsExpectations )
		if len( args ) != len( self._voodooParamExpectations ):
			raise VoodooException(	"Wrong number of parameters while calling %s; "
						 			"expected %d parameters, found %d" % (
									self._voodooPath ,
									len( self._voodooParamExpectations ),
									len( args ) ) )
		if len( kwargs ) != len( self._voodooKwargsExpectations ):
			raise VoodooException(	"Wrong number of kwargs parameters while calling %s; "
						 			"expected %d kwargs parameters, found %d" % (
									self._voodooPath ,
									len( self._voodooKwargsExpectations ),
									len( kwargs ) ) )
		for i in range( len( self._voodooParamExpectations ) ):
			if not hasattr( self._voodooParamExpectations[ i ], 'compare' ):
				message = ( "ERROR: the expectation does not have a 'compare' method: type %s;"
							"perhaps you forgot 'ParamEquals'? " ) % type( self._voodooParamExpectations[ i ] )
				print "PyVoodoo:", message
				raise VoodooException( message )
			self._voodooParamExpectations[ i ].compare( args[ i ] )

		TS_ASSERT_EQUALS( sorted( kwargs.keys() ),
						sorted( self._voodooKwargsExpectations.keys() ) )
		for key in kwargs.keys():
			if not hasattr( self._voodooKwargsExpectations[ key ], 'compare' ):
				message = ( "ERROR: the expectation does not have a 'compare' method: type %s, key %s;"
							"perhaps you forgot 'ParamEquals'? " ) % (
									type( self._voodooKwargsExpectations[ key ] ),
									key )
				print "PyVoodoo:", message
				raise VoodooException( message )
			self._voodooKwargsExpectations[ key ].compare( kwargs[ key ] )

	def returnValue( self ):
		if self._voodooHook is not None:
			if isinstance( self._voodooHook, list ) or isinstance( self._voodooHook, tuple ):
				self._voodooHook[ 0 ]( * self._voodooHook[ 1 : ] )
			else:
				self._voodooHook()
		if self._voodooException is not None:
			raise self._voodooException
		return self._voodooReturnValue

	def voodooPath( self ):
		return self._voodooPath

class RaisingCall( Call ):
	def __init__( self , path , paramExpectations , exception, kwargsExpectations = {}, hook = None, bookmark = None ):
		Call.__init__( self , path , paramExpectations , None, kwargsExpectations, hook, bookmark )
		self._voodooException = exception
		self._voodooExpectationType = "RaisingCall"

class CallbackCall( Call ):
	def __init__( self , path , paramExpectations , callback , kwargsExpectations = {} ):
		Call.__init__( self , path , paramExpectations , None, kwargsExpectations )
		self._voodooCallback = callback
		self._voodooExpectationType = "CallbackCall"

	def returnValue( self ):
		Call.returnValue( self )
		return self._voodooCallback()

class Instantiate( Call ):
	def __init__( self , * args ):
		Call.__init__( self , * args )
		self.voodooPath = self.returnValue
		self.returnValue = None

class ParamBase:
	def formatTrace( self ):
		return "%s: %s" % ( self._voodooExpectationType, self.formatValueTrace() )

	def formatValueTrace( self ):
		return "NA"

class ParamEquals( ParamBase ):
	def __init__( self , value ):
		self._voodooValue = value
		self._voodooExpectationType = "ParamEquals"

	def compare( self , value ):
		if value != self._voodooValue:
			raise VoodooException( "Parameters not equal (%s != %s)" % ( pprint.pformat( value ), pprint.pformat( self._voodooValue ) ) )

	def formatValueTrace( self ):
		return str( self._voodooValue )

class ParamFloatEquals( ParamBase ):
	def __init__( self , value ):
		self._voodooValue = value
		self._voodooExpectationType = "ParamFloatEquals"

	def compare( self , value ):
		if value / self._voodooValue < 0.999999 or value / self._voodooValue > 1.000001:
			raise VoodooException( "Parameters not (float) equal (%s != %s)" % ( value, self._voodooValue ) )

	def formatValueTrace( self ):
		return str( self._voodooValue )

class ParamDiffers( ParamBase ):
	def __init__( self , value ):
		self._voodooValue = value
		self._voodooExpectationType = "ParamDiffers"

	def compare( self , value ):
		if value == self._voodooValue:
			raise VoodooException( "Parameters equal (%s == %s)" % ( value, self._voodooValue ) )

class ParamMatchesRE( ParamBase ):
	def __init__( self, expression ):
		self._voodooExpression = expression
		self._voodooExpectationType = "ParamMatchesRE"

	def compare( self, value ):
		import re
		if re.search( self._voodooExpression, value ) is None:
			raise VoodooException( "Parameter '%s' does not match regular expression '%s'" % ( value, self._voodooExpression ) )

class ParamIgnore( ParamBase ):
	def __init__( self ):
		self._voodooExpectationType = "ParamIgnore"

	def compare( self , value ):
		pass

class ParamSave( ParamBase ):
	def __init__( self ):
		self._voodooExpectationType = "ParamSave"

	def compare( self, value ):
		self.value = value

class ParamTrue( ParamBase ):
	def __init__( self ):
		self._voodooExpectationType = "ParamTrue"

	def compare( self , value ):
		if not value:
			raise VoodooException( "Parameter (%s) expected to evaluate to True" % pprint.pformat( value ) )

class ParamIs( ParamBase ):
	def __init__( self , value ):
		self._voodooValue = value
		self._voodooExpectationType = "ParamIs"

	def compare( self , value ):
		if value is not self._voodooValue:
			raise VoodooException( "Parameter (%s) expected to be (%s)" % ( pprint.pformat( value ), pprint.pformat( self._voodooValue ) ) )

class ParamFalse( ParamBase ):
	def __init__( self ):
		self._voodooExpectationType = "ParamFalse"

	def compare( self , value ):
		if value:
			raise VoodooException( "Parameter (%s) expected to evaluate to False" % pprint.pformat( value ) )

class ParamIsUltimateObject( ParamBase ):
	def __init__( self , voodooPath ):
		self._voodooPath = voodooPath
		self._voodooExpectationType = "ParamIsUltimateObject"

	def compare( self , candidate ):
		if not isinstance( candidate, UltimateObject ):
			raise VoodooException( "Parameter (%s) is not an UltimateObject" % pprint.pformat( candidate ) )
		if candidate.voodooPath() != self._voodooPath:
			raise VoodooException( "UltimateObject's path (%s) is not as expected (%s)" % ( pprint.pformat( candidate ), pprint.pformat( self._voodooPath ) ) )

	def formatValueTrace( self ):
		return self._voodooPath

class ParamPredicate( ParamBase ):
	def __init__( self , predicate, * args ):
		self._predicate = predicate
		self._args = args
		self._voodooExpectationType = "ParamPredicate"

	def compare( self, candidate ):
		TSM_ASSERT( self._predicate, self._predicate( candidate, * self._args ) )

class ParamCallback( ParamBase ):
	def __init__( self, callback, * args ):
		self._callback = callback
		self._args = args
		self._voodooExpectationType = "ParamCallback"

	def compare( self, candidate ):
		self._callback( candidate, * self._args )

class ParamInstance( ParamBase ):
	def __init__( self, object ):
		self._object = object
		self._voodooExpectationType = "ParamInstance"

	def compare( self, object ):
		TS_ASSERT( isinstance( object, self._object ) )

class SetAttrEquals:
	def	__init__( self , value ):
		self._voodooValue = value
		self._voodooExpectationType = "SetAttrEquals"

	def compare( self , value ):
		TS_ASSERT_EQUALS( value , self._voodooValue )
	
class SetAttrIs:
	def __init__( self , value ):
		self._voodooValue = value
		self._voodooExpectationType = "SetAttrIs"

	def compare( self , value ):
		TS_ASSERT( value is self._voodooValue )

__all__ = [
		"Call" ,
		"RaisingCall" ,
		"CallbackCall" ,
		"Instantiate" ,
		"ParamSave" ,
		"ParamTrue" ,
		"ParamFalse" ,
		"ParamIs" ,
		"ParamEquals" ,
		"ParamFloatEquals" ,
		"ParamDiffers" ,
		"ParamMatchesRE" ,
		"ParamIgnore" ,
		"ParamPredicate" ,
		"ParamCallback" ,
		"ParamIsUltimateObject" ,
		"ParamInstance",
		"SetAttrEquals" ,
		"SetAttrIs"
	]
