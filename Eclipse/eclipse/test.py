#!/usr/bin/evn python
#-*- coding: utf-8 -*-
'''
Created on 2018年2月7日

@author: jinfeng
'''

from bs4 import BeautifulSoup
import urllib2
from myLog import MyLog as mylog

#url = 'https://tieba.baidu.com/f?kw=%E6%9D%83%E5%8A%9B%E6%B8%B8%E6%88%8F&ie=utf-8&pn=100'
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
        
    def getUrls(self,pageSum):
        urls = []
        pns = [str(i*50) for i in range(pageSum)]
        ul = self.url.split('=')
        for pn in pns:
            ul[-1] = pn
            url = '='.join(ul)
            urls.append(url)
        self.log.info(u'获取URLS成功')
        return urls
    
    def spider(self, urls):
        items = []
        for url in urls:
            htmlContent = self.getResponseContent(url)
            soup = BeautifulSoup(htmlContent, 'lxml')
            tagsli = soup.find_all('li',attrs={'class':' j_thread_list clearfix'})
            for tag in tagsli:
                item = Item()
                item.title = tag.find('a', attrs={'class':'j_th_tit'}).get_text().strip()
                item.firstAuthor = tag.find('span', attrs={'class':'frs-author-name-wrap'}).a.get_text().strip()
                item.firstTime = tag.find('span', attrs={'title':u'创建时间'.encode('utf8')}).get_text().strip()
                item.reNum = tag.find('span', attrs={'title':u'回复'.encode('utf8')}).get_text().strip()
                item.content = tag.find('div', attrs={'class':'threadlist_abs threadlist_abs_onlyline '}).get_text().strip()
                item.lastAuthor = tag.find('span', attrs={'class':'tb_icon_author_rely j_replyer'}).a.get_text().strip()
                item.lastTime = tag.find('span', attrs={'title':u'最后回复时间'.encode('utf8')}).get_text().strip()
                items.append(item)
                self.log.info(u'获取标题为<<%s>>的项成功 ...' %item.title)
        return items
    
    def pipelines(self, items):
        fileName = u'百度贴吧_权利的游戏.txt'.encode('GBK')
        with open(fileName, 'w') as fp:
            for item in items:
                fp.write('title:%s \t author:%s \t firstTime:%s \n content:%s \n return:%s \n lastAuthor:%s \t lastTime:%s \n\n\n\n' 
                         %(item.title.encode('utf8'),item.firstAuthor.encode('utf8'),item.firstTime.encode('utf8'),item.content.encode('utf8'),item.reNum.encode('utf8'),item.lastAuthor.encode('utf8'),item.lastTime.encode('utf8')))
                self.log.info(u'标题为<<%s>>的项输入到"%s"成功' %(item.title, fileName.decode('GBK')))

    def getResponseContent(self, url):
        '''这里单独使用一个函数返回页面返回值，是为了后期方便的加入proxy和headers等
        '''
        try:
            response = urllib2.urlopen(url.encode('utf8'))
        except:
            self.log.error(u'Python 返回URL:%s  数据失败' %url)
        else:
            self.log.info(u'Python 返回URUL:%s  数据成功' %url)
            return response.read()
    

if __name__ == '__main__':
    url = u'http://tieba.baidu.com/f?kw=权利的游戏&ie=utf-8&pn=50'
    GTI = GetTiebaInfo(url)