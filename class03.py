#!/usr/bin/python
# -*- coding:utf-8 -*-

class Animal(object):
	def some_run(self, animal):
		animal.run()
		animal.run()

class Cat(Animal):
	def run(self):
		print('cat is runing')

class Dog(Animal):
	def run(self):
		print('dog is runing')

class Test(object):
	def run(self):
		print('test is runing')

ll = Animal()

qq = Test()

ll.some_run(qq)
