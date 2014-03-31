import PyTest;

class PyTestUi:
    def loadSuiteFailed( self, where, message ):
        pass ;

    def caughtException( self, traceback ):
        pass ;

    def writeMessage( self, fullPath, lineNum, message ):
        pass ;

    def enterWorld( self, description ):
        pass ;

    def enterSuite( self, description ):
        pass ;

    def enterTest( self, description ):
        pass ;

    def failTest( self, description, where, traceback ):
        pass ;

    def leaveTest( self, description ):
        pass ;

    def leaveSuite( self, description ):
        pass ;

    def leaveWorld( self, description ):
        pass ;

__all__ = [ "PyTestUi" ];
