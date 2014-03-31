from imp import new_module;
from sys import modules;
PyTest = modules["PyTest"] = new_module( "PyTest" );

from pytestsuite import *;
from pytestworld import *;
from pytesttracker import *;
from pytestverbosecui import *;
from pytestsimplecui import *;
from pytestmock import *;

class PyTestRunner:
    def __init__( self, places, singleTest ):
        self._singleTest = singleTest
        self._world = PyTestWorld( places );
        self._buildSuites();

    def run( self ):
        if self._world.loadFailed():
            return ;
        self._runSuites();

    def _buildSuites( self ):
        PyTest.suites = [];
        for ( suiteName, suiteClass ) in PyTest.suiteClasses.items():
            PyTest.suites.append( suiteClass() );

    def _runSuites( self ):
        self._setUpWrapper();
        self._runSuiteWrapper();
        self._tearDownWrapper();

    def _setUpWrapper( self ):
        PyTest.tracker.enterWorld( self._world.description() );
        self._world.setUp();

    def _runSuiteWrapper( self ):
        for suite in PyTest.suites:
            if self._singleTest:
                suite._runSingleTest( self._singleTest )
            else:
                suite._run();

    def _tearDownWrapper( self ):
        self._world.tearDown();
        PyTest.tracker.leaveWorld( self._world.description() );

def run( argv ):
    if len( argv ) > 2 and argv[1] == "--verbose":
        PyTest.ui = PyTestVerboseCui();
        del argv[1];
    elif len( argv ) > 2 and argv[1] == "--cui":
        PyTest.ui = PyTestSimpleCui();
        del argv[1];
    else:
        PyTest.ui = PyTestSimpleGui();
    SINGLE_TEST = "--singleTest="
    if len( argv ) > 2 and argv[ 1 ].startswith( SINGLE_TEST ):
        singleTest = argv[ 1 ][ len( SINGLE_TEST ) : ]
    else:
        singleTest = None
    places = argv[1:];
    PyTest.tracker = PyTestTracker();
    PyTest.mockTable = PyTestMockTable();
    PyTest.runner = PyTestRunner( places, singleTest );
    PyTest.runner.run();
    if PyTest.tracker._testsFailed > 0:
        exit( 1 )

__all__ = [ "PyTestRunner", "run" ];

if __name__ == "__main__":
    from sys import argv;
    run( argv )
