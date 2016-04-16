#!/usr/bin/python
# -*- coding:utf-8 -*-

from types import MethodType

def __len__(self):		#必须要有self
	print('excute __len__')
	print(self)
	print(__len__.__name__)

class Mine(object):
	def print_name(self):
		print(self)

class Mine02(object):
	def print_name(self):
		print(self)

a = Mine()

b = Mine02()
Mine02.len = MethodType(__len__, Mine02)  #给类绑定实例
a.len = MethodType(__len__, a)

c = Mine02()

a.len()
b.len()
c.len()


