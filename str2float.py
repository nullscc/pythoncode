#!/usr/bin/python
# -*- utf-8 -*-

from functools import reduce

def str2float(x):
	n = x.index('.')
	str1 = x[:n]
	str2 = x[n+1:]
	def f(m, n):
		return m*10 + n
	def char2num(s):
		return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
	return reduce(f, map(char2num, str1)) + reduce(f, map(char2num, str2))/(10**(len(x)-n-1))
	
s = input("Please input a str:")

print(str2float(s))
