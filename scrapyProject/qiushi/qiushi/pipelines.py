# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import urllib2
import os
import re

class QiushiPipeline(object):
    def process_item(self, item, spider):
        filename = time.strftime('%Y%m%d',time.localtime()) + 'qiubai.txt'
        imgDir = 'IMG'
        if os.path.isdir(imgDir):
            pass
        else:
            os.mkdir(imgDir)
        with open(filename,'a') as fp:
            fp.write('-'*50 + '\n' + '*'*50 + '\n')
            fp.write("author: %s\n" % item['author'].encode('utf8'))
            fp.write("content: %s\n" % item['content'].encode('utf8'))
            imgUrl = 'https:'+item['img']
            try:
                imgName = os.path.basename(re.findall(r'\/(.+?JPEG)\?image',imgUrl)[0])
                fp.write("img: %s\n" % (imgName))
                imgPathName = imgDir + os.sep + imgName
                with open(imgPathName,'wb') as fpi:
                    fpi.write(urllib2.urlopen(imgUrl).read())
            except:
                fp.write("img: %s\n" % imgUrl)
                
            fp.write("fun: %s\t talk: %s\n" % (item['funNum'],item['talkNum']))
            fp.write('*'*50 + '\n' + '-'*50 + '\n\n\n')
        
        return item
