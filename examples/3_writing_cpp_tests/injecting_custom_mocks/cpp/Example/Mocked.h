#ifndef __MOCKED_H__
#define __MOCKED_H__

#include <memory>

class SomeClass
{
public:
	int generateValue();
};

#endif // __MOCKED_H__
// FILE_EXEMPT_FROM_CODE_COVERAGE
/*VOODOO_PERFILESETTINGS IGNORE_PARAMETER_PACK.append( 'ClassWithIgnoredParameterPack::someOperation' ) */
/*VOODOO_PERFILESETTINGS IGNORE_PARAMETER_PACK.append( 'ClassWithIgnoredParameterPack::ClassWithIgnoredParameterPack' ) */
