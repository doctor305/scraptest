#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018��4��11��

@author: jinfeng
'''
import csv
import urllib2
import random


def getproxylist(filename):
    proxylist = []
    reader = csv.reader(open(filename,'rb'))
    for proxy in reader:
        proxylist.append(proxy)
        print proxy
    return proxylist

def getresponsecontent(url,proxylist):
    #import requests
    Headers = {"User-Agent":"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11"}
    request = urllib2.Request(url.encode('utf8'),headers = Headers)
    #proxy = random.choice(proxylist)
    proxy = ['117.95.105.9','24096','HTTPS']
    server = proxy[2].lower() + r'://' + proxy[0] + ':' + proxy[1]
    #requests.get("http://example.org", proxies={proxy[2].lower():server,}) 
    opener = urllib2.build_opener(urllib2.ProxyHandler({proxy[2].lower():server}))
    urllib2.install_opener(opener)
#     try:
#         response = urllib2.urlopen(request,timeout=3)
#     except:
#         print u'连接URL: %s 失败' % url
#         return ''
#     else:
#         print u'连接URL: %s 成功' % url
#         return response.read()
    response = urllib2.urlopen(request,timeout=3)
    
    return response
        
if __name__ == '__main__':
    proxylist = getproxylist('proxylist.csv')
    response = getresponsecontent('http://www.china-yao.com/',proxylist)
    #response = getresponsecontent('https://www.baidu.com/',proxylist)
    print '#### Response :'
    print response
    print response.read()