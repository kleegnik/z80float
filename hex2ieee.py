#!/usr/bin/python

from struct import unpack
from sys import argv

if len(argv)==2:
    h = argv[1]
    if len(h)!=8:
        print "Must be 8 hex nibbles"
    else:
        print unpack('!f', h.decode('hex'))[0]
