#!/usr/bin/python
# -*- coding:utf-8 -*- 
import urllib  
import urllib2  
import string
import os
import sys
import re
import json as simplejson
import MySQLdb

from  datetime  import  *
import  time

import cookielib

import re
import httplib

reload(sys)
sys.setdefaultencoding("utf-8")

def bIsDbExists():
    conn = MySQLdb.connect(host="192.168.131.82",user="gamerank",passwd="gamerank",db="gamerank",charset="utf8")
    cursor = conn.cursor()
    SQLDate=time.strftime('%Y_%m_%d',time.localtime(time.time()))
    rankSQLName=SQLDate[0:7]
    sql="create table if not exists NewappRank_"+rankSQLName+" like NewappRank"

    cursor.execute(sql)
    cursor.close()

def bIsConflict(primaryName,m):
    if (primaryName,) in m:
        return 1
    else:
        return 0

def bIsDescriptionNull(gameName,cursor):
    Description=""
    n = cursor.execute("select description from NewappGameName where gameName = '" + str(gameName) + "'")
    for row in cursor.fetchall():
        for r in row:
            if not r:
                return 1
            else:
                return 0

def bIsWebsiteNull(gameName,cursor):
    #Website=""
    gameName=gameName.replace('\'','\\\'')
    n = cursor.execute("select website from NewappGameName where gameName = '" + str(gameName) + "'")
    for row in cursor.fetchall():
        for r in row:
            if not r:
                return 1
            else:
                return 0


def bInsectTableToday(gameName,m):
    gameName=gameName.replace('\'','\\\'')
    if (gameName,) in m:
        return 1
    else:
        return 0

def clearData(dealDate):
    conn = MySQLdb.connect(host="192.168.131.82",user="gamerank",passwd="gamerank",db="gamerank",charset="utf8")
    cursor = conn.cursor()
    SQLDate=time.strftime('%Y_%m_%d',time.localtime(time.time()))
    rankSQLName=SQLDate[0:7]
    sql="delete from NewappRank_"+rankSQLName+" where rankDate like '"+dealDate+"%'"
    cursor.execute(sql)
    conn.commit()
    cursor.close()

def deal_iosData(channel,path,dealData,bInsertGameNameTable):
    fileName = channel + ".html"
    SQLDate=time.strftime('%Y_%m_%d',time.localtime(time.time()))
    tableName = "NewappRank_"+SQLDate[0:7]
    print("dealing  " + fileName)
    if 1:
        from BeautifulSoup import BeautifulSoup
        soup = BeautifulSoup(open(path + "//" + fileName))
        rankTag  = 1 
        
        conn=MySQLdb.connect(host="192.168.131.82",user="gamerank",passwd="gamerank",db="gamerank",charset="utf8")
        cursor = conn.cursor()
        
        titleP = re.compile('float:left;margin:15px 0px 0px 15px;min-height:204px;width:120px;border:1px solid #ccc;text-align:center; padding-top:5px;line-height:25px')
        n1 = cursor.execute("select gameName from NewappGameName")
        m1 = cursor.fetchall()
        n2 = cursor.execute("select gameName from NewappRank_"+SQLDate[0:7]+" where rankDate like '" + str(dealDate) + "%' and channel = '" + str(channel) + "'")
        m2 = cursor.fetchall()
        for i in soup.findAll(attrs={"style":titleP}):
            appgamename=i.findAll('a')[0].findAll('img')[0].get('alt')
            targetwebsite=i.findAll('span')[0].findAll('a')[0].get('href')
            appganmecompany=i.findAll('span')[1].findAll('a')[0].get('title')
            appganmecompany = urllib.unquote(str(appganmecompany))           
            if not bIsConflict(appgamename,m1) and bInsertGameNameTable == 1 :
                sql = "insert into NewappGameName(gameName,company,addDate,website) values(%s,%s,%s,%s)"
                print("add new game")
                param = (appgamename,appganmecompany,dealDate,targetwebsite)
                n = cursor.execute(sql,param)
                conn.commit()      
            if not bInsectTableToday(appgamename,m2):
                sql = "insert into " + tableName +  "(gameName,rankDate,ranking,website,channel) values(%s,%s,%s,%s,%s)"
                param = (appgamename,dealDate,rankTag,targetwebsite,channel)
                n = cursor.execute(sql,param)
                conn.commit()       
            rankTag=rankTag+1
        cursor.close()
        conn.close()



def get_iosData(country,path,dealDate):
    
    htmlName=""
    url={}

    if country == "chinaIphone":
        print("begin to download china iphone data")
        htmlName = "ios_chinaIphone"
        url['free'] = r"http://www.ann9.com/21_11?p=0"
        url['pay'] = r"http://www.ann9.com/21_12?p=0"
        url['sell'] = r"http://www.ann9.com/21_13?p=0"
    elif country == "chinaIpad":
        print("begin to download china Ipad data")
        htmlName = "ios_chinaIpad"
        url['free'] = r"http://www.ann9.com/21_21?p=0"
        url['pay'] = r"http://www.ann9.com/21_22?p=0"
        url['sell'] = r"http://www.ann9.com/21_23?p=0"
    elif country == "japanIphone":
        print("begin to download japan data")
        htmlName = "ios_japanIphone"
        url['free'] = r"http://jpn.ann9.com/21_11?p=0"
        url['pay'] = r"http://jpn.ann9.com/21_12?p=0"
        url['sell'] = r"http://jpn.ann9.com/21_13?p=0"
    elif country == "japanIpad":
        print("begin to download japan ipad data")
        htmlName = "ios_japanIpad"
        url['free'] = r"http://jpn.ann9.com/21_21?p=0"
        url['pay'] = r"http://jpn.ann9.com/21_22?p=0"
        url['sell'] = r"http://jpn.ann9.com/21_23?p=0"
    elif country == "koreaIphone":
        print("begin to download korea data")
        htmlName = "ios_koreaIphone"
        url['free'] = r"http://kor.ann9.com/21_11?p=0"
        url['pay'] = r"http://kor.ann9.com/21_12?p=0"
        url['sell'] = r"http://kor.ann9.com/21_13?p=0"
    elif country == "koreaIpad":
        print("begin to download korea ipad data")
        htmlName = "ios_koreaIpad"
        url['free'] = r"http://kor.ann9.com/21_21?p=0"
        url['pay'] = r"http://kor.ann9.com/21_22?p=0"
        url['sell'] = r"http://kor.ann9.com/21_23?p=0"
    elif country == "americanIphone":
        print("begin to download american data")
        htmlName = "ios_americanIphone"
        url['free'] = r"http://usa.ann9.com/21_11?p=0"
        url['pay'] = r"http://usa.ann9.com/21_12?p=0"
        url['sell'] = r"http://usa.ann9.com/21_13?p=0"
    elif country == "americanIpad":
        print("begin to download american ipad data")
        htmlName = "ios_americanIpad"
        url['free'] = r"http://usa.ann9.com/21_21?p=0"
        url['pay'] = r"http://usa.ann9.com/21_22?p=0"
        url['sell'] = r"http://usa.ann9.com/21_23?p=0"
    elif country == "taiwanIphone":
        print("begin to download taiwan data")
        htmlName = "ios_taiwanIphone"
        url['free'] = r"http://twn.ann9.com/21_11?p=0"
        url['pay'] = r"http://twn.ann9.com/21_12?p=0"
        url['sell'] = r"http://twn.ann9.com/21_13?p=0"
    elif country == "taiwanIpad":
        print("begin to download taiwan ipad data")
        htmlName = "ios_taiwanIpad"
        url['free'] = r"http://twn.ann9.com/21_21?p=0"
        url['pay'] = r"http://twn.ann9.com/21_22?p=0"
        url['sell'] = r"http://twn.ann9.com/21_23?p=0"
    else:
        print("the arg of country is error!")
        return

    for k,v in url.iteritems():
        tt=""
        tt = path + "//" + htmlName + "_" + k + ".html"
        print(tt + v)
        fhtml = open(tt,'w+')
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31'
        req = urllib2.Request(v)
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        try:
            the_page = response.read()
        except httplib.BadStatusLine:
            print("the ios download out of time!!!!")
        except Exception,e:
            print e
        fhtml.write(the_page)
        fhtml.close()
        time.sleep(10)
        

    
def get_channelData(country,path,dealDate):
    
    htmlName = ""
    url = ""
    SQLDate=time.strftime('%Y_%m_%d',time.localtime(time.time()))
    tableName = "NewappRank_"+SQLDate[0:7]
    rankTag=1

    conn=MySQLdb.connect(host="192.168.131.82",user="gamerank",passwd="gamerank",db="gamerank",charset="utf8")
    cursor = conn.cursor()

    if country == 'android_360':
        print "begin to download 360 Data"
        url = "http://zhushou.360.cn/list/index/cid/2/size/all/lang/all/order/download/?page="
        begin_page = 1
        end_page = 3
        n1 = cursor.execute("select gameName from NewappGameName")
        m1 = cursor.fetchall()
        n2 = cursor.execute("select gameName from NewappRank_"+SQLDate[0:7]+" where rankDate like '" + str(dealDate) + "%' and channel = '" + str(country) + "'")
        m2 = cursor.fetchall()

        for i in range(begin_page, end_page+1):
            htmlName = path + "//channel_360_" + str(i) + '.html'
            fhtml = open(htmlName,'w+')
            try:
                the_page = urllib2.urlopen(url + str(i)).read()
            except httplib.BadStatusLine:
                print("the ios download out of time!!!!")
            except Exception,e:
                print e
            fhtml.write(the_page)
            fhtml.close()
            
            from BeautifulSoup import BeautifulSoup;
            soup = BeautifulSoup(the_page);

            for j in soup.find("ul",{'class':['iconList'],}).findAll('li'):

                baidu=0
                targetWebsite=""
                if j.findAll('a') and j.findAll('a'):
                    targetWebsite= "http://zhushou.360.cn" + str(j.findAll('a')[0].get('href'))
                
                gamename = j.findAll('a')[1].string
                #str2 = str2.replace('&#39;','\'')

                if not bIsConflict(gamename,m1) :
                    sql = "insert into NewappGameName(gameName,addDate,website) values(%s,%s,%s)"
                    param = (gamename,dealDate,targetWebsite)
                    n = cursor.execute(sql,param)
                    conn.commit()

                if not bInsectTableToday(gamename,m2):
                    sql = "insert into " + tableName + "(gameName,rankDate,ranking,baidu,website,channel) values(%s,%s,%s,%s,%s,%s)"
                    param = (gamename,dealDate,rankTag,baidu,targetWebsite,country)
                    n = cursor.execute(sql,param)
                    conn.commit()
                rankTag = rankTag+1
            
        print "finish download 360 data"
        return
    elif country == 'android_qq':
        print "begin to download qq Data"
        htmlName = path + '//channel_qq.html'
        fhtml = open(htmlName,'w+')
        url = 'http://android.myapp.com/myapp/cate/appList.htm?orgame=2&categoryId=0&pageSize=200&pageContext=0'
        #上述链接是通过careles工具分析http://android.myapp.com/myapp/category.htm?orgame=2这个真实的url得到的，上述代表得到100个app资料

        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
        req = urllib2.Request(url)  
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        the_page = response.read() 
        fhtml.write(the_page)
        fhtml.close()


        ret_dict = simplejson.loads(the_page)
        n1 = cursor.execute("select gameName from NewappGameName")
        m1 = cursor.fetchall()
        n2 = cursor.execute("select gameName from NewappRank_"+SQLDate[0:7]+" where rankDate like '" + str(dealDate) + "%' and channel = '" + str(country) + "'")
        m2 = cursor.fetchall()

        for i in range(0,len(ret_dict['obj'])):
            if ret_dict['obj'][i] and ret_dict['obj'][i]['appName']:
                targetUrl = "http://android.myapp.com/myapp/detail.htm?apkName=" + str(ret_dict['obj'][i]['pkgName'])
                baidu=0

                if not bIsConflict(ret_dict['obj'][i]['appName'],m1) :
                    sql = "insert into NewappGameName(gameName,addDate,website) values(%s,%s,%s)"
                    param = (ret_dict['obj'][i]['appName'],dealDate,targetUrl)
                    n = cursor.execute(sql,param)
                    conn.commit()
    
                if not bInsectTableToday(ret_dict['obj'][i]['appName'],m2):
                    sql = "insert into " + tableName + "(gameName,rankDate,ranking,baidu,channel,website) values(%s,%s,%s,%s,%s,%s)"
                    param = (ret_dict['obj'][i]['appName'],dealDate,rankTag,baidu,country,targetUrl)
                    n = cursor.execute(sql,param)
                    conn.commit()
                rankTag = rankTag+1
        print "finish download qq data"
        return
    elif country == 'android_91':
        print "begin to download 91_android Data"
        url = "http://game.91.com/android/1832_"
        begin_page = 1
        end_page = 17
        n1 = cursor.execute("select gameName from NewappGameName")
        m1 = cursor.fetchall()
        n2 = cursor.execute("select gameName from NewappRank_"+SQLDate[0:7]+" where rankDate like '" + str(dealDate) + "%' and channel = '" + str(country) + "'")
        m2 = cursor.fetchall()
        for i in range(begin_page, end_page+1):
            pageAppNum = 0
            htmlName = path + "//91_android_" + str(i) + '.html'
            fhtml = open(htmlName,'w+')
            try:
                the_page = urllib2.urlopen(url + str(i) + ".html").read()
            except httplib.BadStatusLine:
                print("the 91 android : http://game.91.com/android/1832_"+ str(i)+"   out of time!!!!")
            fhtml.write(the_page)
            fhtml.close()

            from BeautifulSoup import BeautifulSoup;
            soup = BeautifulSoup(the_page);
            for j in soup.findAll("div",{'class':['sty2'],}):
                if pageAppNum <12:

                    targetWebsite=""
                    gamename=j.find('a').string
                    targetWebsite =  j.find('p').find('a').get('href')

                    baidu=0

                    if not bIsConflict(gamename,m1) :
                        sql = "insert into NewappGameName(gameName,addDate,website) values(%s,%s,%s)"
                        param = (gamename,dealDate,targetWebsite)
                        n = cursor.execute(sql,param)
                        conn.commit()
                        
                    if not bInsectTableToday(gamename,m2):
                        sql = "insert into " + tableName + "(gameName,rankDate,ranking,baidu,channel,website) values(%s,%s,%s,%s,%s,%s)"
                        param = (gamename,dealDate,rankTag,baidu,country,targetWebsite)
                        n = cursor.execute(sql,param)
                        conn.commit()
                    rankTag = rankTag+1
                    pageAppNum=pageAppNum+1
                    #因为这里爬虫过来的时候，本页的内容还包括日期排序的app，所以只选取前面的12个app，即按照热度排序的结果，去除按日期排序结果
                else:
                    break
        print "finish download 91 data"
        return
    elif country == 'android_baidu':
        print "begin to download baidu Data"
        url = "http://shouji.baidu.com/rank/top/game/list_"
        begin_page = 1
        end_page = 5
        n1 = cursor.execute("select gameName from NewappGameName")
        m1 = cursor.fetchall()
        n2 = cursor.execute("select gameName from NewappRank_"+SQLDate[0:7]+" where rankDate like '" + str(dealDate) + "%' and channel = '" + str(country) + "'")
        m2 = cursor.fetchall()
        for i in range(begin_page, end_page+1):
            htmlName = path + "//channel_baidu_" + str(i) + '.html'
            fhtml = open(htmlName,'w+')
            try:
                the_page = urllib2.urlopen(url + str(i)+".html").read()
            except httplib.BadStatusLine:
                print("the ios download out of time!!!!")
            except Exception,e:
                print e
            fhtml.write(the_page)
            fhtml.close()  

            from BeautifulSoup import BeautifulSoup;
            soup = BeautifulSoup(the_page);

            for j in soup.find("div",{'class':'app-bd show'}).findAll('li'):
                baidu=0
                targetWebsite=""
                gamename = j.findAll('p')[0].string
                #str2 = str2.replace('&#39;','\'')

                if not bIsConflict(gamename,m1) :
                    sql = "insert into NewappGameName(gameName,addDate,website) values(%s,%s,%s)"
                    param = (gamename,dealDate,targetWebsite)
                    n = cursor.execute(sql,param)
                    conn.commit()

                if not bInsectTableToday(gamename,m2):
                    sql = "insert into " + tableName + "(gameName,rankDate,ranking,baidu,website,channel) values(%s,%s,%s,%s,%s,%s)"
                    param = (gamename,dealDate,rankTag,baidu,targetWebsite,country)
                    n = cursor.execute(sql,param)
                    conn.commit()
                rankTag = rankTag+1
            
        print "finish download baidu data"
        return
    elif country == 'android_google':
        print "begin to download Google Play Data"
        url = "https://play.google.com/store/apps/category/GAME/collection/topselling_free?hl=zh-CN"
        n1 = cursor.execute("select gameName from NewappGameName")
        m1 = cursor.fetchall()
        n2 = cursor.execute("select gameName from NewappRank_"+SQLDate[0:7]+" where rankDate like '" + str(dealDate) + "%' and channel = '" + str(country) + "'")
        m2 = cursor.fetchall()
        htmlName = path + "//channel_google.html"
        fhtml = open(htmlName,'w+')
        try:
            the_page = urllib2.urlopen(url).read()
        except httplib.BadStatusLine:
            print("the ios download out of time!!!!")
        except Exception,e:
            print e
        fhtml.write(the_page)
        fhtml.close()  
        from BeautifulSoup import BeautifulSoup;
        soup = BeautifulSoup(the_page);

        for j in soup.find("div",{'class':'id-card-list card-list two-cards'}).findAll('a',{'class':'subtitle'}):
            baidu=0
            targetWebsite=""
            gamename = j.string
            if not bIsConflict(gamename,m1) :
                sql = "insert into NewappGameName(gameName,addDate,website) values(%s,%s,%s)"
                param = (gamename,dealDate,targetWebsite)
                n = cursor.execute(sql,param)
                conn.commit()
            if not bInsectTableToday(gamename,m2):
                sql = "insert into " + tableName + "(gameName,rankDate,ranking,baidu,website,channel) values(%s,%s,%s,%s,%s,%s)"
                param = (gamename,dealDate,rankTag,baidu,targetWebsite,country)
                n = cursor.execute(sql,param)
                conn.commit()
            rankTag = rankTag+1  
    else:
        print "the arg of website is error"
        return
    cursor.close()
    conn.close()
    print "finish download android data"

if __name__ == '__main__':
    beginBySelfTime = 1
    dt = datetime.now()
    beginBySelf = "false"
    if len(sys.argv) > 1 and sys.argv[1] == "begin" and beginBySelfTime == 1:
        beginBySelf = "true"
        beginBySelfTime = 0 
    dealDate=dt.strftime('%Y-%m-%d')
    path = "htmlData//" + str(dealDate)
    if not os.path.exists(path):
        os.makedirs(path)

    if True:
        print("begin to get data")
        bIsDbExists()
        clearData(dealDate)   
        get_iosData('chinaIphone',path,dealDate)
        time.sleep(2)
        get_iosData('chinaIpad',path,dealDate)
        time.sleep(2)
        get_iosData('japanIphone',path,dealDate)
        time.sleep(2)
        get_iosData('japanIpad',path,dealDate)
        time.sleep(2)
        get_iosData('koreaIphone',path,dealDate)
        time.sleep(2)
        get_iosData('koreaIpad',path,dealDate)
        time.sleep(2)
        get_iosData('americanIphone',path,dealDate)
        time.sleep(2)
        get_iosData('americanIpad',path,dealDate)
        time.sleep(2)
        get_iosData('taiwanIphone',path,dealDate)
        time.sleep(2)       
        get_iosData('taiwanIpad',path,dealDate)
        time.sleep(10)
        get_channelData('android_360',path,dealDate)
        time.sleep(10)
        get_channelData('android_qq',path,dealDate)
        time.sleep(10)
        get_channelData('android_91',path,dealDate)
        time.sleep(10)
        get_channelData('android_baidu',path,dealDate)
        #get_channelData('android_google',path,dealDate)
        print("end get data")
        print(time.strftime("%H:%M:%S",time.localtime(time.time())))

        if 1:
            print("begin to deal the html data")
            print(time.strftime("%H:%M:%S",time.localtime(time.time())))
            #deal_iosData(文件名，路径，时间，mysql表名，是否进入gameName表，county字段)
            deal_iosData('ios_chinaIphone_free',path,dealDate,1)
            deal_iosData('ios_chinaIphone_pay',path,dealDate,1)
            deal_iosData('ios_chinaIphone_sell',path,dealDate,1)
            deal_iosData('ios_chinaIpad_free',path,dealDate,1)
            deal_iosData('ios_chinaIpad_pay',path,dealDate,1)
            deal_iosData('ios_chinaIpad_sell',path,dealDate,1)
            
            deal_iosData('ios_japanIphone_free',path,dealDate,0)
            deal_iosData('ios_japanIphone_pay',path,dealDate,0)
            deal_iosData('ios_japanIphone_sell',path,dealDate,0)
            
            deal_iosData('ios_japanIpad_free',path,dealDate,0)
            deal_iosData('ios_japanIpad_pay',path,dealDate,0)
            deal_iosData('ios_japanIpad_sell',path,dealDate,0)
            
            deal_iosData('ios_americanIphone_free',path,dealDate,0)
            deal_iosData('ios_americanIphone_pay',path,dealDate,0)
            deal_iosData('ios_americanIphone_sell',path,dealDate,0)
            
            deal_iosData('ios_americanIpad_free',path,dealDate,0)
            deal_iosData('ios_americanIpad_pay',path,dealDate,0)
            deal_iosData('ios_americanIpad_sell',path,dealDate,0)
            
            deal_iosData('ios_koreaIphone_free',path,dealDate,0)
            deal_iosData('ios_koreaIphone_pay',path,dealDate,0)
            deal_iosData('ios_koreaIphone_sell',path,dealDate,0)
            
            deal_iosData('ios_koreaIpad_free',path,dealDate,0)
            deal_iosData('ios_koreaIpad_pay',path,dealDate,0)
            deal_iosData('ios_koreaIpad_sell',path,dealDate,0)
            
            deal_iosData('ios_taiwanIphone_free',path,dealDate,0)
            deal_iosData('ios_taiwanIphone_pay',path,dealDate,0)
            deal_iosData('ios_taiwanIphone_sell',path,dealDate,0)
            
            deal_iosData('ios_taiwanIpad_free',path,dealDate,0)
            deal_iosData('ios_taiwanIpad_pay',path,dealDate,0)
            deal_iosData('ios_taiwanIpad_sell',path,dealDate,0)
            print("end deal the html data")
            print(time.strftime("%H:%M:%S",time.localtime(time.time())))
    else:
        print("wait time to begin capture    "+str(dt.strftime('%Y%m%d %H:%M')))
