python ..\..\..\multi.py --input=include --output=voodoo --exclude=VoodooConfiguration --only-if-new
copy /Y ..\..\..\VoodooCommon\VoodooConfigurationForNoTestSuite.hpp voodoo\VoodooConfiguration.h
cl /EHs tests\Test_Sum.cpp -Ivoodoo -Iinclude -I../../..
Test_Sum.exe
