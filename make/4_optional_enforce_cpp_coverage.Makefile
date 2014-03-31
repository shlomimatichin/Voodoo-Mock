enforceCPPCoverage: runEnforcement

include $(VOODOO_ROOT_DIR)/make/common.Makefile

ENFORCE_COVERAGE_CPP_SOURCE_FILES = $(shell find $(ENFORCE_COVERAGE_FIND_PATTERN_CPP) $(__REMOVE_DOT_SLASH_PREFIX))

runEnforcement:
	$(Q)python $(VOODOO_ROOT_DIR)/make/enforce_cpp_coverage.py $(CXXTEST_BINARIES) --enforceOn $(ENFORCE_COVERAGE_CPP_SOURCE_FILES)
