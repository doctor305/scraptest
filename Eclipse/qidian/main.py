#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018��4��28��

@author: jinfeng
'''

from myLog import MyLog
from bs4 import BeautifulSoup

class Item(object):
    pass

class Qidian(object):
    def __init__(self):
        url = 'https://www.qidian.com/'
        self.log = MyLog()
        self.urls = self.geturls(url)
        self.items = self.spider(self.urls)
        self.piplines(self.items)
        
    def geturls(self,url):
        urls = []
        return urls
    
    def spider(self,urls):
        items = []
        return items
    
    def pipilines(self,items):
        pass
        
        
