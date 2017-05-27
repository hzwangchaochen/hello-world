# coding:utf-8
import os
import json
from json import *
import MySQLdb
import MySQLdb.cursors
import xlrd,xlwt
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import StreamingHttpResponse
import re
import sys
import datetime
from models import SceneModel
from django.contrib.auth.decorators import login_required
from Webtool import settings
import time 
import shutil
reload(sys)  
sys.setdefaultencoding('utf8')

password='leiting_qa_163'
# Create your views here.
@login_required
def index(request):
    return render_to_response('analysis_performance/index.html',{'uniqueKey':int(datetime.datetime.now().strftime("%Y%m%d%H")),'currentuser':request.user.username})

def sceneResult(request,tablename):
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    #场景图片
    picpath=''
    scene_name=''
    sqlstr="select scene_pic from analysis_performance_scenemodel where project_name='"+tablename.split('_')[0]+"' and scene_name='"+tablename.split('_')[2]+"'"
    cursor.execute(sqlstr)
    picpath=cursor.fetchall()[0][0]
    cursor.close()
    conn.close()
    return render_to_response('analysis_performance/scene.html',{'picpath':picpath})

#用于前端测试用例集目录结构的自动生成（每个测试用例集leihuo和MTL成对出现）
def findAllSqlName(request,projectname):
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor=conn.cursor()
    cursor.execute('SHOW TABLES')
    allSQLname=cursor.fetchall()
    alltext=[]
    allchildren={}
    res=[]

    for name in allSQLname:
        if ('AP_' in name[0]) and ('RD' in name[0]) and (projectname in name[0]):
            if(len(name[0].split('_'))==5):
                if name[0].split('_')[2] in alltext:
                    allchildren[name[0].split('_')[2]].append(name[0][3:-3])
                else:
                    allchildren[name[0].split('_')[2]]=[]
                    allchildren[name[0].split('_')[2]].append(name[0][3:-3])
                    alltext.append(name[0].split('_')[2])

    for i in alltext:
        children=[]
        for j in allchildren[i]:
            children.append({'text':j})
        res.append({'text':i,'children':children})

    cursor.close()
    conn.close()
    return HttpResponse(JSONEncoder().encode(res))

def getDataFromMysql(request):
    res={}
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    if request.POST.has_key('rows'):
        rows=int(request.POST.get('rows',""))
        page=int(request.POST.get('page',""))
    else:
        page=1
        rows=50
    offset = (page-1)*rows

    SheetType=''
    SheetName=''
    table=''
    sort ='id'
    order='asc'
    if(request.POST.has_key('SheetType')):
        SheetType=request.POST.get('SheetType',"")
    else:
        return HttpResponse('')

    if(request.POST.has_key('SheetName')):
        SheetName = request.POST.get('SheetName',"")
    else:
        return HttpResponse('')
    if(request.POST.has_key('sort')):
        sort = request.POST.get('sort',"")
    if(request.POST.has_key('order')):
        order = request.POST.get('order',"")

    table="AP_"+str(SheetName)+"_"+str(SheetType)
    sqlcountstr="select count(*) from "+table
    sqlstr="select * from "+table
    cursor.execute(sqlcountstr)
    total=cursor.fetchall()[0][u'count(*)']  
    cursor.execute(sqlstr+" order by "+sort+" "+order+" limit "+str(offset)+","+str(rows))
    data=cursor.fetchall()
    res['total']=total
    res['rows']=data   
    jsonRes=JSONEncoder().encode(res)

    cursor.close()
    conn.close()
    return HttpResponse(jsonRes)

def deleteEntry(request,entryname): 
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    projectname=entryname.split("_")[0]
    scenename=entryname.split("_")[2]

    tableFPS="AP_"+entryname+"_FPS"
    tableRD="AP_"+entryname+"_RD"
    tableMEM="AP_"+entryname+"_MEM"
    tableRMEM="AP_"+entryname+"_RMEM"

    cursor.execute("drop table if exists "+tableFPS)
    cursor.execute("drop table if exists "+tableRD)
    cursor.execute("drop table if exists "+tableMEM)
    cursor.execute("drop table if exists "+tableRMEM)
    conn.commit()

    sqlStr="select scene_pic from analysis_performance_scenemodel where project_name='"+projectname+"' and scene_name='"+scenename+"'"
    cursor.execute(sqlStr)
    for row in cursor:
        picpath=row[0]
        file_directory = os.path.join(settings.MEDIA_ROOT,picpath)
        if os.path.isfile(file_directory):
            os.remove(file_directory)

    sqlStr="delete from analysis_performance_scenemodel where project_name='"+projectname+"' and scene_name='"+scenename+"'"
    cursor.execute(sqlStr)

    sqlStr="delete from AP_PhoneInfo where TableName='"+entryname+"'"
    cursor.execute(sqlStr)

    conn.commit()
    cursor.close()
    conn.close()
    return HttpResponse('')

def uploadLog(request):
    return render_to_response('analysis_performance/uploadLog.html')

def getFileContent(request):  
    if request.method == 'POST':
        fpsdata=request.FILES['fpsfile']
        renderdata=request.FILES['renderfile']
        memorydata=request.FILES['memoryfile']
        scenename=request.POST['scenename']
        projectName=request.POST['projectname']
        svnNum=request.POST['svnnum']
        
        new_scene = SceneModel(
            scene_pic=request.FILES.get('scenepic'),
            project_name=request.POST['projectname'],
            scene_name=request.POST['scenename'],
            scene_des=request.POST['scenedes']
        )
        new_scene.save()

        phoneType=request.POST['phonetype']
        resLength=request.POST['reslength']
        resWidth=request.POST['reswidth']

    else:
        return HttpResponse('')

    #1 将log文件存储到服务器
    timeAll=[]
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
    
    logpath='analysis_performance_log/'+projectName+'/'+svnNum+'/'+scenename
    file_directory = os.path.join(settings.MEDIA_ROOT,logpath).encode('utf-8')
    isExists=os.path.exists(file_directory)
    if not isExists:
        os.makedirs(file_directory)
    else:
        shutil.rmtree(file_directory)
        os.makedirs(file_directory)

    data=[fpsdata.read(),renderdata.read(),memorydata.read()]
    files=['fps.log','rendering.log','memory.log']
    for i in range(0,3):
        f_write=open(file_directory+'/'+files[i],'w')
        f_write.write(data[i])
        f_write.close()

    fpsdata=open(file_directory+'/'+files[0])
    renderdata=open(file_directory+'/'+files[1])
    memorydata=open(file_directory+'/'+files[2])

    #2 
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()

    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))

    tableFPS="AP_"+projectName+"_"+svnNum+"_"+scenename+"_FPS"
    tableRD="AP_"+projectName+"_"+svnNum+"_"+scenename+"_RD"
    tableMEM="AP_"+projectName+"_"+svnNum+"_"+scenename+"_MEM"
    tableRMEM="AP_"+projectName+"_"+svnNum+"_"+scenename+"_RMEM"

    cursor.execute("drop table if exists "+tableFPS)
    cursor.execute("drop table if exists "+tableRD)
    cursor.execute("drop table if exists "+tableMEM)
    cursor.execute("drop table if exists "+tableRMEM)

    cursor.execute("create table if not exists "+tableFPS+"  like AP_FPSTemplate")
    cursor.execute("create table if not exists "+tableRD+"  like AP_RDTemplate")
    cursor.execute("create table if not exists "+tableMEM+"  like AP_MEMTemplate")
    cursor.execute("create table if not exists "+tableRMEM+"  like AP_RMEMTemplate")
    conn.commit()

    #3 deal with rendering.log
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
    lines=renderdata.readlines()
    n=len(lines)

    #需要检查一下正确性+++++++++++++++++++++++++++++++++++++++++++++++++
    interval=12
    if(projectName=='LX6'):
        interval=12
    else:
        interval=13
    for line in range(0,n,interval):
        temp=lines[line].split('\t')
        sql="insert into "+tableRD+"(frameIndex,drawCalls,triangles) values(%s,%s,%s)"
        param = (temp[0].split('|')[0],temp[1].split(':')[1],calRD(temp[4].split(':')[1]))
        cursor.execute(sql,param)
    conn.commit()

    #4 deal with fps.log
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
    lines=fpsdata.readlines()
    n=len(lines)
    for line in range(0,n):
        temp=lines[line].split('|')
        sql="insert into "+tableFPS+"(frameIndex,FPS) values(%s,%s)"
        param = (temp[0],float(temp[1]))
        cursor.execute(sql,param)
    conn.commit()

    #5 deal with memory.log
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
    lines=memorydata.readlines()
    n=len(lines)
    
    #memory.log里面多一行WP8开头的
    interval=14
    if(projectName=='L10' or projectName=='L13' or projectName=='LH01'):
        interval=15
    else:
        interval=14
    for line in range(0,n,interval):
        temp0=lines[line].split('   ')
        temp1=lines[line+1].split('   ')
        sql="insert into "+tableMEM+"(frameIndex,UsedTotal,UsedUnity,UsedMono,ReservedTotal,ReservedUnity,ReservedMono,ReservedGFX) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        param = (int(temp0[0].split('|')[0]),float(temp0[0].split(':')[1].split(' ')[1]),float(temp0[1].split(':')[1].split(' ')[1]),float(temp0[2].split(':')[1].split(' ')[1]),\
                 float(temp1[0].split(':')[1].split(' ')[1]),float(temp1[1].split(':')[1].split(' ')[1]),float(temp1[2].split(':')[1].split(' ')[1]),float(temp1[3].split(':')[1].split(' ')[1]))
        cursor.execute(sql,param)

        sql="insert into "+tableRMEM+"(frameIndex,TextureNum,TextureMem,MeshNum,MeshMem,MaterialNum,MaterialMem,AnimClipNum,AnimClipMem,AudioClipNum,AudioClipMem) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        if interval==14:
            param = (int(temp0[0].split('|')[0]),\
                     int(lines[line+4].split('/')[0].split(':')[1]),calMem(lines[line+4].split('/')[1]),int(lines[line+5].split('/')[0].split(':')[1]),calMem(lines[line+5].split('/')[1]),\
                     int(lines[line+6].split('/')[0].split(':')[1]),calMem(lines[line+6].split('/')[1]),int(lines[line+7].split('/')[0].split(':')[1]),calMem(lines[line+7].split('/')[1]),\
                     int(lines[line+8].split('/')[0].split(':')[1]),calMem(lines[line+8].split('/')[1])
                    )
        else:                                   
            param = (int(temp0[0].split('|')[0]),\
                     int(lines[line+5].split('/')[0].split(':')[1]),calMem(lines[line+5].split('/')[1]),int(lines[line+6].split('/')[0].split(':')[1]),calMem(lines[line+6].split('/')[1]),\
                     int(lines[line+7].split('/')[0].split(':')[1]),calMem(lines[line+7].split('/')[1]),int(lines[line+8].split('/')[0].split(':')[1]),calMem(lines[line+8].split('/')[1]),\
                     int(lines[line+9].split('/')[0].split(':')[1]),calMem(lines[line+9].split('/')[1])
                    )
        cursor.execute(sql,param)
    conn.commit()
    
    #6 phoneInfo
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))

    tablename=projectName+"_"+svnNum+"_"+scenename
    sql="insert into AP_PhoneInfo(TableName,PhoneType,ResLength,ResWidth,Resolution) values(%s,%s,%s,%s,%s)"
    param=(tablename,phoneType,int(resLength),int(resWidth),int(resLength)*int(resWidth))

    cursor.execute(sql,param)
    conn.commit()
    cursor.close()
    conn.close()
    #7
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
    return render_to_response('analysis_performance/temp.html',{"timeAll":timeAll})


#绘图功能
def drawResult(request,tablename):
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    FPSname="AP_"+str(tablename)+"_FPS"
    RDname="AP_"+str(tablename)+"_RD"
    MEMname="AP_"+str(tablename)+"_MEM"
    RMEMname="AP_"+str(tablename)+"_RMEM"

    #FPS
    FPSRes={'FPSList':[],'maxFPS':0.0,'minFPS':0.0,'avgFPS':0.0}
    sumFPS=0.0
    sqlstr="select FPS from "+FPSname
    cursor.execute(sqlstr)
    for row in cursor:
        FPSRes['FPSList'].append(row[0])
        sumFPS+=row[0]
    FPSRes['maxFPS']=max(FPSRes['FPSList'])
    FPSRes['minFPS']=min(FPSRes['FPSList'])
    FPSRes['avgFPS']=round(sumFPS/len(FPSRes['FPSList']),1)

    #Draw Calls
    DCRes={'DCList':[],'maxDC':0.0,'minDC':0.0,'avgDC':0.0}
    sumDC=0.0
    sqlstr="select drawCalls from "+RDname
    cursor.execute(sqlstr)
    for row in cursor:
        DCRes['DCList'].append(float(row[0]))
        sumDC+=float(row[0])
    DCRes['maxDC']=max(DCRes['DCList'])
    DCRes['minDC']=min(DCRes['DCList'])
    DCRes['avgDC']=round(sumDC/len(DCRes['DCList']),1)

    #Triangles
    TRIRes={'TRIList':[],'maxTRI':"",'minTRI':"",'avgTRI':0.0}
    sumTRI=0.0
    sqlstr="select triangles from "+RDname
    cursor.execute(sqlstr)
    for row in cursor:
        TRIRes['TRIList'].append(float(row[0]))
        sumTRI+=float(row[0])
    TRIRes['maxTRI']=str(max(TRIRes['TRIList'])/1000)+"k"
    TRIRes['minTRI']=str(min(TRIRes['TRIList'])/1000)+"k"
    TRIRes['avgTRI']=str(round(sumTRI/len(TRIRes['TRIList']),1)/1000)+"k"

    #场景图片
    picpath=''
    scene_name=''
    sqlstr="select scene_name,scene_des,scene_pic from analysis_performance_scenemodel where project_name='"+tablename.split('_')[0]+"' and scene_name='"+tablename.split('_')[2]+"'"
    cursor.execute(sqlstr)
    sceneRes=cursor.fetchall()[0]
    scenename=sceneRes[0]
    scenedes=sceneRes[1]
    picpath=sceneRes[2]

    #Memory
    MEMRes={'frameIndex':[],'UsedTotal':[],'UsedUnity':[],'ReservedTotal':[],'ReservedUnity':[],'ReservedGFX':[]}
    MonoRes={'ReservedMono':[],'UsedMono':[]}
    Sumres={'SumUsedTotal':0.0,'SumUsedUnity':0.0,'SumUsedMono':0.0,'SumReservedTotal':0.0,'SumReservedUnity':0.0,'SumReservedMono':0.0,'SumReservedGFX':0.0}
    sqlstr="select * from "+MEMname
    cursor.execute(sqlstr)
    for sub in cursor:
        #Memory Result
        MEMRes['frameIndex'].append(int(sub[1]))
        MEMRes['UsedTotal'].append(sub[2])
        MEMRes['UsedUnity'].append(sub[3])
        MEMRes['ReservedTotal'].append(sub[5])
        MEMRes['ReservedUnity'].append(sub[6]) 
        MEMRes['ReservedGFX'].append(sub[8])

        Sumres['SumUsedTotal']+=float(sub[2])
        Sumres['SumUsedUnity']+=float(sub[3])
        Sumres['SumReservedTotal']+=float(sub[5])
        Sumres['SumReservedUnity']+=float(sub[6])
        Sumres['SumReservedGFX']+=float(sub[8])

        #Mono Memory Result
        MonoRes['UsedMono'].append(sub[4])
        MonoRes['ReservedMono'].append(sub[7])
        Sumres['SumUsedMono']+=float(sub[4])
        Sumres['SumReservedMono']+=float(sub[7])

    UsedTotalRes={'max':"",'min':"",'avg':0.0}
    UsedUnityRes={'max':"",'min':"",'avg':0.0}
    ReservedTotalRes={'max':"",'min':"",'avg':0.0}
    ReservedUnityRes={'max':"",'min':"",'avg':0.0}
    ReservedGFXRes={'max':"",'min':"",'avg':0.0}

    UsedMonoRes={'max':"",'min':"",'avg':0.0}
    ReservedMonoRes={'max':"",'min':"",'avg':0.0}

    UsedTotalRes['max']=max(MEMRes['UsedTotal'])
    UsedTotalRes['min']=min(MEMRes['UsedTotal'])
    UsedTotalRes['avg']=round(Sumres['SumUsedTotal']/len(MEMRes['UsedTotal']),1)

    UsedUnityRes['max']=max(MEMRes['UsedUnity'])
    UsedUnityRes['min']=min(MEMRes['UsedUnity'])
    UsedUnityRes['avg']=round(Sumres['SumUsedUnity']/len(MEMRes['UsedUnity']),1)

    ReservedTotalRes['max']=max(MEMRes['ReservedTotal'])
    ReservedTotalRes['min']=min(MEMRes['ReservedTotal'])
    ReservedTotalRes['avg']=round(Sumres['SumReservedTotal']/len(MEMRes['ReservedTotal']),1)

    ReservedUnityRes['max']=max(MEMRes['ReservedUnity'])
    ReservedUnityRes['min']=min(MEMRes['ReservedUnity'])
    ReservedUnityRes['avg']=round(Sumres['SumReservedUnity']/len(MEMRes['ReservedUnity']),1)

    ReservedGFXRes['max']=max(MEMRes['ReservedGFX'])
    ReservedGFXRes['min']=min(MEMRes['ReservedGFX'])
    ReservedGFXRes['avg']=round(Sumres['SumReservedGFX']/len(MEMRes['ReservedGFX']),1)

    UsedMonoRes['max']=max(MonoRes['UsedMono'])
    UsedMonoRes['min']=min(MonoRes['UsedMono'])
    UsedMonoRes['avg']=round(Sumres['SumUsedMono']/len(MonoRes['UsedMono']),1)

    ReservedMonoRes['max']=max(MonoRes['ReservedMono'])
    ReservedMonoRes['min']=min(MonoRes['ReservedMono'])
    ReservedMonoRes['avg']=round(Sumres['SumReservedMono']/len(MonoRes['ReservedMono']),1)

    #resource memory
    RMEMRes={'frameIndex':[],'TextureNum':[],'TextureMem':[],'MeshNum':[],'MeshMem':[],'MaterialNum':[],'MaterialMem':[],'AnimClipNum':[],'AnimClipMem':[],'AudioClipNum':[],'AudioClipMem':[]}
    sqlstr="select * from "+RMEMname
    cursor.execute(sqlstr)
    for sub in cursor:
        #Memory Result
        RMEMRes['frameIndex'].append(int(sub[1]))
        RMEMRes['TextureNum'].append(int(sub[2]))
        RMEMRes['TextureMem'].append(sub[3])
        RMEMRes['MeshNum'].append(int(sub[4]))
        RMEMRes['MeshMem'].append(sub[5]) 
        RMEMRes['MaterialNum'].append(int(sub[6]))
        RMEMRes['MaterialMem'].append(sub[7])
        RMEMRes['AnimClipNum'].append(int(sub[8])) 
        RMEMRes['AnimClipMem'].append(sub[9])
        RMEMRes['AudioClipNum'].append(int(sub[10])) 
        RMEMRes['AudioClipMem'].append(sub[11])

    #Questions
    sqlstr="select count(*) from AP_Queations where FileName='"+str(tablename)+"'"
    cursor.execute(sqlstr)
    LongfunctionPath=int(cursor.fetchall()[0][0])
    questionExists=False
    if LongfunctionPath>0:
        questionExists=True


    #分辨率和机型数据
    PhoneInfo={"PhoneType":"","ResLength":"","ResWidth":"","Resolution":65025.0}
    sqlstr="select PhoneType,ResLength,ResWidth,Resolution from AP_PhoneInfo where TableName='"+tablename+"'"
    cursor.execute(sqlstr)
    PhoneRes=cursor.fetchall()
    if len(PhoneRes)!=0:
        PhoneInfo["PhoneType"]=PhoneRes[0][0]
        PhoneInfo["ResLength"]=PhoneRes[0][1]
        PhoneInfo["ResWidth"]=PhoneRes[0][2]
        PhoneInfo["Resolution"]=float(PhoneRes[0][3])
    cursor.close()
    conn.close()
    return render_to_response('analysis_performance/drawResult.html',{'FPSRes':FPSRes,'DCRes':DCRes,'TRIRes':TRIRes,'PhoneInfo':PhoneInfo,\
                              'picpath':picpath,'scenedes':scenedes,'scenename':scenename,'LongfunctionPath':LongfunctionPath,\
                              'questionExists':questionExists,'tablename':tablename,'MEMRes':MEMRes,'MonoRes':MonoRes,'UsedTotalRes':UsedTotalRes,\
                              'UsedUnityRes':UsedUnityRes,'ReservedTotalRes':ReservedTotalRes,'ReservedUnityRes':ReservedUnityRes,\
                              'ReservedGFXRes':ReservedGFXRes,'UsedMonoRes':UsedMonoRes,'ReservedMonoRes':ReservedMonoRes,'RMEMRes':RMEMRes\
                              })

def exportToExcel(request,tablename):
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor=conn.cursor()

    tableFPS="AP_"+str(tablename)+"_FPS"
    tableRD="AP_"+str(tablename)+"_RD"

    response = HttpResponse(content_type='application/vnd.ms-excel') 
    response['Content-Disposition'] = "attachment; filename="+str(tablename)+".xls"  
    wbk = xlwt.Workbook()

    FPSSheet = wbk.add_sheet("FPS")
    FPSSheet.write(0,0,u"帧数")
    FPSSheet.write(0,1,u"FPS值")

    RDSheet = wbk.add_sheet("Rendering")
    RDSheet.write(0,0,u"帧数")
    RDSheet.write(0,1,"Draw Calls")
    RDSheet.write(0,2,"Total Batches")
    RDSheet.write(0,3,"Triangles")
    RDSheet.write(0,4,"Verticals")

    #FPS
    row_list=[]
    cursor.execute("select * from "+tableFPS)
    row_list=cursor.fetchall()
    rowlen=len(row_list)
    for i in range(rowlen):
        for j in range(1,3):
            FPSSheet.write(i+1,j-1,row_list[i][j])

    #Rendering
    row_list=[]
    cursor.execute("select * from "+tableRD)
    row_list=cursor.fetchall()
    rowlen=len(row_list)
    for i in range(rowlen):
        for j in range(1,6):
            RDSheet.write(i+1,j-1,row_list[i][j])  
    wbk.save(response) 
    cursor.close()
    conn.close()
    return response

def exportLogToTxt(request,tablename):
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor=conn.cursor()
    #Questions  
    response = HttpResponse()
    response['Content-Disposition'] = "attachment; filename="+str(tablename)+".txt"
    response.write("Scene Name|Function Length|Row Index|FunctionPath\r\n")        
    sqlstr="select * from AP_Queations where FileName='"+str(tablename)+"'"
    cursor.execute(sqlstr)
    for row in cursor:
        response.write(str(row[1])+"|"+str(row[4])+"|"+str(row[3])+"|"+str(row[2])+"\r\n")
    cursor.close()
    conn.close()
    return response

def downloadFile(request):
    the_file_name = "/home/leitingqa/project_web_lt/Webtool/templates/analysis_performance/SProfiler.cs"
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="SProfiler.cs"'
    return response
    
def file_iterator(file_name, chunk_size=512):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

def calGC(gc):
    gcList=gc.split(' ')
    if gcList[1]=='B':
        return  float(gcList[0])
    elif gcList[1]=='KB':
        return float(gcList[0])*1024
    elif gcList[1]=='MB':
        return float(gcList[0])*1024*1024

def calRD(num):
    if 'k' in num:
        return int(float(num[:-2])*1000)
    else:
        return int(num)

def calMem(mem):
    num=float(mem.split(' ')[1])
    unit=mem.split(' ')[2]
    if 'MB' in unit:
        return round(num,3)
    elif 'KB' in unit:
        return round(num/1024,3)
    elif 'GB' in unit:
        return round(num*1024,3)
    elif 'B' in unit:
        return round(num/(1024*1024),3)