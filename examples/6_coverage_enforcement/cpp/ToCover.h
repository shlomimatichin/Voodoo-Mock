#ifndef __TO_COVER_H__
#define __TO_COVER_H__

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
}

#endif // __TO_COVER_H__
