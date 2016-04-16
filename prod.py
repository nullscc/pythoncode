#!/usr/bin/python
# -*- utf-8 -*-

from functools import reduce

def prod(x, y):
	return x*y

print(reduce(prod, [1,2,10,10,10]))
