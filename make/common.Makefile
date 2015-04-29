ifdef SystemRoot
  FixPath = $(subst /,\,$1)
  MKDIR = if not exist $1 mkdir $(call FixPath, $1)
  RM = del /Q
  RM_RECURSIVE = if exist $1 (rd /S /Q $1)
  DIR_SEP = \\
  	
else
  FixPath = $1
  MKDIR = mkdir --parents $1
  RM = rm -f
  RM_RECURSIVE = rm -rf $1
  DIR_SEP = /
endif

UNITTEST_BUILD_DIRECTORY ?= build_unittest
CXXTEST_FIND_ROOT ?=
CXXTEST_FIND_PATTERN ?= $(CXXTEST_FIND_ROOT) -iname Test_*.h
PYTEST_FIND_ROOT ?=
PYTEST_FIND_PATTERN ?= $(PYTEST_FIND_ROOT) -iname test_*.py
ENFORCE_COVERAGE_FIND_ROOT_CPP ?=
ENFORCE_COVERAGE_FIND_EXCLUDE_REGEXES ?= ".*\<$(UNITTEST_BUILD_DIRECTORY)\>.*" ".*\<tests\>.*" ".*\<build\>.*"
ifdef SystemRoot
ENFORCE_COVERAGE_FIND_PATTERN_CPP ?= $(ENFORCE_COVERAGE_FIND_ROOT_CPP) "(" -iname *\.cpp -or -iname *\.h ")" $(patsubst %,-and -not -regex %,$(ENFORCE_COVERAGE_FIND_EXCLUDE_REGEXES))
else
ENFORCE_COVERAGE_FIND_PATTERN_CPP ?= $(ENFORCE_COVERAGE_FIND_ROOT_CPP) "(" -name "*.cpp" -or -name "*.h" ")" $(patsubst %,-and -not -regex %,$(ENFORCE_COVERAGE_FIND_EXCLUDE_REGEXES))
endif

VOODOO_MIRROR_TREE ?= $(call FixPath,$(UNITTEST_BUILD_DIRECTORY)/voodoo)

__REMOVE_DOT_SLASH_PREFIX = | sed "s@^\./@@"
__POSSIBLE_UNITTEST_SUFFIXES = .h .H .hh .HH .hxx .HXX .hpp .HPP
CXXTEST_TEST_FILES = $(shell find $(CXXTEST_FIND_PATTERN) $(__REMOVE_DOT_SLASH_PREFIX))
CXXTEST_GENERATED = $(call FixPath,$(filter %.cxx,$(foreach suffix,$(__POSSIBLE_UNITTEST_SUFFIXES),$(patsubst %$(suffix),$(UNITTEST_BUILD_DIRECTORY)/%.cxx,$(subst /,_,$(CXXTEST_TEST_FILES))))))
CXXTEST_BINARIES = $(call FixPath,$(patsubst %.cxx,%.bin,$(CXXTEST_GENERATED)))

ifeq ($(V),1)
  Q =
else
  Q = @
endif
