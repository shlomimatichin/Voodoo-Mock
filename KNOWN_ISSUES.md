Known Issues:
-------------
- #define of a built in type (e.g., 'int', 'bool'), causes CLang compiler
  to behave unexpectedly. Do not define those. A special treatment for
  including GCCs stdbool.h is handled inside
  voodoo/emulate_gcc_in_clang_preinclude.h . You might need to edit this
  file to force skipping of other issues not encoutered yet in voodoo
  development. If you do, please send a email or bug report our way.
- code created from macros can be included, but not parsed correctly
  to produce a valid header
