#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018��2��11��

@author: jinfeng
'''

import xlwt

if __name__ == '__main__':
    book = xlwt.Workbook(encoding = 'utf8',style_compression=0)
    sheet = book.add_sheet('test1')
    sheet.write(0,0,'hskfds')
    sheet.write(1,1,u'中文测试'.encode('utf8'))
    sheet.write(2,3,1500)
    sheet2 = book.add_sheet('test2')
    sheet2.write(0,0,'test2')
    sheet2.write(1,1,u'中文测试2'.encode('utf8'))
    book.save('test.xls')
    