#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018��2��22��

@author: jinfeng
'''

from selenium import webdriver
from myLog import MyLog
import os
import time

class GetCartoon(object):
    def __init__(self):
        self.startUrl = u'http://www.1kkk.com/ch2-469799/'
        self.log = MyLog()
        self.browser = self.getBrowser()
        self.saveCartoon(self.browser)
    
    def getBrowser(self):
        browser = webdriver.PhantomJS()
        try:
            browser.get(self.startUrl)
        except:
            self.log.error('Open the %s failed' % self.startUrl)
        browser.implicitly_wait(20)
        return browser
    
    def saveCartoon(self,browser):
        cartoontitle = browser.title.split('_')[0]
        self.createDir(cartoontitle)
        os.chdir(cartoontitle)
        sumpage = int(self.browser.find_element_by_xpath('//div[@class="view-paging"]/div/div/a[8]').text)
        i = 1
        while i <= sumpage:
            imgname = str(i)+'.png'
            browser.get_screenshot_as_file(imgname)
            self.log.info('save img %s success' % imgname)
            i += 1
            NextTag = browser.find_element_by_id('dm5_key')
            NextTag.click()
            time.sleep(5)
            self.log.info('go to nextpage %s' % str(i))
        self.log.info('save all img success')
        exit()
    
    def createDir(self,dirname):
        if os.path.exists(dirname):
            self.log.error('create directory %s failed, have a same name file or directory' % dirname)
        else:
            try:
                os.makedirs(dirname)
            except:
                self.log.error('create diretory %s failed' % dirname)
            else:
                self.log.info('create diretory %s success' % dirname)
    
if __name__ == '__main__':
    GetCartoon()