#!/usr/bin/python
# -*- coding:utf-8 -*-

class Stu(object):
	@property	
	def sscore(self):
		return self._score

	@sscore.setter
	def sscore(self, value):
		if not isinstance(value, int):
			raise ValueError('score must be an integer!')
		if value < 0 or value > 100:
			raise ValueError('score must between 0 ~ 100!')
		self._score = value

s = Stu()
s.sscore = 70
print(s.sscore)
