Your options:
1. Used packaged makefiles (linux/g++), quick and easy to get started,
   should be ok for most c++ projects.
2. Understand the flow for building tests, the tools, and reproduce the
   steps yourself in your faviourite build system. I have successfully
   used voodoo in a Windows environment this way.

Packaged Makefiles:
-------------------
Take a look at the examples directory. In short, you just need to create
a target with this recipe:
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/1_generate.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/2_build.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/3_run.Makefile
	$(MAKE) -f $(VOODOO_ROOT_DIR)/make/4_optional_enforce_cpp_coverage.Makefile
The last line, enforcing code coverage, is not mandatory.

Customization:
- Verbose output: Specify V=1 on the make command line to view the commands
  being run.
- Override the default compilation flags:
  UNITTEST_CXXFLAGS = -DDEBUG -DUNITTEST
  UNITTEST_INCLUDES = -I.
  UNITTEST_LDFLAGS =
  UNITTEST_LIBS = -ldl
  note: --coverage, -std=gnu++0x and other flags are added
  to these flags
- Scan a smaller directory structure than the whole project:
  Override the variables: CXXTEST_FIND_ROOT, PYTEST_FIND_ROOT,
  ENFORCE_COVERAGE_FIND_ROOT_CPP with a space separated list
  of directories to scan
- Customize file extensions and scanning rules:
  Override the variables: CXXTEST_FIND_PATTERN,
  PYTEST_FIND_PATTERN, ENFORCE_COVERAGE_FIND_PATTERN_CPP
- Generate voodoo mirror tree elsewhere:
  Override the variable: VOODOO_MIRROR_TREE
- use a different build directory than build_unittest:
  Override the variable: UNITTEST_BUILD_DIRECTORY

Flow for building unit tests:
-----------------------------
1. Voodoo Mirror Tree code generation - your projects header files are scanned, and for
   each one, a "voodoo header" is created at the same include path, under
   the voodoo mirror tree root. In the packaged makefiles, the root is
   placed under build_unittest/voodoo. So, for example, if you have a header
   directory/header.h, voodoo will generate
   build_unittest/voodoo/directory/header.h . This header does nothing but
   to include the original one, unless the interception macros are defined
   (see HOWTO_WRITING_TESTS.md).
   Generation of the Voodoo mirror tree is done by triggering the command
   line utility voodoo/multi.py (use --help to view command line options).
   You can trigger the build of any example with V=1 to view an example
   command line use.
2. Voodoo External Headers code generation - external headers allow you
   to deal with complicated headers from other projects (see relevant
   examples). These are generated with calling voodoo/single.py once for
   each such header.
3. Generate the CxxTest test-runner files - tools/cxxtest/cxxtestgen.py
   should be called once for each. cxxtestgen.py is documented as part of
   the CxxTest project (newer version of the framework exist online).
4. Build - build the generated CxxTest test-runner files. The include path
   must contain the Voodoo Mirror Tree as the first component in the
   include lookup paths list (first -I parameter for the compiler).
   Consider compiling the unittest without optimizations, with replacement
   of the ASSERT macro with a TS_FAIL (fail test macro), with debugging
   information and with coverage reporting.
5. Run the tests - the pytests/pytestharness.py runs all the executables
   concurrently, plus runs python unit tests (if given).
6. Optionally - report or enforce coverage. The tool
   make/enforce_cpp_coverage.py is one option you can use.
