#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018��7��4��

@author: jinfeng
'''

import datetime
import re

def get_record(filename):
    with open(filename,'r') as f:
        content = f.read()
    infor_list = re.findall(r'time="(.+?)" id="(.+?)" name="(.+?)"',content)
    return infor_list

infor_list = get_record("TIME182.TXT")
print  infor_list

