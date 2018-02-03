# -*- coding: utf-8 -*-
import scrapy


class ProxyspiderSpider(scrapy.Spider):
    name = 'proxyspider'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://xicidaili.com/']

    def parse(self, response):
        pass
