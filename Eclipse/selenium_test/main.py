#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018��2��13��

@author: jinfeng
'''


class Item(object):
    ip = None
    port = None
    anonymous = None
    type = None
    support = None
    local = None
    speed = None
    
class GetProxy(object):
    def __init__(self):
        self.startUrl = 'https://www.kuaidaili.com/free/inha/'
        self.log = MyLog()
        self.urls = self.getUrls()
        self.proxyList = self.getProxyList(self.urls)
        self.fileName = 'proxylist.txt'
        self.saveFile(self.fileName,self.proxyList)
        
    def getUrls(self):
        urls = []
        for i in xrange(1,21):
            url = self.startUrl+str(i)
            urls.append(url)
            self.log.info('get url %s to urls' % url)
        return urls
    
    def getProxyList(self,urls):
        browser = webdriver.PhantomJS()
        proxyList = []
        for url in urls:
            self.log.info('open link %s' % url)
            browser.get(url)
            browser.implicitly_wait(5)
            elements = browser.find_elements_by_xpath('//tbody/tr')
            self.log.info('number of proxy is %s' % len(elements))
            for element in elements:
                item = Item()
                item.ip = element.find_elements_by_xpath('./td')[0].text.encode('utf8')
                item.port = element.find_elements_by_xpath('./td')[1].text.encode('utf8')
                item.anonymous = element.find_elements_by_xpath('./td')[2].text.encode('utf8')
                item.type = element.find_elements_by_xpath('./td')[3].text.encode('utf8')
                item.local = element.find_elements_by_xpath('./td')[4].text.encode('utf8')
                item.speed = element.find_elements_by_xpath('./td')[5].text.encode('utf8')
                proxyList.append(item)
                self.log.info('add proxy %s:%s to list' % (item.ip,item.port))
        browser.quit()
        return proxyList
    
    def saveFile(self,filename,proxyList):
        self.log.info('add all proxy to %s' % filename)
        with open(filename,'w') as fp:
            for item in proxyList:
                fp.write(item.ip + '\t')
                fp.write(item.port + '\t')
                fp.write(item.anonymous + '\t')
                fp.write(item.type + '\t')
                fp.write(item.local + '\t')
                fp.write(item.speed + '\n')
            self.log.info('save %s complete' % filename)
            
if __name__ == '__main__':
    GP = GetProxy()
            
    