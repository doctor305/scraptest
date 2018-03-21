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
import xlwt

class Item(object):
    shengfen = None
    xiangmubianhao = None
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
        self.hospitalPriceurl = 'http://www.zgyyjgw.com/front/cn/hospitalPrice'
        self.log = MyLog()
        self.filename = u'医疗服务价格.xls'.encode('GBK')
        self.namelist = self.getname('name.txt')
        self.hospitallist = self.gethospitalprice(self.hospitalPriceurl,self.namelist)
        self.savefiletoxls(self.filename,self.hospitallist)
    
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
        list_hospitalprice = []
        n = 1
        self.log.info('open the link %s' % url)
        browser.get(url)
        #browser.implicitly_wait(10)
        for name in namelist:
            textelement = browser.find_element_by_id('projectname')
            textelement.clear()
            try:
                textelement.send_keys(name.decode('GBK'))  #text中填入项目名称
            except:
                self.log.error('get data %s error  (%d)' % (name,n))
                n += 1
                continue
            else:
                self.log.info('get data %s (%d)\n' % (name.decode('GBK'),n))
                n += 1
            selectelement = browser.find_element_by_id('provName')
            Select(selectelement).select_by_value(u'河南省')  #省份select控件选择河南省
            submitelement = browser.find_element_by_class_name('l-btn-left')
            submitelement.click() #点击查询按钮
            time.sleep(10)
            #print browser.page_source
            #browser.get_screenshot_as_file('test.png')
            resultelement = browser.find_element_by_class_name('xxbTable')
            #print resultelement.text
            elements=resultelement.find_elements_by_xpath('./tbody[2]/tr/td')
            item = Item()
            if len(elements)==0:
                self.log.info('%s has no data' % name.decode('GBK'))
            else:
                self.log.info('save data %s to list' % name.decode('GBK'))
                item.shengfen = elements[1].text
                item.xiangmubianhao = elements[2].text
                item.xiangmumingcheng = elements[3].text
                item.xiangmuneihan = elements[4].text
                item.chuwaineirong = elements[5].text
                item.danwei = elements[6].text
                item.jiage = elements[7].text
                item.shuoming = elements[8].text
                item.wenhao = elements[9].text
                item.zhixingriqi = elements[10].text
                list_hospitalprice.append(item)
        return list_hospitalprice
                
    def savefiletoxls(self,filename,hospitallist):
        self.log.info('save data to excel')
        book = xlwt.Workbook(encoding = 'utf8',style_compression=0)
        sheet = book.add_sheet(u'医疗服务项目收费')
        sheet.write(0,0,u'省份'.encode('utf8'))
        sheet.write(0,1,u'项目编号'.encode('utf8'))
        sheet.write(0,2,u'项目名称'.encode('utf8'))
        sheet.write(0,3,u'项目内涵'.encode('utf8'))
        sheet.write(0,4,u'除外内容'.encode('utf8'))
        sheet.write(0,5,u'单位'.encode('utf8'))
        sheet.write(0,6,u'价格'.encode('utf8'))
        sheet.write(0,7,u'说明'.encode('utf8'))
        sheet.write(0,8,u'文号'.encode('utf8'))
        sheet.write(0,9,u'执行日期'.encode('utf8'))
        for i in range(1,len(hospitallist)+1):
            item = hospitallist[i-1]
            sheet.write(i,0,item.shengfen)
            sheet.write(i,1,item.xiangmubianhao)
            sheet.write(i,2,item.xiangmumingcheng)
            sheet.write(i,3,item.xiangmuneihan)
            sheet.write(i,4,item.chuwaineirong)
            sheet.write(i,5,item.danwei)
            sheet.write(i,6,item.jiage)
            sheet.write(i,7,item.shuoming)
            sheet.write(i,8,item.wenhao)
            sheet.write(i,9,item.zhixingriqi)
        book.save(filename)
        self.log.info('save excel success')
        
    
if __name__ == '__main__':
    Get_medicalprice()
    
        
        