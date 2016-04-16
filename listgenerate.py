#!/usr/bin/python
# -*-utf-8 -*-
import os

dt = {"one":'1', "two":'2', "three":'3'}

L = [x*x for x in range(10) if x%2 == 0]
print(L)

L = [a+b for a in "ABC" for b in 'xyz']
print(L)

L = [n for n in os.listdir()]
print(L)

for x, y in dt.items():
	print('%s = %s' %(x, y))

L = [x+'='+y for x, y in dt.items()]

print(L)

L = ['Hello', 'World', 18, 'Apple', None]
L = [s.lower() for s in L if isinstance(s, str) ]
print(L)
