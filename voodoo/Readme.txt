Voodoo-Mock 8
------------------------------

Voodoo-Mock is a C++ parser and generator. It parses your code, and produces
header files that can "replace" your classes and functions, with expectation
based mock objects, or programmable mock objects.

Expectation based mock objects and Programmable mock objects are two paradigms
for writing stubs code, for the purpose of unit testing. In unit testing, you
select your unit, and seperate it from the rest of the code, by emulating
the enviroment it expects. In C++, this is done by providing stub
implementations for the functions and classes the unit "sees". Voodoo-Mock
takes much of the burden off the tester, for writing these stubs.

In expectations based mock objects, the tester writes the "scenario" he or
she expects to accour, then the tester calls the unit itself. The code in
the tested unit runs, and it's inputs and outputs are compared agaist the
scenario. This approach has the advantage of very simple and fast unit test
implementation.

In programmable mock objects, every mock entity becomes a pointer to
implementation. The tester programs the stubs, but can "replace" the
implementation of any entity at any time during run time.

Voodoo-Mock parser-generator is written in python, and is based on the CLang
compiler for parsing (CLang is the C++ frontend of the LLVM project).

Quick Example:
--------------

To quickly grasp the concept of Voodoo-Mock, consider the following function:

void something( Object & o )
{
	if ( o.path1() ) {
		o.doPath1( 1 );
	} else {
		o.doPath2( 2 );
	}
}

to cover it completly, using expectation based mock objects, two test cases
are required:

Scenario scenario;
scenario <<
	new CallReturnValue< bool >( "Fake Object::something" , true ) <<
	new CallReturnVoid( "Fake Object::doPath1" ) <<
		new EqualsValue< unsigned >( 1 );
something( FakeND_Object( "Fake Object" ) );
scenario.assertFinished();

Scenario scenario;
scenario <<
	new CallReturnValue< bool >( "Fake Object::something" , true ) <<
	new CallReturnVoid( "Fake Object::doPath2" ) <<
		new EqualsValue< unsigned >( 2 );
something( FakeND_Object( "Fake Object" ) );
scenario.assertFinished();

Design Considerations:
----------------------
The reason for writing voodoo-mock, is that no existing package for this
purpose has the following concerns in mind:
1. No modification of real code required - can add tests to existing code.
2. Prefers recompilation of code for testing, rather than testing the
   real object files.
3. Scalable for large projects - automatic, no user intervention, fast.

Getting Started:
----------------
to get started, please check the chapters in the Tutorial directory.

Credit and License:
-------------------
Voodoo-Mock 9 is written as my contribution to the world of quality software
development. I encourage you to switch to the eXtreme Programming methodology,
I would gladly provide advice, if contacted. shlomomatichin at gmail dot com.

Voodoo-Mock is released under the GPLv3 and any future version of the GPL.
CLang by the LLVM project: http://clang.llvm.org/
The Exceptional C++ parser by the Open C++ Core project: http://www.opencc.org.
Voodoo-Mock homepage: http://voodoo-mock.sf.net
Other projects you might find interesting:
CxxTest: http://cxxtest.sf.net
PyVoodoo: http://pyvoodoo.sf.net
Copyright Shlomo Matichin 2013
