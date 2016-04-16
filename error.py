#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging

def fun(s):
	if s == 0:
		raise ValueError('could not be zero')


try:
	print('hehe')
	fun(0)
	print('haha')
except ValueError as e:
#except ValueError:	
	print('ValueError')
	#logging.exception(e)
finally:
	print('finally...')
print("i'm here")

