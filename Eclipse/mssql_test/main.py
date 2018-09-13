#!/usr/bin/evn python
#-*- coding:utf-8 -*-
'''
Created on 2018年5月5日

@author: jinfeng
'''

import pymssql,os,re
import decimal
from myLog import MyLog
import xlwt

class Test(object):
    def __init__(self):
        self.log = MyLog()
        self.hospitalname = ''
        self.log.info(u'准备登陆MSSQL')
        conn = self.login()
        filename = u'校验结果.xls'.encode('GBK')
        self.book = xlwt.Workbook(encoding = 'utf8',style_compression=0)
        #self.test1(conn)
        self.test(conn)
        self.book.save(filename)
        self.log.info(u'excel文件保存成功！')
           
    def get_user_pswd(self):
        print u'服务器名称： \t',
        server = raw_input()
        print u'登录名：  \t',
        user = raw_input()
        print u'密码：  \t',
        pswd = raw_input()
        return server,user,pswd
    
    def connect(self,server,user,password,db):
        try:
            conn=pymssql.connect(server,user,password,database=db)
        except:
            self.log.error(u'登陆信息有误！')
            return 'Error'
        else:
            return conn
    
    def login(self):
        while True:
            server,user,pswd = self.get_user_pswd()
            conn = self.connect(server,user,pswd,'master')
            if conn != 'Error':
                self.log.info(u'数据库登陆成功!')
                break
        cursor=conn.cursor()
        cursor.execute("select name from sys.databases")
        row=cursor.fetchone()
        list_database = []
        N = 0
        while row:
            list_database.append(row[0])
            print '#',N,'-----',row[0]
            row=cursor.fetchone()
            N += 1
        print u'选择需要校验的数据库（填写对应的序号。注意数据库名不能是中文！）：',
        n = raw_input()
        conn=pymssql.connect(server,user,pswd,database=list_database[int(n)])
        self.hospitalname = list_database[int(n)]
        return conn
    
    def write_to_file(self,string):
        filename = u'result.txt'
        with open(filename,'a') as fd:
            fd.write(string)
    
    def save_to_xls(self,sheet,tablename,n,ls_name,ls_data):
        for i in range(len(ls_name)):
            sheet.write(n*2,i,ls_name[i])
            sheet.write(n*2+1,i,ls_data[i])
        
    
    def test1(self,conn):
        cursor=conn.cursor()
        print u'输入需要查看的表名：'
        table = raw_input()
        cursor.execute("select * from %s" % table)
        row=cursor.fetchone()
        while row:
            for element in row:
                print element,
            print
            row=cursor.fetchone()
    
    def date_check(self,string):
        if string == None:
            return False
        regex=re.compile(r'^19[0-9]{6}$|^20[0-9]{6}$')
        if regex.search(string):
            return True
        else:
            return False
    
    def number_check(self,string):
        if string == None:
            return False
        regex = re.compile(r'^[1-9][0-9]*$')
        if regex.search(string):
            return True
        else:
            return False 
                   
    def test(self,conn):  
        cursor=conn.cursor()
        ## 标准表MZBRFYJSXX
        cursor.execute("select top 1000 YYDM,YYMC,YXBZ,XZQHDM,XZQHMC,YXBZ,RYSJ,CYSJ,ZYH,BRXM,SFZHM FROM ZYBRJBXX")
        row=cursor.fetchone()
        list_ZYBRJBXX = [0,0,0,0,0,0,0,0,0,0,0]
        self.log.info(u'开始对表 ZYBRJBXX前1000条数据进行校验！')
        while row:
            if row[0] == None:
                list_ZYBRJBXX[0] += 1
            if row[1] == None:
                list_ZYBRJBXX[1] += 1
            if row[2] == None:
                list_ZYBRJBXX[2] += 1
            if row[3] == None:
                list_ZYBRJBXX[3] += 1
            if row[4] == None:
                list_ZYBRJBXX[4] += 1
            if row[5] not in ('0','1'):
                list_ZYBRJBXX[5] += 1
            if not self.date_check(row[6]):
                list_ZYBRJBXX[6] += 1
            if not self.date_check(row[7]):
                list_ZYBRJBXX[7] += 1
            if row[8] == None:
                list_ZYBRJBXX[8] += 1
            if row[9] == None:
                list_ZYBRJBXX[9] += 1
            if row[10] == None:
                list_ZYBRJBXX[10] += 1
            row=cursor.fetchone()
        self.log.info(u'保存表%s校验数据到excel中...' % 'ZYBRJBXX')
        sheet = self.book.add_sheet(self.hospitalname)
        msg = u'表ZYBRJBXX中列YYDM%d,YYMC%d,YXBZ%d,XZQHDM%d,XZQHMC%d,YXBZ%d,RYSJ%d,CYSJ%d,ZYH%d,BRXM%d,SFZHM%d条记录不符合要求' % (list_ZYBRJBXX[0],list_ZYBRJBXX[1],list_ZYBRJBXX[2],list_ZYBRJBXX[3],list_ZYBRJBXX[4],list_ZYBRJBXX[5],list_ZYBRJBXX[6],list_ZYBRJBXX[7],list_ZYBRJBXX[8],list_ZYBRJBXX[9],list_ZYBRJBXX[10])
        #self.write_to_file(msg)
        self.log.info(msg)
        ls_name = ['YYDM','YYMC','YXBZ','XZQHDM','XZQHMC','YXBZ','RYSJ','CYSJ','ZYH','BRXM','SFZHM']
        ls_data = [str(list_ZYBRJBXX[0])+'条记录为空',str(list_ZYBRJBXX[1])+'条记录为空',str(list_ZYBRJBXX[2])+'条记录为空',str(list_ZYBRJBXX[3])+'条记录为空',str(list_ZYBRJBXX[4])+'条记录为空',\
                   str(list_ZYBRJBXX[5])+'条记录取值非0和1',str(list_ZYBRJBXX[6])+'条记录日期格式不合规定',str(list_ZYBRJBXX[7])+'条记录日期格式不合规定',str(list_ZYBRJBXX[8])+'条记录为空',str(list_ZYBRJBXX[9])+'条记录为空',\
                   str(list_ZYBRJBXX[10])+'条记录为空']
        self.save_to_xls(sheet,'表ZYBRJBXX',0,ls_name,ls_data)
        ## 标准表MZBRJBXX
        cursor.execute("select top 1000 YYDM,YYMC,YXBZ,XZQHDM,XZQHMC,YXBZ,MZH,JZHSJ,CSRQ,BRXM FROM MZBRJBXX")
        row=cursor.fetchone()
        list_MZBRJBXX = [0,0,0,0,0,0,0,0,0,0]
        self.log.info(u'开始对表 ZYBRJBXX前1000条数据进行校验！')
        while row:
            if row[0] == None:
                list_MZBRJBXX[0] += 1
            if row[1] == None:
                list_MZBRJBXX[1] += 1
            if row[2] == None:
                list_MZBRJBXX[2] += 1
            if row[3] == None:
                list_MZBRJBXX[3] += 1
            if row[4] == None:
                list_MZBRJBXX[4] += 1
            if row[5] not in ('0','1'):
                list_MZBRJBXX[5] += 1
            if row[6] == None:
                list_MZBRJBXX[6] += 1
            if not self.date_check(row[7]):
                list_MZBRJBXX[7] += 1
            if not self.date_check(row[8]):
                list_MZBRJBXX[8] += 1
            if row[9] == None:
                list_MZBRJBXX[9] += 1
            row=cursor.fetchone()
        msg = u'表MZBRJBXX中列YYDM%d,YYMC%d,YXBZ%d,XZQHDM%d,XZQHMC%d,YXBZ%d,MZH%d,JZHSJ%d,CSRQ%d,BRXM%d条记录不符合要求' % (list_ZYBRJBXX[0],list_ZYBRJBXX[1],list_ZYBRJBXX[2],list_ZYBRJBXX[3],list_ZYBRJBXX[4],list_ZYBRJBXX[5],list_ZYBRJBXX[6],list_ZYBRJBXX[7],list_ZYBRJBXX[8],list_ZYBRJBXX[9])
        #self.write_to_file(msg)
        self.log.info(msg)
        ## 标准表ZYBRFYMX
        cursor.execute("select top 1000 YYDM,YYMC,YXBZ,XZQHDM,XZQHMC,YXBZ,RYSJ,CYSJ,SFSJ,ZYH,RYCS,BRXM,YYXMDM,YYXMMC,XMBZDM,XMBZMC,YYXMDW,YYXMGG,YYXMDJ,YYXMSL,YYXMFYJEXJ FROM ZYBRFYMX")
        row=cursor.fetchone()
        list_ZYBRFYMX = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.log.info(u'开始对表 ZYBRFYMX前1000条数据进行校验！')
        while row:
            if row[0] == None:
                list_ZYBRFYMX[0] += 1
            if row[1] == None:
                list_ZYBRFYMX[1] += 1
            if row[2] == None:
                list_ZYBRFYMX[2] += 1
            if row[3] == None:
                list_ZYBRFYMX[3] += 1
            if row[4] == None:
                list_ZYBRFYMX[4] += 1
            if row[5] not in ('0','1'):
                list_ZYBRFYMX[5] += 1
            if not self.date_check(row[6]):
                list_ZYBRFYMX[6] += 1
            if not self.date_check(row[7]):
                list_ZYBRFYMX[7] += 1
            if not self.date_check(row[8]):
                list_ZYBRFYMX[8] += 1
            if row[9] == None:
                list_ZYBRFYMX[9] += 1
            if row[10] == None:
                list_ZYBRFYMX[10] += 1
            if row[11] == None:
                list_ZYBRFYMX[11] += 1
            if row[12] == None:
                list_ZYBRFYMX[12] += 1
            if row[13] == None:
                list_ZYBRFYMX[13] += 1
            if row[14] == None:
                list_ZYBRFYMX[14] += 1
            if row[15] == None:
                list_ZYBRFYMX[15] += 1
            if row[16] == None:
                list_ZYBRFYMX[16] += 1
            if row[17] == None:
                list_ZYBRFYMX[17] += 1
            if row[18] == None:
                list_ZYBRFYMX[18] += 1
            if row[19] == None:
                list_ZYBRFYMX[19] += 1
            if row[20] == None:
                list_ZYBRFYMX[20] += 1
            row=cursor.fetchone()
        msg = u'表ZYBRFYMX中列YYDM%d,YYMC%d,YXBZ%d,XZQHDM%d,XZQHMC%d,YXBZ%d,RYSJ%d,CYSJ%d,SFSJ%d,ZYH%d,RYCS%d,BRXM%d,YYXMDM%d,YYXMMC%d,XMBZDM%d,XMBZMC%d,YYXMDW%d,YYXMGG%d,YYXMDJ%d,YYXMSL%d,YYXMFYJEXJ%d条记录不符合要求' % \
        (list_ZYBRFYMX[0],list_ZYBRFYMX[1],list_ZYBRFYMX[2],list_ZYBRFYMX[3],list_ZYBRFYMX[4],list_ZYBRFYMX[5],list_ZYBRFYMX[6],list_ZYBRFYMX[7],list_ZYBRFYMX[8],list_ZYBRFYMX[9],list_ZYBRFYMX[10],list_ZYBRFYMX[11],\
         list_ZYBRFYMX[12],list_ZYBRFYMX[13],list_ZYBRFYMX[14],list_ZYBRFYMX[15],list_ZYBRFYMX[16],list_ZYBRFYMX[17],list_ZYBRFYMX[18],list_ZYBRFYMX[19],list_ZYBRFYMX[20])
        #self.write_to_file(msg)
        self.log.info(msg)
        ## 标准表MZBRFYMX
        cursor.execute("select top 1000 YYDM,YYMC,YXBZ,XZQHDM,XZQHMC,YXBZ,JZHSJ,SFSJ,JZSJ,MZH,BRXM,YYXMDM,YYXMMC,XMBZDM,XMBZMC,YYXMDW,YYXMGG,YYXMDJ,YYXMSL,YYXMFYJEXJ FROM MZBRFYMX")
        row=cursor.fetchone()
        list_MZBRFYMX = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.log.info(u'开始对表 MZBRFYMX前1000条数据进行校验！')
        while row:
            if row[0] == None:
                list_MZBRFYMX[0] += 1
            if row[1] == None:
                list_MZBRFYMX[1] += 1
            if row[2] == None:
                list_MZBRFYMX[2] += 1
            if row[3] == None:
                list_MZBRFYMX[3] += 1
            if row[4] == None:
                list_MZBRFYMX[4] += 1
            if row[5] not in ('0','1'):
                list_MZBRFYMX[5] += 1
            if not self.date_check(row[6]):
                list_MZBRFYMX[6] += 1
            if not self.date_check(row[7]):
                list_MZBRFYMX[7] += 1
            if not self.date_check(row[8]):
                list_MZBRFYMX[8] += 1
            if row[9] == None:
                list_MZBRFYMX[9] += 1
            if row[10] == None:
                list_MZBRFYMX[10] += 1
            if row[11] == None:
                list_MZBRFYMX[11] += 1
            if row[12] == None:
                list_MZBRFYMX[12] += 1
            if row[13] == None:
                list_MZBRFYMX[13] += 1
            if row[14] == None:
                list_MZBRFYMX[14] += 1
            if row[15] == None:
                list_MZBRFYMX[15] += 1
            if row[16] == None:
                list_MZBRFYMX[16] += 1
            if row[17] == None:
                list_MZBRFYMX[17] += 1
            if row[18] == None:
                list_MZBRFYMX[18] += 1
            if row[19] == None:
                list_MZBRFYMX[19] += 1
            row=cursor.fetchone()
        msg = u'表MZBRFYMX中列YYDM%d,YYMC%d,YXBZ%d,XZQHDM%d,XZQHMC%d,YXBZ%d,JZHSJ%d,SFSJ%d,JZSJ%d,MZH%d,BRXM%d,YYXMDM%d,YYXMMC%d,XMBZDM%d,XMBZMC%d,YYXMDW%d,YYXMGG%d,YYXMDJ%d,YYXMSL%d,YYXMFYJEXJ%d条记录不符合要求' % \
        (list_MZBRFYMX[0],list_MZBRFYMX[1],list_MZBRFYMX[2],list_MZBRFYMX[3],list_MZBRFYMX[4],list_MZBRFYMX[5],list_MZBRFYMX[6],list_MZBRFYMX[7],list_MZBRFYMX[8],list_MZBRFYMX[9],list_MZBRFYMX[10],list_MZBRFYMX[11],list_MZBRFYMX[12],list_MZBRFYMX[13],list_MZBRFYMX[14],list_MZBRFYMX[15],list_MZBRFYMX[16],list_MZBRFYMX[17],list_MZBRFYMX[18],list_MZBRFYMX[19])
        #self.write_to_file(msg)
        self.log.info(msg)  
        ## 标准表YYZLXMSFZD
        cursor.execute("select top 1000 YYDM,YYMC,YXBZ,XZQHDM,XZQHMC,YXBZ,SHENGXIAOSJ,SHIXIAOSJ,XMBZDM,XMBZMC,XMDW,XMDJ,XMZGXJ FROM YYZLXMSFZD")
        row=cursor.fetchone()
        list_YYZLXMSFZD = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.log.info(u'开始对表 YYZLXMSFZD前1000条数据进行校验！')
        while row:
            if row[0] == None:
                list_YYZLXMSFZD[0] += 1
            if row[1] == None:
                list_YYZLXMSFZD[1] += 1
            if row[2] == None:
                list_YYZLXMSFZD[2] += 1
            if row[3] == None:
                list_YYZLXMSFZD[3] += 1
            if row[4] == None:
                list_YYZLXMSFZD[4] += 1
            if row[5] not in ('0','1'):
                list_YYZLXMSFZD[5] += 1
            if not self.date_check(row[6]):
                list_YYZLXMSFZD[6] += 1
            if not self.date_check(row[7]):
                list_YYZLXMSFZD[7] += 1
            if row[8] == None:
                list_YYZLXMSFZD[8] += 1
            if row[9] == None:
                list_YYZLXMSFZD[9] += 1
            if row[10] == None:
                list_YYZLXMSFZD[10] += 1
            if row[11] == None:
                list_YYZLXMSFZD[11] += 1
            if row[12] == None:
                list_YYZLXMSFZD[12] += 1
            row=cursor.fetchone()
        msg = u'表YYZLXMSFZD中列YYDM%d,YYMC%d,YXBZ%d,XZQHDM%d,XZQHMC%d,YXBZ%d,SHENGXIAOSJ%d,SHIXIAOSJ%d,XMBZDM%d,XMBZMC%d,XMDW%d,XMDJ%d,XMZGXJ%d条记录不符合要求' % \
        (list_YYZLXMSFZD[0],list_YYZLXMSFZD[1],list_YYZLXMSFZD[2],list_YYZLXMSFZD[3],list_YYZLXMSFZD[4],list_YYZLXMSFZD[5],list_YYZLXMSFZD[6],list_YYZLXMSFZD[7],list_YYZLXMSFZD[8],list_YYZLXMSFZD[9],list_YYZLXMSFZD[10],list_YYZLXMSFZD[11],list_YYZLXMSFZD[12])
        #self.write_to_file(msg)
        self.log.info(msg) 
        ## 标准表 YYYPSYZD
        cursor.execute("select top 1000 YYDM,YYMC,YXBZ,XZQHDM,XZQHMC,YXBZ,SHENGXIAOSJ,SHIXIAOSJ,YPID,YPSFDM,YPSFMC,KFYPDM,KFYPMC,YPDW,YPGG,YPDJ,YPLXDM,YPLXMC,SFJBYW FROM YYYPSYZD")
        row=cursor.fetchone()
        list_YYYPSYZD = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.log.info(u'开始对表 YYYPSYZD前1000条数据进行校验！')
        while row:
            if row[0] == None:
                list_YYYPSYZD[0] += 1
            if row[1] == None:
                list_YYYPSYZD[1] += 1
            if row[2] == None:
                list_YYYPSYZD[2] += 1
            if row[3] == None:
                list_YYYPSYZD[3] += 1
            if row[4] == None:
                list_YYYPSYZD[4] += 1
            if row[5] not in ('0','1'):
                list_YYYPSYZD[5] += 1
            if not self.date_check(row[6]):
                list_YYYPSYZD[6] += 1
            if not self.date_check(row[7]):
                list_YYYPSYZD[7] += 1
            if row[8] == None:
                list_YYYPSYZD[8] += 1
            if row[9] == None:
                list_YYYPSYZD[9] += 1
            if row[10] == None:
                list_YYYPSYZD[10] += 1
            if row[11] == None:
                list_YYYPSYZD[11] += 1
            if row[12] == None:
                list_YYYPSYZD[12] += 1
            if row[13] == None:
                list_YYYPSYZD[13] += 1
            if row[14] == None:
                list_YYYPSYZD[14] += 1
            if row[15] == None:
                list_YYYPSYZD[15] += 1
            if row[16] == None:
                list_YYYPSYZD[16] += 1
            if row[17] == None:
                list_YYYPSYZD[17] += 1
            if row[18] == None:
                list_YYYPSYZD[18] += 1
            row=cursor.fetchone()
        msg = u'表YYYPSYZD中列YYDM%d,YYMC%d,YXBZ%d,XZQHDM%d,XZQHMC%d,YXBZ%d,SHENGXIAOSJ%d,SHIXIAOSJ%d,YPID%d,YPSFDM%d,YPSFMC%d,KFYPDM%d,KFYPMC%d,YPDW%d,YPGG%d,YPDJ%d,YPLXDM%d,YPLXMC%d,SFJBYW%d条记录不符合要求' % \
        (list_YYYPSYZD[0],list_YYYPSYZD[1],list_YYYPSYZD[2],list_YYYPSYZD[3],list_YYYPSYZD[4],list_YYYPSYZD[5],list_YYYPSYZD[6],list_YYYPSYZD[7],list_YYYPSYZD[8],list_YYYPSYZD[9],list_YYYPSYZD[10],\
         list_YYYPSYZD[11],list_YYYPSYZD[12],list_YYYPSYZD[13],list_YYYPSYZD[14],list_YYYPSYZD[15],list_YYYPSYZD[16],list_YYYPSYZD[17],list_YYYPSYZD[18])
        #self.write_to_file(msg)
        self.log.info(msg)  
        ## 标准表YYWSCLSFZD
        cursor.execute("select top 1000 YYDM,YYMC,YXBZ,XZQHDM,XZQHMC,YXBZ,SHENGXIAOSJ,SHIXIAOSJ FROM YYWSCLSFZD")
        row=cursor.fetchone()
        list_YYWSCLSFZD = [0,0,0,0,0,0,0,0]
        self.log.info(u'开始对表 YYWSCLSFZD前1000条数据进行校验！')
        while row:
            if row[0] == None:
                list_YYWSCLSFZD[0] += 1
            if row[1] == None:
                list_YYWSCLSFZD[1] += 1
            if row[2] == None:
                list_YYWSCLSFZD[2] += 1
            if row[3] == None:
                list_YYWSCLSFZD[3] += 1
            if row[4] == None:
                list_YYWSCLSFZD[4] += 1
            if row[5] not in ('0','1'):
                list_YYWSCLSFZD[5] += 1
            if not self.date_check(row[6]):
                list_YYWSCLSFZD[6] += 1
            if not self.date_check(row[7]):
                list_YYWSCLSFZD[7] += 1
            row=cursor.fetchone()
        msg = u'表YYWSCLSFZD中列YYDM%d,YYMC%d,YXBZ%d,XZQHDM%d,XZQHMC%d,YXBZ%d,SHENGXIAOSJ%d,SHIXIAOSJ%d条记录不符合要求' % \
        (list_YYWSCLSFZD[0],list_YYWSCLSFZD[1],list_YYWSCLSFZD[2],list_YYWSCLSFZD[3],list_YYWSCLSFZD[4],list_YYWSCLSFZD[5],list_YYWSCLSFZD[6],list_YYWSCLSFZD[7])
        #self.write_to_file(msg)
        self.log.info(msg)
        ## 标准表YPRKXX
        cursor.execute("select top 1000 YYDM,YYMC,YXBZ,XZQHDM,XZQHMC,YXBZ,RKSJ,SCSJ,RZSJ FROM YPRKXX")
        row=cursor.fetchone()
        list_YPRKXX = [0,0,0,0,0,0,0,0,0]
        self.log.info(u'开始对表 YPRKXX前1000条数据进行校验！')
        while row:
            if row[0] == None:
                list_YPRKXX[0] += 1
            if row[1] == None:
                list_YPRKXX[1] += 1
            if row[2] == None:
                list_YPRKXX[2] += 1
            if row[3] == None:
                list_YPRKXX[3] += 1
            if row[4] == None:
                list_YPRKXX[4] += 1
            if row[5] not in ('0','1'):
                list_YPRKXX[5] += 1
            if not self.date_check(row[6]):
                list_YPRKXX[6] += 1
            if not self.date_check(row[7]):
                list_YPRKXX[7] += 1
            if not self.date_check(row[8]):
                list_YPRKXX[8] += 1
            row=cursor.fetchone()
        msg = u'表YPRKXX中列YYDM%d,YYMC%d,YXBZ%d,XZQHDM%d,XZQHMC%d,YXBZ%d,RKSJ%d,SCSJ%d,RZSJ%d条记录不符合要求' % \
        (list_YPRKXX[0],list_YPRKXX[1],list_YPRKXX[2],list_YPRKXX[3],list_YPRKXX[4],list_YPRKXX[5],list_YPRKXX[6],list_YPRKXX[7],list_YPRKXX[8])
        #self.write_to_file(msg)
        self.log.info(msg)
        ## 标准表YPCKXX
        cursor.execute("select top 1000 YYDM,YYMC,YXBZ,XZQHDM,XZQHMC,YXBZ,CKSJ,SCSJ FROM YPCKXX")
        row=cursor.fetchone()
        list_YPCKXX = [0,0,0,0,0,0,0,0]
        self.log.info(u'开始对表 YPCKXX前1000条数据进行校验！')
        while row:
            if row[0] == None:
                list_YPCKXX[0] += 1
            if row[1] == None:
                list_YPCKXX[1] += 1
            if row[2] == None:
                list_YPCKXX[2] += 1
            if row[3] == None:
                list_YPCKXX[3] += 1
            if row[4] == None:
                list_YPCKXX[4] += 1
            if row[5] not in ('0','1'):
                list_YPCKXX[5] += 1
            if not self.date_check(row[6]):
                list_YPCKXX[6] += 1
            if not self.date_check(row[7]):
                list_YPCKXX[7] += 1
            row=cursor.fetchone()
        msg = u'表YPCKXX中列YYDM%d,YYMC%d,YXBZ%d,XZQHDM%d,XZQHMC%d,YXBZ%d,CKSJ%d,SCSJ%d条记录不符合要求' % \
        (list_YPRKXX[0],list_YPRKXX[1],list_YPRKXX[2],list_YPRKXX[3],list_YPRKXX[4],list_YPRKXX[5],list_YPRKXX[6],list_YPRKXX[7])
        #self.write_to_file(msg)
        self.log.info(msg)   
        ## 标准表WSCLCKXX
        cursor.execute("select top 1000 YYDM,YYMC,YXBZ,XZQHDM,XZQHMC,YXBZ,CKSJ,SCSJ FROM WSCLCKXX")
        row=cursor.fetchone()
        list_WSCLCKXX = [0,0,0,0,0,0,0,0]
        self.log.info(u'开始对表 WSCLCKXX前1000条数据进行校验！')
        while row:
            if row[0] == None:
                list_WSCLCKXX[0] += 1
            if row[1] == None:
                list_WSCLCKXX[1] += 1
            if row[2] == None:
                list_WSCLCKXX[2] += 1
            if row[3] == None:
                list_WSCLCKXX[3] += 1
            if row[4] == None:
                list_WSCLCKXX[4] += 1
            if row[5] not in ('0','1'):
                list_WSCLCKXX[5] += 1
            if not self.date_check(row[6]):
                list_WSCLCKXX[6] += 1
            if not self.date_check(row[7]):
                list_WSCLCKXX[7] += 1
            row=cursor.fetchone()
        msg = u'表WSCLCKXX中列YYDM%d,YYMC%d,YXBZ%d,XZQHDM%d,XZQHMC%d,YXBZ%d,CKSJ%d,SCSJ%d条记录不符合要求' % \
        (list_WSCLCKXX[0],list_WSCLCKXX[1],list_WSCLCKXX[2],list_WSCLCKXX[3],list_WSCLCKXX[4],list_WSCLCKXX[5],list_WSCLCKXX[6],list_WSCLCKXX[7])
        #self.write_to_file(msg)
        self.log.info(msg)
        ## 标准表WSCLRKXX
        cursor.execute("select top 1000 YYDM,YYMC,YXBZ,XZQHDM,XZQHMC,YXBZ,RKSJ,SCSJ FROM WSCLRKXX")
        row=cursor.fetchone()
        list_WSCLRKXX = [0,0,0,0,0,0,0,0]
        self.log.info(u'开始对表WSCLRKXX前1000条数据进行校验！')
        while row:
            if row[0] == None:
                list_WSCLRKXX[0] += 1
            if row[1] == None:
                list_WSCLRKXX[1] += 1
            if row[2] == None:
                list_WSCLRKXX[2] += 1
            if row[3] == None:
                list_WSCLRKXX[3] += 1
            if row[4] == None:
                list_WSCLRKXX[4] += 1
            if row[5] not in ('0','1'):
                list_WSCLRKXX[5] += 1
            if not self.date_check(row[6]):
                list_WSCLRKXX[6] += 1
            if not self.date_check(row[7]):
                list_WSCLRKXX[7] += 1
            row=cursor.fetchone()
        msg = u'表WSCLRKXX中列YYDM%d,YYMC%d,YXBZ%d,XZQHDM%d,XZQHMC%d,YXBZ%d,RKSJ%d,SCSJ%d条记录不符合要求' % \
        (list_WSCLRKXX[0],list_WSCLRKXX[1],list_WSCLRKXX[2],list_WSCLRKXX[3],list_WSCLRKXX[4],list_WSCLRKXX[5],list_WSCLRKXX[6],list_WSCLRKXX[7])
        #self.write_to_file(msg)
        self.log.info(msg)
        ## 标准表ZYBRFYJSXX
        cursor.execute("select top 1000 YYDM,YYMC,YXBZ,XZQHDM,XZQHMC,YXBZ,CYJSRQ,JFFWQ,JFFWZ,KPRQ FROM ZYBRFYJSXX")
        row=cursor.fetchone()
        list_ZYBRFYJSXX = [0,0,0,0,0,0,0,0,0,0]
        self.log.info(u'开始对表ZYBRFYJSXX前1000条数据进行校验！')
        while row:
            if row[0] == None:
                list_ZYBRFYJSXX[0] += 1
            if row[1] == None:
                list_ZYBRFYJSXX[1] += 1
            if row[2] == None:
                list_ZYBRFYJSXX[2] += 1
            if row[3] == None:
                list_ZYBRFYJSXX[3] += 1
            if row[4] == None:
                list_ZYBRFYJSXX[4] += 1
            if row[5] not in ('0','1'):
                list_ZYBRFYJSXX[5] += 1
            if not self.date_check(row[6]):
                list_ZYBRFYJSXX[6] += 1
            if not self.date_check(row[7]):
                list_ZYBRFYJSXX[7] += 1
            if not self.date_check(row[8]):
                list_ZYBRFYJSXX[8] += 1
            if not self.date_check(row[9]):
                list_ZYBRFYJSXX[9] += 1
            row=cursor.fetchone()
        msg = u'表ZYBRFYJSXX中列YYDM%d,YYMC%d,YXBZ%d,XZQHDM%d,XZQHMC%d,YXBZ%d,CYJSRQ%d,JFFWQ%d,JFFWZ%d,KPRQ%d条记录不符合要求' % \
        (list_ZYBRFYJSXX[0],list_ZYBRFYJSXX[1],list_ZYBRFYJSXX[2],list_ZYBRFYJSXX[3],list_ZYBRFYJSXX[4],list_ZYBRFYJSXX[5],list_ZYBRFYJSXX[6],list_ZYBRFYJSXX[7],list_ZYBRFYJSXX[8],list_ZYBRFYJSXX[9])
        #self.write_to_file(msg)
        self.log.info(msg)
        ## 标准表MZBRFYJSXX
        cursor.execute("select top 1000 YYDM,YYMC,YXBZ,XZQHDM,XZQHMC,YXBZ,KPRQ FROM MZBRFYJSXX")
        row=cursor.fetchone()
        list_MZBRFYJSXX = [0,0,0,0,0,0,0]
        self.log.info(u'开始对表MZBRFYJSXX前1000条数据进行校验！')
        while row:
            if row[0] == None:
                list_MZBRFYJSXX[0] += 1
            if row[1] == None:
                list_MZBRFYJSXX[1] += 1
            if row[2] == None:
                list_MZBRFYJSXX[2] += 1
            if row[3] == None:
                list_MZBRFYJSXX[3] += 1
            if row[4] == None:
                list_MZBRFYJSXX[4] += 1
            if row[5] not in ('0','1'):
                list_MZBRFYJSXX[5] += 1
            if not self.date_check(row[6]):
                list_MZBRFYJSXX[6] += 1
            row=cursor.fetchone()
        msg = u'表MZBRFYJSXX中列YYDM%d,YYMC%d,YXBZ%d,XZQHDM%d,XZQHMC%d,YXBZ%d,KPRQ%d条记录不符合要求' % \
        (list_MZBRFYJSXX[0],list_MZBRFYJSXX[1],list_MZBRFYJSXX[2],list_MZBRFYJSXX[3],list_MZBRFYJSXX[4],list_MZBRFYJSXX[5],list_MZBRFYJSXX[6])
        #self.write_to_file(msg)
        self.log.info(msg)
        
           
if __name__ == '__main__':
    Test()
    os.system('pause')
    
    
