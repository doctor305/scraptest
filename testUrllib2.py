#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = 'Jin Feng'

import urllib2
import time

def clear():
    print "Clear"
    time.sleep(3)
    OS = platform.system()
    if OS == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def linkBaidu():
    url = 'http://www.baidu.com'
    try:
        response = urllib2.urlopen(url,timeout=3)
    except urllib2.URLError:
        print "URL error! "
        exit()
    with open('baidu.txt','w') as fp:
        fp.write(response.read())
    print "response.geturl() :\n %s" % response.geturl()
    print "response.getcode() :\n %s" % response.getcode()
    print "response.info(): \n %s" % response.info()

if __name__ == "__main__":
    linkBaidu()
