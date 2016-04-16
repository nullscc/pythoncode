#!/usr/bin/python
# -*- coding:utf-8 -*-

import re

s1 = 'bill.gates@microsoft.com'
s2 = '     <Tom Paris>    tom@voyager.org'

if re.match(r'([\w\d]+.)*[\w\d]+@[\w\d]+\.(com|org)', s1):
	print("s1 is email address")
else:
	print('s1 not email address')
m = re.match(r'(^((\s{0,5})\<)[\w\d\s]*\>)[\s]*(([\w\d]+.)*[\w\d]+@[\w\d]+\.(com|org))', s2)
if m:
	print('s2 is email address with name')
	print(m.group(0))	#注意打印结果
	print(m.group(1))
	print(m.group(2))
	print(m.group(3))
	print(m.group(4))
	print(m.group(5))
	print(m.group(6))
	print(m.group(7))
else:
	print('s2 isnot  email address with name')
