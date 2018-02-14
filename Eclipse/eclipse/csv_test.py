#!/usr/bin/evn python
#-*- coding: utf-8 -*-
'''
Created on 2018��2��11��

@author: jinfeng
'''
filename = u'测试.txt'.encode('GBK')
with open(filename,'w') as fp:
    fp.write(u'测试1'.encode('utf'))
    fp.write(u'测试gbk'.encode('GBK'))