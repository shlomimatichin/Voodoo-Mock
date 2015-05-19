#ifndef __VOODOO_PRE_INCLUDE_H__
#define __VOODOO_PRE_INCLUDE_H__

typedef float __m128 __attribute__ ((__vector_size__ (16), __may_alias__));
typedef float __v4sf __attribute__ ((__vector_size__ (16)));
typedef float __v2sf __attribute__((__vector_size__(8)));
typedef double __v2df __attribute__ ((__vector_size__ (16)));
typedef double __m128d __attribute__((__vector_size__(16)));
typedef int __v4si __attribute__((__vector_size__(16)));
typedef long long __v2di __attribute__ ((__vector_size__ (16)));
typedef long long __m128i __attribute__((__vector_size__(16)));
typedef char __v16qi __attribute__((__vector_size__(16)));
typedef short __v8hi __attribute__ ((__vector_size__ (16)));
typedef int __v4si __attribute__ ((__vector_size__ (16)));


int __builtin_ia32_bsrsi( int ) { return 0; }
// unsigned long long __builtin_ia32_rdpmc( int ) { return 0; }
// unsigned long long __builtin_ia32_rdtsc() { return 0; }
unsigned long long __builtin_ia32_rdtscp( void * ) { return 0; }
unsigned char __builtin_ia32_rolqi(unsigned char __X, int __C) { return '\0'; }
unsigned short __builtin_ia32_rolhi (unsigned short __X, int __C) { return 0; }
unsigned char __builtin_ia32_rolqi (unsigned short __X, int __C) { return 0; }
unsigned char __builtin_ia32_rorqi(unsigned char __X, int __C) { return '\0'; }
unsigned short __builtin_ia32_rorhi(unsigned short __X, int __C) { return 0; }
void __builtin_ia32_pause( void ) {}
int __builtin_ia32_bsrdi( long long ) { return 0; }
__m128 __builtin_ia32_addss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpeqss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpless( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpltss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpneqss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpnless( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpnltss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpordss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpunordss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_cvtsi2ss( __v4sf, int ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_cvtsi642ss( __v4sf, long long ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_divss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_movss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_mulss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_rcpss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_rsqrtss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_sqrtss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_subss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_addps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_andnps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_andps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpeqps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_cmpgeps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_cmpgtps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpleps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpltps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpneqps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_cmpngeps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_cmpngtps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpnleps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpnltps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpordps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
// __m128 __builtin_ia32_cmpunordps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_cvtpi2ps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_divps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_loadhps( __v4sf, const __v2sf * ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_loadlps( __v4sf, const __v2sf * ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_loadups( float const * ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_movhlps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_movlhps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_movmskps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_movntps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_mulps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_orps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_rcpps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_rsqrtps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__v4sf __builtin_ia32_shufps( __v4sf, __v4sf, int ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_sqrtps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_storehps( __v2sf *, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
void __builtin_ia32_storelps( __v2sf *, __v4sf ) {}
__m128 __builtin_ia32_storeups( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_subps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_unpckhps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_unpcklps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_xorps( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
long long __builtin_ia32_cvttss2si64( __v4sf ) { return 0; }
int __builtin_ia32_cvttss2si( __v4sf ) { return 0; }
float __builtin_ia32_vec_ext_v4sf( __v4sf, int ) { return 0.0; }
void __builtin_ia32_movntq( unsigned long long *, unsigned long long ) {};
__m128d __builtin_ia32_movsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_loadupd(double const *) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_shufpd( __m128d, __m128d, int ) { return (__m128d){ 0.0, 0.0 }; }
double __builtin_ia32_vec_ext_v2df( __m128d, int ) { return 0.0; }
int __builtin_ia32_vec_ext_v4si( __v4si, int ) { return 0; }
long long __builtin_ia32_vec_ext_v2di( __v2di, int ) { return 0; }
__m128d __builtin_ia32_addpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_addsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_subpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_subsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_mulpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_mulsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_divpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_divsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_andpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_andsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_andnpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_andnsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_orpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_orsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_xorpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpltpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpunordsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpnltpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpnlesd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_cmpgtpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpneqsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpordpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_cmpngtpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_cmpgepd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpneqpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpordsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpeqpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128d __builtin_ia32_cmpngepd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpnlepd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmplepd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpnltsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpeqsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmplesd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpltsd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
// __m128d __builtin_ia32_cmpunordpd( __v2df, __v2df ) { return (__m128d){ 0.0, 0.0 }; }
__m128i __builtin_ia32_loaddqu( char const * ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_movq128( __v2di ) { return (__m128i){ 0, 0 }; }
int __builtin_ia32_cvttsd2si( __v2df ) { return 0; }
long long __builtin_ia32_cvttsd2si64( __v2df ) { return 0; }
__m128 __builtin_ia32_cvtsd2ss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128 __builtin_ia32_cvtsi2ss( __v4sf, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128d __builtin_ia32_cvtsi2sd( __v2df, int ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128d __builtin_ia32_cvtsi642sd( __v2df, long long ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128d __builtin_ia32_cvtss2sd( __v2df, __v4sf ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128d __builtin_ia32_unpckhpd( __v2df, __v2df ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128d __builtin_ia32_unpcklpd( __v2df, __v2df ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128d __builtin_ia32_loadhpd( __v2df, double const * ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128d __builtin_ia32_loadlpd( __v2df, double const * ) { return (__m128){ 0.0f, 0.0f, 0.0f, 0.0f }; }
__m128i __builtin_ia32_punpckhbw128( __v16qi, __v16qi ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_punpckhwd128( __v8hi, __v8hi ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_punpckhdq128( __v4si, __v4si ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_punpckhqdq128( __v2di, __v2di ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_punpcklbw128( __v16qi, __v16qi ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_punpcklwd128( __v8hi, __v8hi ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_punpckldq128( __v4si, __v4si ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_punpcklqdq128( __v2di, __v2di ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_paddb128( __v16qi, __v16qi ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_paddw128( __v8hi, __v8hi ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_paddd128( __v4si, __v4si ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_paddq128( __v2di, __v2di ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_psubb128( __v16qi, __v16qi ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_psubw128( __v8hi, __v8hi ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_psubd128( __v4si, __v4si ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_psubq128( __v2di, __v2di ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_pmullw128( __v8hi, __v8hi ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_pand128( __v2di, __v2di ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_pandn128( __v2di, __v2di ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_por128( __v2di, __v2di ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_pxor128( __v2di, __v2di ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_pcmpeqb128 ( __v16qi, __v16qi ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_pcmpeqw128 ( __v8hi, __v8hi ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_pcmpeqd128 ( __v4si, __v4si ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_pcmpgtb128 ( __v16qi, __v16qi ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_pcmpgtw128 ( __v8hi, __v8hi ) { return (__m128i){ 0, 0 }; }
__m128i __builtin_ia32_pcmpgtd128 ( __v4si, __v4si ) { return (__m128i){ 0, 0 }; }
// unsigned char __builtin_ia32_addcarryx_u32( unsigned char, unsigned int, unsigned int, unsigned int * ) { return '\0'; }
unsigned char __builtin_ia32_addcarryx_u64( unsigned char, unsigned long, unsigned long, unsigned long long * ) { return '\0'; }

#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <functional>

#define __attribute__( x )

#define _X86INTRIN_H_INCLUDED

#define _STDBOOL_H
#define _Bool	bool
#define __bool_true_false_are_defined	1

#endif // __VOODOO_PRE_INCLUDE_H__
