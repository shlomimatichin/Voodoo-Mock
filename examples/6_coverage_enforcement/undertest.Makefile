all: test

export CXXTEST_FIND_ROOT = cpp
export ENFORCE_COVERAGE_FIND_ROOT_CPP = cpp
export UNITTEST_INCLUDES = -Ibuild_unittest/voodoo/cpp -Ibuild_unittest/voodoo/c -Icpp -I.
export VOODOO_INCLUDES = --includePath=cpp
export VOODOO_ROOT_DIR = ../..

clean: clean_unittest
	rm -fr build

include $(VOODOO_ROOT_DIR)/make/integrations/complete.Makefile
