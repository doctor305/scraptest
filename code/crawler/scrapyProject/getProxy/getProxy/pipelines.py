# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GetproxyPipeline(object):
    def process_item(self, item, spider):
        print "start pipelines"
        filename = 'proxy.txt'
        with open(filename,'a') as fp:
            fp.write(item['ip'].encode('utf8').strip()+'\t')
            fp.write(item['port'].encode('utf8').strip()+'\t')
            fp.write(item['protocol'].encode('utf8').strip()+'\t')
            fp.write(item['typ'].encode('utf8').strip()+'\t')
            fp.write(item['loction'].encode('utf8').strip()+'\t')
            fp.write(item['source'].encode('utf8').strip()+'\n')
        return item
