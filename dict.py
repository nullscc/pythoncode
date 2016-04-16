#!/usr/bin/python
#-*- utf-8 -*-

dt = {'hello':98, 'world':100}

print(dt)

st = 'haha'
dt[st] = 99
print(dt)

dt.pop('haha')
print(dt)

print('before for')

for x in dt:
	print(dt[x])

