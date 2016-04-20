#!/usr/bin/python
# -*- coding:utf-8 -*-

import re

regex = r'.{0,3}?(add)\s*(.*)\s*?'

s1 = 'add 602966296@qq.com'
s2 = '     <Tom Paris>    tom@voyager.org'

m = re.match(regex, s1)
if m:
	print(m.group(0))
else:
	print('s1 not email address')
m = re.match(r'(^((\s{0,5})\<)[\w\d\s]*\>)[\s]*(([\w\d]+.)*[\w\d]+@[\w\d]+\.(com|org))', s2)
if m:
	print('s2 is email address with name')

else:
	print('s2 isnot  email address with name')
