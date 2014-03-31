import PyTest;
from pystacktrace import *;

class PyTestTracker:
    def __init__( self ):
        self._testsRun = 0;
        self._testsFailed = 0;
        if PyTest.ui is None:
            from pytestui import PyTestUi;
            PyTest.ui = PyTestUi();

    def loadSuiteFailed( self, suitePath, lineNum, message ):
        self._testsFailed += 1;
        PyTest.ui.loadSuiteFailed( suitePath, lineNum, message );

    def caughtException( self, traceback ):
        PyTest.ui.caughtException( traceback );

    def writeMessage( self, message, stackFrame ):
        ( fullPath, lineNum ) = self.parseStackFrame( stackFrame );
        PyTest.ui.writeMessage( fullPath, lineNum, message );

    def enterWorld( self, description ):
        PyTest.ui.enterWorld( description );

    def enterSuite( self, description ):
        PyTest.ui.enterSuite( description );

    def enterTest( self, description ):
        self._testsRun = self._testsRun + 1;
        PyTest.ui.enterTest( description );

    def failTest( self, message, stack ):
        self._testsFailed += 1;
        ( fullPath, lineNum ) = self.findNonPytestFrame( stack );
        message += "\n" + stackTrace( stack = stack );
        PyTest.ui.failTest( fullPath, lineNum, message );

    def leaveTest( self, description ):
        PyTest.ui.leaveTest( description );

    def leaveSuite( self, description ):
        PyTest.ui.leaveSuite( description );

    def leaveWorld( self, description ):
        PyTest.ui.leaveWorld( description );

    def testsRun( self ):
        return self.testsRun;

    def testsFailed( self ):
        return self._testsFailed;

    def parseStackFrame( self, stackFrame ):
        ( frame, filePath, lineNumber, functionName, lines, lineIndex ) = stackFrame;
        return ( filePath, lineNumber );

    def findNonPytestFrame( self, stack ):
        for frame in stack:
            if 'pytest' not in frame[ 1 ]:
                return ( frame[ 1 ], frame[ 2 ] )
        return ( stack[ -1 ][ 1 ], stack[ -1 ][ 2 ] )

__all__ = [ "PyTestTracker" ];
