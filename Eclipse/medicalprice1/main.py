#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018年3月20日

@author: jinfeng
'''

from bs4 import BeautifulSoup
import urllib2
from myLog import MyLog
import time
import xlwt

class Item(object):
    mc = None #名称
    jx = None #剂型
    gg = None #规格
    ghj = None #供货价
    lsj = None #零售价
    scqy = None #生成企业
    
class GetInfor(object):
    def __init__(self):
        self.url = 'http://www.china-yao.com/?act=search&typeid=1&keyword=%E7%A1%9D%E9%85%B8%E7%94%98%E6%B2%B9%E7%89%87&page=1'
        self.log = MyLog()
        self.starttime = time.time()
        self.log.info(u'爬虫程序开始运行，时间： %s' % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.starttime)))
        self.medicallist = self.getmedicallist('name.txt')
        self.items = self.spider(self.medicallist)
        self.pipelines(self.items)
        self.endtime = time.time()
        self.log.info(u'爬虫程序运行结束，时间： %s' % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.endtime)))
        self.usetime = self.endtime - self.starttime
        self.log.info(u'用时  %d时 %d分%d秒' % (self.usetime//3600,(self.usetime%3600)//60,(self.usetime%3600)%60))
        
    def getmedicallist(self,filename):
        medicallist = []
        with open(filename,'r') as fp:
            s = fp.read()
            for name in s.split():
                medicallist.append(name)
        self.log.info(u'从文件%s 中读取药品名称成功！获取药品名称 %d 个' % (filename,len(medicallist)))
        
    
    def spider(self,names):
        items = []
        for name in names:
            if name != '':
                
    
    def pipelines(self,medicallist):
        filename = u'西药药品价格数据.xls'.encode('GBK')
        self.log.info(u'准备保存数据到excel中...')
        book = xlwt.Workbook(encoding = 'utf8',style_compression=0)
        sheet = book.add_sheet(u'西药药品价格')
        sheet.write(0,0,u'名称'.encode('utf8'))
        sheet.write(0,1,u'剂型'.encode('utf8'))
        sheet.write(0,2,u'规格'.encode('utf8'))
        sheet.write(0,3,u'供货价'.encode('utf8'))
        sheet.write(0,4,u'零售价'.encode('utf8'))
        sheet.write(0,5,u'生产企业'.encode('utf8'))
        for i in range(1,len(medicallist)+1):
            item = medicallist[i-1]
            sheet.write(i,0,item.mc)
            sheet.write(i,1,item.jx)
            sheet.write(i,2,item.gg)
            sheet.write(i,3,item.ghj)
            sheet.write(i,4,item.lsj)
            sheet.write(i,5,item.scqy)
        book.save(filename)
        self.log.info(u'excel文件保存成功！')
        
    
    def getresponsecontent(self,url):
        try:
            response = urllib2.urlopen(url.encode('utf8'))
        except:
            self.log.error(u'返回 URL: %s 数据失败' % url)
        else:
            self.log.info(u'返回URL: %s 数据成功' % url)
            return response

if __name__ == '__main__':
    GetInfor()
    
        
        