python ..\..\..\multi.py --input=include --output=voodoo --exclude=VoodooConfiguration --only-if-new
copy /Y ..\..\..\VoodooCommon\VoodooConfigurationForNoTestSuite.hpp voodoo\VoodooConfiguration.h
cl /EHs tests\Test_All.cpp -Ivoodoo -Iinclude -I../../.. /Zi
Test_All.exe
