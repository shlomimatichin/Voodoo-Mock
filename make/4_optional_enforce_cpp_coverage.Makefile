enforceCPPCoverage: runEnforcement

include $(VOODOO_ROOT_DIR)/make/common.Makefile

ENFORCE_COVERAGE_CPP_SOURCE_FILES  := $(shell find $(ENFORCE_COVERAGE_FIND_PATTERN_CPP) $(__REMOVE_DOT_SLASH_PREFIX))

runEnforcement:
	@echo $(ENFORCE_COVERAGE_FIND_PATTERN_CPP)
	@echo $(ENFORCE_COVERAGE_CPP_SOURCE_FILES)
	$(Q)python $(VOODOO_ROOT_DIR)/make/enforce_cpp_coverage.py $(CXXTEST_BINARIES) --enforceOn $(call FixPath,$(ENFORCE_COVERAGE_CPP_SOURCE_FILES))
