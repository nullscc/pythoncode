#!/usr/bin/python
# -*- coding:utf-8 -*-

import threading

n = 0
lock = threading.Lock()

def change_it():
	global n
	n+=1
	n-=1

def child_func():
	for i in range(10000000):
		lock.acquire()
		try:
			change_it()
		finally:
			lock.release()

t1 = threading.Thread(target=child_func, name='teand')
t2 = threading.Thread(target=child_func, name='teand')
t1.start()
t2.start()
t1.join()
t2.join()
print(n)
	
