#ifndef __MAP_EXAMPLE_FILE_H__
#define __MAP_EXAMPLE_FILE_H__

#include <fstream>

namespace MapExample
{

class File
{
public:
	File( std::string filename ) :
		_filename( filename )
	{}

	std::string read()
	{
		std::ifstream input( _filename.c_str(), std::ifstream::in );
		std::string out;
		input >> out;
		return out;
	}

	void write( std::string content )
	{
		std::ofstream output;
		output.open( _filename.c_str() );
		output << content;
	}

private:
	std::string _filename;
};

} // namespace MapExample

#endif // __MAP_EXAMPLE_FILE_H__
//FILE_EXEMPT_FROM_CODE_COVERAGE
