#ifndef __MAP_H__
#define __MAP_H__

#include "File.h"

//A fictitious "map" object from a number to a string
//by using different file in /tmp for each
class Map
{
public:
	Map( std::string name ) :
		_name( name )
	{}

	void set( const std::string & key, const std::string & value )
	{
		File( pathForKey( key ) ).write( value );
	}

	std::string get( const std::string & key )
	{
		return File( pathForKey( key ) ).read();
	}

private:
	std::string _name;

	std::string pathForKey( const std::string & key ) const
	{
		return "/tmp/map_" + _name + "_" + key + ".dat";
	}
};

#endif // __MAP_H__
