#python2.7
import os
import time
import datetime
import subprocess
import re
import MySQLdb

from xml.etree import ElementTree as ET

def _get_id_and_message(text):
    if not text:
        return '',''

    id_pattern=re.compile(r'#([\d\w]+)')
    ids=re.findall(id_pattern,text)

    if ids:
        message_pattern=re.compile(r'#[\d\w]+[\s]+([\s\S]*)')
        text='#'+text[text.find(ids[-1]):].strip()
        message=re.findall(message_pattern,text)
        message=message[0].strip() if message else ''
        id=ids[0].strip()
    else:
        message=text.strip()
        id=''
    return id,message
    
    
def _get_changed_files(paths):
    changed_files = ''
    for path in paths:
        changed_files += path.get('action') + ' ' + path.text + '<br>'
    return changed_files
    
def _get_time(date):
    index = date.find('T') + 1
    try:
        hour = int(date[index:index + 2])
        hour += 8
        if hour >= 24:
            hour -= 24
        return date[:index - 1] + ' ' + str(hour) + date[index + 2:index + 8]
    except:
        print('Wrong svn date from svn log xml!')


today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
tarckerDate = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

#cmd = 'svn log .. -r "{' +  yesterday.strftime("%Y-%m-%d") + " 00:00}:{" + today.strftime("%Y-%m-%d") + ' 23:59}" -v'

#infos = []

#p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
#p.wait()
#for line in lines:


try:
    conn=MySQLdb.connect(host='192.168.131.97',user='autoqa',passwd='mWXel2MH4t4U4TvFHc4xxQ==',db='leiting',port=3306,charset='utf8')
    cur=conn.cursor()
    #cur.execute('select * from svnTracker_L13')
    #cur.close()
    #conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])




#cmd = 'svn log ../../../Client/Assets -r "{' +  yesterday.strftime("%Y-%m-%d") + " 00:00}:{" + today.strftime("%Y-%m-%d") + ' 23:59}" -v --xml > svnTracker_lx6.xml'
cmd = 'svn log ../../../Client/Assets -r "{'  + "2016-12-01 00:00}:{"  + '2016-12-31 23:59}" -v --xml > svnTracker_lx6.xml'
p = subprocess.Popen(cmd, shell=True)
p.wait()
try:
    log = ET.parse("svnTracker_lx6.xml")
except Exception, e:
    print("Parse failed! Can't find svn log or it is empty!")
    print(e.__str__())

    
logentries = log.getiterator('logentry')
for logentry in logentries:

    #print(logentry.get('revision'))
    changed_files=_get_changed_files(logentry.find('paths'))
    #if changed_files.find("StreamingAssets") != -1:
        #continue
    if logentry.find('msg') is None:
        redmine_ids,message = '',''
    else:
        redmine_ids,message=_get_id_and_message(logentry.find('msg').text)

    version=logentry.get('revision')
    #author=svn_authors.get(logentry.find('author').text, logentry.find('author').text)
    author=logentry.find('author').text
    if author.find("LeitingBuilding1") != -1:
        continue
    time=_get_time(logentry.find('date').text)
    
    

    info = {'version':version ,
            'author':author ,
            'time': time,
            'redmine_id': redmine_ids,
            'message': message,
            'changed_files':changed_files }
    #infos.append(info)
    mysqlStr = "insert ignore into svn_info_lx6 values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(info["version"],info["time"],info["author"],info["changed_files"],info["redmine_id"],info["message"],tarckerDate,'0','0','')
    res = cur.execute(mysqlStr)

conn.commit()
cur.close()
conn.close()
print("Parse Successfully!")
#return infos
    


