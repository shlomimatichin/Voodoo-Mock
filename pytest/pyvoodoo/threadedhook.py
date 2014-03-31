import threading

_allExceptions = {}
_threads = []

def voodooAssertAllThreadsCompletedSuccessfully():
	assert _threads == []
	assert _allExceptions == {}

def voodooAssertThreadCompletedWithException( thread ):
	assert thread in _allExceptions

VoodooEvent = threading.Event

class VoodooThreadedHook( threading.Thread ):
	def __init__( self, callback ):
		self._callback = callback
		threading.Thread.__init__( self, name = "VoodooThreadedHook" )
		self.setDaemon( True )

	def __call__( self ):
		_threads.append( self )
		self.start()

	def run( self ):
		try:
			self._callback()
		except Exception, e:
			_allExceptions[ self ] = e
		finally:
			_threads.remove( self )
