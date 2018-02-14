#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018��2��12��

@author: jinfeng
'''

import mechanize

cj = mechanize.CookieJar()
br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_gzip(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
br.addheaders = [('User-agent','Mozilla/5.0 (X11; U; Linux i685; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_cookiejar(cj)
br.open('http://www.baidu.com')

for form in br.forms():
    print form
#print br.read()
#print br.response().read()
print br.title()

    
