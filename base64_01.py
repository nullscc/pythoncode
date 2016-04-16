#!/usr/bin/python
# -*- coding:utf-8 -*-

import base64

#print(base64.b64encode(b'binary\x00string'))
#print(base64.b64decode(b'YmluYXJ5AHN0cmluZw=='))

def mybase64(s):
	a = (-len(s)) % 4
	s=s+b'='*a
	print(type(s))
	print(s)
	return base64.b64decode(s)

m = b'w'
print(mybase64(b'w==='))

print(type(b'wwww'))
print(type('ssss'))
print(type(m))

#print((-len(s))%4)

#print((-1)%4)


