#!/usr/bin/python
#-*- utf-8 -*-

h = float(input('请输入身高：'))
s = float(input('请输入体重：'))

m = s/(h*h)

n = h*h
print('h*h:%s' % n)

n = h**2
print("h**2:%s" % n)

print('BMI:%f' %m)
if m<=18.5:
	print('过轻')
elif m<=25:
	print('正常')
elif m<=28:
	print('过重')
elif m<=32:
	print('肥胖')
else:
	print('严重肥胖')
	


