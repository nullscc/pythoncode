#!/usr/bin/python
#-*- coding:utf-8 -*-

#还有问题

import functools

def log(*args):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			f = func
			print('%s %s start' %(args, func.__name__))
			f(*args, **kw)
			print('%s %s end' %(args, func.__name__))
			return f
		return wrapper
	if hasattr(args,'__call__')
		return log()(args)
	return decorator

@log('excute')
def printdate():
	print('2016-04-13')


printdate()
