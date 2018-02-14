#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018��2��13��

@author: jinfeng
'''
from selenium import webdriver
browser = webdriver.PhantomJS()
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options

#chrome_options = Options()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')
#browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('https://www.baidu.com')
browser.implicitly_wait(10)
textElement = browser.find_element_by_class_name('s_ipt')
textElement.clear()
textElement.send_keys('Python selenium')
submitElement = browser.find_element_by_id('su')
submitElement.click()
print browser.title

resultElements = browser.find_elements_by_class_name('c-tools')
print len(resultElements)

for s in resultElements:
    value = s.get_attribute('data-tools')
    valueDic = eval(value)
    print valueDic.get('title').decode('utf8')
    print valueDic.get('url')