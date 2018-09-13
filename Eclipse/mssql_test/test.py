#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018年5月5日

@author: jinfeng
'''

import pymssql

server="127.0.0.1"  #服务器IP或服务器名称
user="sa"           #登陆数据库所用账号
password="12345678" #该账号密码
conn=pymssql.connect(server,user,password,database='test')
cursor=conn.cursor()
cursor.execute("insert into dbo.test ([NO.],Name,Address) values ('003','张三','郑州') ")
conn.commit()
conn.close()


