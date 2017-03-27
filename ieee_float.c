#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
   float f;
   unsigned int *u;
   unsigned int fraction, exponent, sign;

   if (argc!=2) return 0;
   f = atof(argv[1]);

   /* Assuming sizeof(float) == sizeof(unsigned int) */
   u = (unsigned int *) &f;
   printf("%.8X\n", *u);

   sign = ((*u)>>31) & 1;
   exponent = ((*u)>>23) & 0xFF;
   fraction = ((*u) & 0x007FFFFF) | 0x00800000;

   printf("sign = %d\n", sign);
   if (exponent==0 && fraction==0x800000) {
      /* +/- zero */
      printf("fraction = 0x000000 (0)\n");
      printf("exponent = 0 (0)\n");
   }
   else {
      printf("fraction = 0x%X (%d)\n", fraction,fraction);
      printf("exponent = %d (%d)\n", exponent-127,exponent);
   }

   return 0;
}
