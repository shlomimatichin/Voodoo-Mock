Voodoo-Mock is a framework for `mock objects' based unit testing in C++.
Written in python (wrapping over CLang by LLVM project), Voodoo-Mock
parses C++ code, and generates redirection and mock classes. Voodoo-Mock
can be used with test suite frameworks such as CXXTest or CPPUnit.

The directory structure is as following:
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

Compiling:
----------
Voodoo-Mock requires a compiled version of libclang. The script
voodoo/compileclang.py helps with the steps necessary. The sources
of the project contain a version compiled for fedora19.

Using:
------
Please take a look at the examples directory.
