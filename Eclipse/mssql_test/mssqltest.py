#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018年5月5日

@author: jinfeng
'''

import pymssql,os,re
import msvcrt
import decimal


server="127.0.0.1"
user="sa"
password="12345678"
conn=pymssql.connect(server,user,password,database='master')
cursor=conn.cursor()
cursor.execute("select name from sys.databases")
row=cursor.fetchone()
list_database = []
N = 0
while row:
    list_database.append(row[0])
    print '#',N,'-----',row[0]
    row=cursor.fetchone()
    N += 1

n = raw_input('select database : ')
conn=pymssql.connect(server,user,password,database=list_database[int(n)])

cursor=conn.cursor()
cursor.execute("select * from 测试表_new")
row=cursor.fetchone()
while row:
    #regex = re.compile(r'^[1-9][0-9]*$')
    #if  regex.search(row[0]):
    if row[0] not in ('20161312'):
        for i in row:
            print i,
        print
    row = cursor.fetchone()

###cursor.execute("""select getdate()""")
##cursor.execute("select * from 测试表_new")
##row=cursor.fetchone()
##
##n = 1
##while row:
##    regex=re.compile(r'[0-9]{8}')
##    if not regex.search(row[0]):
##        for i in row:
##            print i,
##        print 
##    n += 1
##    row=cursor.fetchone()
##
##cursor.execute("select * from 预算单位信息表")
##row=cursor.fetchone()
##while row:
##    for i in row:
##        print i,
##    print
##    row=cursor.fetchone()
conn.close()

#os.system('pause')

