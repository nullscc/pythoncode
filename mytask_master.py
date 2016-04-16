#!/usr/bin/python
# -*- coding:utf-8 -*-

import random, queue
from multiprocessing.managers import BaseManager

task_queue = queue.Queue()
result_queue = queue.Queue()

class QueueManager(BaseManager):
    pass

QueueManager.register('send_task', callable = lambda:task_queue)
QueueManager.register('recv_task', callable = lambda:result_queue)

manager = QueueManager(address=('', 5000), authkey=b'abcd')

manager.start()

task = manager.send_task()
result = manager.recv_task()

for i in range(10):
	n = random.randint(0, 10000)
	print('put %d into task' %n)
	task.put(n)

for i in range(10):
	r = result.get(timeout=100)
	print('result is:%d' %r)
	
manager.shutdown()
