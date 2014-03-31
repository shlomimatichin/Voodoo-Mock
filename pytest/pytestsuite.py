import PyTest;
from sys import exc_info;
from types import MethodType;
from inspect import stack, trace;
import pprint

class PyTestFailure:
    pass ;

class PyTestSuite:
    def __init__( self, testPrefix = "test" ):
        self._testCases = [];
        self._collectCases( testPrefix );
        self._sortCases();

    def setUp( self ):
        pass ;

    def tearDown( self ):
        pass ;

    def _run( self ):
        PyTest.tracker.enterSuite( self._suiteDescription() );
        for ( testName, testMethod ) in self._testCases:
            PyTest.tracker.enterTest( self._testDescription( testName ) );
            self._setUpWrapper();
            self._callTestWrapper( testMethod );
            self._tearDownWrapper();
            PyTest.tracker.leaveTest( self._testDescription( testName ) );
        PyTest.tracker.leaveSuite( self._suiteDescription() );

    def _runSingleTest( self, singleTest ):
        PyTest.tracker.enterSuite( self._suiteDescription() );
        for ( testName, testMethod ) in self._testCases:
            if testName != singleTest:
                continue
            PyTest.tracker.enterTest( self._testDescription( testName ) );
            self._setUpWrapper();
            self._callTestWrapper( testMethod );
            self._tearDownWrapper();
            PyTest.tracker.leaveTest( self._testDescription( testName ) );
        PyTest.tracker.leaveSuite( self._suiteDescription() );

    def _setUpWrapper( self ):
        try:
            self.setUp();
        except PyTestFailure:
            pass ;
        except Exception, e:
            PyTest.tracker.failTest( "Exception thrown from test <%s>" % e,
                                     trace() );
            PyTest.tracker.caughtException( exc_info()[2] );
        except:
            PyTest.tracker.failTest( "Unknown exception thrown from setUp",
                                     trace() );
            PyTest.tracker.caughtException( exc_info()[2] );

    def _callTestWrapper( self, testMethod ):
        try:
            testMethod();
        except PyTestFailure:
            pass ;
        except Exception, e:
            PyTest.tracker.failTest( "Exception thrown from test <%s>" % e,
                                     trace() );
            PyTest.tracker.caughtException( exc_info()[2] );
        except:
            PyTest.tracker.failTest( "Unknown exception thrown from test",
                                     trace() );
            PyTest.tracker.caughtException( exc_info()[2] );

    def _tearDownWrapper( self ):
        try:
            self.tearDown();
        except PyTestFailure:
            pass ;
        except Exception, e:
            PyTest.tracker.failTest( "Exception thrown from test <%s>" % e,
                                     trace() );
            PyTest.tracker.caughtException( exc_info()[2] );
        except:
            PyTest.tracker.failTest( "Unknown exception thrown from tearDown",
                                     trace() );
            PyTest.tracker.caughtException( exc_info()[2] );

    def _collectCases( self, testPrefix ):
        for key in dir( self ):
            value = getattr( self, key );
            if type( value ) is MethodType:
                if ( key.startswith( testPrefix ) ):
                    self._testCases.append( ( key, value ) );

    def _sortCases( self ):
        self._testCases.sort( lambda x,y: cmp( x[1].func_code.co_firstlineno,
                                               y[1].func_code.co_firstlineno ) );

    def _testDescription( self, testName ):
        return testName;

    def _suiteDescription( self ):
        return str(self.__class__);

    def _numTests( self ):
        return len(self._testCases);

def TS_FAIL( message ):
    PyTest.tracker.failTest( message, stack() );
    raise PyTestFailure();

def TS_WARN( message ):
    PyTest.tracker.writeMessage( message, stack()[1] );

def TS_TRACE( message ):
    PyTest.tracker.writeMessage( message, stack()[1] );

def TS_ASSERT( x ):
    if not x :
        PyTest.tracker.failTest( "Assert failed", stack() );
        raise PyTestFailure();

def TSM_ASSERT( m, x ):
    if not x:
        PyTest.tracker.writeMessage( m, stack()[1] );
        PyTest.tracker.failTest( "Assert failed", stack() );
        raise PyTestFailure();

def TS_ASSERT_EQUALS( x, y ):
    if not ( x == y ):
        PyTest.tracker.failTest( "Assert equals failed -- %s and %s are not equal" %
                                 ( pprint.pformat(x), pprint.pformat(y) ),
                                 stack() );
        raise PyTestFailure();

def TS_ASSERT_SAME_DATA( x, y ):
    if not ( x == y ):
        PyTest.tracker.failTest( "Assert equals failed -- %s and %s are not equal" %
                                 ( x.encode('hex'), y.encode('hex') ),
                                 stack() );
        raise PyTestFailure();

def TSM_ASSERT_EQUALS( m, x, y ):
    if not ( x == y ):
        PyTest.tracker.writeMessage( m, stack()[1] );
        PyTest.tracker.failTest( "Assert equals failed -- %s and %s are not equal" %
                                 ( str(x), str(y) ),
                                 stack() );
        raise PyTestFailure();

def TS_ASSERT_DIFFERS( x, y ):
    if ( x == y ):
        PyTest.tracker.failTest( "Assert differs failed -- %s and %s are equal" %
                                 ( str(x), str(y) ),
                                 stack() );
        raise PyTestFailure();


def TSM_ASSERT_DIFFERS( m, x, y ):
    if ( x == y ):
        PyTest.tracker.writeMessage( m );
        PyTest.tracker.failTest( "Assert differs failed -- %s and %s are equal" %
                                 ( str(x), str(y) ),
                                 stack() );
        raise PyTestFailure();

def TS_ASSERT_LESS_THAN( x, y ):
    if not ( x < y ):
        PyTest.tracker.failTest( "Assert less than -- %s is not less than %s" %
                                 ( str(x), str(y) ),
                                 stack() );
        raise PyTestFailure();

def TSM_ASSERT_LESS_THAN( m, x, y ):
    if not ( x <= y ):
        PyTest.tracker.writeMessage( m );
        PyTest.tracker.failTest( "Assert less than -- %s is not less than equals %s" %
                                 ( str(x), str(y) ),
                                 stack() );
        raise PyTestFailure();

def TS_ASSERT_LESS_THAN_EQUALS( x, y ):
    if not ( x <= y ):
        PyTest.tracker.failTest( "Assert less than -- %s is not less than equals %s" %
                                 ( str(x), str(y) ),
                                 stack() );
        raise PyTestFailure();

def TSM_ASSERT_LESS_THAN_EQUALS( m, x, y ):
    if not ( x <= y ):
        PyTest.tracker.writeMessage( m );
        PyTest.tracker.failTest( "Assert less than -- %s is not less than %s" %
                                 ( str(x), str(y) ),
                                 stack() );
        raise PyTestFailure();

def TS_ASSERT_THROWS_ANYTHING( c, *args, **kwargs ):
    try:
        c( *args, **kwargs );
    except:
        pass ;
    else:
        PyTest.tracker.failTest( "Expected %s to throw, but it didn't" % str(c),
                                 stack() );
        raise PyTestFailure();

def TSM_ASSERT_THROWS_ANYTHING( m, c, *args, **kwargs ):
    try:
        c( *args, **kwargs );
    except:
        pass ;
    else:
        PyTest.tracker.writeMessage( m );
        PyTest.tracker.failTest( "Expected %s to throw, but it didn't" % str(c),
                                 stack() );
        raise PyTestFailure();

def TS_ASSERT_THROWS( e, c, *args, **kwargs ):
    try:
        c( *args, **kwargs );
    except e:
        pass ;
    else:
        PyTest.tracker.failTest( "Expected %s to throw %s, but it didn't" % ( str(c), str(e) ),
                                 stack() );
        raise PyTestFailure();

def TSM_ASSERT_THROWS( m, e, c, *args, **kwargs ):
    try:
        c( *args, **kwargs );
    except e:
        pass ;
    else:
        PyTest.tracker.writeMessage( m );
        PyTest.tracker.failTest( "Expected %s to throw %s, but it didn't" % ( str(c), str(e) ),
                                 stack() );
        raise PyTestFailure();

def TS_ASSERT_THROWS_EQUALS( e, strval, c, *args, **kwargs ):
    try:
        c( *args, **kwargs );
    except e, ei:
        if not ( str( ei ) == strval ):
            PyTest.tracker.failTest( "%s has thrown %s: but it's string [%s] != [%s]" % ( str(c), str(e), str(ei), str(strval) ) ,
                                     stack() );
            raise PyTestFailure();
    else:
        PyTest.tracker.failTest( "Expected %s to throw %s, but it didn't" % ( str(c), str(e) ),
                                 stack() );
        raise PyTestFailure();

def TSM_ASSERT_THROWS_EQUALS( m, e, strval, c, *args, **kwargs ):
    try:
        c( *args, **kwargs );
    except e, ei:
        if not ( str( ei ) == strval ):
            PyTest.tracker.writeMessage( m );
            PyTest.tracker.failTest( "%s has thrown %s: but it's string [%s] != [%s]" % ( str(c), str(e), str(ei), str(strval) ) ,
                                     stack() );
            raise PyTestFailure();
    else:
        PyTest.tracker.writeMessage( m );
        PyTest.tracker.failTest( "Expected %s to throw %s, but it didn't" % ( str(c), str(e) ),
                                 stack() );
        raise PyTestFailure();

__all__ = [ "PyTestFailure",
            "PyTestSuite",
            "TS_FAIL",
            "TS_WARN",
            "TS_TRACE",
            "TS_ASSERT",
            "TSM_ASSERT",
            "TS_ASSERT_EQUALS",
            "TS_ASSERT_SAME_DATA",
            "TSM_ASSERT_EQUALS",
            "TS_ASSERT_DIFFERS",
            "TSM_ASSERT_DIFFERS",
            "TS_ASSERT_LESS_THAN",
            "TSM_ASSERT_LESS_THAN",
            "TS_ASSERT_LESS_THAN_EQUALS",
            "TSM_ASSERT_LESS_THAN_EQUALS",
            "TS_ASSERT_THROWS",
            "TSM_ASSERT_THROWS",
            "TS_ASSERT_THROWS_EQUALS",
            "TSM_ASSERT_THROWS_EQUALS",
            "TS_ASSERT_THROWS_ANYTHING",
            "TSM_ASSERT_THROWS_ANYTHING" ];
