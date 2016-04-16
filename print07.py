#!/usr/bin/python
#-*- utf-8 -*-

L = list(range(101))

sum = 0
n = 100


while n >= 0:
	sum = sum + L[n]
	n -=1
print(sum)


