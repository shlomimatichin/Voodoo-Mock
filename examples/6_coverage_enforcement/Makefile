all: 
	( make -f undertest.Makefile 2>&1 || true ) | grep 'cpp/FileNotCovered.h:1: COVERAGE ERROR: file is not covered by unit test'
	( make -f undertest.Makefile 2>&1 || true ) | grep 'cpp/ToCover.h:21: COVERAGE ERROR: line is not covered by unit test'
	( make -f undertest.Makefile 2>&1 || true ) | grep 'cpp/ToCover.h:32: COVERAGE ERROR: line is not covered by unit test'
	( make -f undertest.Makefile 2>&1 || true ) | grep 'cpp/ToCover.h:33: COVERAGE ERROR: line is not covered by unit test'
	( make -f undertest.Makefile 2>&1 || true ) | grep 'cpp/ToCover.h:19: COVERAGE_WARNING: non code line marked as exempt'
	test `( make -f undertest.Makefile 2>&1 || true ) | grep COVERAGE.ERROR | wc -l` -eq 4
	test `( make -f undertest.Makefile 2>&1 || true ) | grep COVERAGE.WARNING | wc -l` -eq 1

clean:
	rm -fr build_unittest
