from pytestsuite import *

class ScenarioIterator:
	def __init__(	self,
					story = 'DEFAULT',
					expectationPath = None,
					expectationBookmark = None,
					lastExpectation = False,
					pos = None ):
		assert sum( [ int( bool( x ) ) for x in
						[ expectationPath, expectationBookmark, lastExpectation, pos ] ] ) == 1
		self._story = story
		if lastExpectation:
			self._expectation = self.story()[ -1 ]
			return
		if expectationPath is not None:
			self._lookForExpectationByPath( expectationPath )
		elif expectationBookmark is not None:
			self._lookForExpectationByBookmark( expectationBookmark )
		else:
			self._expectation = self.story()[ pos ]

	def __add__( self, step ):
		self._expectation = self.story()[ self.pos() + step ]
		return self

	def story( self ):
		if self._story == 'ALWAYS':
			return Scenario._it._always
		return Scenario._it._stories[ self._story ]

	def pos( self ):
		return self.story().index( self.expectation() )

	def expectation( self ):
		return self._expectation

	def _lookForExpectationByPath( self, path ):
		for expectation in self.story():
			if expectation._voodooPath == path:
				self._expectation = expectation
				return
		raise Exception( "Expectation '%s' not found in story '%s'" % (
			path, self._story ) )

	def _lookForExpectationByBookmark( self, bookmark ):
		for expectation in self.story():
			if expectation._voodooBookmark == bookmark:
				self._expectation = expectation
				return
		raise Exception( "Expectation with bookmark '%s' not found in story '%s'" % (
					bookmark, self._story ) )

class Scenario:
	_it = None

	def __init__( self ):
		self._stories = { 'DEFAULT':[] }
		self._storiesNames = [ 'DEFAULT' ]
		self._always = []
		self._running = False
		TS_ASSERT( Scenario._it is None )
		Scenario._it = self

	def finished( self ):
		self._backupStoriesToOriginalStories()
		for story in self._stories:
			if len( self._stories[ story ] ) > 0:
				formattedStory = "\n".join( [ x.voodooFormat() for x in \
						self._originalStories[ story ][ : self._currentExpectationNumber( story ) ] ] )
				TS_FAIL( "Story '%s' was not completed; at expectation %d; %s\nStory: %s" %
							(	story ,
								self._currentExpectationNumber( story ),
								self._stories[ story ][ 0 ].voodooFormat(),
								formattedStory ) )
		Scenario._it = None

	def _makeIterator( self, iterator, kwargs ):
		if iterator is None:
			assert len( kwargs ) > 0
			return ScenarioIterator( ** kwargs )
		else:
			assert len( kwargs ) == 0
			return iterator

	def truncateStoryInclusive( self, iterator = None, ** kwargs ):
		iterator = self._makeIterator( iterator, kwargs )
		del iterator.story()[ iterator.pos() : ]

	def truncateStoryExclusive( self, iterator = None, ** kwargs ):
		iterator = self._makeIterator( iterator, kwargs )
		del iterator.story()[ iterator.pos() + 1 : ]

	def makeExpectationRaise( self, exception, iterator = None, ** kwargs ):
		iterator = self._makeIterator( iterator, kwargs )
		iterator.expectation()._voodooException = exception

	def addHookToExistingExpectation( self, voodooHook, iterator = None, ** kwargs ):
		iterator = self._makeIterator( iterator, kwargs )
		assert iterator.expectation()._voodooHook is None
		iterator.expectation()._voodooHook = voodooHook

	def overrideHookOfExistingExpectation( self, hook, iterator = None, ** kwargs ):
		iterator = self._makeIterator( iterator, kwargs )
		assert iterator.expectation()._voodooHook is not None
		iterator.expectation()._voodooHook = hook

	def makeExpectationRaiseAndTruncateStory( self, exception, iterator = None, ** kwargs ):
		iterator = self._makeIterator( iterator, kwargs )
		assert iterator.expectation().__class__.__name__ != 'RaisingCall'
		self.makeExpectationRaise( exception = exception, iterator = iterator )
		self.truncateStoryExclusive( iterator = iterator )

	def removeExpectation( self, iterator = None, ** kwargs ):
		iterator = self._makeIterator( iterator, kwargs )
		iterator.story().remove( iterator.expectation() )

	def insertExpecationAfter( self, expectation, iterator = None, ** kwargs ):
		iterator = self._makeIterator( iterator, kwargs )
		iterator.story().insert( iterator.pos() + 1, expectation )

	def overrideExpectation( self, expectation, iterator = None, ** kwargs ):
		iterator = self._makeIterator( iterator, kwargs )
		iterator.story()[ iterator.pos() ] = expectation

	def insertExpecationBefore( self, expectation, iterator = None, ** kwargs ):
		iterator = self._makeIterator( iterator, kwargs )
		iterator.story().insert( iterator.pos(), expectation )

	def specificFinished( self, names ):
		if not isinstance( names, list ):
			names = [ names ]
		for storyName in names:
			story = self._stories[ storyName ]
			if len( story ) > 0:
				formattedStory = "\n".join( [ x.voodooFormat() for x in \
						self._originalStories[ storyName ][ : self._currentExpectationNumber( storyName ) ] ] )
				TS_FAIL( "Story '%s' was not completed; at expectation %d; %s\nStory: %s" %
							(	storyName ,
								self._currentExpectationNumber( storyName ),
								story[ 0 ].voodooFormat(),
								formattedStory ) )
	
	def partiallyFinished( self, names ):
		self.specificFinished( names )
		Scenario._it = None

	def specificNotFinished( self, names ):
		if not isinstance( names, list ):
			names = [ names ]
		for storyName in names:
			story = self._stories[ storyName ]
			if len( story ) == 0:
				TS_FAIL( "Story '%s' was completed" % storyName )

	def _currentExpectationNumber( self , story ):
		return len( self._originalStories[ story ] ) - \
					len( self._stories[ story ] )

	def _backupStoriesToOriginalStories( self ):
		if not self._running:
			self._running = True
			self._originalStories = {}
			for story in self._stories:
				self._originalStories[ story ] = self._stories[ story ][ 0 : ]

	def _completeExpectation( self, expectation ):
		for storyName, story in self._stories.iteritems():
			if len( story ) > 0 and expectation is story[ 0 ]:
				story.pop( 0 )
				return
		for always in self._always:
			if expectation is always:
				return
		TS_FAIL( "completed unknown expectation" )

	def _lookupExpectationsInScenario( self , path ):
		self._backupStoriesToOriginalStories()
		errorMessage = "Event '%s' is not in any of the stories;\n" % path
		expectations = []
		for storyName in reversed( self._storiesNames ):
			story = self._stories[ storyName ]
			if len( story ) > 0 :
				if path == story[ 0 ]._voodooPath:
					expectations.append( story[ 0 ] )
				else:
					errorMessage += "\tStory; '%s';%d expects '%s'\n" % (
								storyName ,
								self._currentExpectationNumber( storyName ) ,
								story[ 0 ]._voodooPath )
		if expectations != []:
			return expectations
		for expectation in reversed( self._always ):
			if path == expectation._voodooPath:
				expectations.append( expectation )
		if len( expectations ) == 0:
			TS_FAIL( errorMessage )
		return expectations

	def addAlways( self , expectation ):
		TS_ASSERT( not self._running )
		expectation._voodooStory = "ALWAYS"
		self._always.append( expectation )

	def addToStory( self , story , expectation ):
		TS_ASSERT( not self._running );
		expectation._voodooStory = story
		if not self._stories.has_key( story ):
			self._stories[ story ] = []
			self._storiesNames.append( story )
		self._stories[ story ].append( expectation )

	def add( self , expectation ):
		self.addToStory( 'DEFAULT' , expectation )

	def __lshift__( self , expectation ):
		self.add( expectation )
		return self

	def formatTraceStory( self, story = 'DEFAULT' ):
		result = []
		for expectation in self._stories[ story ]:
			index = self._stories[ story ].index( expectation )
			result.append( ( "%d: " % index ) + expectation.formatTrace() )
		return "\n".join( result )

	def formatTrace( self ):
		result = []
		for story in self._stories:
			storyTrace = self.formatTraceStory( story )
			indented = "Story '%s':\n\t" % story + storyTrace.replace( "\n", "\n\t" )
			result.append( indented )
		return "\n".join( result )

def lookupExpectationsInScenario( path ):
	TSM_ASSERT( "Scenario object does not exist, while looking for %s" % path,
				Scenario._it is not None )
	return Scenario._it._lookupExpectationsInScenario( path )

def completeExpectation( expectation ):
	Scenario._it._completeExpectation( expectation )
