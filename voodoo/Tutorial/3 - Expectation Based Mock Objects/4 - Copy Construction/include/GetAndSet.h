#ifndef __GET_AND_SET_H__
#define __GET_AND_SET_H__

#include "PseudoSharedPtr.h"

void getAndSet()
{
	PseudoSharedPtr shared = get();
	setFirst( shared );
	setSecond( shared );
}

#endif // __GET_AND_SET_H__
