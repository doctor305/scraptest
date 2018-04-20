#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018年4月12日

@author: jinfeng
'''
import sqlite3

connect = sqlite3.connect('Cookies')

for row in connect.execute('select * from Cookies'):
#for row in connect.execute("select * from sqlite_master"):
    print row
    
