#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

pid = os.fork()

if pid == 0:
	print('child process')
else:
	print("hihi")
	print('father process')
