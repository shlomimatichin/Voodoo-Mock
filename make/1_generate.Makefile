generateTests: generateCxxtest generateVoodoo

include $(VOODOO_ROOT_DIR)/make/common.Makefile

VOODOO_SCAN_HEADERS_ROOTS ?= .
VOODOO_MULTI_EXCLUDES ?= "\btests/"
VOODOO_FLAGS ?= --define=DEBUG --define=BOOST_ASIO_HAS_MOVE
VOODOO_EXTERNALS_FLAGS ?=
VOODOO_INCLUDES ?= --includePath=.

__VOODOO_ENVIRONMENT = PYTHONPATH=$(VOODOO_ROOT_DIR)/voodoo LD_LIBRARY_PATH=$(VOODOO_ROOT_DIR)/voodoo:$(LD_LIBRARY_PATH)
__VOODOO_MULTI_EXECUTABLE = $(__VOODOO_ENVIRONMENT) python $(VOODOO_ROOT_DIR)/voodoo/multi.py
__VOODOO_MULTI_INPUT = $(addprefix --input=,$(VOODOO_SCAN_HEADERS_ROOTS))
__VOODOO_MULTI_EXCLUDES = $(addprefix --exclude=,$(VOODOO_MULTI_EXCLUDES) \b$(UNITTEST_BUILD_DIRECTORY)\b)
__VOODOO_SINGLE_EXECUTABLE = $(__VOODOO_ENVIRONMENT) python $(VOODOO_ROOT_DIR)/voodoo/single.py
__VOODOO_FLAGS = $(VOODOO_FLAGS) --voodooDB=$(UNITTEST_BUILD_DIRECTORY)/voodooDB.tmp $(VOODOO_INCLUDES)

$(if $(filter-out %.cxx,$(CXXTEST_GENERATED)),\
	$(error "Unfamiliar extension for test suite files. Supported:" $(__POSSIBLE_UNITTEST_SUFFIXES)))

define template_per_TEST_FILE
template_per_TEST_FILE_cxx = $$(filter %.cxx,$$(foreach suffix,$(__POSSIBLE_UNITTEST_SUFFIXES),$$(patsubst %$$(suffix),$(UNITTEST_BUILD_DIRECTORY)/%.cxx,$$(subst /,_,$(1)))))
generateCxxtest: $$(template_per_TEST_FILE_cxx)
$$(template_per_TEST_FILE_cxx): $(1)
endef
$(foreach testFile,$(CXXTEST_TEST_FILES), $(eval $(call template_per_TEST_FILE,$(testFile))) )

generateCxxtest: $(CXXTEST_GENERATED)

generateVoodoo:
	@echo "Generating voodoo mirror tree"
	-@mkdir --parents $(VOODOO_MIRROR_TREE)
	$(Q)$(__VOODOO_MULTI_EXECUTABLE) $(__VOODOO_MULTI_INPUT) --output=$(VOODOO_MIRROR_TREE) --concurrent $(__VOODOO_FLAGS) $(__VOODOO_MULTI_EXCLUDES) --onlyIfNew

#TODO: missing force external headers
generateVoodooForce:
	@echo "Force Generating voodoo mirror tree"
	-@mkdir --parents $(VOODOO_MIRROR_TREE)
	$(Q)$(__VOODOO_MUTLI_EXECUTABLE) $(__VOODOO_MULTI_INPUT) --output=$(VOODOO_MIRROR_TREE) --concurrent $(__VOODOO_FLAGS) $(__VOODOO_MULTI_EXCLUDES)

generateSingleVoodoo:
	$(Q)$(__VOODOO_SINGLE_EXECUTABLE) --input=$(SINGLE_HEADER) --output=/tmp/t.h $(__VOODOO_FLAGS)

$(VOODOO_MIRROR_TREE)/%.h:
	@mkdir -p $(@D)
	@echo 'VOODOOEX' $@
	$(Q)$(__VOODOO_SINGLE_EXECUTABLE) --input=$< --output=$@ $(__VOODOO_FLAGS) $(VOODOO_EXTERNALS_FLAGS)

$(UNITTEST_BUILD_DIRECTORY)/%.cxx:
	-$(Q)mkdir --parents $(@D)
	@echo 'CXXTSTGN' $@
	$(Q)python $(VOODOO_ROOT_DIR)/cxxtest/simplecxxtestgen.py --output=$@ --input=$< 
