#ifndef __FILE_H__
#define __FILE_H__

#include <fstream>

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

#endif // __FILE_H__
//FILE_EXEMPT_FROM_CODE_COVERAGE
