[![Build status](https://ci.appveyor.com/api/projects/status/vf533umpc9rodgwj?svg=true)](https://ci.appveyor.com/project/ShlomiMatichin/voodoo-mock)
[![wercker status](https://app.wercker.com/status/6319d5b975f2523fdd6baa807c13a91a/m "wercker status")](https://app.wercker.com/project/bykey/6319d5b975f2523fdd6baa807c13a91a)

Voodoo-Mock is a framework for `mock objects' based unit testing in C++.
Written in python (wrapping over CLang by LLVM project), Voodoo-Mock
parses C++ code, and generates redirection and mock classes. Voodoo-Mock
can be used with test suite frameworks such as CXXTest or CPPUnit.

Features:
---------
1. Code-generation of stubs:
   - no stub code maintainance
   - no need to change original code (no macros, no interfaces)
   - you only need to write the test
2. Simple language to describe "recorded scenarios" which are
   "played back" when the code under test runs.
   - write less code to test
   - uniformity - most tests in the project look alike.
   - alternativly - redirect call to stub code easily, and dynamically
     change implementation.
3. Start in minutes using attached makefiles and tools
   - attached makefiles fit most linux projects
   - include coverage-not-degraded enforcement tool
   - include awesome VIM integration utilitys - quicken your cycle.
4. Voodoo-mock now supports C++0x11 parsing using CLang

More than 10000 unit tests were already written using the
different versions of Voodoo-mock. Projects using it include windows
drivers (c), linux drivers (c), linux daemons (c++0x11), and python
eco-systems. This version is the 9th major update. Hope you'll find
it useful, and good luck in your endeavours.

What does it do?
----------------
Auto-generates code stub that allows you to write tests that look like this
(pseudo code):
```
Create Scenario:
   The function A would be called with parameters a and b
   The function C would be called with parameters c and d
Run the unit under test
Verify all calls in the scenario completed successfully
```
A simple concrete example can be found in examples/1_simplest_example/tests/Test_Map.h

Directory Structure:
--------------------
- voodoo - the C++ mock objects code generator. The two command line
           entry points are "single.py" and "multi.py". Have a look at
           their "--help" options, or just look in the "examples"
           directory to learn how to use it.
- cxxtest - a forked version of CXXTest framework. Contains several
            extensions over the original CXXTest version is got forked
            from.
- make - an example makefile of how to integrate voodoo into your project.
         the makefiles here are called from production projects, and so
         are proven to work.
- pytest - a python unit testing and under pytest/pyvoodoo, a python unit
           test framework that uses the same paradigm as voodoo's
           expectation based mock objects. This helps to keep a single
           "language" for unit tests, for projects that use both languages.
- vim - plugins with awesome shortcuts for vim editor.
- examples - some examples of projects that use voodoo.

Installation:
-------------
1. Checkout the code
2. Compile libclang.so (fedora19 compiled version is already included)
3. Integrate into your project and IDE.

Compiling libclang.so:
----------------------
Voodoo-Mock requires a compiled version of libclang. The script
voodoo/compileclang.py helps with the steps necessary. The sources
of the project contain a version compiled for fedora19.

Quickest Integration:
---------------------
Take a look at examples/1_simplest_project/Makefile. All you need
to do is:
1. Export VOODOO_ROOT_DIR=<path to this directory>
2. create the "test" target. It is recommended that the main targets
   will be compiled first, as compilation errors are usually easier
   to handle.
3. All unittest build product will be created under the directory
   build_unittest. Add it to your clean list.

What now?
---------
Read the other .md files in this directory for more information.
