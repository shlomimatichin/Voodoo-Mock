#ifndef __TO_COVER_H__
#define __TO_COVER_H__

#include "SemiCoveredExemptFile.h"
#include <stdexcept>

void throwExceptionFunction()
{
	throw std::runtime_error( "Some error" );
}

template < typename T >
void aFunction( T input )
{
	input += 1; // covered line
	if ( input == 1000000 )
		input -= 1; // LINE_EXEMPT_FROM_CODE_COVERAGE
	// the next line is not a code line, but the EXCEPT comment will report misuse of the whitelisting
	// LINE_EXEMPT_FROM_CODE_COVERAGE
	if ( input == 10 )
		input -= 2; // this line is not covered therefore its a coverage error
	semiCoveredFunction( 10 );
	try {
		throwExceptionFunction();
	}
	catch ( std::runtime_error ) {
		input += 4;
	}
	catch ( std::exception ) { // LINE_EXEMPT_FROM_CODE_COVERAGE
		printf("hello\n"); // LINE_EXEMPT_FROM_CODE_COVERAGE
	}
	catch ( ... ) { // this line is not covered therefore its a coverage error
		printf("hello again\n"); // this line is not covered therefore its a coverage error
	}
}

void anotherFunction()
{
}

#endif // __TO_COVER_H__
