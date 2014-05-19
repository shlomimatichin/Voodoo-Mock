all: 
	( make -f undertest.Makefile 2>&1 || true ) | grep 'cpp/FileNotCovered.h:1: COVERAGE ERROR: file is not covered by unit test'
	( make -f undertest.Makefile 2>&1 || true ) | grep 'cpp/ToCover.h:13: COVERAGE ERROR: line is not covered by unit test'
	( make -f undertest.Makefile 2>&1 || true ) | grep 'cpp/ToCover.h:        -:   11:	// LINE_EXEMPT_FROM_CODE_COVERAGE: COVERAGE_WARNING: non code line marked as exempt'

clean:
	rm -fr build_unittest
