import sys
import os
import re

def newPYFile( filename ):
    def normalize( part ):
        part = part.lower()
        if part.startswith( 'test_' ):
            part = part[ 5 : ]
        return part

    assert filename.endswith( ".py" )

    filename = os.path.splitext( filename )[ 0 ]
    parts = filename.split( os.path.sep )
    assert parts[ 0 ] == "py"
    assert parts[ -1 ].lower().startswith( 'test' )
    parts.pop( 0 )

    print "from pytestsuite import *"
    print "from pyvoodoo import *"
    print "from pyvoodoo.expectations import *"
    print ""
    print "castVoodooUponModule( '' )"
    print ""
    print "from %s import *" % ".".join( [ normalize( part ) for part in parts if part != "tests" ] )
    print ""
    print "class %s( PyTestSuite ):" % parts[ -1 ]
    print "    def setUp( self ):"
    print "        pass"
    print ""
    print "    def tearDown( self ):"
    print "        pass"
    print ""
    print "    def test_Normal( self ):"
    print "        pass"

def newCLanguageHFile( filename ):
    assert filename.endswith( ".h" )
    withoutExtension = os.path.splitext( filename )[ 0 ]
    parts = withoutExtension.split( os.path.sep )
    assert parts[ 0 ] == "c"
    parts.pop( 0 )
    className = "_".join( parts )
    assert className.replace( "Test_", "test_" ) == className.lower(), \
            "directories and filenames in the 'c/' folder should only contain lower case letters and underscores"
    protectMacro = "__" + className.upper() + "_H__"

    def printNewHeaderFile():
        print "#ifndef %s" % protectMacro
        print "#define %s" % protectMacro
        print ""
        print "struct %s" % className
        print "{"
        print "};"
        print ""
        print "static int %s_init(struct %s * self);" % ( className, className )
        print "static void %s_destroy(struct %s * self);" % ( className, className )
        print ""
        print "static int %s_init(struct %s * self)" % ( className, className )
        print "{"
        print "\treturn 0;"
        print "}"
        print ""
        print "static void %s_destroy(struct %s * self)" % ( className, className )
        print "{"
        print "}"
        print ""
        print "#endif /* %s */" % protectMacro

    if parts[ -1 ].startswith( "Test_" ):
        printNewTestSuiteFile( "Test_" + className )
    else:
        printNewHeaderFile()

def printNewTestSuiteFile( className ):
    print "#include <cxxtest/TestSuite.h>"
    print ""
    print "#define VOODOO_EXPECT_"
    print ""
    print '#include "TestLibrariesThatHave VOODOO_EXPECT"'
    print ''
    print '#include "TestedFile"'
    print ''
    print '#include "TestLibraries"'
    print ''
    print 'using namespace VoodooCommon::Expect;'
    print 'using namespace VoodooCommon::Expect::Parameter;'
    print ''
    print 'class %s : public CxxTest::TestSuite' % className
    print '{'
    print 'public:'
    print '\tAlways * always;'
    print ''
    print '\tvoid setUp()'
    print '\t{'
    print '\t\talways = new Always;'
    print '\t}'
    print ''
    print '\tvoid tearDown()'
    print '\t{'
    print '\t\tdelete always;'
    print '\t}'
    print ''
    print '\tvoid test_Normal()'
    print '\t{'
    print '\t}'
    print '};'

def newHFile( filename ):
    def makeWords( parts ):
        result = []
        for part in parts:
            result += re.findall( r"[A-Z]+[^A-Z]*", part )
        return result

    assert filename.endswith( ".h" )
    filename = os.path.splitext( filename )[ 0 ]
    parts = filename.split( os.path.sep )
    assert parts[ 0 ] == "cpp"
    parts.pop( 0 )
    words = makeWords( parts )

    protectMacro = "__" + "_".join( [ w.upper() for w in words ] ) + "_H__"
    className = parts[ -1 ]
    namespaces = parts[ : -1 ]

    def printNewHeaderFile():
        print "#ifndef %s" % protectMacro
        print "#define %s" % protectMacro
        print ""
        for namespace in namespaces[ : -1 ]:
            print 'namespace %s {' % namespace
        if len( parts ) > 1:
            print 'namespace %s\n{' % parts[ -2 ]
        print ""
        print "class %s" % className
        print "{"
        print "public:"
        print "private:\n"
        print "\t%s( const %s & rhs ) = delete;" % ( className, className )
        print "\t%s & operator= ( const %s & rhs ) = delete;" % ( className, className )
        print "};"
        print ""
        for namespace in reversed( namespaces ):
            print "} // namespace %s" % namespace
        print ""
        print "#endif // %s" % protectMacro

    if className.startswith( "Test_" ):
        printNewTestSuiteFile( className )
    else:
        printNewHeaderFile()

filename = sys.argv[ 1 ]
if filename.endswith( ".py" ):
    newPYFile( filename )
elif filename.startswith( "c/" ) and filename.endswith( ".h" ):
    newCLanguageHFile( filename )
else:
    newHFile( filename )
