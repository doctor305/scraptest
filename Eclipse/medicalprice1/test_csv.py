#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018��4��10��

@author: jinfeng
'''
import csv

filename = '代理服务器列表.csv'.decode('utf8').encode('GBK')
reader = csv.reader(open(filename,'rb'))
for item in reader:
    print item