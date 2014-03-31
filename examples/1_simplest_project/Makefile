all: test

export VOODOO_ROOT_DIR = ../..

clean:
	rm -fr build_unittest build

test: buildall
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/1_generate.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/2_build.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/3_run.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/4_optional_enforce_cpp_coverage.Makefile

buildall: build/main

build/main: main.cpp File.h Map.h
	-mkdir $(@D)
	g++ -o $@ $< -Wall
