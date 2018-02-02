# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem

class ZhengzhouspiderSpider(scrapy.Spider):
    name = 'zhengzhouspider'
    allowed_domains = ['tianqi.com']
    citys = ['luoyang','zhengzhou','kaifeng','xinxiang']
    start_urls = []
    for city in citys:
	start_urls.append('http://'+city+'.tianqi.com/')
    def parse(self, response):
        subSelector =  response.xpath('//ul[@class="raweather760"]')
	items = []
	for sub in subSelector:
            for n in range(len(sub.xpath('./li/a/h5//text()').extract())):
                item = WeatherItem()
                item['cityDate']=sub.xpath('./li/a/h5//text()').extract()[n]
                item['week']='null'
                item['img']=sub.xpath('./li/a/i/img/@src').extract()[n]
                item['temperature']=sub.xpath('./li/a/p/em//text()').extract()[n]
                item['weather']=sub.xpath('./li/a/p/b//text()').extract()[n]
                item['wind']='null'
                items.append(item)
	return items

