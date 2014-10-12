#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
typedef struct {
	unsigned int negative:1;
	unsigned int exponent:8;
	unsigned int fraction:23;
} ieee_float;
*/
 
int main(int argc, char **argv)
{
	float f;
	unsigned int *u;
	unsigned int fraction, exponent, sign;

	if (argc!=2) return 0;
	f = atof(argv[1]);

	/* Assuming sizeof(float) == sizeof(unsigned int) */
	u = (unsigned int *) &f;
	printf("%X\n", *u);

	sign = ((*u)>>31) & 1;
	exponent = ((*u)>>23) & 0xFF;
	fraction = ((*u) & 0x007FFFFF) | 0x00800000;

/*	printf("float    = %.9f\n", f);
	printf("sign     = %d\n", sign); */
	printf("fraction = 0x%X (%d)\n", fraction,fraction);
	printf("exponent = %d (%d)\n", exponent-127,exponent);
/*	printf("bias     = 127\n"); */

	/* printf("value    = (-1)^sign * (radix)^(exponent - bias) * (1).fraction\n"); */

	return 0;
}
