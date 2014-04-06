VIM Shortcuts For Running Tests:
--------------------------------
F4 - runs make, which usually runs all tests too
F3 - switches to the buffer marked by the Captial-T marker, and attempts
     to run it as a test file. Works both for Test_*.h C++/C tests files,
     and test_*.py test files.
F2 - switches to the buffer marked by the Captial-T marker, and attempts
     to run the single test the marker points to (the marker is on one of
     the lines in the test). This works for with Test_*.h C++/C test files,
     and test_*.py test files.

These shortcuts are defined by vim/plugin/runtests.vim, and depend on a
working test_singletest and test_singletestsuite make targets. Take a look
at examples/2_feature_full_project_scaffold__copy_me/Makefile .

VIM Shortcuts For Writing Voodoo Based UnitTests:
-------------------------------------------------
Ctrl-F3 - Runs the voodoo compiler over the header currently open in vim.
          When the voodoo compiler reports error compiling a specific
          header file, this helps to shorten the fixing cycles.
          This shortcut depends on a voodoo_compileSingleHeader makefile
          target (take a look at 
          examples/2_feature_full_project_scaffold__copy_me/Makefile )
Ctrl-F4 - Forces regeneration of all the voodoo mirror tree. Helpful when
          the compilation error of a voodoo header is from a dependency
          header.
          This shortcut is just a wrapper around a voodoo_forceGenerateAll
          makefile target (take a look at
          examples/2_feature_full_project_scaffold__copy_me/Makefile )

VoodooHint:
-----------
While compiling the voodoo mirror tree, voodoo indexes the signatures
of all functions and methods it encounters. The vim shortcut Ctrl-F6,
which wraps the script voodoo/voodoohint.py, allows the lookup of the
indentifier in this index, and fills the basic << new Call...<>() <<
parameters structure for you. For example, if you want to call File::read
then you only need to write the identifier 'read' in a line, and press
Ctrl-F6.

ColumIdent:
-----------
ColumIdent fancy indents lists of function parameters and variable
definitions, in c/c++/python. For example: if you stand over a line in c++
that looks like this:
void func( int a, bool * b, unsigned long long c ) and press F6, the output
will look something like this:
void func( int                 a,
           bool *              b,
           unsigned long long  c )
Please note: if your list is already spanning several lines, you must tell
this shortcut how many lines to scan. For example, take the following
class member list:
int a;
bool * b;
unsigned long long c;
you will have to invoke the shortcut by going to the first line, and
pressing 3F6 (the numeral key 3).
The configuration of ColumIndent is located at vim/columindent/configmain.py
. You might want to change parameters according to your project preferences:
For example, the maximum line length, and wither to use tabs or spaces for
indentation is configured there.

ConstructorReferenceArguments:
------------------------------
The VIM command ":ConstructorReferenceArguments" generates the initialization
list both for python __init__ functions and CPP constructors. Saves some
typing time.

DirtyTrace:
-----------
The VIM command ":DirtyTrace" puts a print statement in python files, or a 
cout<< statement in cpp files, surrounded by zero level indentation comments.
This allows to spot left behind debugging code easily when reviewing the
diff before commit.

NewFile:
--------
The VIM command ":NewFile" will create a file from a template. The files this
python script knows to generate: Test_*.h C++ test files, python test_*.py
test files, and *.h class header files.

this command is just a wrapper for the script vim/newfile.py, and defined in
vim/settings.vim

Ctags:
------
The VIM command ":Ctags" will use the "ctags" command line utility to create
tags for your project.

VIM buffer explorer plugin:
---------------------------
enter the three charaters '\be' when not in edit mode in VIM, to open the
buffer explorer.
