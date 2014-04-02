#include <iostream>
#include "MapExample/Map.h"

int main()
{
	std::cout << "hello world" << std::endl;
	MapExample::Map map( "example" );

	map.set( "firstKey", "firstValue" );
	std::cout << "firstKey: " << map.get( "firstKey" ) << std::endl;
	return 0;
}
//FILE_EXEMPT_FROM_CODE_COVERAGE
