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

clean: clean_unittest
	rm -fr build
	find -name "*.pyc" -exec rm {} \;

test: targets

targets:
	$(MAKE) -f tools/make/Makefile

include $(VOODOO_ROOT_DIR)/make/integrations/complete.Makefile
