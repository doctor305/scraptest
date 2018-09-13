#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018��7��5��

@author: jinfeng
'''
import re
import datetime
import xlwt


def get_record(filename):
    with open(filename,'r') as f:
        content = f.read()
    infor_list = re.findall(r'time="(.+?)" id="(.+?)" name="(.+?)"',content)
    return infor_list

if __name__ == "__main__":
    name_list = get_name('name.txt')
    list_infor = get_record('TIME182.TXT')
    print list_infor