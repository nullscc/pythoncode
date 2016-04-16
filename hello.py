#!/usr/bin/python
#-*- coding:utf-8 -*-

'a hello module'

__author__ = 'nullscc'

import sys
def test():
	args = sys.argv
	lenarg = len(sys.argv)
	if lenarg == 1:
		print('hello world')
	elif lenarg == 2:
		print('hello %s' % sys.argv[1])
	else:
		print('hello another')

if __name__ == '__main__':
	test()
	
	
