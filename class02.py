#!/usr/bin/python
# -*- coding:utf-8 -*-

class Stu(object):
	def __init__(self, name, score):
		self.__name = name
		self.__score = score

	def print_score(self):
		print('name:%s\nscore:%s' %(self.__name, self.__score) )


hello = Stu('haha', 100)

hello.print_score()
