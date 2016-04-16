#!/usr/bin/python
# -*- utf-8 -*-

def findkey(s):
	return s[0]

L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

print(sorted(L, key=findkey))
