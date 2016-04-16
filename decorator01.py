#!/usr/bin/python
#-*- coding:utf-8 -*-
import functools

def log(func):
	@functools.wraps(func)
	def wrapper(*args, **kw):
		f = func
		print('%s start' %func.__name__)
		func(*args, **kw)
		print('%s end' %func.__name__)
		return f
	return wrapper

@log
def printdate():
	print('2016-04-13')

printdate()

print(printdate.__name__)

