#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'Jin Feng'

import urllib2
import userAgents

class Urllib2ModifyHeader(object):
    def __init__(self):
        PIUA = userAgents.pcUserAgent.get('IE 9.0')
        MUUA = userAgents.mobileUserAgent.get('UC standard')
        self.url = 'http://fanyi.youdao.com'
        self.userUserAgent(PIUA,1)
        self.userUserAgent(MUUA,2)

    def userUserAgent(self,userAgent,name):
        request = urllib2.Request(self.url)
        request.add_header(userAgent.split(':')[0],userAgent.split(':')[1])
        reponse = urllib2.urlopen(request)
        filename = str(name)+'.html'
        with open(filename,'a') as f:
            f.write("%s\n\n" % userAgent)
            f.write(reponse.read())

if __name__ == '__main__':
    umh = Urllib2ModifyHeader()
