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
import csv
import random
from getproxy2 import Get_proxy
import threading

class Item(object):
    mc = None #名称
    jx = None #剂型
    gg = None #规格
    ghj = None #供货价
    lsj = None #零售价
    scqy = None #生成企业
    
class GetInfor(object):
    def __init__(self):
        Get_proxy()
        self.log = MyLog()
        self.items = []
        self.thread = 5
        self.starttime = time.time()
        self.log.info(u'爬虫程序开始运行，时间： %s' % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.starttime)))
        self.medicallist = self.getmedicallist('name.txt')
        self.proxylist = self.getproxylist('proxylist.csv')
        self.urls = self.geturls(self.medicallist)
        self.run(self.urls,self.thread)
        self.log.info(u'共获取信息  %d 条' % len(self.items))
        self.pipelines_xls(self.items)
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
        return medicallist
    
    def getproxylist(self,filename):
        proxylist = []
        reader = csv.reader(open(filename,'rb'))
        for proxy in reader:
            proxylist.append(proxy)
        return proxylist
    
    def geturls(self,names):
        urls = []
        for name in names:
            if name != '':
                self.log.info(u'尝试爬取%s 信息' % name.decode('GBK'))
                url = 'http://www.china-yao.com/?act=search&typeid=1&keyword='+name.decode('GBK')
                try:
                    htmlcontent = self.getresponsecontent(url)
                except:
                    self.log.info(u'药品 %s 信息获取失败！' % name.decode('GBK'))
                    with open('namelist_error.txt','a') as namelist_error:
                        namelist_error.write(name+'\n')
                    continue
                if htmlcontent == '':
                    self.log.info(u'药品 %s 信息获取失败！' % name.decode('GBK'))
                    with open('namelist_error.txt','a') as namelist_error:
                        namelist_error.write(name+'\n')
                    continue
                soup = BeautifulSoup(htmlcontent,'lxml')
                tagul = soup.find('ul',attrs={'class':'pagination'})
                tagpage = tagul.find_all('a')
                self.log.info(u'此药品信息共%d 页' % len(tagpage))
                time.sleep(4)
                if len(tagpage) == 0:
                    page = 0
                else:
                    try:
                        page = int(tagpage[-1].get_text().strip())
                    except:
                        page = int(tagpage[-2].get_text().strip())
                for i in range(1,page+1):
                    newurl = url+'&page='+str(i)
                    urls.append(newurl)
##        print urls
        return urls
    
    def spider(self,urls,thread_num):
        filename_error = u'N%dthread_errorlist.txt' % thread_num
##        n = 0
        for url in urls:
            try:
                htmlcontent = self.getresponsecontent_by_proxy(url)
                if htmlcontent == '':
                    self.log.info(u'%s 页面读取失败！' % url)
                    with open(filename_error,'a') as f_error:
                        f_error.write(url.encode('utf8')+'\n') 
                    continue
                soup = BeautifulSoup(htmlcontent,'lxml')
                tagtbody = soup.find('tbody')
                tagtr = tagtbody.find_all('tr')
                self.log.info(u'该页面共有记录 %d 条，开始爬取' % len(tagtr))
                for tr in tagtr:
                    tagtd = tr.find_all('td')
                    item = Item()
                    item.mc = tagtd[0].get_text().strip()
                    item.jx = tagtd[1].get_text().strip()
                    item.gg = tagtd[2].get_text().strip()
                    item.ghj = tagtd[3].get_text().strip()
                    item.lsj = tagtd[4].get_text().strip()
                    item.scqy = tagtd[5].get_text().strip()
                    self.items.append(item)
                self.log.info(u'页面%s 数据已保存' % url)
                sleeptime = random.randint(2,5)
                time.sleep(sleeptime)
            except:
                with open(filename_error,'a') as f_error:
                    f_error.write(url.encode('utf8')+'\n')
                continue
##                n += 1
##                if n >= 5:
##                    break
##        self.log.info(u'数据爬取结束，共获取 %d条数据。' % len(items))
        
    def run(self,urls,thread):
        urls_list = []
        if len(urls)%thread==0:
            length = len(urls)//thread
        else:
            length = len(urls)//thread+1
        for i in range(thread):
            urls_list.append(urls[length*i:length*i+length])
        self.log.info(u'开始多线程模式，线程数： %d' % thread)
        for j in range(1,thread+1):
            time.sleep(1)
            t = threading.Thread(target=self.spider,args=(urls_list[j-1],j,))
            t.start()
        t.join()
        self.log.info(u'多线程模式结束')
                    
    
    def pipelines_xls(self,medicallist):
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
        
    def pipelines_csv(self,medicallist):
        filename = u'西药药品价格数据.csv'.encode('GBK')
        self.log.info(u'准备保存数据到csv中...')
        writer = csv.writer(file(filename,'wb'))
        writer.writerow([u'名称'.encode('utf8'),u'剂型'.encode('utf8'),u'规格'.encode('utf8'),u'供货价'.encode('utf8'),u'零售价'.encode('utf8'),u'生产企业'.encode('utf8')])
        for i in range(1,len(medicallist)+1):
            item = medicallist[i-1]
            writer.writerow([item.mc.encode('utf8'),item.jx.encode('utf8'),item.gg.encode('utf8'),item.ghj.encode('utf8'),item.lsj.encode('utf8'),item.scqy.encode('utf8')])
        self.log.info(u'csv文件保存成功！')
    
    def getresponsecontent(self,url):
        Headers = {"User-Agent":"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11"}
        request = urllib2.Request(url.encode('utf8'),headers = Headers)
        response = urllib2.urlopen(request)
        try:
            response = urllib2.urlopen(request,timeout=3)
        except:
            self.log.error(u'返回 URL: %s 数据失败' % url)
            return ''
        else:
            self.log.info(u'返回URL: %s 数据成功' % url)
            return response.read()
    
    def getresponsecontent_by_proxy(self,url):
        Headers = {"User-Agent":"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11"}
        request = urllib2.Request(url.encode('utf8'),headers = Headers)
        proxy = random.choice(self.proxylist)
        server = proxy[2].lower() + r'://' + proxy[0] + ':' + proxy[1]
        self.log.info(u'使用代理服务器 %s 访问  %s' % (server,url))
        opener = urllib2.build_opener(urllib2.ProxyHandler({proxy[2].lower():server}))
        urllib2.install_opener(opener)
        try:
            response = urllib2.urlopen(request,timeout=3)
        except:
            self.log.error(u'返回 URL: %s 数据失败' % url)
            return ''
        else:
            self.log.info(u'返回URL: %s 数据成功' % url)
            return response.read()

if __name__ == '__main__':
    GetInfor()
    
        
        
