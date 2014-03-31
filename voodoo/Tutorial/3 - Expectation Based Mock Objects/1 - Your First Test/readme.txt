First of all, to use Voodoo-Mock, you must configure it. Don't worry, it
takes two seconds: You need to define few macros, in a file included as
#include "VoodooConfiguration.h"

There ready configurations in the VoodooCommon dir: one for CxxTest unit
testing frame work (very recommended), one for CppUnit (less recommended),
and one for working with plain exceptions, no unit testing frame work.
If you do happen to implement more configuration files for other unit-testing
frameworks, please contribute them back to the community.

For the purpose of the tutorial, the tests are written without a framework.

Now, just read the test file and two header files.
