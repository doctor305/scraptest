#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018年2月22日

@author: jinfeng
'''
from selenium import webdriver
from selenium.webdriver.support.select import Select
from myLog import MyLog
import time

class Item(object):
    shengfen = None
    xiangmubiaohao = None
    xiangmumingcheng = None
    xiangmuneihan = None
    chuwaineirong = None
    danwei = None
    jiage = None
    shuoming = None
    wenhao = None
    zhixingriqi = None

class Get_medicalprice(object):
    def __init__(self):
        self.hospitalPriceurl = 'https://www.baidu.com'
        self.log = MyLog()
        self.filename = u'医疗服务价格.xls'
        self.namelist = self.getname('name.txt')
        self.hospitallist = self.gethospitalprice(self.hospitalPriceurl,self.namelist)
        #self.savefile(self.filename,self.hospitallist)
    
    def getname(self,filename): 
        namelist = []
        with open(filename,'r') as fp:
            s = fp.read()
            for name in s.split():
                namelist.append(name)
        self.log.info('open namelist success , the length of list is %d' % len(namelist))
        return namelist
    
    def gethospitalprice(self,url,namelist):
        browser = webdriver.PhantomJS()
        #list_hospitalprice = []
        self.log.info('open the link %s' % url)
        browser.get(url)
        #browser.implicitly_wait(20)
        print browser.title
        textelement = browser.find_element_by_id('kw')
        #textelement = browser.find_element_by_name('wd')
        textelement.clear()
        textelement.send_keys(u'数学')
        submitelement = browser.find_element_by_id('su')
        submitelement.click()
        time.sleep(10)
        #print browser.page_source
        print browser.title
        #resultelement = browser.find_element_by_xpath('//div[@class="datagrid-view"]/div/table/tbody/tr')
        #print resultelement
        #elements=resultelement.find_elements_by_xpath('./td')
        #print elements
       
        
        
        
    def savefile(self,filename,hospitallist):
        pass
    
if __name__ == '__main__':
    Get_medicalprice()
    
        
        