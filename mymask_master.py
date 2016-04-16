#!/usr/bin/python
# -*- coding:utf-8 -*-

import random
from multiprocessing.managers import BaseManager

task_queue = BaseManager.queue()
result_queue = BaseManager.queue()

BaseManager.register('send_task', task_queue)
BaseManager.register('recv_task', result_queue)

manager = BaseManager(address=('', 5000), authkey=b'abcd')

manager.start()

task = manager.send_task()
result = manager.recv_task()

for i in range(10):
	n = random.randint(0, 10000)
	print('put %d into task' %n)
	task.put(n)

for i in range(10):
	print('put %d into task' %i)
	r = result.get(timeout=100)
	print('result is:%d' %r)
	
manager.shutdown()
