#!/usr/bin/python
# -*- coding:utf-8 -*-

class Mine(object):
	def __len__(self):
		return 100
	def print_name(self):
		print(self)


my = Mine()
print(len(my))
print(dir(my))
