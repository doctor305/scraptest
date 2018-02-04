# -*- coding: utf-8 -*-
import scrapy
from getProxy.items import GetproxyItem

class ProxyspiderSpider(scrapy.Spider):
    name = 'proxyspider'
    allowed_domains = ['xicidaili.com']
    wds = ['nn','nt','wn','wt']
    pages = 20
    start_urls = []
    for types in wds:
        for i in xrange(1,pages+1):
            start_urls.append('http://www.xicidaili.com/'+types+'/'+str(i))
            

    def parse(self, response):
        subSelector = response.xpath('//tr[@class=""]|//tr[@class="odd"]')
        items = []
        for sub in subSelector:
            item = GetproxyItem()
            item['ip'] = sub.xpath('.//td[2]/text()').extract()[0]
            item['port'] = sub.xpath('.//td[3]/text()').extract()[0]
            item['typ'] = sub.xpath('.//td[5]/text()').extract()[0]
            if sub.xpath('.//td[4]/a/text()'):
                item['loction'] = sub.xpath('.//td[4]/a/text()').extract()[0]
            else:
                item['loction'] = sub.xpath('.//td[4]/text()').extract()[0]
            item['protocol'] = sub.xpath('.//td[6]/text()').extract()[0]
            item['source'] = 'xicidaili'
        return items
