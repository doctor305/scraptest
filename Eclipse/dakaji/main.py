#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018年7月4日

@author: jinfeng
'''

import re
import datetime
import xlwt


def get_name(filename):
    names = []
    with open(filename,'r') as f:
        for name in f.read().split():
            names.append(name)
    return names

def get_record(filename):
    with open(filename,'r') as f:
        content = f.read()
    infor_list = re.findall(r'time="(.+?)" id="(.+?)" name="(.+?)"',content)
    return infor_list

def result(infor_list,name_list):
    d_min = datetime.datetime.strptime('3000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    d_max = datetime.datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    for i in infor_list:
        d = datetime.datetime.strptime(i[0],'%Y-%m-%d %H:%M:%S')
        if d > d_max:
            d_max = d
        if d < d_min:
            d_min = d
    day = datetime.timedelta(days=1)
    date_list = []
    d_temp = d_min
    while d_temp <= d_max:
        date_list.append(d_temp)
        d_temp += day
    path = u"考勤结果表%s至%s.xls".encode('GBK') % (d_min.strftime('%Y%m%d'),d_max.strftime('%Y%m%d'))
    rb = xlwt.Workbook()
    sheet = rb.add_sheet(u'考勤结果',cell_overwrite_ok=True)
    
    for k in range(len(date_list)):
        sheet.write(0,k+1,date_list[k].strftime('%Y-%m-%d')) 
    
    for m in range(len(name_list)):
        sheet.write(m+1,0,name_list[m].decode('GBK'))
        for n in range(len(date_list)):
            for l in range(len(infor_list)):
                if name_list[m]==infor_list[l][2] and date_list[n].strftime('%Y-%m-%d') == datetime.datetime.strptime(infor_list[l][0],'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'):
                    sheet.write(m+1,n+1,'#####')
    rb.save(path) 
    print "Complete!"  
        


def main():
    name_list = get_name('name.txt')
    list_infor1 = get_record('TIME182.TXT')
    result(list_infor1,name_list)

if __name__ == '__main__':
    main()
   