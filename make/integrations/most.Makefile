ifeq ($(V),1)
  Q =
else
  Q = @
endif

clean_unittest:
	rm -fr build_unittest coverage

test_all:
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/1_generate.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/2_build.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/3_run.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/4_optional_enforce_cpp_coverage.Makefile

test_allPython:
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/3_run.Makefile

__SINGLE_TEST_SUITE_PYTHON = $(filter-out %.py,$(SINGLE_TEST_SUITE))

test_singletest:
	$(Q)echo "Running single test $(SINGLE_TEST_SUITE) Line/Name $(REGEX_OR_LINE_NUMBER)"
	$(Q)[ "$(SINGLE_TEST_SUITE)" ] || echo 'You must specify "SINGLE_TEST_SUITE=<filename>"'
	$(Q)[ "$(SINGLE_TEST_SUITE)" ]
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/1_generate.Makefile
	test -z '$(__SINGLE_TEST_SUITE_PYTHON)' || $(MAKE) -f $(VOODOO_ROOT_DIR)/make/2_build.Makefile CXXTEST_FIND_PATTERN=$(SINGLE_TEST_SUITE)
	$(Q)$(VOODOO_ROOT_DIR)/make/runsingletest.sh $(SINGLE_TEST_SUITE) $(REGEX_OR_LINE_NUMBER)

test_singletestsuite:
	$(Q)echo "Running single test suite $(SINGLE_TEST_SUITE)"
	$(Q)[ "$(SINGLE_TEST_SUITE)" ] || echo 'You must specify "SINGLE_TEST_SUITE=<filename>"'
	$(Q)[ "$(SINGLE_TEST_SUITE)" ]
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/1_generate.Makefile
	test -z '$(__SINGLE_TEST_SUITE_PYTHON)' || $(MAKE) -f $(VOODOO_ROOT_DIR)/make/2_build.Makefile CXXTEST_FIND_PATTERN=$(SINGLE_TEST_SUITE)
	$(Q)$(VOODOO_ROOT_DIR)/make/runsingletestsuite.sh $(SINGLE_TEST_SUITE)

voodoo_compileSingleHeader:
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/1_generate.Makefile generateSingleVoodoo

voodoo_forceGenerateAll:
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/1_generate.Makefile generateVoodooForce
