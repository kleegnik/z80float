#!/usr/bin/python

from math import exp
from matplotlib import pyplot as plt
from sys import argv,exit

# Chebyshev expansion as polynomial -> near Maclaurin series

# double accuracy (8)
"""
coeff = [0.999999801337,
0.999999900943,
0.500006347345,
0.166667985598,
0.0416350120349,
0.00832859610679,
0.00143927433455,
0.000204699933615,
]

(12)
0 0.999999999999
1 0.999999999999
2 0.500000000075
3 0.166666666681
4 0.0416666657961
5 0.00833333321726
6 0.00138889259965
7 0.00019841309582
8 2.47944430434e-05
9 2.75507080616e-06
10 2.81901799326e-07
11 2.55791945847e-08
"""

# for single IEEE float
coeff = [0.99999980,
0.99999990,
0.50000635,
0.16666799,
0.04163501,
0.00832860,
0.00143927,
0.00020470]

ncoeff = len(coeff)

xdata = []
ydata = []
x = -1.0
while x<=1.0:
    e = coeff[ncoeff-1]
    for n in range(ncoeff-2,-1,-1):
        e = e*x+coeff[n]

    ex = exp(x)
    print x,e,ex,e-ex
    x += 0.1
    xdata.append(x)
    ydata.append(ex-e)

plt.plot(xdata,ydata)
plt.show()
plt.close()


"""
; a 7th order Chebyshev polynomial:
; sin(x) ~= x - 0.166666546*x^3 + 0.00833216076*x^5 - 0.000195152832*x^7
;
;x2 = x*x
;sin(x) = x*(1+x2*(a + x2*(b + c*x2)))
;
; [= x-a*pow(x,3)+b*pow(x,5)-c*pow(x,7)]
"""
