#ifndef __NUMBER_H__
#define __NUMBER_H__

class Number
{
public:
	Number( unsigned value ) : _value( value ) {}
	unsigned value() const { return _value; }
private:
	unsigned _value;
};

#endif
