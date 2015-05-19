import sys
import subprocess
import os.path
import imp
import re
import stat
import getopt
import threading
import pickle
import time
import json
import argparse

PYTESTDIR = os.path.dirname( sys.argv[ 0 ] )
PYTESTRUNNER = os.path.join( PYTESTDIR, "pytestrunner.py" )

parser = argparse.ArgumentParser()
parser.add_argument( "suites", nargs = '+' )
parser.add_argument( "--coverage", action = "store_true" )
parser.add_argument( "--coverageFlags", default = "--branch" )
parser.add_argument( "--verbose", action = "store_true" )
parser.add_argument( "--jobs", type = int, default = 4 )
parser.add_argument( "--cacheFile", default = "testharnesscache.tmp" )
parser.add_argument( "--reportFile", default = "testharnessreport.json" )
args = parser.parse_args()

if args.verbose:
    args.jobs = 1

def isPythonTestSuite( suite ):
    return suite.endswith( ".py" )

def isCppTestSuite( suite ):
    return suite.endswith( ".bin" )

def popenSuite( suite ):
    if isPythonTestSuite( suite ):
        if args.coverage:
            coverageFlags = args.coverageFlags.split(" ")
            return subprocess.Popen( [ 'coverage', 'run', '--append' ] + coverageFlags +
                                    [ PYTESTRUNNER, "--verbose", suite ],
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.STDOUT )
        else:
            return subprocess.Popen( [ 'python', PYTESTRUNNER,
                                            "--verbose", suite ],
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.STDOUT )
    elif isCppTestSuite( suite ):
        return subprocess.Popen( [ suite ],
                                stdout = subprocess.PIPE,
                                stderr = subprocess.STDOUT,
                                env = dict( os.environ,
                                    GCOV_PREFIX_STRIP = "100",
                                    GCOV_PREFIX = os.path.dirname( suite ) ) )
    else:
        raise Exception( "Suite type is not recongnized: %s" % suite )

def lastModifiedTime( fileName ):
    return os.stat( fileName )[ stat.ST_MTIME ];

report = []
lastRun = {}
try:
    with open( args.cacheFile, "rb" ) as f:
        lastRun = pickle.load( f )
except:
    pass

if args.coverage:
    os.system( "coverage erase" )
needToRunSuites = []
oldCppTests = 0
for suite in args.suites:
    if suite.endswith( ".py" ) or \
            suite not in lastRun or \
            lastModifiedTime( suite ) > lastRun[ suite ][ 0 ]:
        needToRunSuites.append( suite )
    else:
        oldCppTests += lastRun[ suite ][ 1 ]

print "Running %d fresh suites (total %d)" % ( len( needToRunSuites ), len( args.suites ) )

class ParallelRun:
    def __init__( self, suites ):
        self._suites = suites
        self._lock = threading.Lock()
        self._quitEvent = threading.Event()
        self._success = True
        self._cppTests = 0
        self._pythonTests = 0

    def go( self ):
        self._startThreads()
        self._waitForThreadsToComplete()
        if self._success:
            print ""
            print "OK!"
            print "CPP tests: %d (%d skipped)" % (    self._cppTests,
                                                    oldCppTests )
            print "Python tests: %d" % self._pythonTests
            print "Total: %d tests" % (
                    self._cppTests + oldCppTests + self._pythonTests )
            return 0
        else:
            print "FAILED!"
            return 1

    def _startThreads( self ):
        self._threads = []
        for i in range( 0, args.jobs ):
            self._threads.append( threading.Thread( target = self._testerThread ) )
            self._threads[ -1 ].start()

    def _waitForThreadsToComplete( self ):
        for thread in self._threads:
            thread.join()

    def _testerThread( self ):
        while True:
            if self._quitEvent.isSet():
                return
            self._lock.acquire()
            try:
                if self._suites == []:
                    return
                else:
                    suite = self._suites.pop( 0 )
                    sys.stdout.write( "." )
                    sys.stdout.flush()
            finally:
                self._lock.release()
            self._runSuite( suite )

    def _runSuite( self, suite ):
        if args.verbose:
            print "Running %s" % suite
            sys.stdout.flush()
        before = time.time()
        popen = popenSuite( suite )
        all = popen.stdout.readlines()
        if args.verbose:
            print "".join( all )
            sys.stdout.flush()
        testCount = len( [ l for l in all if "TEST '" in l ] )
        popen.stdout.close()
        success = popen.wait()
        took = time.time() - before
        for l in all:
            if "TEST '" in l:
                testname = re.search( r"TEST '(.*)'", l ).group( 1 )
                suiteRelative = os.path.relpath( suite )
                report.append( dict( suite = suiteRelative,
                                    name = testname,
                                    passed = success == 0,
                                    timeTook = took / testCount ) )
        if success != 0:
            self._lock.acquire()
            try:
                print ""
                print "Suite '%s' failed:" % suite
                print "".join( all )
                self._success = False
            finally:
                self._lock.release()
            self._quitEvent.set()
        else:
            self._lock.acquire()
            try:
                lastRun[ suite ] = ( lastModifiedTime( suite ), testCount )
                if isPythonTestSuite( suite ):
                    self._pythonTests += testCount
                else:
                    self._cppTests += testCount
            finally:
                self._lock.release()

result = ParallelRun( needToRunSuites ).go()
if os.path.dirname( args.cacheFile ) != '' and not os.path.isdir( os.path.dirname( args.cacheFile ) ):
    os.makedirs( os.path.dirname( args.cacheFile ) )
with open( args.cacheFile, "wb" ) as f:
    pickle.dump( lastRun, f )
if os.path.dirname( args.reportFile ) != '' and not os.path.isdir( os.path.dirname( args.reportFile ) ):
    os.makedirs( os.path.dirname( args.reportFile ) )
with open( args.reportFile, "w" ) as f:
    json.dump( report, f, indent = 4 )
exit( result )
