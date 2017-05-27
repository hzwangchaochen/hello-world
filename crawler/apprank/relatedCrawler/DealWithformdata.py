# -*- coding: utf-8 -*-
import httplib
import urllib
import urllib2
print "begin to download Google Play Data"
url = "https://play.google.com/store/apps/category/GAME/collection/topselling_free?hl=zh-CN"
htmlName ="channel_google1.html"
fhtml = open(htmlName,'w+')
values={"start":0,"num":60}
the_page=""
try:
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    print(the_page)
except httplib.BadStatusLine:
    print("the ios download out of time!!!!")
except Exception,e:
    print e
fhtml.write(the_page)
fhtml.close()  
from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(the_page)
for j in soup.find("div",{'class':'id-card-list card-list two-cards'}).findAll('a',{'class':'subtitle'}):
    baidu=0
    targetWebsite=""
    gamename = j.string