#ifndef __DATA_H_
#define __DATA_H_

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

struct MoveableCtorData
{
	MoveableCtorData( unsigned aa ) : a( aa ) {}
	MoveableCtorData( MoveableCtorData && o ) : a( std::move( o.a ) ) {}

	unsigned a;
};

struct MoveableData
{
	MoveableData( unsigned aa ) : a( aa ) {}
	MoveableData( const MoveableData & o ) : a( o.a ) {}
	MoveableData( MoveableCtorData && o ) : a( std::move( o.a ) ) {}

	MoveableData & operator=( MoveableData && o ) { a = std::move( o.a ); return *this; }

	unsigned a;
};

#endif // __DATA_H_
// FILE_EXEMPT_FROM_CODE_COVERAGE
