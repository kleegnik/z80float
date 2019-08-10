#!/usr/bin/env python3

i = 1
while True:
    print(i, i & 0x7F)

    if i == 4 or i == 13:
        i |= 0x80
        continue

    i &= 0x7F
    i += 1
    if i > 19:
        break
