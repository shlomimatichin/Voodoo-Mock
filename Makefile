all: build unittest

build: build_examples
clean: clean_examples

unittest: unittest_c unittest_cpp
unittest_c:
	cd voodoo; PYTHONPATH=. LD_LIBRARY_PATH=. python unittests/test_c_parsing.py
unittest_cpp:
	cd voodoo; PYTHONPATH=. LD_LIBRARY_PATH=. python unittests/test_cpp_parsing.py

clean_examples:
	make -C examples/1_simplest_project clean
	cd examples/2_feature_full_project_scaffold__copy_me; ./env make clean
	make -C examples/3_writing_cpp_tests/mocking_template_methods clean
	make -C examples/3_writing_cpp_tests/mocking_template_classes clean
	make -C examples/3_writing_cpp_tests/custom_stubs clean
	make -C examples/3_writing_cpp_tests/deriving_a_mocked_interface clean
	make -C examples/3_writing_cpp_tests/expectation_based_mock_objects clean
	make -C examples/6_coverage_enforcement clean

build_examples:
	make -C examples/1_simplest_project
	cd examples/2_feature_full_project_scaffold__copy_me; ./env make
	make -C examples/3_writing_cpp_tests/mocking_template_methods
	make -C examples/3_writing_cpp_tests/mocking_template_classes
	make -C examples/3_writing_cpp_tests/custom_stubs
	make -C examples/3_writing_cpp_tests/deriving_a_mocked_interface
	make -C examples/3_writing_cpp_tests/expectation_based_mock_objects
	make -C examples/6_coverage_enforcement
