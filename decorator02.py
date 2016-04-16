#!/usr/bin/python
#-*- coding:utf-8 -*-
import functools

def log(text):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			f = func
			print('%s %s start' %(text, func.__name__))
			f(*args, **kw)
			print('%s %s end' %(text, func.__name__))
			return f
		return wrapper
	return decorator

@log('excute')
def printdate():
	print('2016-04-13')

printdate()
