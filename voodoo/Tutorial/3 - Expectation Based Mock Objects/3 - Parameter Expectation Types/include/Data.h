#ifndef __DATA_H__
#define __DATA_H__

struct Data
{
	unsigned a;
	unsigned b;
};

class DoItInterface
{
public:
	virtual ~DoItInterface() {}
	virtual void doIt() = 0;
};

#endif // __DATA_H__
