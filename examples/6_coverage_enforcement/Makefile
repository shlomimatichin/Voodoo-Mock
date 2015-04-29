include $(VOODOO_ROOT_DIR)/make/common.Makefile

all: 
	@( make -f undertest.Makefile 2>&1 || true ) | grep "cpp$(DIR_SEP)FileNotCovered.h:1: COVERAGE ERROR: file is not covered by unit test"
	@( make -f undertest.Makefile 2>&1 || true ) | grep "cpp$(DIR_SEP)ToCover.h:21: COVERAGE ERROR: line is not covered by unit test"
	@( make -f undertest.Makefile 2>&1 || true ) | grep "cpp$(DIR_SEP)ToCover.h:32: COVERAGE ERROR: line is not covered by unit test"
	@( make -f undertest.Makefile 2>&1 || true ) | grep "cpp$(DIR_SEP)ToCover.h:33: COVERAGE ERROR: line is not covered by unit test"
	@( make -f undertest.Makefile 2>&1 || true ) | grep "cpp$(DIR_SEP)ToCover.h:19: COVERAGE_WARNING: non code line marked as exempt"
	test $(shell (make -f undertest.Makefile 2>&1 || true ) | grep COVERAGE.ERROR | wc -l) -eq 4
	test $(shell (make -f undertest.Makefile 2>&1 || true ) | grep COVERAGE.WARNING | wc -l) -eq 1

clean:
	rm -fr build_unittest
