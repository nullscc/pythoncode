#!/usr/bin/python
#-*- coding:utf-8 -*-

dt = {1:'hello', 2:'hi', 3:'ssss'}


print(dt.get(4, 'jiong'))

print(dt)
dt[4] = 'jiong'
print(dt)
dt.add(5, 'pia')
print(dt)
