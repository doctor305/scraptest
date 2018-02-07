#!/usr/bin/evn python
#-*- coding: utf-8 -*-
'''
Created on 2018年2月7日

@author: jinfeng
'''

from bs4 import BeautifulSoup
import urllib2
from myLog import MyLog as mylog

url = 'https://tieba.baidu.com/f?kw=%E6%9D%83%E5%8A%9B%E6%B8%B8%E6%88%8F&ie=utf-8&pn=100'
#soup = BeautifulSoup(,'lxml')
 
class Item(object):
    title = None
    firstAuthor = None
    firstTime = None
    reNum = None
    content = None
    lastAuthor = None
    lastTime = None

class GetTiebaInfo(object):
    def __init__(self,url):
        self.url = url
        self.log = mylog()
        self.pageSum = 5
        self.urls = self.getUrls(self.pageSum)
        self.items = self.spider(self.urls)
        self.pipelines(self.items)
    