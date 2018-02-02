# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem

class ZhengzhouspiderSpider(scrapy.Spider):
    name = 'zhengzhouspider'
    allowed_domains = ['tianqi.com']
	citys = ['luoyang','zhengzhou']
    start_urls = []
	for city in citys:
		start_urls.append('http://'+city+'.tianqi.com/')
    def parse(self, response):
        subSelector =  response.xpath('//ul[@class="raweather760"]')
		items = []
		for sub in subSelector:
			item = WeatherItem()
			item['cityDate']=sub.xpath('./li/a/h5//text()').extract()[0]
			item['week']=''
			item['img']=sub.xpath('./li/a/i/img/@src').extract()[0]
			item['temperature']=sub.xpath('./li/a/p/em//text()').extract()[0]
			item['weather']=sub.xpath('./li/a/p/b//text()').extract()[0]
			item['wind']=''
			items.append(item)
		return items

