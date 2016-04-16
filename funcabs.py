#!/usr/bin/python
#-*- utf-8 -*-

def my_abs(x):
	if(x>0):
		return x
	else:
		return -x

n = int(input('请输入一个整数：'))

print('abs(%d) = %d' %(n, my_abs(n)))
