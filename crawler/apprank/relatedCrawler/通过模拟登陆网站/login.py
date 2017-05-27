# -*- coding: utf-8 -*-
import urllib  
import urllib2  
import cookielib
import re
import httplib
import sys
import requests
from BeautifulSoup import BeautifulSoup;
reload(sys)
sys.setdefaultencoding("utf-8")

login_url='https://www.appannie.com/account/login/?_ref=header/'
headers = {
'Referer':'https://www.appannie.com/cn/',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}
s=requests.session()
token=''
html=s.get(login_url,headers=headers).content
from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html)
for j in soup.find("form",{'class':'uc-form'}).findAll("input",{'name':'csrfmiddlewaretoken'}):
	token=j['value']

login_data ={
'csrfmiddlewaretoken':token,
#'next':'/dashboard/home/',
'username': '461693106@qq.com',
'password': 'Initial0'
}
s.post(login_url,data=login_data, headers=headers)

apprank_url='https://www.appannie.com/apps/ios/top-chart/?device=iphone'
response=s.get(apprank_url,headers=headers).content
print response
    

