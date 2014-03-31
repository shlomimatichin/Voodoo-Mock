Voodoo can be invoked to run on a single file at a time, or to scan a
complete trees of source code.

The goal is to provide each header file an alternative implementation. The
test suite compiler must make sure that the header file generated is included
before the real header, in the include order. I.e., if the output of multi
mode goes into the directory 'voodoo', then the compile switch -Ivoodoo must
come before any other -I switches.

Also note, that an #include directive with "" (instead of <>), adds the
current directory as the first directory in the include order, and therefore
can mess things up. This is solved by generating code for every file in the
source tree, so the #include "" will first look for files under the voodoo
output tree.

Single mode:
------------
please run python single.py --help for command line usage.

Multi mode:
-----------
please run python multi.py --help for command line usage.


just view the examples, and run them.
