# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time

class Meiju100Pipeline(object):
    def process_item(self, item, spider):
        filename = time.strftime('%Y%m%d',time.localtime())+'meiju.txt'
        with open(filename,'a') as fp:
            fp.write("%s\t" % item['number'].encode('utf8'))
            fp.write("%s\t" % item['storyName'].encode('utf8'))
            if len(item['storyState']) == 0:
                fp.write("unknow\t")
            else:
                fp.write("%s\t" % item['storyState'][0].encode('utf8'))
            fp.write("%s\t" % item['storyType'].encode('utf8'))
            if len(item['tvStation']) == 0:
                fp.write("unknow\t")
            else:
                fp.write("%s\t" % item['tvStation'][0].encode('utf8'))
            if len(item['updateTime']) == 0:
                fp.write("unknow\t")
            else:
                fp.write("%s\t" % item['updateTime'][0].encode('utf8'))
            fp.write("%s\n" % ('http://www.meijutt.com'+item['address']))
        return item
