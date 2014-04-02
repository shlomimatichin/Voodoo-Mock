Unit Test Terminology:
----------------------
Unit Test is a term used for different things. Voodoo-Mock encourages a
recompilation tests, completly isolated from a real environment. No real
files, real network (even localhost), real timers or real OSes should be
used during the test - the test is a tool to verify that what you wrote
is what you had in mind to write. It is not a replacement for other kinds
of testing - but helps to reach those tests with a more mature result.

Since Voodoo-Mock works by replacing the classes and functions with a stub
implementations, each test file is compiled to its own executable.
Each file might have a different unit under test or stubbed APIs.

Good Unit-Test:
---------------
- Described a requirement from the unit under test, as an example flow.
- Test function name is detailed enough to catch which flow is implemented,
  and whats the difference from adjacent tests.
- Acts as a detailed documentation for other readers (or yourself few months
  from now).
- The unit under tests is logically separated from other layers in the code.
- Encourages you to write better designed code.
- Reproduces a found bug - and acts as regression for its return.

Bad Unit-Test:
--------------
- Unit under test is too small - test is overwhelmed with technical details,
  flows are tightly coupled. No concepts are abstracted, no complexity hidden
  away by unit. This might happen if you are testing a single class which is
  tightly coupled with others in the same layer.
- Unit under test is too large - it hard to express the exact condition you
  want to reproduce. Reader can get confused with what you had in mind. Test
  gets harder to maintain, and exception cases are harder to reach.
- Styrofoam test - a unittest for a "car" should test turning the wheel,
  accelerating and breaking. It should not enforce the exact shape of the
  car, the way you expect a pc monitor be enclosed inside styrofoam inside
  its packaging. Too much strictness, when testing something that is not an
  actuall requirement is a bad idea. This is especially relevant for Voodoo-Mock:
  because you need to write very little code for a unit test, its sometimes
  actually less code to write it more strict (e.g., adding an expectation
  to an existing scenario object, instead of creating an always object).
  For example: testing that the clock has been read exactly twice, or
  before or after a different uncorolated method, is a bad idea.
- Not strict enough - if someone can introduce a major defect without the
  test detecting it - then you might be testing too little. For example:
  ignoring paramters is dangerous. If your test checks that a file has been
  erased, but not which file, then a major defect can be introduced to the
  code without the unit test noticing. Implementing a stub call with
  "return 0;" has the same effect. So does adding an "environment effecting"
  call to an Always object.
- Coverage oriented - coverage verification is a feedback tool for writing
  tests. When the coverage is not good enough, you can improve it by writing
  a test for the missing flow. Do not write tests to "make the coverage tool
  happy" - you will just end up with crap. The packaged makefiles contain
  a feature to enforce code coverage. Turning it on just to produce crap
  tests is not a good idea.
