# -*- coding: utf-8 -*-
import os
import sys
import time 
import MySQLdb
import log27

initialMin=0
res={}
timeStamp=0

path = os.path.dirname(os.path.realpath(__file__))
ResPath=path+"/../../../Client/Assets/Res/"

def initialData():
    global initialMin
    global res
    global timeStamp
    initialMin=sys.maxint
    res={'png':{'type':'pic','size':0,'num':0,'max':0,'min':initialMin},\
         'jpg':{'type':'pic','size':0,'num':0,'max':0,'min':initialMin},\
         'bmp':{'type':'pic','size':0,'num':0,'max':0,'min':initialMin},\
         'tga':{'type':'pic','size':0,'num':0,'max':0,'min':initialMin},\
         'psd':{'type':'pic','size':0,'num':0,'max':0,'min':initialMin},\
         'exr':{'type':'pic','size':0,'num':0,'max':0,'min':initialMin},\
         'hdr':{'type':'pic','size':0,'num':0,'max':0,'min':initialMin},\
         'tif':{'type':'pic','size':0,'num':0,'max':0,'min':initialMin},\
         'anim':{'type':'anim','size':0,'num':0,'max':0,'min':initialMin},\
         'controller':{'type':'anim','size':0,'num':0,'max':0,'min':initialMin},\
         'txt':{'type':'txt','size':0,'num':0,'max':0,'min':initialMin},\
         'fnt':{'type':'font','size':0,'num':0,'max':0,'min':initialMin},\
         'ttf':{'type':'font','size':0,'num':0,'max':0,'min':initialMin},\
         'otf':{'type':'font','size':0,'num':0,'max':0,'min':initialMin},\
         'meta':{'type':'meta','size':0,'num':0,'max':0,'min':initialMin},\
         'prefab':{'type':'prefab','size':0,'num':0,'max':0,'min':initialMin},\
         'fbx':{'type':'fbx','size':0,'num':0,'max':0,'min':initialMin},\
         'mat':{'type':'mat','size':0,'num':0,'max':0,'min':initialMin},\
         'unity':{'type':'scene','size':0,'num':0,'max':0,'min':initialMin},\
         'asset':{'type':'asset','size':0,'num':0,'max':0,'min':initialMin},\
         'giparams':{'type':'config','size':0,'num':0,'max':0,'min':initialMin},\
         'cubemap':{'type':'config','size':0,'num':0,'max':0,'min':initialMin},\
         'xml':{'type':'config','size':0,'num':0,'max':0,'min':initialMin}}
    currentdate=time.strftime("%Y-%m-%d", time.localtime()) 
    timeArray = time.strptime(currentdate,"%Y-%m-%d")
    timeStamp = (int(time.mktime(timeArray))+8*3600)*1000

def processFile(ResPath):
    global res
    for root,dirs,files in os.walk(ResPath):
        for filename in files:
            #print root + '\\' + filename
            suffix=os.path.splitext(filename)[1][1:]
            if suffix=='':
                continue
            suffix=suffix.lower()
            filesize=os.path.getsize(root + '/' + filename)
            try:
                res[suffix]['size']+=filesize
                res[suffix]['num']+=1
                res[suffix]['max']=max(res[suffix]['max'],filesize)
                res[suffix]['min']=min(res[suffix]['min'],filesize)
            except:
                res[suffix]={'type':'other','size':filesize,'num':1,'max':filesize,'min':filesize}
    print res

def optimizeRes():
    global res
    for k,v in res.items():
        v['size']=round(v['size']/float(1024*1024),4)
        v['max']=round(v['max']/float(1024*1024),4)
        v['min']=round(v['min']/float(1024*1024),4)

def writeToSQL():
    conn= MySQLdb.connect(
        host='192.168.131.97',
        #unix_socket='/srv/mysqls/3306/run/mysqld.sock',
        port = 3306,
        user='autoqa',
        passwd='mWXel2MH4t4U4TvFHc4xxQ==',
        charset='utf8',
        db ='leiting',
        )
    cursor = conn.cursor()
    tablename="ResourcesOutline"
    sql="delete from ResourcesOutline where TimeLine='"+str(timeStamp)+"'"
    cursor.execute(sql)
    for k,v in res.items():
        sql="insert into ResourcesOutline(FileType,ExtensionName,NumberOfFile,TotalSize,MaximalSize,MinimalSize,TimeLine) values(%s,%s,%s,%s,%s,%s,%s)"
        param=(v['type'],k,v['num'],v['size'],v['max'],v['min'],str(timeStamp))
        cursor.execute(sql,param)
    conn.commit()
    cursor.close()
    conn.close()

# def writeToFile():
#     file=open('FileStatistics.log','w')
#     for k,v in res.items():
#         file.write(k+"|"+v['type']+"|"+str(v['num'])+"|"+str(v['size'])+"|"+str(v['max'])+"|"+str(v['min'])+"\r\n")
#     file.close()

if __name__ == '__main__':

    log27.LOG_START("ResourcesOutlineCheck","ResourcesOutlineCheck")
    initialData()
    #ResPath=r"D:\2.SVN\LX6\Client\Assets\Res"
    processFile(ResPath)
    optimizeRes()
    writeToSQL()
    log27.LOG_END("ResourcesOutlineCheck","ResourcesOutlineCheck")
    