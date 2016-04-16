#!/usr/bin/python
# -*- utf-8 -*-

def angle(n):
	if(n>0):
		yield n
		n-=1
	return None

L = angle(5)
for x in L:
	print(x)
