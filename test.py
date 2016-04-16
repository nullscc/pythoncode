#!/usr/bin/python
'''
def deco(func):
    print("before myfunc() called.")
    func()
    print("  after myfunc() called.")
    return func

@deco
def myfunc():
    print(" myfunc() called.")

myfunc()
myfunc()
'''

'''
def foo(a):  
    def subfoo(b):  
        return(b + a)  
    return(subfoo)  

f = foo('content') #由于foo返回的是subfoo，所以f是对subfoo的引用  

print(f('sub_')) #因为subfoo记录了foo的参数变量'content'，所以返回值为'sub_content'  
'''

def func2():
	print("excute func2")

def func1(fun):
	fun()

func1(func2)





