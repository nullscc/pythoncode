#!/usr/bin/python
# -*- utf-8 -*-

def firstupper(x):
	x = x.lower()
	x = x.capitalize()
	return x


L = map(firstupper, ['adam', 'LISA', 'barT'])

print(list(L))

