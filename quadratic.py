#!/usr/bin/python
#-*- utf-8 -*-
import math

def quadratic(a, b, c):
	delta = b**2 - 4*a*c
	if delta < 0:
		return None
	elif delta > 0:
		return ((((-b)+math.sqrt(delta))/(2*a)), (((-b)-math.sqrt(delta))/(2*a)))
	elif delta == 0:
		return (((-b)+math.sqrt(delta))/(2*a))

print("Please input three number:");

a = int(input())
b = int(input())
c = int(input())

print('a:%d, b:%d, c:%d' % (a, b, c))

#print('result is:%s' % quadratic(a, b, c))
print(quadratic(a, b, c))
