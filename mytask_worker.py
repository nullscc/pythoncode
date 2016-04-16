#!/usr/bin/python
# -*- coding:utf-8 -*-

from multiprocessing.managers import BaseManager
import queue

task_queue = queue.Queue()
result_queue = queue.Queue()

BaseManager.register('send_task', task_queue)
BaseManager.register('recv_task', result_queue)

server_addr = '127.0.0.1'
m = BaseManager(address=(server_addr, 5000), authkey=b'abcd')

m.connect()

task = m.send_task()
result = m.recv_task()

for i in range(10):
	n = task.get(timeout=1)
	print('get %d from server' %n)
	r = n**2
	result.put(r)

	
