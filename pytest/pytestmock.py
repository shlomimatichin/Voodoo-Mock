import PyTest;
import sys;

class DefaultFunctionCall:
    def __init__( self, unitName, functionName ):
        self.unitName = unitName;
        self.functionName = functionName;

    def missingImplementation( self, *args ):
        raise Exception( "You forgot to mock: <%s.%s>" %
                         ( self.unitName, self.functionName ) );

class PyTestMockTable:
    def __init__( self ):
        self.units = {};

    def registerMockFunction( self, unitName, functionName ):
        if not unitName in self.units:
            self.units[unitName] = {};

        missingObject = DefaultFunctionCall( unitName, functionName );
        self.units[unitName][functionName] = [ missingObject.missingImplementation ];

    def exportMockFunction( self, unitName, functionName ):
        m = sys.modules["T." + unitName];
        m.__dict__[ functionName ] = \
                lambda *args, **more: self.callFunction( unitName, functionName, *args , **more );

    def importRealFunction( self, unitName, functionName ):
        __import__( unitName );
        m = sys.modules["T." + unitName];
        m.__dict__[ functionName ] = \
                sys.modules[unitName].__dict__[ functionName ];

    def callFunction( self, unitName, functionName, *args , **more ):
        mockStack = self.units[unitName][functionName];
        mockMethod = mockStack[-1];
        return mockMethod( *args , **more );

    def mockStack( self, unitName, functionName ):
        if not unitName in self.units:
            raise Exception( "No redirector: <%s>" % ( unitName ) );
        if not functionName in self.units[ unitName ]:
            raise Exception( "No redirector: <%s.%s>" %
                    ( unitName , functionName ) );
        return self.units[ unitName ][ functionName ];

class PyTestMockable:
    def mockFunction( self, unitName, functionName, mockMethod ):
        mockStack = PyTest.mockTable.mockStack( unitName, functionName );
        mockStack.append( mockMethod );

def PyTest_MockFunction( unitName, functionName ):
    PyTest.mockTable.registerMockFunction( unitName, functionName );
    PyTest.mockTable.exportMockFunction( unitName, functionName );

def PyTest_RealFunction( unitName, functionName ):
    try:
        PyTest.mockTable.importRealFunction( unitName, functionName );
    except Exception, e:
        print unitName, functionName;
        print str(e);

PyTest_MockObject = PyTest_MockFunction;
PyTest_RealObject = PyTest_RealFunction;
PyTest_RealValue = PyTest_RealFunction;

__all__ = [ "PyTestMockTable",
            "PyTestMockable",
            "PyTest_MockFunction",
            "PyTest_RealFunction",
            "PyTest_MockObject",
            "PyTest_RealObject",
            "PyTest_RealValue" ];
