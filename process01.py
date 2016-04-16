#!/usr/bin/python
# -*- coding:utf-8 -*-

from multiprocessing import Process

def child_func(name):
	print('run child_func,paramater is:%s' %name)

p = Process(target=child_func, args=('hapara',)) #参数是一个tuple
p.start()

p.join()  # Process没有close方法
print("i'm child")

