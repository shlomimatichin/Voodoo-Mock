Copy Construction In Expectation Based Mock Objects:
----------------------------------------------------

When a fake object called "ABC", of a mocked class or struct, is
copied, the new instance will automatically be called "Copy of ABC".
If that object gets copied, the new instance will be called
"Copy of Copy of ABC", and so on.

For every expectation primitive, except destruction, there is another
primitives, which ignores the "Copy of" prefix, or prefixes.

This allows maximum flexability: in some tests the exact copy makes
the difference, and in some, the exact copy does not matter.

Destruction does not have an "ignoring" sibling, as a way to force
the tester to be aware to the number of copies the code produces,
since each copy must have a destruction expectation for itself.

The voodoo expectations, and their "Copy of" ignoring alternatives are:
CallReturnVoid - CallOrCopyOfReturnVoid
CallReturnValue - CallOrCopyOfReturnValue
CallReturnReference - CallOrCopyOfReturnReference
CallReturnAuto - CallOrCopyOfReturnAuto
CallThrowValue - CallOrCopyOfThrowValue

The voodoo parameter expectation, which has an "Copy of" ignoring
version is:
Named - NamedOrCopyOf

When to ignore: if the tested code has a ownership of resources
symantics (i.e., you are testing auto_ptr, or shared_ptr), then
you don't want to ignore copies - the test should describe the life
of each copy, to be sure the resources are handled correctly.

however, if you are testing code, and mocking some other class,
which ownership symantics, and the mocked class is tested as a
different unit, and tested to be defensive againt abuse, then you
can safely ignore copying, since that aspect of the code you are not
testing.

The example tests a code that is suitable for ignoring copies.
Still, an example for how to test the same code considering copies
is also provided.
