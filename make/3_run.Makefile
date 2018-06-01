runUnittests: runAllTests

include $(VOODOO_ROOT_DIR)/make/common.Makefile

PYTESTHARNESS_FLAGS ?= --cacheFile=$(UNITTEST_BUILD_DIRECTORY)/testharnesscache.tmp --reportFile=$(UNITTEST_BUILD_DIRECTORY)/testharnessreport.json
PYTEST_TEST_FILES = $(shell find $(PYTEST_FIND_PATTERN) $(__HIDE_FIND_ERRORS) $(__REMOVE_DOT_SLASH_PREFIX))

runAllTests:
	$(Q)echo "Running all tests"
	$(Q)rm -fr .coverage*
	$(Q)python $(VOODOO_ROOT_DIR)/pytest/pytestharness.py $(PYTESTHARNESS_FLAGS) $(CXXTEST_BINARIES) $(PYTEST_TEST_FILES)
