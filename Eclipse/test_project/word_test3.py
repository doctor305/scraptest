#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018年7月12日

@author: jinfeng
'''
import zipfile

f=zipfile.ZipFile('demo.docx','r') 
print(f.namelist())

f.extract('word/document.xml')
content = f.read('word/document.xml')

with open('word/document.xml','w') as f_temp:
    f_temp.write(content.replace('A plain paragraph','Heading测试文本'))
f.close()
f=zipfile.ZipFile('demo.docx','a') 
f.write('word/document.xml')
        
f.close()