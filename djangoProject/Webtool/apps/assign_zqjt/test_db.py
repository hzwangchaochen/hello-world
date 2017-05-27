# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors

import json
from json import *


def getDataFromMysql():
    res={}
    conn= MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='123456',db ='leiting',charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    sqlstr="select * from ust_hangulstrings where QAer like '黄超群%'"
    cursor.execute(sqlstr)
    data=cursor.fetchall()
    print data
if __name__ == '__main__':
    getDataFromMysql()
    print 'nihao'