#ifndef __SEMI_COVERED_EXEMPT_FILE_H__
#define __SEMI_COVERED_EXEMPT_FILE_H__

int semiCoveredFunction( int i )
{
	if ( i == 123456 )
		i -= 1; // not covered, but it's ok since the file is exempt
	return i;
}

#endif // __SEMI_COVERED_EXEMPT_FILE_H__
//FILE_EXEMPT_FROM_CODE_COVERAGE
