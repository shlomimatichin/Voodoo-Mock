#ifndef __MAP_EXAMPLE_MAP_H__
#define __MAP_EXAMPLE_MAP_H__

#include "MapExample/File.h"
#include "Common/Debug.h"

namespace MapExample
{

//A fictitious "map" object from a number to a string
//by using different file in /tmp for each
class Map
{
public:
	Map( std::string name ) :
		_name( name )
	{
		ASSERT_VERBOSE( name.size() > 0, "Map name must not be zero" );
		ASSERT_VERBOSE( name.find( ' ' ) != std::string::npos, "Map name must not contain spaces" );
	}

	void set( const std::string & key, const std::string & value )
	{
		TRACE_INFO( "Saving key '" << key << "'" );
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

} // namespace MapExample

#endif // __MAP_EXAMPLE_MAP_H__
