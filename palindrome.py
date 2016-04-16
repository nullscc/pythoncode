#!/usr/bin/python
# -*- utf-8 -*-
'''
def is_palindrome(s):
	L = str(s)
	i = len(L)
	n = 0
	while n<=(i//2):
		if L[n] != L[i-n-1]:
			return False
		n+=1
	return True
'''
def is_palindrome(n):
	s = str(n)
	return s == s[::-1]

output = filter(is_palindrome, range(1, 1000))
print(list(output))

