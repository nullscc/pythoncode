#!/usr/bin/python
# -*- coding:utf-8 -*-

import threading

def chile_thread(para):
	print('excute thread, para is %s' % para)
	print('thread name is %s' % threading.current_thread().name)

thr = threading.Thread(target = chile_thread, name = 'hchild', args = ('hello', ))
#Thread首字母要大写，表示是一个类名
#如果不带参数，那么args可以省略


thr.start()
thr.join()
