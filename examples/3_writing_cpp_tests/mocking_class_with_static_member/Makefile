all: test

ifeq ($(V),1)
  Q =
else
  Q = @
endif

export VOODOO_ROOT_DIR=../../..
export CXXTEST_FIND_ROOT = cpp
export ENFORCE_COVERAGE_FIND_ROOT_CPP = cpp
export UNITTEST_INCLUDES = -Ibuild_unittest/voodoo/cpp -Icpp -I.
export VOODOO_INCLUDES = --includePath=cpp

clean: clean_unittest

include $(VOODOO_ROOT_DIR)/make/integrations/complete.Makefile
