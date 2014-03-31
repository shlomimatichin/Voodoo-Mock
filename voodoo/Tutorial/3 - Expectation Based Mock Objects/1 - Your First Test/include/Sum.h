#ifndef __SUM_H__
#define __SUM_H__

#include <Number.h>

class Sum
{
public:
	Sum( const Number & first , const Number & second ) :
		_result( first.value() + second.value() )
	{
	}

	unsigned result() const { return _result; }
private:
	unsigned _result;
};

#endif
