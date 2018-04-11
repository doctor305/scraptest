#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018��4��11��

@author: jinfeng
'''

import time
import threading

ls = []
ls2 = []
ls_list = []
for i in range(1,50):
    ls.append(i)
    
thread = 5
length = len(ls)//5+1
for j in range(thread):
    print ls[j*length:j*length+length]
    ls_list.append(ls[j*length:j*length+length])
    
def print_list(printlist,num):
    print " %d Start!" % num
    print "length is %d" % len(printlist)
    for n in printlist:
        ls2.append(n)
        time.sleep(1)
    print " %d Finish!" % num

for m in range(1,thread+1):
    t = threading.Thread(target=print_list,args=(ls_list[m-1],m,))
    t.start()

t.join()   
print ls2 
print "END!"