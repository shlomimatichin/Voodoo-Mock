all: targets test

ifeq ($(V),1)
  Q =
else
  Q = @
endif

export CXXTEST_FIND_ROOT = c cpp
export PYTEST_FIND_ROOT = py
export ENFORCE_COVERAGE_FIND_ROOT_CPP = c cpp
export UNITTEST_INCLUDES = -Ibuild_unittest/voodoo/cpp -Ibuild_unittest/voodoo/c -Icpp -Ic -I.
export VOODOO_INCLUDES = --includePath=cpp --includePath=c

clean:
	rm -fr build_unittest build coverage
	find -name "*.pyc" -delete

test: targets
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/1_generate.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/2_build.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/3_run.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/4_optional_enforce_cpp_coverage.Makefile

targets:
	$(MAKE) -f tools/make/Makefile

test_singletest:
	$(Q)echo "Running single test $(SINGLE_TEST_SUITE) Line $(SINGLE_TEST_LINE)"
	$(Q)[ "$(SINGLE_TEST_SUITE)" ] || echo 'You must specify "SINGLE_TEST_SUITE=<filename>"'
	$(Q)[ "$(SINGLE_TEST_SUITE)" ]
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/1_generate.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/2_build.Makefile CXXTEST_FIND_PATTERN=$(SINGLE_TEST_SUITE)
	$(Q)$(VOODOO_ROOT_DIR)/make/runsingletest.sh $(SINGLE_TEST_SUITE) $(SINGLE_TEST_LINE)

test_singletestsuite:
	$(Q)echo "Running single test suite $(SINGLE_TEST_SUITE)"
	$(Q)[ "$(SINGLE_TEST_SUITE)" ] || echo 'You must specify "SINGLE_TEST_SUITE=<filename>"'
	$(Q)[ "$(SINGLE_TEST_SUITE)" ]
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/1_generate.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/2_build.Makefile CXXTEST_FIND_PATTERN=$(SINGLE_TEST_SUITE)
	$(Q)$(VOODOO_ROOT_DIR)/make/runsingletestsuite.sh $(SINGLE_TEST_SUITE)

voodoo_compileSingleHeader:
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/1_generate.Makefile generateSingleVoodoo

voodoo_forceGenerateAll:
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/1_generate.Makefile generateVoodooForce
