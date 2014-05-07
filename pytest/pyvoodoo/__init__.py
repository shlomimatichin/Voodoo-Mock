from pyvoodoo.scenario import Scenario, ScenarioIterator
from pyvoodoo.ultimateobject import UltimateObject
from pyvoodoo.ultimateobject import UltimateObjectNC
from pyvoodoo.ultimateclass import UltimateClass
from pyvoodoo.expectations import *
from pyvoodoo.threadedhook import *
import sys

def _pleaseDontMock( message ):
	raise Exception( message )
_exceptions = {
		'threading': lambda: sys.modules[ 'threading' ].voodooAddAttribute( '_shutdown', lambda: 0 ),
		'os': lambda: _pleaseDontMock( "Os is dangerous to mock: logging and other modules use it. Please override specific functions" )
}

def castVoodooUponModule( module ):
	assert isinstance( module , str )
	obj = UltimateObject( module )
	sys.modules[ module ] = obj
	if module in _exceptions:
		_exceptions[ module ]()
	ancestorModuleNameParts = module.split( "." ) [ : -1 ]
	moduleName = module.split( "." ) [ -1 ]
	if len( ancestorModuleNameParts ) > 0:
		ancestorModuleName = ".".join( ancestorModuleNameParts )
		ancestorModule = __import__( ancestorModuleName, globals(), locals(), [ '__name__' ], -1 )
		ancestorModule.__dict__[ moduleName ] = obj

def castVoodooUponClass( classPath ):
	parts = classPath.split( "." )
	module = parts[ : -1 ]
	ultimateObjects = []
	className = parts[ -1 ]
	while True:
		if len( module ) == 0:
			raise Exception( "no exsiting module for '%s'" % classPath )
		moduleName = ".".join( module )
		if moduleName in sys.modules:
			break
		ultimateObjects.push( module.pop() )
	if not isinstance( sys.modules[ moduleName ] , UltimateObject ):
		raise Exception( "'%s' is in a non voodoo module '%s'" % ( classPath , path ) )
	current = sys.modules[ moduleName ]
	while len( ultimateObjects ) > 0:
		current.voodooAddAttribute( ultimateObjects[ 0 ] , UltimateObject( current._voodooPath + "." + ultimateObjects[ 0 ] ) )
		current = current.__dict__[ ultimateObjects[ 0 ] ]
		ultimateObjects.pop( 0 )
	current.voodooAddAttribute( className , UltimateClass( current._voodooPath + "." + className ) )
