all: build unittest

build: build_examples
clean: clean_examples

ifdef SystemRoot
# Windows system
SET_ENV_VAR=& set PYTHONPATH=%PYTHONPATH%;. & set LD_LIBRARY_PATH=%LD_LIBRARY_PATH%;. &
MAKE_EXAMPLE_2=make -C examples/2_feature_full_project_scaffold__copy_me
else
#Non-winsodw system
SET_ENV_VAR=; PYTHONPATH=. LD_LIBRARY_PATH=.
MAKE_EXAMPLE_2=cd examples/2_feature_full_project_scaffold__copy_me; ./env make
endif

unittest: unittest_c unittest_cpp
unittest_c:
	cd voodoo $(SET_ENV_VAR) python unittests/test_c_parsing.py
unittest_cpp:
	cd voodoo $(SET_ENV_VAR) python unittests/test_cpp_parsing.py

clean_examples:
	make -C examples/1_simplest_project clean
	$(MAKE_EXAMPLE_2) clean
	make -C examples/3_writing_cpp_tests/mocking_template_methods clean
	make -C examples/3_writing_cpp_tests/mocking_template_classes clean
	make -C examples/3_writing_cpp_tests/custom_stubs clean
	make -C examples/3_writing_cpp_tests/deriving_a_mocked_interface clean
	make -C examples/3_writing_cpp_tests/expectation_based_mock_objects clean
	make -C examples/6_coverage_enforcement clean

build_examples:
	make -C examples/1_simplest_project
	$(MAKE_EXAMPLE_2)
	make -C examples/3_writing_cpp_tests/mocking_template_methods
	make -C examples/3_writing_cpp_tests/mocking_template_classes
	make -C examples/3_writing_cpp_tests/custom_stubs
	make -C examples/3_writing_cpp_tests/deriving_a_mocked_interface
	make -C examples/3_writing_cpp_tests/expectation_based_mock_objects
	make -C examples/6_coverage_enforcement
