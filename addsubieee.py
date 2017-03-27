#!/usr/bin/python

from sys import argv,exit
from struct import pack,unpack


# --------------------------------------------------------------
"""
op  A  B   result (using absolute values of A and B)
+   +  +    A+B
+   -  -   -(A+B)
+   -  +   -(A-B)  $ *
+   +  -    A-B    $ *
-   +  +    A-B    $
-   -  -    -(A-B) $
-   -  +    -(A+B)   *
-   +  -    A+B      *

$ = sign changed when operands are exchanged
* = operation (+/-) exchanged
"""

# --------------------------------------------------------------
def printbin(l):
  for byte in range(4):
    bytestr = ''
    for bit in range(8):
      bytestr += str((l & 0x80000000)>>31)
      l <<= 1
    print bytestr,

  print


# --------------------------------------------------------------
if len(argv)!=4 or argv[1] not in ('-','+'):
  print 'Usage: %s <+|-> <augend> <addend>' % argv[0]
  exit(0)
op = argv[1]

# -- convert floats to unsigned long int of IEEE representation --
n1f = float(argv[2])
p = pack('f',n1f)
n1 = unpack('L',p)[0]
n2f = float(argv[3])
p = pack('f',n2f)
n2 = unpack('L',p)[0]
#print hex(n1),hex(n2)
if op=='+':
  r = n1f+n2f
else:
  r = n1f-n2f

# -- unpack into sign,exponent,fraction (setting implied bit at 23) --
s1 = n1>>31
e1 = (n1>>23) & 0xFF
f1 = (n1 & 0x007FFFFF) | 0x00800000
s2 = n2>>31
e2 = (n2>>23) & 0xFF
f2 = (n2 & 0x007FFFFF) | 0x00800000
#printbin(f1)
#printbin(f2)

print s1,e1,hex(f1)
print s2,e2,hex(f2)

# initialise sign of result
st = s1   # same as sign of first operand

# -- compare exponents, swap if needed, align other fraction --
d = e1-e2
if d<0:
  print 'swap operands'
  tmp = (s1,e1,f1)
  (s1,e1,f1) = (s2,e2,f2)
  (s2,e2,f2) = tmp
  tmp = n1f
  n1f = n2f
  n2f = tmp
  d = -d
  if (s1!=s2) ^ (op=='-'):
    # swap sign if:
    # for addition - signs are different
    # for subtraction - signs are the same
    st = 1-st
    print 'swap sign as operands are reversed'

if d>23:
  # exponent difference is too large; nothing to add
  print 'large exp diff = %d' % d
  print 'result = %f' % n1f
  exit(0)

if d!=0:
  # shift addend right until exponents match
  f2 >>= d


# -- add fractions --
#    1.xxxxxxx
# +  1.xxxxxxx or 0.xxxxxxx (shifted addend)
#
# =  01.xxxxxxx
# or 10.xxxxxxx
# or 11.xxxxxxx
#
# result will be one of (with leftmost bit being 24):
#
#  0 1xxxxxxx ..
#  1 0xxxxxxx ..
#  1 1xxxxxxx ..
#
# -- subtract fractions --
# result may be negative (but no overflow)
#
#    1.xxxxxxx
# -  1.xxxxxxx or 0.xxxxxxx (shifted subtrahend)
#
# =  0 0xxxxxxx
# or 0 1xxxxxxx
# or 1 0xxxxxxx
# or 1 1xxxxxxx

if s1!=s2:
  # signs are different: change add/sub operation
  if op=='+':
    op = '-'
  else:
    op = '+'
if op=='+':
  a = f1+f2
else:
  a = f1-f2

print ' ',
printbin(f1)
print op,
printbin(f2)
print '=',
printbin(a)

if (a&0x01000000)!=0:
  # bit 24 set
  if op=='+':
    a >>= 1
    e1 += 1
    print '>>1: ',
  else:
    # negate fraction
    a = (-a) & 0x007FFFFF
    st = 1-st     # swap sign
    print 'swap sign as negative result after subtracting'

  # otherwise bit 24 clear - no overflow or change of sign.

# for subtraction, normalise
if op=='-':
  if a==0:
    # zero result
    e1 = 0
    st = 0
  else:
    while (a&0x00800000)==0:
      a <<= 1
      e1 -=1

printbin(a)
print

# -- pack everything back --
a &= 0x007FFFFF
s = (st<<31) | (e1<<23) | a
print
print s1,e1
print hex(s)
printbin(s)

p = pack('L',s)
fl = unpack('f',p)[0]
print '=', fl, '(%.7f)' % r   # without formatting or rounding
