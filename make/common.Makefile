UNITTEST_BUILD_DIRECTORY ?= build_unittest
CXXTEST_FIND_ROOT ?=
CXXTEST_FIND_PATTERN ?= $(CXXTEST_FIND_ROOT) -name 'test_*.h' -or -name 'Test_*.h'
PYTEST_FIND_ROOT ?=
PYTEST_FIND_PATTERN ?= $(PYTEST_FIND_ROOT) -name 'test_*.py'
ENFORCE_COVERAGE_FIND_ROOT_CPP ?=
ifeq ($(OS),Windows_NT)
ENFORCE_COVERAGE_FIND_EXCLUDE_REGEXES ?= '.*\\<$(UNITTEST_BUILD_DIRECTORY)\\>/.*' '.*\\<tests\\>.*' '.*\\<build\\>.*'
else
ENFORCE_COVERAGE_FIND_EXCLUDE_REGEXES ?= '.*\<$(UNITTEST_BUILD_DIRECTORY)\>/.*' '.*\<tests\>.*' '.*\<build\>.*'
endif
ENFORCE_COVERAGE_FIND_PATTERN_CPP ?= $(ENFORCE_COVERAGE_FIND_ROOT_CPP) '(' -name '*.cpp' -or -name '*.h' ')' $(patsubst %,-and -not -regex %,$(ENFORCE_COVERAGE_FIND_EXCLUDE_REGEXES))

VOODOO_MIRROR_TREE ?= $(UNITTEST_BUILD_DIRECTORY)/voodoo

__REMOVE_DOT_SLASH_PREFIX = | sed 's@^\./@@'
__HIDE_FIND_ERRORS = 2>/dev/null
__POSSIBLE_UNITTEST_SUFFIXES = .h .H .hh .HH .hxx .HXX .hpp .HPP
CXXTEST_TEST_FILES = $(shell find $(CXXTEST_FIND_PATTERN) $(__HIDE_FIND_ERRORS) $(__REMOVE_DOT_SLASH_PREFIX))
CXXTEST_GENERATED = $(filter %.cxx,$(foreach suffix,$(__POSSIBLE_UNITTEST_SUFFIXES),$(patsubst %$(suffix),$(UNITTEST_BUILD_DIRECTORY)/%.cxx,$(subst /,_,$(CXXTEST_TEST_FILES)))))
CXXTEST_BINARIES = $(patsubst %.cxx,%.bin,$(CXXTEST_GENERATED))

ifeq ($(V),1)
  Q =
else
  Q = @
endif
