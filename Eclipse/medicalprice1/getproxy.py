#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018年4月9日

@author: jinfeng
'''

from bs4 import BeautifulSoup
import urllib2
from myLog import MyLog
import csv
import time
import re

class Item(object):
    IP = None  #IP地址
    port = None #端口
    type = None #类型
    address = None #地址

class Get_proxy(object):
    def __init__(self):
        self.log = MyLog()
        self.log.info(u'Get_proxy 开始运行！')
        self.urls = self.get_urls()
        self.log.info(u'获取需要访问的url，共 %d 个' % len(self.urls))
        self.proxy_list = self.spider(self.urls)
        self.log.info(u'获取到代理服务器地址，共 %d 个' % len(self.proxy_list))
        self.alivelist = self.testproxy(self.proxy_list)
        self.pipelines(self.alivelist)
        self.log.info(u'Get_proxy 运行结束！')
    
    def get_urls(self):
        urls = []
        num_max = 10
        for n in range(1,num_max+1):
            url = 'https://www.kuaidaili.com/free/inha/'+str(n)
            urls.append(url)
        return urls
    
    def getresponsecontent(self,url):
        try:
            Headers = {"User-Agent":"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11"}
            request = urllib2.Request(url.encode('utf8'),headers = Headers)
            response = urllib2.urlopen(request)
        except:
            self.log.error(u'返回 URL: %s 数据失败' % url)
            return ''
        else:
            self.log.info(u'返回URL: %s 数据成功' % url)
            return response
    
    def spider(self,urls):
        items = []
        for url in urls:
            time.sleep(10)
            htmlcontent = self.getresponsecontent(url)
            if htmlcontent == '':
                continue
            soup = BeautifulSoup(htmlcontent,'lxml')
            tagtbody = soup.find('tbody')
            proxys = tagtbody.find_all('tr')
            for proxy in proxys:
                item = Item()
                elements = proxy.find_all('td')
                item.IP = elements[0].get_text().strip()
                item.port = elements[1].get_text().strip()
                item.type = elements[3].get_text().strip()
                item.address = elements[4].get_text().strip()
                items.append(item)
            
        return items
    
    def testproxy(self,proxylist):
        self.log.info(u'开始对获取到的代理服务器进行测试 ...')
        aliveList = []
        ip_list = []
        URL = r'https://www.baidu.com'
        regex = re.compile(r'baidu.com')
        for proxy in proxylist:
            if proxy.IP in ip_list:
                continue   #去除列表中重复的代理服务器
            server = proxy.type.lower() + r'://' + proxy.IP + ':' + proxy.port
            self.log.info(u'开始测试 %s' % server)
            opener = urllib2.build_opener(urllib2.ProxyHandler({proxy.type.lower():server}))
            urllib2.install_opener(opener)
            try:
                response = urllib2.urlopen(URL,timeout=3)
            except:
                self.log.info(u'%s 连接失败' % server)
                continue
            else:
                try:
                    string = response.read()
                except:
                    self.log.info(u'%s 连接失败' % server)
                    continue
                if regex.search(string):
                    self.log.info(u'%s 连接成功 .......' % server)
                    ip_list.append(proxy.IP)
                    aliveList.append(proxy)
        return aliveList
            
    
    def pipelines(self,alivelist):
        filename = 'proxylist.csv'
        self.log.info(u'准备将获取到的代理服务器地址保存数据到csv文件中...')
        writer = csv.writer(file(filename,'wb'))
        #writer.writerow([u'IP地址'.encode('utf8'),u'端口'.encode('utf8'),u'类型'.encode('utf8'),u'地址'.encode('utf8')])
        for aliveproxy in alivelist:
            writer.writerow([aliveproxy.IP.encode('utf8'),aliveproxy.port.encode('utf8'),aliveproxy.type.encode('utf8'),aliveproxy.address.encode('utf8')])
        self.log.info(u'数据保存完毕！')

if __name__ == '__main__':
    Get_proxy()
    
    