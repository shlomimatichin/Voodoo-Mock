import PyTest

from pytestui import *
from sys import stderr
from traceback import format_tb

class PyTestVerboseCui(PyTestUi):
    def __init__( self ):
        self.currentTest = ""

    def loadSuiteFailed( self, suitePath, lineNum, message ):
        stderr.write( "%s:%s: Failed to load suite: %s\n" %
                      ( suitePath, lineNum, message ) )

    def caughtException( self, traceback ):
        lines = format_tb( traceback )
        stderr.write( "\n%s\n" % "\n".join( lines ) )

    def writeMessage( self, fullPath, lineNum, message ):
        stderr.write( "\n%s:%d: %s\n" %
                      ( fullPath, lineNum, message ) )

    def enterWorld( self, description ):
        stderr.write( "COUNT %d\n" % self._countTests() )

    def failTest( self, fullPath, lineNum, message ):
        stderr.write( "\n%s:%d: %s: %s\n" %
                      ( fullPath, lineNum, self.currentTest, message ) )

    def enterSuite( self, description ):
        stderr.write( "SUITE '%s'\n" % description )

    def enterTest( self, description ):
        stderr.write( "TEST '%s'\n" % description )
        self.currentTest = description

    def leaveWorld( self, description ):
        if ( PyTest.tracker.testsFailed() == 0 ):
            stderr.write( "OK!\n" )
        else:
            stderr.write( "Failed %d tests\n" % PyTest.tracker.testsFailed() )

    def _countTests( self ):
        numTests = 0
        for suite in PyTest.suites:
            numTests += suite._numTests()
        return numTests

__all__ = [ "PyTestVerboseCui" ]
