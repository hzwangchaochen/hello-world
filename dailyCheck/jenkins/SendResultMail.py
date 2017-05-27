# coding=utf-8
#common.py is for all scripts in dailybuild fold
import time
import os
import shutil
import glob
import smtplib
import zipfile
import bz2
import tarfile
import sys
import socket


from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

from os.path import join, getsize



def send_mail(subject, content, fro, toList):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = fro
    msg["To"] = COMMASPACE.join(toList)
    #content = MIMEText(content.encode("utf-8"), "html", "utf8")
    content = MIMEText(content, "html")
    content.set_charset("utf-8")
    msg.attach(content)
    try:
        s = smtplib.SMTP("192.168.131.88")
        s.sendmail(fro, toList, msg.as_string())
        s.quit()
    except Exception, e:
        s = smtplib.SMTP("192.168.131.88")
        s.sendmail(fro, toList, msg.as_string())
        s.quit()

def Buildtime2Time(bt):
    return int(time.mktime(time.strptime(bt, "%y-%m-%d-%H-%M")))
    
if __name__ == '__main__':
    print("into mail")
    #file_log=open('html.log','w+')
    if os.path.exists("Result.html"):
        #file_log.write('exist file')
        print("exist file")
    else:
        #file_log.write('no file')
        print("no file")
    file_object = open('Result.html')
    try:
        all_the_text = file_object.read()
    except e:
        print('read failed')
    finally:
        file_object.close()
    title = "[Automation][LX6] Resource Check Result of " + time.strftime('%y-%m-%d-%H-%M',time.localtime(time.time()))
    #MAILTOLIST          = ["hzwangchaochen@corp.netease.com"]
    MAILTOLIST          = ["hzzhujie@corp.netease.com","hzhuangyating@corp.netease.com","hzzhoufeng@corp.netease.com","wangdongjiang@corp.netease.com","qianghuang@corp.netease.com","hzhuangchaoqun1@corp.netease.com","hzwangchaochen@corp.netease.com","hzguchaoqun@corp.netease.com","hzsunww2014@corp.netease.com","lylu@corp.netease.com","bianpeng@corp.netease.com","hzzhangwt@corp.netease.com","hzluowei2014@corp.netease.com","luocheng@corp.netease.com","automation.leihuo@list.nie.netease.com"]
    send_mail(title,all_the_text, "dailybuild@qiannv.com",MAILTOLIST)

