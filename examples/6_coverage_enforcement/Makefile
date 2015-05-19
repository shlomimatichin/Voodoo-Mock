all: 
	mkdir -p build_unittest
	make -f undertest.Makefile 2>&1 > build_unittest/undertest.log || true
	cat build_unittest/undertest.log | grep 'cpp[/\\]FileNotCovered.h:1: COVERAGE ERROR: file is not covered by unit test'
	cat build_unittest/undertest.log | grep 'cpp[/\\]ToCover.h:21: COVERAGE ERROR: line is not covered by unit test'
	cat build_unittest/undertest.log | grep 'cpp[/\\]ToCover.h:32: COVERAGE ERROR: line is not covered by unit test'
	cat build_unittest/undertest.log | grep 'cpp[/\\]ToCover.h:33: COVERAGE ERROR: line is not covered by unit test'
	cat build_unittest/undertest.log | grep 'cpp[/\\]ToCover.h:19: COVERAGE_WARNING: non code line marked as exempt'
	test `cat build_unittest/undertest.log | grep COVERAGE.ERROR | wc -l` -eq 4
	test `cat build_unittest/undertest.log | grep COVERAGE.WARNING | wc -l` -eq 1

clean:
	rm -fr build_unittest
