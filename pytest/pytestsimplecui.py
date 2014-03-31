import PyTest;

from pytestui import *;
from sys import stderr;
from traceback import format_tb;

class PyTestSimpleCui(PyTestUi):
    def __init__( self ):
        self.currentTest = "";

    def loadSuiteFailed( self, suitePath, lineNum, message ):
        stderr.write( "%s:%d: Failed to load suite: %s\n" %
                      ( suitePath, lineNum, message ) );

    def caughtException( self, traceback ):
        lines = format_tb( traceback );
        stderr.write( "\n%s\n" % "\n".join( lines ) );

    def writeMessage( self, fullPath, lineNum, message ):
        stderr.write( "\n%s:%d: %s\n" %
                      ( fullPath, lineNum, message ) );

    def enterWorld( self, description ):
        stderr.write( "Running %d tests:\n" % self._countTests() );

    def failTest( self, fullPath, lineNum, message ):
        stderr.write( "\n%s:%d: %s: %s\n" %
                      ( fullPath, lineNum, self.currentTest, message ) );

    def enterTest( self, description ):
        self.currentTest = description;
        stderr.write( "." );

    def leaveWorld( self, description ):
        if ( PyTest.tracker.testsFailed() == 0 ):
            stderr.write( "\nOK!\n" );
        else:
            stderr.write( "\nFailed %d tests\n" % PyTest.tracker.testsFailed() );

    def _countTests( self ):
        numTests = 0;
        for suite in PyTest.suites:
            numTests += suite._numTests();
        return numTests;

__all__ = [ "PyTestSimpleCui" ];
