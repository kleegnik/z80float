#!/usr/bin/python

from struct import unpack
from sys import argv

if len(argv)==2:
	h = argv[1]
	print unpack('!f', h.decode('hex'))[0]

