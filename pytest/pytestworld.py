import PyTest;

from glob import glob;
from imp import load_source;
from os import path;
from types import ClassType;
from exceptions import SyntaxError;
from sys import stderr, exc_info;

import fixtures

class PyTestWorld:
    def __init__( self, places ):
        PyTest.suiteClasses = {};
        self._loadFailed = False;
        self._places = places;
        self._collectSuites();

    def loadFailed( self ):
        return self._loadFailed;

    def setUp( self ):
        pass ;

    def tearDown( self ):
        pass ;

    def _collectSuites( self ):
        for place in self._places:
            files = glob( place );
            for fullPath in files:
                self._collectSuitesFromFile( fullPath );

    def _collectSuitesFromFile( self, fullPath ):
        mod = self._loadModule( fullPath );
        if mod is None: return ;
        for ( key, value ) in mod.__dict__.items():
            if self._isTestClass( value ):
                PyTest.suiteClasses[ key ] = value;

    def _isTestClass( self, value ):
        if not type(value) in [ClassType, type]:
            return False;
        if value.__name__ == "PyTestSuite":
            return False;
        basenames = [ base.__name__ for base in value.__bases__ ];
        return ("PyTestSuite" in basenames);

    def _loadModule( self, fullPath ):
        ( head, tail ) = path.split( fullPath );
        ( basename, ext ) = path.splitext( tail );
        try:
            return load_source( basename, fullPath );
        except SyntaxError, e:
            PyTest.tracker.loadSuiteFailed( e.filename, e.lineno,
                                            "Syntax error at offset %s" % str( e.offset ) );
            PyTest.tracker.caughtException( exc_info()[2] );
        except Exception, e:
            PyTest.tracker.loadSuiteFailed( fullPath, -1, "Exception: <%s> while loading <%s>" % ( str(e) , basename ) );
            PyTest.tracker.caughtException( exc_info()[2] );
        except:
            stderr.write( fullPath + ":-1: Unknown exception" );

        self._loadFailed = True;
        return None;

    def description( self ):
        return "PyTest";

__all__ = [ "PyTestWorld" ];
