import re
import os
import subprocess
import glob

class EnforceCPPCoverage:
    _SOURCE_FILENAME = re.compile( "0:Source:(\S+)" )
    _NON_COVERED_PREFIX = '    #####'
    _NON_COVERED_EXCEPTIONAL_PREFIX = '    ====='
    _LINE_EXEMPT_FROM_CODE_COVERAGE = 'LINE_EXEMPT_FROM_CODE_COVERAGE'
    _FILE_EXEMPT_FROM_CODE_COVERAGE = 'FILE_EXEMPT_FROM_CODE_COVERAGE'
    _NON_COVERED_REGEX = re.compile( r"^    [=#]{5}:\s*(\d+):" )
    _COVERED_REGEX = re.compile( r"^\s*\-?\d+:\s*(\d+):" )
    _NON_CODE_REGEX = re.compile( r"^\s*-:\s*(\d+):" )

    def __init__( self, filesToCover, unitTestExecutables ):
        self._filesToCover = set( [ os.path.normpath( f ) for f in filesToCover ] )
        self._filesWithoutCoverageReport = set( self._filesToCover )
        self._init()

        try:
            self._scan( unitTestExecutables )
        finally:
            os.system( "rm -fr *.gcov" )

        self._conclude()

    def coveredLines( self ): return self._coveredLines
    def nonCoveredLines( self ): return self._nonCoveredLines
    def filesWithoutCoverageReport( self ): return self._filesWithoutCoverageReport
    def linesExemptFromCodeCoverage( self ): return self._linesExemptFromCodeCoverage
    def nonCodeLinesMarkedAsExempt( self ): return self._nonCodeLinesMarkedAsExempt
    def coveredLinesMarkedAsExempt( self ): return self._coveredLinesMarkedAsExempt
    def filesExemptFromCodeCoverage( self ): return self._filesExemptFromCodeCoverage

    def _init( self ):
        self._coveredLines = set()
        self._nonCoveredLines = set()
        self._linesExemptFromCodeCoverage = set()
        self._nonCodeLinesMarkedAsExempt = set()
        self._coveredLinesMarkedAsExempt = set()
        self._filesExemptFromCodeCoverage = set()

    def _conclude( self ):
        self._nonCoveredLines -= self._coveredLines
        for filename, line in list( self._nonCoveredLines ):
            if filename in self._filesExemptFromCodeCoverage:
                self._nonCoveredLines.remove( ( filename, line ) )
        self._nonCodeLinesMarkedAsExempt -= self._coveredLines
        self._nonCodeLinesMarkedAsExempt -= self._nonCoveredLines
        self._nonCodeLinesMarkedAsExempt -= self._linesExemptFromCodeCoverage
        for filename in list( self._filesWithoutCoverageReport ):
            with open( filename ) as f:
                if self._FILE_EXEMPT_FROM_CODE_COVERAGE in f.read():
                    self._filesWithoutCoverageReport.discard( filename )
                    self._filesExemptFromCodeCoverage.add( filename )

    def _readGCOV( self, gcovFilename ):
        with open( gcovFilename ) as f:
            lines = f.readlines()
        sourceFilename = os.path.relpath( self._SOURCE_FILENAME.search( lines[ 0 ] ).group( 1 ) )
        if sourceFilename not in self._filesToCover:
            return
        self._filesWithoutCoverageReport.discard( sourceFilename )
        for line in lines:
            self._readGCOVLine( line, sourceFilename )
            if self._FILE_EXEMPT_FROM_CODE_COVERAGE in line:
                self._filesExemptFromCodeCoverage.add( sourceFilename )

    def _readGCOVLine( self, line, sourceFilename ):
        if line.startswith( self._NON_COVERED_PREFIX ) or \
           line.startswith( self._NON_COVERED_EXCEPTIONAL_PREFIX ):
            lineNumber = int( self._NON_COVERED_REGEX.match( line ).group( 1 ) )
            if self._LINE_EXEMPT_FROM_CODE_COVERAGE in line:
                self._linesExemptFromCodeCoverage.add( ( sourceFilename, lineNumber ) )
            else:
                self._nonCoveredLines.add( ( sourceFilename, int( lineNumber ) ) )
        else:
            match = self._COVERED_REGEX.match( line )
            if match is None:
                if self._LINE_EXEMPT_FROM_CODE_COVERAGE in line:
                    match = self._NON_CODE_REGEX.match( line )
                    lineNumber = int( match.group( 1 ) )
                    self._nonCodeLinesMarkedAsExempt.add( ( sourceFilename, lineNumber ) )
            else:
                lineNumber = int( match.group( 1 ) )
                self._coveredLines.add( ( sourceFilename, lineNumber ) )
                if self._LINE_EXEMPT_FROM_CODE_COVERAGE in line:
                    self._coveredLinesMarkedAsExempt.add( ( sourceFilename, lineNumber ) )

    def _scan( self, unitTestExecutables ):
        for executable in unitTestExecutables:
            command = [ 'gcov', '--long-file-names', '--preserve-paths', '--relative-only', executable ]
            output = subprocess.check_output( command, stderr = subprocess.STDOUT )
            dirList = glob.glob( "*.gcov" )
            if len( dirList ) == 0:
                raise Exception( "GCOV failed:\n%s\n%s" % ( command, output ) )
            for gcovFilename in dirList:
                self._readGCOV( gcovFilename )
                os.unlink( gcovFilename )

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument( "--enforceOn", nargs = '*' )
    parser.add_argument( "testExecutables", nargs = '+' )
    parser.add_argument( "--printExemptFiles", action = "store_true" )
    parser.add_argument( "--printExemptLines", action = "store_true" )
    args = parser.parse_args()

    enforcer = EnforceCPPCoverage( filesToCover = args.enforceOn,
                                    unitTestExecutables = args.testExecutables )

    for filename in sorted( enforcer.filesWithoutCoverageReport() ):
        print "%s:1: COVERAGE ERROR: file is not covered by unit test" % filename
        print "Hint: add FILE_EXEMPT_FROM_CODE_COVERAGE to a comment inside the " \
                "file to make this message go away. Make sure this is allowed " \
                "under the coding policy in your project - someone turned on " \
                "coverage enforcement for a reason"
    for filename, line in sorted( enforcer.nonCoveredLines() ):
        print "%s:%d: COVERAGE ERROR: line is not covered by unit test" % ( filename, line )
        print "Hint: add LINE_EXEMPT_FROM_CODE_COVERAGE to a comment inside the " \
                "line to make this message go away. Make sure this is allowed " \
                "under the coding policy in your project - someone turned on " \
                "coverage enforcement for a reason"
    for filename, line in sorted( enforcer.nonCodeLinesMarkedAsExempt() ):
        print "%s:%d: COVERAGE_WARNING: non code line marked as exempt" % ( filename, line )
        print "Hint: the compiler does not think this is a code block relevant for " \
                "coverage tracking (like empty space or comment lines). " \
                "Remove the LINE_EXEMPT_FROM_CODE_COVERAGE comment"
    for filename, line in sorted( enforcer.coveredLinesMarkedAsExempt() ):
        print "%s:%d: COVERAGE_WARNING: covered line marked as exempt" % ( filename, line )
        print "Hint: your test suite actually did cover this line. " \
                "Remove the LINE_EXEMPT_FROM_CODE_COVERAGE comment"

    print "Coverage Summary:"
    print "Covered Lines: ", len( enforcer.coveredLines() )
    print "Lines exempt from code coverage: ", len( enforcer.linesExemptFromCodeCoverage() )
    print "Files exempt from code coverage: ", len( enforcer.filesExemptFromCodeCoverage() )
    print "Files not exempt from code coverage: ", len( args.enforceOn ) - len( enforcer.filesExemptFromCodeCoverage() )

    if args.printExemptFiles:
        print "List of files exempt from code coverage:"
        for filename in sorted( enforcer.filesExemptFromCodeCoverage() ):
            print filename
    if args.printExemptLines:
        print "List of lines exempt from code coverage:"
        for filename, line in sorted( enforcer.linesExemptFromCodeCoverage() ):
            print "%s:%d" % ( filename, line )

    hasErrors = 0 < \
            len( enforcer.filesWithoutCoverageReport() ) + \
            len( enforcer.nonCoveredLines() ) + \
            len( enforcer.nonCodeLinesMarkedAsExempt() ) + \
            len( enforcer.coveredLinesMarkedAsExempt() )
    sys.exit( 1 if hasErrors else 0 )
