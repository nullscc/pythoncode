#!/usr/bin/python
# -*- coding:utf-8 -*-

class Stu(object):
	def print_score(self):
		print('name:%s\nscore:%s' %(self.name, self.score) )


hello = Stu()
hello.name = 'hel'
hello.score = 75

hello.print_score()
