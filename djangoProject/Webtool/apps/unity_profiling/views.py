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
    return render_to_response('unity_profiling/index.html',{'uniqueKey':int(datetime.datetime.now().strftime("%Y%m%d%H")),'currentuser':request.user.username})

def sceneResult(request,tablename):
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    #场景图片
    picpath=''
    scene_name=''
    sqlstr="select scene_pic from unity_profiling_scenemodel where project_name='"+tablename.split('_')[0]+"' and scene_name='"+tablename.split('_')[2]+"'"
    cursor.execute(sqlstr)
    picpath=cursor.fetchall()[0][0]
    cursor.close()
    conn.close()
    return render_to_response('unity_profiling/scene.html',{'picpath':picpath})


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
        if ('UF_' in name[0]) and ('GC' in name[0]) and (projectname in name[0]):
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

    table="UF_"+str(SheetName)+"_"+str(SheetType)
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
    tableGC="UF_"+entryname+"_GC"
    tableST="UF_"+entryname+"_ST"
    tableTT="UF_"+entryname+"_TT"
    tableFPS="UF_"+entryname+"_FPS"
    tableRD="UF_"+entryname+"_RD"
    tableMEM="UF_"+entryname+"_MEM"
    tableCSV="UF_"+entryname+"_CSV"
    #半透明不透明渲染
    tableTRA="UF_"+entryname+"_TRA"

    cursor.execute("drop table if exists "+tableGC)
    cursor.execute("drop table if exists "+tableST)
    cursor.execute("drop table if exists "+tableTT)
    cursor.execute("drop table if exists "+tableFPS)
    cursor.execute("drop table if exists "+tableRD)
    cursor.execute("drop table if exists "+tableMEM)
    cursor.execute("drop table if exists "+tableTRA)
    cursor.execute("drop table if exists "+tableCSV)
    conn.commit()
    sqlStr="select scene_pic from unity_profiling_scenemodel where project_name='"+projectname+"' and scene_name='"+scenename+"'"
    cursor.execute(sqlStr)
    for row in cursor:
        picpath=row[0]
        file_directory = os.path.join(settings.MEDIA_ROOT,picpath)
        if os.path.isfile(file_directory):
            os.remove(file_directory)

    sqlStr="delete from unity_profiling_scenemodel where project_name='"+projectname+"' and scene_name='"+scenename+"'"
    cursor.execute(sqlStr)

    sqlStr="delete from UF_PhoneInfo where TableName='"+entryname+"'"
    cursor.execute(sqlStr)

    conn.commit()
    cursor.close()
    conn.close()
    return HttpResponse('')


def uploadFile(request):
    if request.method == 'POST':
        scenename=request.POST['scenename']
        projectName=request.POST['projectname']
        svnNum=request.POST['svnnum']
        phoneType=request.POST['phonetype']
        resLength=request.POST['reslength']
        resWidth=request.POST['reswidth']

    else:
        return HttpResponse('')
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    tablename=projectName+"_"+svnNum+"_"+scenename
    sql="insert into UF_PhoneInfo(TableName,PhoneType,ResLength,ResWidth,Resolution) values(%s,%s,%s,%s,%s)"
    param=(tablename,phoneType,int(resLength),int(resWidth),int(resLength)*int(resWidth))
    cursor.execute(sql,param)
    conn.commit()
    cursor.close()
    conn.close()

    return render_to_response('unity_profiling/temp.html')

def uploadFilePage(request):
    return render_to_response('unity_profiling/uploadFile.html')

def getFileContent(request):
    csvFlag=False   
    if request.method == 'POST':
        cpudata=request.FILES['cpufile']
        fpsdata=request.FILES['fpsfile']
        renderdata=request.FILES['renderfile']
        memorydata=request.FILES['memoryfile']
        if request.FILES.has_key('csvfile'):
            csvdata=request.FILES['csvfile']
            csvFlag=True

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

    timeAll=[]
    #1
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
    #将log文件存储到服务器
    logpath='log/'+projectName+'/'+svnNum+'/'+scenename
    file_directory = os.path.join(settings.MEDIA_ROOT,logpath).encode('utf-8')
    isExists=os.path.exists(file_directory)
    if not isExists:
        os.makedirs(file_directory)
    else:
        shutil.rmtree(file_directory)
        os.makedirs(file_directory)

    data=[cpudata.read(),fpsdata.read(),renderdata.read(),memorydata.read()]
    files=['cpu_stack.txt','fps.log','rendering.log','memory.log']
    for i in range(0,4):
        f_write=open(file_directory+'/'+files[i],'w')
        f_write.write(data[i])
        f_write.close()
    cpudata=open(file_directory+'/'+files[0])
    fpsdata=open(file_directory+'/'+files[1])
    renderdata=open(file_directory+'/'+files[2])
    memorydata=open(file_directory+'/'+files[3])

    #2
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    #deal with cpu_stack.log
    flag=True
    pathTable=[]
    GCTable=[]
    selfTable=[]
    totalTable=[]
    #不透明渲染
    OPATable={"frameIndex":[],"CPUTime":[]}
    #半透明渲染
    TRATable={"frameIndex":[],"CPUTime":[]}
    #UIPanel.LateUpdate
    UIPTable={"frameIndex":[],"CPUTime":[]}
    #Canvas.SendWillRenderCanvases
    CANTable={"frameIndex":[],"CPUTime":[]}
    #Animation.Update
    ANITable={"frameIndex":[],"CPUTime":[]}
    #MeshSkinning.Update
    MSKTable={"frameIndex":[],"CPUTime":[]}
    currentFrameIndex=0
    OPATable["frameIndex"].append(currentFrameIndex)
    OPATable["CPUTime"].append(0.0)
    TRATable["frameIndex"].append(currentFrameIndex)
    TRATable["CPUTime"].append(0.0)

    UIPTable["frameIndex"].append(currentFrameIndex)
    UIPTable["CPUTime"].append(0.0)
    CANTable["frameIndex"].append(currentFrameIndex)
    CANTable["CPUTime"].append(0.0)
    ANITable["frameIndex"].append(currentFrameIndex)
    ANITable["CPUTime"].append(0.0)
    MSKTable["frameIndex"].append(currentFrameIndex)
    MSKTable["CPUTime"].append(0.0)

    TRAIndex=0
    rowIndex=1
    while flag:
        line=cpudata.readline()
        if line:
            row=line.split('|')
            rowIndex+=1
            if len(row[1])>500:
                sql="insert into UF_Queations(FileName,FunctionPath,rowIndex,functionLength) values(%s,%s,%s,%s)"
                param = (projectName+"_"+svnNum+"_"+scenename,row[1],rowIndex,len(row[1]))
                cursor.execute(sql,param)
            else:
                newFrameIndex=int(row[0])
                if newFrameIndex != currentFrameIndex:
                    currentFrameIndex=newFrameIndex
                    OPATable["frameIndex"].append(currentFrameIndex)
                    OPATable["CPUTime"].append(0.0)
                    TRATable["frameIndex"].append(currentFrameIndex)
                    TRATable["CPUTime"].append(0.0)
                    UIPTable["frameIndex"].append(currentFrameIndex)
                    UIPTable["CPUTime"].append(0.0)
                    CANTable["frameIndex"].append(currentFrameIndex)
                    CANTable["CPUTime"].append(0.0)
                    ANITable["frameIndex"].append(currentFrameIndex)
                    ANITable["CPUTime"].append(0.0)
                    MSKTable["frameIndex"].append(currentFrameIndex)
                    MSKTable["CPUTime"].append(0.0)
                    TRAIndex+=1

                else:
                    if "Render.OpaqueGeometry" in row[1]:
                        OPATable["CPUTime"][TRAIndex]+=float(row[3])
                    elif "Render.TransparentGeometry" in row[1]:
                        TRATable["CPUTime"][TRAIndex]+=float(row[3])
                    elif "UIPanel.LateUpdate" in row[1]:
                        UIPTable["CPUTime"][TRAIndex]+=float(row[3])
                    elif "Canvas.SendWillRenderCanvases" in row[1]:
                        CANTable["CPUTime"][TRAIndex]+=float(row[3])
                    elif "Animation.Update" in row[1]:
                        ANITable["CPUTime"][TRAIndex]+=float(row[3])
                    elif "MeshSkinning.Update" in row[1]:
                        MSKTable["CPUTime"][TRAIndex]+=float(row[3])

                tempgc=calGC(row[2])
                if row[1] in pathTable:
                    index=pathTable.index(row[1])
                    #GCTable
                    GCTable[index]['totalGC']=GCTable[index]['totalGC']+tempgc
                    GCTable[index]['totalCalls']=GCTable[index]['totalCalls']+1
                    if tempgc>0.0:
                        GCTable[index]['totalGCCalls']=GCTable[index]['totalGCCalls']+1
                    else:
                        GCTable[index]['totalCalls']=GCTable[index]['totalCalls']+1
                    #selfTimeTable
                    selfTable[index]['totalST']=selfTable[index]['totalST']+float(row[3])
                    selfTable[index]['totalCalls']=selfTable[index]['totalCalls']+1
                    #totalTimeTable
                    totalTable[index]['totalTT']=totalTable[index]['totalTT']+float(row[4])
                    totalTable[index]['totalCalls']=totalTable[index]['totalCalls']+1
                else:
                    pathTable.append(row[1])
                    #GCTable
                    if tempgc>0.0:
                        GCTable.append({'functionPath':row[1],'totalGC':tempgc,'totalGCCalls':1,'totalCalls':1})
                    else:
                        GCTable.append({'functionPath':row[1],'totalGC':tempgc,'totalGCCalls':0,'totalCalls':1})
                    #selfTimeTable
                    selfTable.append({'functionPath':row[1],'totalST':float(row[3]),'totalCalls':1})
                    #totalTimeTable
                    totalTable.append({'functionPath':row[1],'totalTT':float(row[4]),'totalCalls':1})
        else:
            flag=False
    conn.commit()
    #3
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))

    tableGC="UF_"+projectName+"_"+svnNum+"_"+scenename+"_GC"
    tableST="UF_"+projectName+"_"+svnNum+"_"+scenename+"_ST"
    tableTT="UF_"+projectName+"_"+svnNum+"_"+scenename+"_TT"
    tableFPS="UF_"+projectName+"_"+svnNum+"_"+scenename+"_FPS"
    tableRD="UF_"+projectName+"_"+svnNum+"_"+scenename+"_RD"
    tableMEM="UF_"+projectName+"_"+svnNum+"_"+scenename+"_MEM"
    tableCSV="UF_"+projectName+"_"+svnNum+"_"+scenename+"_CSV"

    #半透明不透明渲染
    tableTRA="UF_"+projectName+"_"+svnNum+"_"+scenename+"_TRA"

    cursor.execute("drop table if exists "+tableGC)
    cursor.execute("drop table if exists "+tableST)
    cursor.execute("drop table if exists "+tableTT)
    cursor.execute("drop table if exists "+tableFPS)
    cursor.execute("drop table if exists "+tableRD)
    cursor.execute("drop table if exists "+tableMEM)
    cursor.execute("drop table if exists "+tableTRA)

    cursor.execute("create table if not exists "+tableGC+" like UF_GCTemplate")
    cursor.execute("create table if not exists "+tableST+"  like UF_STTemplate")
    cursor.execute("create table if not exists "+tableTT+"  like UF_TTTemplate")
    cursor.execute("create table if not exists "+tableFPS+"  like UF_FPSTemplate")
    cursor.execute("create table if not exists "+tableRD+"  like UF_RDTemplate")
    cursor.execute("create table if not exists "+tableMEM+"  like UF_MEMTemplate")
    cursor.execute("create table if not exists "+tableTRA+"  like UF_TRATemplate")
    

    commonfunction=['Camera.Render/Drawing/GLTextManager.OnPostRender()','ParticleSystem.EndUpdateAll/WaitingForJob','Camera.Render/WaitingForJob', 'BehaviourUpdate/CMainCamera.Update()',\
                    'Camera.Render/Flare.Render', 'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/AddActiveLocalLights',\
                    'Camera.Render/Culling/SceneCulling/CullSendEvents/Terrain.Trees.OnWillRender', 'GUI.ProcessEvents/Event.Internal_MakeMasterEventCurrent()',\
                    'GUI.Repaint/AutoQATestInfo.OnGUI()', 'Physics.Processing/PhysX.SapUpdateWorkTask', 'Destroy/UIWidget.OnDestroy()',\
                    'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Render/Shadows.RenderShadowmap/Shadows.RenderJob/Shadows.RenderJobDir/RenderTexture.SetActive',\
                    'GUI.Repaint/Event.Internal_MakeMasterEventCurrent()', 'Camera.Render/Culling/CullingGroupSendEvents','Loading.UpdatePreloading/Application.Integrate Assets in Background',\
                    'Camera.Render/WaitingForJob/Shadows.CullShadowCastersDirectional/Shadows.CullShadowCastersDirectionalDetail',\
                    'Camera.Render/Camera.FireOnPreRender()', 'GUI.Repaint/GUIUtility.BeginGUI()', 'BehaviourUpdate/UICamera.Update()/UIEventListener.OnPress()',\
                    'Physics.Processing/PhysX.Sc::Scene::ccdBroadPhase', 'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Render/Shadows.RenderShadowmap/Shadows.RenderJob',\
                    'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Render/WaitingForJob/WaitingForJob', 'WaitingForJob', 'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/Shadows.CullDirectionalShadowCasters',\
                    'GUI.ProcessEvents/GUIUtility.EndGUI()', 'Camera.Render/Culling/SceneCulling/CullSendEvents/WaitingForJob', 'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/WaitingForJob', 'Camera.Render/Culling/Recalc Bounds',\
                    'Physics.Processing/PhysX.Sc::Scene::collideStep', 'Camera.Render/Camera.GUILayer', 'GPUProfiler.EndQueries', 'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/AddDirectionalLights',\
                    'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Render/Shadows.RenderShadowmap/WaitingForJob/Shadows.PrepareJob/Shadows.ExtractCasters', 'BehaviourUpdate/UIRoot.Update()',\
                    'Camera.Render/Culling/SceneCulling/CullSendEvents/ParticleSystem.ScheduleGeometryJobs', 'CGrassChunk.OnBecameInvisible()', 'ParticleSystem.Update', 'Physics.Processing/PhysX.NpSceneCompletion',\
                    'UIPanel.LateUpdate()/GameObject.Activate', 'GUI.Repaint', 'AudioManager.FixedUpdate', 'Physics.Processing/PhysX.Sc::Scene::solveStep', 'Camera.Render/WaitingForJob/Shadows.CombineDirectionalShadowCasterCullignIndexListsAndDestroy',\
                    'BehaviourUpdate/UIProgressBar.Update()', 'Monobehaviour.OnMouse_/SendMouseEvents.DoSendMouseEvents()/Physics2D.GetRayIntersection/Physics2D.GetRayIntersectionAll/Physics2D.LinecastAll/Physics2D.OverlapPointAll',\
                    'CBoneTracer.LateUpdate()', 'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Render/Clear', 'Substance.Update', 'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Render/RenderTexture.SetActive',\
                    'Monobehaviour.OnMouse_/SendMouseEvents.DoSendMouseEvents()/Physics2D.GetRayIntersection/Physics2D.GetRayIntersectionAll/Physics2D.LinecastAll', 'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/Shadows.CullDirectionalShadowCasters/JobAlloc.Grow',\
                    'Physics.Processing/PhysX.SingleAABBTask', 'Physics2D.FixedUpdate/Physics2D.UpdateTransforms', 'MeshSkinning.Update/MeshSkinning.Prepare/JobAlloc.Grow', 'Physics.Processing/PhysX.SapPostUpdateWorkTask', 'Camera.Render/DestroyCullResults',\
                    'Physics.Processing/PhysX.Sc::Scene::updateCCDMultiPass', 'Camera.Render/Culling/SceneCulling/CullSendEvents', 'Physics.Processing/PhysX.AggregateOverlapTask', 'UIPanel.LateUpdate()/GameObject.Activate/UIDrawCall.OnEnable()',\
                    'UIPanel.LateUpdate()/GameObject.Deactivate/UIDrawCall.OnDisable()', 'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/WaitingForJob/FrustumAndOcculusionCullLocalLightsCombine',\
                    'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Render/Shadows.RenderShadowmap/WaitingForJob/Shadows.PrepareJob', 'UIDragScrollView.Start()', 'Camera.Render/Culling/CMainCamera.OnPreCull()',\
                    'Camera.Render/Drawing/Render.TransparentGeometry/RenderForwardAlpha.Sort/JobAlloc.Grow', 'BehaviourUpdate/UICamera.Update()', 'Destroy/CAnimationFast.OnDestroy()', 'UICamera.LateUpdate()',\
                    'Physics.Processing/PhysX.Sc::Scene::updateCCDSinglePass', 'Physics.Processing/PhysX.Sc::Scene::postBroadPhase', 'Destroy/GameObject.Deactivate/UIWidget.OnDisable()', 'Mesh.SubmitVBO', 'Camera.Render/Camera.ImageEffects',\
                    'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/FindLocalShadowCastingLights/FindShadowCastingLights', 'BehaviourUpdate/UICamera.Update()/UIEventListener.OnSelect()', 'Camera.Render', \
                    'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/FindLocalShadowCastingLights', 'Physics.Processing/PhysX.BPWorkTask', 'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Prepare/WaitingForJob/CullPerObjectLightsCombine', \
                    'Physics2D.FixedUpdate', 'Camera.Render/RenderTexture.SetActive', 'ParticleSystem.EndUpdateAll', 'Physics.ProcessReports', 'Physics.Processing/PhysX.Sc::Scene::collisionTask', 'Animation.Update', 'GUI.Repaint/GUIUtility.EndGUI()', \
                    'Camera.Render/Culling/SceneCulling/CullAllVisibleLights', 'BehaviourUpdate/CSlotTracer.Update()', 'BehaviourUpdate/UISpriteAnimation.Update()', 'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Render', \
                    'Physics.Processing/PhysX.Sc::Scene::postCCDPass', 'MeshSkinning.Update', 'Physics2D.FixedUpdate/Physics2D.Callbacks', 'GUI.ProcessEvents', 'Cleanup Unused Cached Data', 'BehaviourUpdate/CGrassFast.Update()', \
                    'Camera.Render/Culling/SceneCulling/CullSendEvents/UIDrawCall.OnWillRenderObject()', 'ReflectionProbes.Update', 'Graphics.PresentAndSync', 'Camera.Render/Culling/SceneCulling/CullSendEvents/WaitingForJob/CullSceneDynamicObjectsCombineJob', \
                    'Physics.ExecuteDeferredTriggerErase', 'Physics.Processing/PhysX.AggregateAABBTask', 'Camera.Render/Drawing/Render.OpaqueGeometry/Shadows.PrepareShadowmap/Shadows.GenerateRenderNodeQueue', \
                    'Camera.Render/Drawing/Render.OpaqueGeometry/Shadows.PrepareShadowmap/Terrain.Trees.OnWillRender', 'BehaviourUpdate/FMOD_StudioSystem.Update()', 'UITable.Start()', 'Camera.Render/Drawing', \
                    'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/WaitingForJob/FrustumAndOcculusionCullLocalLights/OcclusionAndConnectivityCullLight', 'Physics.Processing/PhysX.PxsContext::mergeCMDiscreteUpdateResults', 'Camera.Render/Culling/SceneCulling', \
                    'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/FindDirectionalShadowCastingLights', 'BehaviourUpdate/UICamera.Update()/UIEventListener.OnClick()', 'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/FindActiveLights', \
                    'BehaviourUpdate/EasyTouch.Update()', 'Physics2D.FixedUpdate/Physics2D.Callbacks/Physics2D.ContactReporting', 'Loading.UpdatePreloading', 'BehaviourUpdate/CRenderScene.Update()', 'UIPanel.LateUpdate()/Font.CacheFontForText', 'MeshSkinning.Update/MeshSkinning.Prepare', \
                    'Camera.Render/Culling/PrepareSceneCullingParameters/LOD.ComputeLOD', 'Physics2D.FixedUpdate/Physics2D.EffectorFixedUpdate', 'Camera.Render/Culling/PrepareSceneCullingParameters', 'UIPanel.LateUpdate()', 'Physics2D.FixedUpdate/Physics2D.JointBreakLimits', \
                    'UIRect.Start()/Font.CacheFontForText', 'Monobehaviour.OnMouse_', 'Camera.Render/CMainCamera.OnPreRender()', 'Physics2D.DynamicUpdate', 'CAnimationFast.LateUpdate()', 'Camera.Render/Culling/SceneCulling/CullSendEvents/WaitingForJob/CullSceneDynamicObjectsCombineJob/CombineJobResults', \
                    'Camera.Render/Culling/SceneCulling/CullSendEvents/WaitingForJob/CullSceneDynamicObjects/CullObjectsWithoutUmbra', 'Monobehaviour.OnMouse_/SendMouseEvents.DoSendMouseEvents()', 'Camera.Render/Culling/SceneCulling/CullSendEvents/WaitingForJob/SceneNodesInitJob',\
                    'BehaviourUpdate/CDecalEffect.Update()','Physics.ProcessReports/Physics.TriggerEnterExits', 'DOTweenComponent.LateUpdate()', 'Camera.Render/Culling/SceneCulling/CullPerObjectLights/ComputeNeedsPerObjectLights',\
                    'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Render/Shadows.RenderShadowmap/Shadows.RenderJob/Shadows.RenderJobDir','UIScrollView.LateUpdate()', 'Monobehaviour.OnMouse_/SendMouseEvents.DoSendMouseEvents()/Physics.Raycast',\
                    'Camera.Render/Drawing/Render.TransparentGeometry/RenderForwardAlpha.Render', 'Camera.Render/Drawing/Camera.RenderSkybox', 'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Sort/JobAlloc.Grow', \
                    'Physics.FetchResults', 'Physics.Processing/PhysX.Sc::Scene::rigidBodySolver', 'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/WaitingForJob/FrustumAndOcculusionCullLocalLights',\
                    'Camera.Render/Culling/Camera.FireOnPreCull()', 'BehaviourUpdate/UITweener.Update()', 'Camera.Render/Culling/SceneCulling/PrepareSceneNodes', 'Physics.Interpolation', 'Physics2D.FixedUpdate/Physics2D.Simulate', 'Physics2D.DynamicUpdate/Physics2D.MovementState', 'Destroy', \
                    'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Render/Shadows.RenderShadowmap/WaitingForJob', 'Destroy/CSkinFast.OnDestroy()', 'BehaviourUpdate/UIRect.Update()', 'BehaviourUpdate', \
                    'Camera.Render/WaitingForJob/Shadows.CullShadowCastersDirectional/Shadows.CullShadowCastersWithoutUmbra', 'Physics.Processing/PhysX.Sc::Scene::clothPreprocessing', 'Camera.Render/WaitingForJob/WaitForJobSet', 'Physics.Processing/PhysX.Sc::Scene::postIslandGen', 'BehaviourUpdate/GLTextManager.Update()', \
                    'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Render/Shadows.RenderShadowmap', 'Camera.Render/WaitingForJob/Shadows.CombineDirectionalShadowCasterCullignIndexListsAndDestroy/CombineJobResults', \
                    'Profiler.FinalizeAndSendFrame', 'Camera.Render/Culling/PrepareSceneCullingParameters/LOD.ComputeLOD/LOD.ComputeLOD', 'BehaviourUpdate/FMOD_Listener.Update()', 'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Render/WaitingForJob', \
                    'Camera.Render/Drawing/Render.Prepare', 'Physics.Processing/PhysX.PxsContext::prepareCMDiscreteUpdateResults', 'Physics.Simulate','Physics.Processing/PhysX.Sc::Scene::islandGen', 'Physics.Processing/PhysX.ProcessBPResultsTask', \
                    'BehaviourUpdate/AutoQATestInfo.Update()', 'Camera.Render/Culling/ScheduleCullingGroups', 'Rendering.UpdateDirtyRenderers', 'Camera.Render/Drawing/Camera.FireOnPostRender()', \
                    'Camera.Render/Culling/SceneCulling/CullPerObjectLights', 'DOTweenComponent.FixedUpdate()', 'Camera.Render/Drawing/Camera.RenderSkybox/FindBrightestDirectionalLight', 'BehaviourUpdate/UIInput.Update()', \
                    'Camera.Render/Drawing/Render.TransparentGeometry/RenderForwardAlpha.Prepare', 'Physics.Processing', 'UIRect.Start()', 'Monobehaviour.OnMouse_/SendMouseEvents.DoSendMouseEvents()/Physics2D.GetRayIntersection/Physics2D.GetRayIntersectionAll', \
                    'Monobehaviour.OnMouse_/SendMouseEvents.DoSendMouseEvents()/Physics2D.GetRayIntersection', 'Material.SetPassFast', 'Camera.Render/Drawing/Render.OpaqueGeometry', \
                    'AudioManager.Update', 'Physics.UpdateCloth', 'BehaviourUpdate/CDecal.Update()', 'ParticleSystem.EndUpdateAll/WaitingForJob/ParticleSystem.UpdateJob', 'Camera.Render/Drawing/Render.OpaqueGeometry/Shadows.PrepareShadowmap/JobAlloc.Grow', \
                    'Canvas.SendWillRenderCanvases()', 'Camera.Render/WaitingForJob/Shadows.CullShadowCastersDirectional', 'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/FindDirectionalShadowCastingLights/FindShadowCastingLights', \
                    'GUI.ProcessEvents/GUIUtility.BeginGUI()', 'Physics.Processing/PhysX.Sc::Scene::rigidBodyNarrowPhase', 'BehaviourUpdate/DOTweenComponent.Update()', 'Destroy/GameObject.Deactivate', 'Physics.Processing/PhysX.ActorAABBTask', \
                    'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Prepare', 'Loading.UpdateWebStream', 'Camera.Render/Culling/SceneCulling/CullSendEvents/WaitingForJob/PrepareSceneNodesJob', 'Physics2D.FixedUpdate/Physics2D.MovementState', \
                    'Camera.Render/Drawing/Camera.ImageEffects', 'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Prepare/WaitingForJob', 'Camera.Render/Culling/SceneCulling/JobAlloc.Grow', \
                    'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Prepare/WaitingForJob/CullPerObjectLights', 'Camera.Render/Drawing/CMainCamera.OnPostRender()', 'Graphics.PresentAndSync/Device.Present', \
                    'Physics2D.FixedUpdate/Physics2D.Callbacks/Physics2D.Simulate', 'Overhead', 'Camera.Render/Drawing/Render.OpaqueGeometry/Shadows.PrepareShadowmap', 'Physics.Processing/PhysX.Sc::Scene::postSolver', 'Animation.Update/Animation.Sample', \
                    'Destroy/AttributeHelperEngine.GetRequiredComponents()', 'Physics.Processing/PhysX.Sc::Scene::postNarrowPhase', 'NavMeshManager', 'RenderTexture.SetActive', 'Camera.Render/Culling/SceneCulling/PrepareSceneNodes/JobAlloc.Grow', \
                    'BehaviourUpdate/CWater.Update()', 'ParticleSystem.EndUpdateAll/ParticleSystem.Update2', 'BehaviourUpdate/UITweener.Update()/UITweener.OnDisable()', 'Physics.UpdateBodies', 'Physics.Processing/PhysX.Sc::Scene::finalizationPhase', \
                    'Camera.Render/Culling/SceneCulling/CullSendEvents/WaitingForJob/WaitForJobSet', 'Camera.Render/Drawing/Render.OpaqueGeometry/Shadows.PrepareShadowmap/WaitingForJob', 'Physics.ProcessReports/Physics.Contacts', \
                    'Physics.Processing/PhysX.Completion Task', 'Camera.Render/Culling/SceneCulling/CullAllVisibleLights/WaitingForJob/FrustumAndOcculusionCullLocalLights/CullLightFrustumLocal', 'Physics.Processing/PhysX.NpSceneExecution', \
                    'Camera.Render/Culling/SceneCulling/CullPerObjectLights/JobAlloc.Grow', 'Camera.Render/Culling', 'Camera.Render/Drawing/Render.TransparentGeometry/RenderForwardAlpha.Sort', 'Network.Update', 'ProcessRemoteInput', \
                    'Animation.Update/Animation.Sample/ValidateBoundCurves', 'Camera.Render/Drawing/Render.OpaqueGeometry/RenderForwardOpaque.Sort', 'Physics.ProcessReports/Physics.JointBreaks', 'UIPanel.LateUpdate()/GameObject.Deactivate', \
                    'Camera.Render/Drawing/Render.TransparentGeometry/RenderForwardAlpha.Render/WaitingForJob', 'Camera.Render/Culling/SceneCulling/CullSendEvents/WaitingForJob/CullSceneDynamicObjects']
    functionDict={}
    for rownum in range(0,len(GCTable)):
        if(re.match(r'.*Render',GCTable[rownum]['functionPath'],2)!=None):
            functionDict[GCTable[rownum]['functionPath']]='Rendering'
        elif(re.match(r'.*ParticleSystem',GCTable[rownum]['functionPath'],2)!=None):
            functionDict[GCTable[rownum]['functionPath']]='ParticleSystem'
        elif(re.match(r'.*Animation',GCTable[rownum]['functionPath'],2)!=None):
            functionDict[GCTable[rownum]['functionPath']]='Animation'
        elif(re.match(r'.*Physics',GCTable[rownum]['functionPath'],2)!=None):
            functionDict[GCTable[rownum]['functionPath']]='Physics'
        elif(re.match(r'.*Audio',GCTable[rownum]['functionPath'],2)!=None):
            functionDict[GCTable[rownum]['functionPath']]='Audio'
        elif(re.match(r'.*Load',GCTable[rownum]['functionPath'],2)!=None):
            functionDict[GCTable[rownum]['functionPath']]='Loading'
        elif(re.match(r'.*UI',GCTable[rownum]['functionPath'])!=None):
            functionDict[GCTable[rownum]['functionPath']]='UI'
        elif(GCTable[rownum]['functionPath'] in commonfunction):
            functionDict[GCTable[rownum]['functionPath']]='OtherUnity3DFunction'
        else:
            functionDict[GCTable[rownum]['functionPath']]=projectName+"Function"

    for rownum in range(0,len(GCTable)):
        sql="insert into "+tableGC+"(functionPath,modules,totalGC,totalGCCalls,totalCalls,averageGC) values(%s,%s,%s,%s,%s,%s)"
        if GCTable[rownum]['totalGCCalls']==0:
            param = (GCTable[rownum]['functionPath'],functionDict[GCTable[rownum]['functionPath']],GCTable[rownum]['totalGC'],GCTable[rownum]['totalGCCalls'],GCTable[rownum]['totalCalls'],0.0)
        else:
            param = (GCTable[rownum]['functionPath'],functionDict[GCTable[rownum]['functionPath']],GCTable[rownum]['totalGC'],GCTable[rownum]['totalGCCalls'],GCTable[rownum]['totalCalls'],GCTable[rownum]['totalGC']/GCTable[rownum]['totalGCCalls'])
        cursor.execute(sql,param)

    for rownum in range(0,len(selfTable)):
        sql="insert into "+tableST+"(functionPath,modules,totalST,totalCalls,averageST) values(%s,%s,%s,%s,%s)"
        param = (selfTable[rownum]['functionPath'],functionDict[selfTable[rownum]['functionPath']],selfTable[rownum]['totalST'],selfTable[rownum]['totalCalls'],selfTable[rownum]['totalST']/selfTable[rownum]['totalCalls'])

        cursor.execute(sql,param)

    for rownum in range(0,len(totalTable)):
        sql="insert into "+tableTT+"(functionPath,modules,totalTT,totalCalls,averageTT) values(%s,%s,%s,%s,%s)"
        param = (totalTable[rownum]['functionPath'],functionDict[totalTable[rownum]['functionPath']],totalTable[rownum]['totalTT'],totalTable[rownum]['totalCalls'],totalTable[rownum]['totalTT']/totalTable[rownum]['totalCalls'])
        cursor.execute(sql,param)
    conn.commit()
    #deal with rendering.log
    #4
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
    lines=renderdata.readlines()
    n=len(lines)
    if(projectName=='LX6'):
        for line in range(0,n,12):
            temp=lines[line].split('\t')
            sql="insert into "+tableRD+"(frameIndex,drawCalls,totalBatches,Tris,Verts) values(%s,%s,%s,%s,%s)"
            param = (temp[0].split('|')[0],temp[1].split(':')[1],temp[3].split(':')[1],calRD(temp[4].split(':')[1]),calRD(temp[5].split(':')[1]))
            cursor.execute(sql,param)
    else:
        for line in range(0,n,13):
            temp=lines[line].split('\t')
            sql="insert into "+tableRD+"(frameIndex,drawCalls,totalBatches,Tris,Verts) values(%s,%s,%s,%s,%s)"
            param = (temp[0].split('|')[0],temp[1].split(':')[1],temp[3].split(':')[1],calRD(temp[4].split(':')[1]),calRD(temp[5].split(':')[1]))
            cursor.execute(sql,param)
    conn.commit()
    #deal with fps.log
    #5
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
    lines=fpsdata.readlines()
    n=len(lines)
    for line in range(0,n):
        temp=lines[line].split('|')
        sql="insert into "+tableFPS+"(frameIndex,FPS) values(%s,%s)"
        param = (temp[0],float(temp[1]))
        cursor.execute(sql,param)
    conn.commit()
    #deal with memory.log
    #6
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
    lines=memorydata.readlines()
    n=len(lines)
    
    #memory.log里面多一行WP8开头的
    if(projectName=='L10' or projectName=='L13' or projectName=='LH01'):
        for line in range(0,n,15):
            temp0=lines[line].split('   ')
            temp1=lines[line+1].split('   ')
            sql="insert into "+tableMEM+"(frameIndex,UsedTotal,UsedUnity,UsedGFX,ReservedTotal,ReservedUnity,ReservedGFX) values(%s,%s,%s,%s,%s,%s,%s)"
            param = (int(temp0[0].split('|')[0]),float(temp0[0].split(':')[1].split(' ')[1]),float(temp0[1].split(':')[1].split(' ')[1]),float(temp0[3].split(':')[1].split(' ')[1]),float(temp1[0].split(':')[1].split(' ')[1]),float(temp1[1].split(':')[1].split(' ')[1]),float(temp1[3].split(':')[1].split(' ')[1]))
            cursor.execute(sql,param)
    #memory.log里面没有多一行WP8开头的
    else:
        for line in range(0,n,14):
            temp0=lines[line].split('   ')
            temp1=lines[line+1].split('   ')
            sql="insert into "+tableMEM+"(frameIndex,UsedTotal,UsedUnity,UsedGFX,ReservedTotal,ReservedUnity,ReservedGFX) values(%s,%s,%s,%s,%s,%s,%s)"
            param = (int(temp0[0].split('|')[0]),float(temp0[0].split(':')[1].split(' ')[1]),float(temp0[1].split(':')[1].split(' ')[1]),float(temp0[3].split(':')[1].split(' ')[1]),float(temp1[0].split(':')[1].split(' ')[1]),float(temp1[1].split(':')[1].split(' ')[1]),float(temp1[3].split(':')[1].split(' ')[1]))
            cursor.execute(sql,param)
    conn.commit()
    #函数耗时统计
    #7
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
    for rownum in range(0,len(OPATable["frameIndex"])):
        sql="insert into "+tableTRA+"(frameIndex,functionName,CPUTime) values(%s,%s,%s)"
        param =(OPATable["frameIndex"][rownum],u"Render.OpaqueGeometry",round(OPATable["CPUTime"][rownum],2))
        cursor.execute(sql,param)

        sql="insert into "+tableTRA+"(frameIndex,functionName,CPUTime) values(%s,%s,%s)"
        param =(TRATable["frameIndex"][rownum],u"Render.TransparentGeometry",round(TRATable["CPUTime"][rownum],2))
        cursor.execute(sql,param)

        sql="insert into "+tableTRA+"(frameIndex,functionName,CPUTime) values(%s,%s,%s)"
        param =(UIPTable["frameIndex"][rownum],u"UIPanel.LateUpdate",round(UIPTable["CPUTime"][rownum],2))
        cursor.execute(sql,param)

        sql="insert into "+tableTRA+"(frameIndex,functionName,CPUTime) values(%s,%s,%s)"
        param =(CANTable["frameIndex"][rownum],u"Canvas.SendWillRenderCanvases",round(CANTable["CPUTime"][rownum],2))
        cursor.execute(sql,param)

        sql="insert into "+tableTRA+"(frameIndex,functionName,CPUTime) values(%s,%s,%s)"
        param =(ANITable["frameIndex"][rownum],u"Animation.Update",round(ANITable["CPUTime"][rownum],2))
        cursor.execute(sql,param)

        sql="insert into "+tableTRA+"(frameIndex,functionName,CPUTime) values(%s,%s,%s)"
        param =(MSKTable["frameIndex"][rownum],u"MeshSkinning.Update",round(MSKTable["CPUTime"][rownum],2))
        cursor.execute(sql,param)
    conn.commit()
    if csvFlag:
        cursor.execute("drop table if exists "+tableCSV)
        cursor.execute("create table if not exists "+tableCSV+" like UF_CSVTemplate")

        line=csvdata.readline()
        flag=True
        while flag:
            line=csvdata.readline()
            if line:
                currentRow=line.split(',')
                sql="insert into "+tableCSV+"(Metric,TimeStampReal,TimestampRaw,MetricValue) values(%s,%s,%s,%s)"
                param = (currentRow[1],currentRow[2],currentRow[3],float(currentRow[4]))
                cursor.execute(sql,param)
            else:
                flag=False
    conn.commit()
    #phoneInfo
    #8
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))

    tablename=projectName+"_"+svnNum+"_"+scenename
    sql="insert into UF_PhoneInfo(TableName,PhoneType,ResLength,ResWidth,Resolution) values(%s,%s,%s,%s,%s)"
    param=(tablename,phoneType,int(resLength),int(resWidth),int(resLength)*int(resWidth))

    cursor.execute(sql,param)
    conn.commit()
    cursor.close()
    conn.close()
    #9
    timeAll.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
    return render_to_response('unity_profiling/temp.html',{"timeAll":timeAll})


#绘图功能
def drawResult(request,tablename):
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    GCname="UF_"+str(tablename)+"_GC"
    STname="UF_"+str(tablename)+"_ST"
    FPSname="UF_"+str(tablename)+"_FPS"
    RDname="UF_"+str(tablename)+"_RD"
    MEMname="UF_"+str(tablename)+"_MEM"
    TRAname="UF_"+str(tablename)+"_TRA"
    CSVname="UF_"+str(tablename)+"_CSV"
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

    #半透明不透明
    TRARes={"TRA":{'List':[],'max':0.0,'min':0.0,'avg':0.0},"OPA":{'List':[],'max':0.0,'min':0.0,'avg':0.0},\
            "UIP":{'List':[],'max':0.0,'min':0.0,'avg':0.0},"CAN":{'List':[],'max':0.0,'min':0.0,'avg':0.0},\
            "ANI":{'List':[],'max':0.0,'min':0.0,'avg':0.0},"MSK":{'List':[],'max':0.0,'min':0.0,'avg':0.0}}

    sumTRA=0.0;sumOPA=0.0;sumUIP=0.0;sumCAN=0.0;sumANI=0.0;sumMSK=0.0
    sqlstr="select CPUTime from "+TRAname+" where functionName='Render.TransparentGeometry'"
    cursor.execute(sqlstr)
    for row in cursor:
        TRARes["TRA"]['List'].append(row[0])
        sumTRA+=row[0]

    sqlstr="select CPUTime from "+TRAname+" where functionName='Render.OpaqueGeometry'"
    cursor.execute(sqlstr)
    for row in cursor:
        TRARes["OPA"]['List'].append(row[0])
        sumOPA+=row[0]

    sqlstr="select CPUTime from "+TRAname+" where functionName='UIPanel.LateUpdate'"
    cursor.execute(sqlstr)
    for row in cursor:
        TRARes["UIP"]['List'].append(row[0])
        sumUIP+=row[0]

    sqlstr="select CPUTime from "+TRAname+" where functionName='Canvas.SendWillRenderCanvases'"
    cursor.execute(sqlstr)
    for row in cursor:
        TRARes["CAN"]['List'].append(row[0])
        sumCAN+=row[0]

    sqlstr="select CPUTime from "+TRAname+" where functionName='Animation.Update'"
    cursor.execute(sqlstr)
    for row in cursor:
        TRARes["ANI"]['List'].append(row[0])
        sumANI+=row[0]

    sqlstr="select CPUTime from "+TRAname+" where functionName='MeshSkinning.Update'"
    cursor.execute(sqlstr)
    for row in cursor:
        TRARes["MSK"]['List'].append(row[0])
        sumMSK+=row[0]

    TRARes["TRA"]['max']=max(TRARes["TRA"]['List'])
    TRARes["TRA"]['min']=min(TRARes["TRA"]['List'])
    TRARes["TRA"]['avg']=round(sumTRA/len(TRARes["TRA"]['List']),1)

    TRARes["OPA"]['max']=max(TRARes["OPA"]['List'])
    TRARes["OPA"]['min']=min(TRARes["OPA"]['List'])
    TRARes["OPA"]['avg']=round(sumOPA/len(TRARes["OPA"]['List']),1)

    TRARes["UIP"]['max']=max(TRARes["UIP"]['List'])
    TRARes["UIP"]['min']=min(TRARes["UIP"]['List'])
    TRARes["UIP"]['avg']=round(sumUIP/len(TRARes["UIP"]['List']),1)

    TRARes["CAN"]['max']=max(TRARes["CAN"]['List'])
    TRARes["CAN"]['min']=min(TRARes["CAN"]['List'])
    TRARes["CAN"]['avg']=round(sumCAN/len(TRARes["CAN"]['List']),1)

    TRARes["ANI"]['max']=max(TRARes["ANI"]['List'])
    TRARes["ANI"]['min']=min(TRARes["ANI"]['List'])
    TRARes["ANI"]['avg']=round(sumANI/len(TRARes["ANI"]['List']),1)

    TRARes["MSK"]['max']=max(TRARes["MSK"]['List'])
    TRARes["MSK"]['min']=min(TRARes["MSK"]['List'])
    TRARes["MSK"]['avg']=round(sumMSK/len(TRARes["MSK"]['List']),1)

    #Memory allocation
    sqlstr="select functionPath,totalGC/1024 as totalGC  from "+GCname+" order by totalGC desc limit 20"
    cursor.execute(sqlstr)
    GCRes=cursor.fetchall()

    funtionGC={"UIP":0.0,"CAN":0.0,"ANI":0.0,"MSK":0.0}
    sqlstr="select totalGC/1024 from "+GCname+" where functionPath like '%UIPanel.LateUpdate%'"
    cursor.execute(sqlstr)
    for row in cursor:
        funtionGC["UIP"]+=row[0]

    sqlstr="select totalGC/1024 from "+GCname+" where functionPath like '%Canvas.SendWillRenderCanvases%'"
    cursor.execute(sqlstr)
    for row in cursor:
        funtionGC["CAN"]+=row[0]

    sqlstr="select totalGC/1024 from "+GCname+" where functionPath like '%Animation.Update%'"
    cursor.execute(sqlstr)
    for row in cursor:
        funtionGC["ANI"]+=row[0]

    sqlstr="select totalGC/1024  from "+GCname+" where functionPath like '%MeshSkinning.Update%'"
    cursor.execute(sqlstr)
    for row in cursor:
        funtionGC["MSK"]+=row[0]

    #GC.Collect
    GCCollectRes={'FPSCount':len(FPSRes['FPSList']),'GCCalls':0,'GCCPUTime':0.0}
    sqlstr="select totalST,totalCalls from "+STname+" where functionPath like '%GC.Collect%'"
    cursor.execute(sqlstr)
    temp=cursor.fetchall()
    if len(temp)>0:
        for i in range(0,len(temp)):
            GCCollectRes['GCCPUTime']+=temp[i][0]
            GCCollectRes['GCCalls']+=temp[i][1]

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
    sqlstr="select Tris from "+RDname
    cursor.execute(sqlstr)
    for row in cursor:
        TRIRes['TRIList'].append(float(row[0]))
        sumTRI+=float(row[0])
    TRIRes['maxTRI']=str(max(TRIRes['TRIList'])/1000)+"k"
    TRIRes['minTRI']=str(min(TRIRes['TRIList'])/1000)+"k"
    TRIRes['avgTRI']=str(round(sumTRI/len(TRIRes['TRIList']),1)/1000)+"k"

    #FPS范围（帧数占比)
    sqlstr="select count(*) from "+FPSname+" where FPS>40.0"
    cursor.execute(sqlstr)
    FPS0=float(cursor.fetchall()[0][0])

    sqlstr="select count(*) from "+FPSname+" where FPS>35.0 and FPS<=40.0"
    cursor.execute(sqlstr)
    FPS1=float(cursor.fetchall()[0][0])
    sqlstr="select count(*) from "+FPSname+" where FPS>30.0 and FPS<=35.0"
    cursor.execute(sqlstr)
    FPS2=float(cursor.fetchall()[0][0])
    sqlstr="select count(*) from "+FPSname+" where FPS>20.0 and FPS<=30.0"
    cursor.execute(sqlstr)
    FPS3=float(cursor.fetchall()[0][0])
    sqlstr="select count(*) from "+FPSname+" where FPS>15.0 and FPS<=20.0"
    cursor.execute(sqlstr)
    FPS4=float(cursor.fetchall()[0][0])
    sqlstr="select count(*) from "+FPSname+" where FPS>10.0 and FPS<=15.0"
    cursor.execute(sqlstr)
    FPS5=float(cursor.fetchall()[0][0])
    sqlstr="select count(*) from "+FPSname+" where FPS<=10.0"
    cursor.execute(sqlstr)
    FPS6=float(cursor.fetchall()[0][0])
    sqlstr="select count(*) from "+FPSname
    cursor.execute(sqlstr)
    FPS7=float(cursor.fetchall()[0][0])

    FPSrate=[round((FPS0/FPS7),3)*100,round((FPS1/FPS7),3)*100,round((FPS2/FPS7),3)*100,round((FPS3/FPS7),3)*100,round((FPS4/FPS7),3)*100,round((FPS5/FPS7),3)*100,round((FPS6/FPS7),3)*100]
    #各模块耗时占比
    sqlstr="select modules,sum(totalST) as totalST from "+STname+" group by modules"
    cursor.execute(sqlstr)
    totalST=0.0
    moduleRes=[]
    for line in cursor:
        totalST+=line[1]

    for line in cursor:
        moduleRes.append({"name":line[0],"y":round(line[1]/totalST,2)*100})
    #场景图片
    picpath=''
    scene_name=''
    sqlstr="select scene_name,scene_des,scene_pic from unity_profiling_scenemodel where project_name='"+tablename.split('_')[0]+"' and scene_name='"+tablename.split('_')[2]+"'"
    cursor.execute(sqlstr)
    sceneRes=cursor.fetchall()[0]
    scenename=sceneRes[0]
    scenedes=sceneRes[1]
    picpath=sceneRes[2]

    #Memory
    MEMres={'frameIndex':[],'UsedTotal':[],'UsedUnity':[],'UsedGFX':[],'ReservedTotal':[],'ReservedUnity':[],'ReservedGFX':[]}
    Sumres={'SumUsedTotal':0.0,'SumUsedUnity':0.0,'SumUsedGFX':0.0,'SumReservedTotal':0.0,'SumReservedUnity':0.0,'SumReservedGFX':0.0}
    sqlstr="select * from "+MEMname
    cursor.execute(sqlstr)
    for sub in cursor:
        MEMres['frameIndex'].append(int(sub[1]))
        MEMres['UsedTotal'].append(sub[2])
        MEMres['UsedUnity'].append(sub[3])
        MEMres['UsedGFX'].append(sub[4])
        MEMres['ReservedTotal'].append(sub[5])
        MEMres['ReservedUnity'].append(sub[6])
        MEMres['ReservedGFX'].append(sub[7])

        Sumres['SumUsedTotal']+=float(sub[2])
        Sumres['SumUsedUnity']+=float(sub[3])
        Sumres['SumUsedGFX']+=float(sub[4])
        Sumres['SumReservedTotal']+=float(sub[5])
        Sumres['SumReservedUnity']+=float(sub[6])
        Sumres['SumReservedGFX']+=float(sub[7])

    UsedTotalRes={'max':"",'min':"",'avg':0.0}
    UsedUnityRes={'max':"",'min':"",'avg':0.0}
    UsedGFXRes={'max':"",'min':"",'avg':0.0}
    ReservedTotalRes={'max':"",'min':"",'avg':0.0}
    ReservedUnityRes={'max':"",'min':"",'avg':0.0}
    ReservedGFXRes={'max':"",'min':"",'avg':0.0}

    UsedTotalRes['max']=max(MEMres['UsedTotal'])
    UsedTotalRes['min']=min(MEMres['UsedTotal'])
    UsedTotalRes['avg']=round(Sumres['SumUsedTotal']/len(MEMres['UsedTotal']),1)

    UsedUnityRes['max']=max(MEMres['UsedUnity'])
    UsedUnityRes['min']=min(MEMres['UsedUnity'])
    UsedUnityRes['avg']=round(Sumres['SumUsedUnity']/len(MEMres['UsedUnity']),1)

    UsedGFXRes['max']=max(MEMres['UsedGFX'])
    UsedGFXRes['min']=min(MEMres['UsedGFX'])
    UsedGFXRes['avg']=round(Sumres['SumUsedGFX']/len(MEMres['UsedGFX']),1)

    ReservedTotalRes['max']=max(MEMres['ReservedTotal'])
    ReservedTotalRes['min']=min(MEMres['ReservedTotal'])
    ReservedTotalRes['avg']=round(Sumres['SumReservedTotal']/len(MEMres['ReservedTotal']),1)

    ReservedUnityRes['max']=max(MEMres['ReservedUnity'])
    ReservedUnityRes['min']=min(MEMres['ReservedUnity'])
    ReservedUnityRes['avg']=round(Sumres['SumReservedUnity']/len(MEMres['ReservedUnity']),1)

    ReservedGFXRes['max']=max(MEMres['ReservedGFX'])
    ReservedGFXRes['min']=min(MEMres['ReservedGFX'])
    ReservedGFXRes['avg']=round(Sumres['SumReservedGFX']/len(MEMres['ReservedGFX']),1)

    #Questions
    sqlstr="select count(*) from UF_Queations where FileName='"+str(tablename)+"'"
    cursor.execute(sqlstr)
    LongfunctionPath=int(cursor.fetchall()[0][0])
    questionExists=False
    if LongfunctionPath>0:
        questionExists=True


    #分辨率和机型数据
    PhoneInfo={"PhoneType":"","ResLength":"","ResWidth":"","Resolution":65025.0}
    sqlstr="select PhoneType,ResLength,ResWidth,Resolution from UF_PhoneInfo where TableName='"+tablename+"'"
    cursor.execute(sqlstr)
    PhoneRes=cursor.fetchall()
    if len(PhoneRes)!=0:
        PhoneInfo["PhoneType"]=PhoneRes[0][0]
        PhoneInfo["ResLength"]=PhoneRes[0][1]
        PhoneInfo["ResWidth"]=PhoneRes[0][2]
        PhoneInfo["Resolution"]=float(PhoneRes[0][3])

    #GPU数据
    GPURes={"FragmentsShaded":[],"ShadersBusy":[]}
    FRARes={'sum':0.0,'avg':0.0,'max':0.0,'min':0.0}
    SHARes={'sum':0.0,'avg':0.0,'max':0.0,'min':0.0}
    GPUFlag=False
    cursor.execute('SHOW TABLES')
    for row in cursor:
        if row[0]==CSVname:
            GPUFlag=True
            sqlstr="select a.TimeStampReal as TimeStampReal,b.MetricValue/a.MetricValue as MetricValue from "+CSVname+" a, "+CSVname+" b where a.Metric like 'FPS' and b.Metric like 'Fragments Shaded / Second' and a.TimeStampReal=b.TimeStampReal"
            cursor.execute(sqlstr)
            firstFlag=True
            index=0
            for row in cursor:
                index+=1
                if index>100:
                    if firstFlag:
                        temp=row[0]
                        firstFlag=False
                        FRARes['sum']+=round(row[1]/PhoneInfo["Resolution"],2)
                        FRARes['max']=round(row[1]/PhoneInfo["Resolution"],2)
                        FRARes['min']=round(row[1]/PhoneInfo["Resolution"],2)
                    if row[1]>0.000001:
                        FRARes['sum']+=round(row[1]/PhoneInfo["Resolution"],2)
                        if round(row[1]/PhoneInfo["Resolution"],2)>FRARes['max']:
                            FRARes['max']=round(row[1]/PhoneInfo["Resolution"],2)
                        if round(row[1]/PhoneInfo["Resolution"],2)<FRARes['min']:
                            FRARes['min']=round(row[1]/PhoneInfo["Resolution"],2)
                        GPURes["FragmentsShaded"].append([float((row[0]-temp)/1000000.0),round(row[1]/PhoneInfo["Resolution"],2)])
            FRARes['avg']=round(FRARes['sum']/len(GPURes["FragmentsShaded"]),2)

            firstFlag=True
            sqlstr="select TimeStampReal,MetricValue from "+CSVname+" where Metric like '% Shaders Busy'"
            cursor.execute(sqlstr)
            index=0
            for row in cursor:
                index+=1
                if index>100:
                    if firstFlag:
                        temp=row[0]
                        SHARes['sum']+=round(row[1],2)
                        SHARes['max']=round(row[1],2)
                        SHARes['min']=round(row[1],2)
                        firstFlag=False
                    if row[1]>0.000001:
                        SHARes['sum']+=round(row[1],2)
                        if round(row[1],2)>SHARes['max']:
                            SHARes['max']=round(row[1],2)
                        if round(row[1],2)<SHARes['min']:
                            SHARes['min']=round(row[1],2)
                        GPURes["ShadersBusy"].append([float((row[0]-temp)/1000000.0),round(row[1],2)])
            SHARes['avg']=round(SHARes['sum']/len(GPURes["ShadersBusy"]),2)

            FRARes['max']=round((FRARes['max']),2)
            FRARes['min']=round((FRARes['min']),2)
            FRARes['avg']=round((FRARes['avg']),2)
            break



    cursor.close()
    conn.close()
    return render_to_response('unity_profiling/drawResult.html',{'MEMRes':MEMres,'FPSRes':FPSRes,'DCRes':DCRes,'TRIRes':TRIRes,'TRARes':TRARes,'GCCollectRes':GCCollectRes,'GCRes':JSONEncoder().encode(GCRes),'GPURes':GPURes,'GPUFlag':GPUFlag,'PhoneInfo':PhoneInfo,\
                              'FPSrate':FPSrate,'picpath':picpath,'scenedes':scenedes,'scenename':scenename,'moduleRes':JSONEncoder().encode(moduleRes),'questionExists':questionExists,'tablename':tablename,'LongfunctionPath':LongfunctionPath,'FRARes':FRARes,'SHARes':SHARes,\
                              'UsedTotalRes':UsedTotalRes,'UsedUnityRes':UsedUnityRes,'UsedGFXRes':UsedGFXRes,'ReservedTotalRes':ReservedTotalRes,'ReservedUnityRes':ReservedUnityRes,'ReservedGFXRes':ReservedGFXRes,'funtionGC':funtionGC})

def drawMEMResult(request,tablename):
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    MEMname="UF_"+str(tablename)+"_MEM"
    #Memory
    res={'frameIndex':[],'UsedTotal':[],'UsedUnity':[],'UsedGFX':[],'ReservedTotal':[],'ReservedUnity':[],'ReservedGFX':[]}
    sqlstr="select * from "+MEMname
    cursor.execute(sqlstr)
    for sub in cursor:
        res['frameIndex'].append(int(sub[1]))
        res['UsedTotal'].append(sub[2])
        res['UsedUnity'].append(sub[3])
        res['UsedGFX'].append(sub[4])
        res['ReservedTotal'].append(sub[5])
        res['ReservedUnity'].append(sub[6])
        res['ReservedGFX'].append(sub[7])

    #场景图片
    picpath=''
    sqlstr="select scene_pic from unity_profiling_scenemodel where project_name='"+tablename.split('_')[0]+"' and scene_name='"+tablename.split('_')[2]+"'"
    cursor.execute(sqlstr)
    picpath=cursor.fetchall()[0][0]
    cursor.close()
    conn.close()
    return render_to_response('unity_profiling/drawMEMResult.html',{'picpath':picpath,'MEMRes':res})

def drawResultAll(request):
    conn=MySQLdb.connect(host='127.0.0.1',port=3306,user='leiting',passwd=password,db='leiting',charset='utf8')
    cursor=conn.cursor()
    #scene_name,table_name
    cursor.execute('SHOW TABLES')
    allprojects=['L13','L10','L15']

    FPStables={'L13':[],'L10':[],'L15':[]}
    Rendertables={'L13':[],'L10':[],'L15':[]}
    scene_res={'L13':[],'L10':[],'L15':[]}
    allSQLname=cursor.fetchall()
    for name in allSQLname:
        if 'UF_L13_' in name[0] and 'FPS' in name[0]:
            FPStables['L13'].append(name[0])
            scene_res['L13'].append(name[0].split('_')[3])
        if 'UF_L10_' in name[0] and 'FPS' in name[0]:
            FPStables['L10'].append(name[0])
            scene_res['L10'].append(name[0].split('_')[3])
        if 'UF_L15_' in name[0] and 'FPS' in name[0]:
            FPStables['L15'].append(name[0])
            scene_res['L15'].append(name[0].split('_')[3])

        if 'UF_L13_' in name[0] and 'RD' in name[0]:
            Rendertables['L13'].append(name[0])
        if 'UF_L10_' in name[0] and 'RD' in name[0]:
            Rendertables['L10'].append(name[0])
        if 'UF_L15_' in name[0] and 'RD' in name[0]:
            Rendertables['L15'].append(name[0])

    sceneCount={'L13':len(FPStables['L13']),'L10':len(FPStables['L10']),'L15':len(FPStables['L15'])}  
    #FPS
    FPSRes={'scene':[],'avgFPS':[],'maxFPS':[],'minFPS':[]}
    for project in allprojects: 
        if sceneCount[project]>0:
            for tablename in FPStables[project]:
                sqlstr="select FPS from "+tablename
                cursor.execute(sqlstr)
                List=[]
                sumFPS=0.0
                for row in cursor:
                    List.append(row[0])
                    sumFPS+=row[0]
                FPSRes['scene'].append(tablename.split('_')[3])
                FPSRes['maxFPS'].append(max(List))
                FPSRes['avgFPS'].append(round(sumFPS/len(List),1))
                FPSRes['minFPS'].append(min(List))
        else:
            FPSRes['scene'].append('')
            FPSRes['maxFPS'].append('')
            FPSRes['avgFPS'].append('')
            FPSRes['minFPS'].append('')
    #DrawCalls
    DCRes={'scene':[],'avgDC':[],'maxDC':[],'minDC':[]}
    for project in allprojects: 
        if sceneCount[project]>0:
            for tablename in Rendertables[project]:
                sqlstr="select drawCalls from "+tablename
                cursor.execute(sqlstr)
                List=[]
                sumDC=0.0
                for row in cursor:
                    List.append(row[0])
                    sumDC+=row[0]
                DCRes['scene'].append(tablename.split('_')[3])
                DCRes['maxDC'].append(max(List))
                DCRes['avgDC'].append(round(sumDC/len(List),1))
                DCRes['minDC'].append(min(List))
        else:
            DCRes['scene'].append('')
            DCRes['maxDC'].append('')
            DCRes['avgDC'].append('')
            DCRes['minDC'].append('')
    #Triangles 
    TRIRes={'scene':[],'avgTRI':[],'maxTRI':[],'minTRI':[]}
    for project in allprojects: 
        if sceneCount[project]>0:
            for tablename in Rendertables[project]:
                sqlstr="select Tris from "+tablename
                cursor.execute(sqlstr)
                List=[]
                sumTRI=0.0
                for row in cursor:
                    List.append(row[0])
                    sumTRI+=row[0]
                TRIRes['scene'].append(tablename.split('_')[3])
                TRIRes['maxTRI'].append(max(List))
                TRIRes['avgTRI'].append(round(sumTRI/len(List),1))
                TRIRes['minTRI'].append(min(List))
        else:
            TRIRes['scene'].append('')
            TRIRes['maxTRI'].append('')
            TRIRes['avgTRI'].append('')
            TRIRes['minTRI'].append('')
    cursor.close()
    conn.close()
    return render_to_response('unity_profiling/drawResultAllNew.html',{'scene_res':scene_res,'sceneCount':sceneCount,'FPS_res':FPSRes,'DC_res':DCRes,'TRI_Res':TRIRes})
    #return render_to_response('unity_profiling/drawResultAll.html',{'allscene':res})

def getResultAll(request):
    projects={'L13':'','L10':'','L15':''}
    Res=[]
    Type=''
    if(request.GET.has_key('L13projects')):
        projects['L13']=request.GET.get('L13projects',"")
    if(request.GET.has_key('L10projects')):
        projects['L10']=request.GET.get('L10projects',"")
    if(request.GET.has_key('L15projects')):
        projects['L15']=request.GET.get('L15projects',"")
    if(request.GET.has_key('type')):
        Type=request.GET.get('type',"")

    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    cursor.execute('SHOW TABLES')
    res={'L13':[],'L10':[],'L15':[]}
    allSQLname=cursor.fetchall()
    for name in allSQLname:
        if Type=="FPS":
            if 'UF_L13_' in name[0] and Type in name[0] and name[0].split('_')[3] in projects['L13']:
                res['L13'].append(name[0])
            if 'UF_L10_' in name[0] and Type in name[0] and name[0].split('_')[3] in projects['L10']:
                res['L10'].append(name[0])
            if 'UF_L15_' in name[0] and Type in name[0] and name[0].split('_')[3] in projects['L15']:
                res['L15'].append(name[0])
        else:
            if 'UF_L13_' in name[0] and "RD" in name[0] and name[0].split('_')[3] in projects['L13']:
                res['L13'].append(name[0])
            if 'UF_L10_' in name[0] and "RD" in name[0] and name[0].split('_')[3] in projects['L10']:
                res['L10'].append(name[0])
            if 'UF_L15_' in name[0] and "RD" in name[0] and name[0].split('_')[3] in projects['L15']:
                res['L15'].append(name[0])
    
    #L13
    for tablename in res['L13']:
        sqlstr="select "+Type+" from "+tablename
        cursor.execute(sqlstr)
        List=[]
        for row in cursor:
            List.append(row[0])
        Res.append({"name":"L13"+tablename.split('_')[3],"data":List})
    #L10
    for tablename in res['L10']:
        sqlstr="select "+Type+" from "+tablename
        cursor.execute(sqlstr)
        List=[]
        for row in cursor:
            List.append(row[0])
        Res.append({"name":"L10"+tablename.split('_')[3],"data":List})
    #L15
    for tablename in res['L15']:
        sqlstr="select "+Type+" from "+tablename
        cursor.execute(sqlstr)
        List=[]
        for row in cursor:
            List.append(row[0])
        Res.append({"name":"L15"+tablename.split('_')[3],"data":List})
    cursor.close()
    conn.close()
    return HttpResponse(JSONEncoder().encode(Res))

def uploadLog(request):
    return render_to_response('unity_profiling/uploadLog.html')

def downloadFile(request):
    the_file_name = "/home/leitingqa/project_web_lt/Webtool/templates/unity_profiling/SProfiler.cs"
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="SProfiler.cs"'
    return response

def exportToExcel(request,tablename):
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor=conn.cursor()

    tableGC="UF_"+str(tablename)+"_GC"
    tableST="UF_"+str(tablename)+"_ST"
    tableTT="UF_"+str(tablename)+"_TT"
    tableFPS="UF_"+str(tablename)+"_FPS"
    tableRD="UF_"+str(tablename)+"_RD"

    response = HttpResponse(content_type='application/vnd.ms-excel') 
    response['Content-Disposition'] = "attachment; filename="+str(tablename)+".xls"  
    wbk = xlwt.Workbook()

    GCSheet = wbk.add_sheet("GC")
    GCSheet.write(0,0,"id")
    GCSheet.write(0,1,u"函数路径")
    GCSheet.write(0,2,u"函数所属模块")
    GCSheet.write(0,3,u"累计GC(单位:B)")
    GCSheet.write(0,4,u"出现GC调用次数")
    GCSheet.write(0,5,u"总调用次数")
    GCSheet.write(0,6,u"平均每次调用GC(单位:B)")

    STSheet = wbk.add_sheet("Self Time")
    STSheet.write(0,0,"id")
    STSheet.write(0,1,u"函数路径")
    STSheet.write(0,2,u"函数所属模块")
    STSheet.write(0,3,u"累计Self Time(单位:ms)")
    STSheet.write(0,4,u"调用次数")
    STSheet.write(0,5,u"平均的Self Time(单位:ms)")

    TTSheet = wbk.add_sheet("Total Time")
    TTSheet.write(0,0,"id")
    TTSheet.write(0,1,u"函数路径")
    TTSheet.write(0,2,u"函数所属模块")
    TTSheet.write(0,3,u"累计Total Time(单位:ms)")
    TTSheet.write(0,4,u"调用次数")
    TTSheet.write(0,5,u"平均的Total Time(单位:ms)")

    FPSSheet = wbk.add_sheet("FPS")
    FPSSheet.write(0,0,u"帧数")
    FPSSheet.write(0,1,u"FPS值")

    RDSheet = wbk.add_sheet("Rendering")
    RDSheet.write(0,0,u"帧数")
    RDSheet.write(0,1,"Draw Calls")
    RDSheet.write(0,2,"Total Batches")
    RDSheet.write(0,3,"Triangles")
    RDSheet.write(0,4,"Verticals")

    #GC
    row_list=[]
    cursor.execute("select * from "+tableGC)
    row_list=cursor.fetchall()
    rowlen=len(row_list)
    for i in range(rowlen):
        for j in range(0,7):
            GCSheet.write(i+1,j,row_list[i][j])
    #self Time
    row_list=[]
    cursor.execute("select * from "+tableST)
    row_list=cursor.fetchall()
    rowlen=len(row_list)
    for i in range(rowlen):
        for j in range(0,6):
            STSheet.write(i+1,j,row_list[i][j])  
    #total Time
    row_list=[]
    cursor.execute("select * from "+tableTT)
    row_list=cursor.fetchall()
    rowlen=len(row_list)
    for i in range(rowlen):
        for j in range(0,6):
            TTSheet.write(i+1,j,row_list[i][j])  
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
    sqlstr="select * from UF_Queations where FileName='"+str(tablename)+"'"
    cursor.execute(sqlstr)
    for row in cursor:
        response.write(str(row[1])+"|"+str(row[4])+"|"+str(row[3])+"|"+str(row[2])+"\r\n")
    cursor.close()
    conn.close()
    return response

# def exportLogToExcel(request,tablename):
#     conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='root',passwd='123456',db ='leiting',charset='utf8')
#     cursor=conn.cursor()
#     #Questions  
#     response = HttpResponse(content_type='application/vnd.ms-excel') 
#     response['Content-Disposition'] = "attachment; filename="+str(tablename)+".xls"  
#     wbk = xlwt.Workbook()
#     Sheet = wbk.add_sheet("longFunctionPath")
#     Sheet.write(0,0,"Scene Name")
#     Sheet.write(0,1,"Function Path")
#     Sheet.write(0,2,"Row Index")

#     sqlstr="select * from UF_Queations where FileName='"+str(tablename)+"'"
#     cursor.execute(sqlstr)
#     index=0
#     for row in cursor:
#         index+=1
#         for j in range(1,4):
#             Sheet.write(index,j-1,row[j])
#     wbk.save(response) 
#     cursor.close()
#     conn.close()
#     return response


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