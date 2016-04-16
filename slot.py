#!/usr/bin/python
# -*- coding:utf-8 -*-

class Hello(object):
	def hello(self):
		print('hello, python')
	__slots__ = ('name', 'score')

a = Hello()

a.baga = 'null'

print(a.baga)
