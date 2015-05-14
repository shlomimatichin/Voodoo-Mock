buildTests:

include $(VOODOO_ROOT_DIR)/make/common.Makefile

UNITTEST_CXXFLAGS ?= -DDEBUG -DUNITTEST
UNITTEST_INCLUDES ?= -I.
UNITTEST_LDFLAGS ?=
ifeq ($(OS),Windows_NT)
UNITTEST_LIBS ?=
else
UNITTEST_LIBS ?= -ldl
endif

UNITTEST_CXXFLAGS += -std=gnu++0x -Werror -Wall -ggdb -DDEBUG -DUNITTEST --coverage
UNITTEST_LDFLAGS += --coverage
__UNITTEST_INCLUDES = -I$(VOODOO_MIRROR_TREE) $(UNITTEST_INCLUDES)
#NOTE: VOODOO_MIRROR_TREE must come first in include order, or interception magia will not work
__UNITTEST_INCLUDES += -I$(VOODOO_ROOT_DIR)/voodoo -I$(VOODOO_ROOT_DIR)/cxxtest

define template_per_TEST_FILE
template_per_TEST_FILE_cxx = $$(addprefix $$(UNITTEST_BUILD_DIRECTORY)/,$$(addsuffix .cxx,$$(basename $$(subst /,_,$(1)))))
template_per_TEST_FILE_bin = $$(patsubst %.cxx,%.bin,$$(template_per_TEST_FILE_cxx))
template_per_TEST_FILE_o_deps = $$(patsubst %.cxx,%.o.deps,$$(template_per_TEST_FILE_cxx))
buildTests: $$(template_per_TEST_FILE_bin)
-include $$(template_per_TEST_FILE_o_deps)
endef
$(foreach testFile,$(CXXTEST_TEST_FILES), $(eval $(call template_per_TEST_FILE,$(testFile))) )

$(UNITTEST_BUILD_DIRECTORY)/%.o: $(UNITTEST_BUILD_DIRECTORY)/%.cxx
	$(Q)echo 'UnitC++ ' $@
	$(Q)g++ $(__UNITTEST_INCLUDES) $(UNITTEST_CXXFLAGS) -MMD -MF $@.deps $< -c -o $@

$(UNITTEST_BUILD_DIRECTORY)/%.bin: $(UNITTEST_BUILD_DIRECTORY)/%.o
	$(Q)echo 'UnitLink' $@
	$(Q)g++ $< -o $@ $(UNITTEST_LDFLAGS) $(UNITTEST_LIBS)
#Crappy GCC bug: without two stage build, .gcno file created in current directory
