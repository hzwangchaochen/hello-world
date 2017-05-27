# coding:utf-8
import json
from json import *
import MySQLdb
import MySQLdb.cursors
import xlrd,xlwt
from django.http import HttpResponse
from django.shortcuts import render_to_response
import re
import sys
from django.contrib.auth.decorators import login_required
import datetime 
from models import PicModel
reload(sys)  
sys.setdefaultencoding('utf8')


password='leiting_qa_163'
# Create your views here.
@login_required
def index(request):
    return render_to_response('assign_test_case/assignTestCase.html',{'currentuser':request.user.username})

#获得数据库数据并放入表格中
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

    qa=''
    state='' 
    table=''
    sort ='superClass'
    order='asc'
    
    if(request.POST.has_key('Sheet')):
        table=request.POST.get('Sheet',"")
    if(request.POST.has_key('sort')):
        sort = request.POST.get('sort',"")
    if(request.POST.has_key('order')):
        order = request.POST.get('order',"")

    if(table==''):
        return HttpResponse('')
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

#将前端对表格的修改更新到数据库中
def updateDataToMysql(request):
    detail=''
    testStep=''
    expectedResult=''
    timeNode=''
    ifPass=''
    executor=''
    comments=''
    table=''
    ifExists=''
    id=1
    if(request.POST.has_key('Sheet')):
        table=request.POST.get('Sheet',"")
    if(request.POST.has_key('id')):
        id = request.POST.get('id',"")   
    if(request.POST.has_key('detail')):
        detail = request.POST.get('detail',"")
    if(request.POST.has_key('testStep')):
        testStep = request.POST.get('testStep',"")
    if(request.POST.has_key('expectedResult')):
        expectedResult = request.POST.get('expectedResult',"")
    if(request.POST.has_key('timeNode')):
        timeNode = request.POST.get('timeNode',"")
    if(request.POST.has_key('ifExists')):
        ifExists = request.POST.get('ifExists',"")
    if(request.POST.has_key('ifPass')):
        ifPass = request.POST.get('ifPass',"")
    if(request.POST.has_key('executor')):
        executor = request.POST.get('executor',"")
    if(request.POST.has_key('comments')):
        comments = request.POST.get('comments',"")
    if(request.POST.has_key('phonetype')):
        phonetype = request.POST.get('phonetype',"")


    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    cursor.execute("update "+str(table)+" set detail='"+str(detail)+"',\
                    testStep='"+str(testStep)+"',\
                    expectedResult='"+str(expectedResult)+"',\
                    timeNode='"+str(timeNode)+"',\
                    ifExists='"+str(ifExists)+"',\
                    ifPass='"+str(ifPass)+"',\
                    executor='"+str(executor)+"',\
                    phonetype='"+str(phonetype)+"',\
                    comments='"+str(comments)+"' where id="+str(id))
    conn.commit()
    cursor.close()
    conn.close()
    return HttpResponse('')

#搜索数据库中的数据
def searchDataFromMysql(request):
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

    table=''
    superClass=''
    mainClass=''
    sort ='superClass'
    order='asc'
    
    if(request.POST.has_key('Sheet')):
        table=request.POST.get('Sheet',"")

    if(request.POST.has_key('superClass')):
        superClass=request.POST.get('superClass',"")

    if(request.POST.has_key('mainClass')):
        mainClass=request.POST.get('mainClass',"")

    if table=='':
        return HttpResponse('')
        
    sqlcountstr="select count(*) from "+table
    sqlstr="select * from "+table
    cursor.execute(sqlcountstr+" where superClass like '%"+str(superClass)+"%' and mainClass like '%"+str(mainClass)+"%'")
    total=cursor.fetchall()[0][u'count(*)']  
    cursor.execute(sqlstr+" where superClass like '%"+str(superClass)+"%' and mainClass like '%"+str(mainClass)+"%' order by "+sort+" "+order+" limit "+str(offset)+","+str(rows))
    data=cursor.fetchall()
    res['total']=total
    res['rows']=data   
    jsonRes=JSONEncoder().encode(res)
    
    cursor.close()
    conn.close()
    return HttpResponse(jsonRes)

#用于前端测试用例集目录结构的自动生成（每个测试用例集leihuo和MTL成对出现）
def findAllSqlName(request,projectname):
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor=conn.cursor()
    cursor.execute('SHOW TABLES')
    allSQLname=cursor.fetchall()
    res=[]
    res.append({'text': '标准测试用例集','children':[{'text': '质量保障通过率'},{'text': '雷火内测用例'}]})
    for name in allSQLname:
        if projectname in name[0]:
            if '质量保障通过率' in name[0]:
                res.append({'text': name[0].split('_')[1],'children':[{'text': name[0]},{'text': '雷火内测用例_'+name[0][8:]}]})
    cursor.close()
    conn.close()
    return HttpResponse(JSONEncoder().encode(res))

#添加测试用例集
def addTestCase(request):
    casename=''
    projectname=''
    if(request.POST.has_key('casename')):
        casename=request.POST.get('casename',"")
    if(request.POST.has_key('projectname')):
        projectname=request.POST.get('projectname',"")
    conn= MySQLdb.connect(host='127.0.0.1',port=3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    cursor.execute("create table if not exists 质量保障通过率_"+casename+"_"+projectname+"  like 质量保障通过率")
    conn.commit()
    cursor.execute("insert into 质量保障通过率_"+casename+"_"+projectname+"  select * from 质量保障通过率")
    conn.commit()
    cursor.execute("create table if not exists 雷火内测用例_"+casename+"_"+projectname+"  like 雷火内测用例")
    conn.commit()
    cursor.execute("insert into 雷火内测用例_"+casename+"_"+projectname+"  select * from 雷火内测用例")
    conn.commit()
    cursor.close()
    conn.close()
    return HttpResponse('')

#删除测试用例集
def deleteTestCase(request):
    tablename1=''
    tablename2=''
    if(request.POST.has_key('tablename1')):
        tablename1=request.POST.get('tablename1',"")
    if(request.POST.has_key('tablename2')):
        tablename2=request.POST.get('tablename2',"")
    conn= MySQLdb.connect(host='127.0.0.1',port=3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    cursor.execute("drop table if exists "+tablename1)
    conn.commit()
    cursor.execute("drop table if exists "+tablename2)
    conn.commit()
    cursor.close()
    conn.close()
    return HttpResponse('')

#获得当前测试用例的通过率圆饼图
def getResult(request,tablename):
    conn= MySQLdb.connect(host='127.0.0.1',port=3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    cursor.execute("select count(*) from "+tablename+" where ifPass=0")
    count_fail=cursor.fetchall()[0][0]
    cursor.execute("select count(*) from "+tablename+" where ifPass=1")
    count_pass=cursor.fetchall()[0][0]
    res=[{"name":"通过率","y":count_pass},{"name":"未通过率","y":count_fail}]
    cursor.close()
    conn.close()
    return HttpResponse(JSONEncoder().encode(res))

#将结果导出excel
def exportToExcel(request,tablename):
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor=conn.cursor()
    response = HttpResponse(content_type='application/vnd.ms-excel') 
    response['Content-Disposition'] = "attachment; filename="+str(tablename)+".xls"  
    wbk = xlwt.Workbook()
    sheet=wbk.add_sheet("Result")
    sheet.write(0,0,u"序号")
    sheet.write(0,1,u"大类型")
    sheet.write(0,2,u"类型")
    sheet.write(0,3,u"子类型")
    sheet.write(0,4,u"描述")
    sheet.write(0,5,u"测试步骤")
    sheet.write(0,6,u"预期结果")
    sheet.write(0,7,u"时间节点")
    sheet.write(0,8,u"是否有该功能")
    sheet.write(0,9,u"是否通过")
    sheet.write(0,10,u"执行者")
    sheet.write(0,11,u"备注")
    sheet.write(0,12,u"测试机型（安卓A&苹果B）")

    cursor.execute("select * from "+str(tablename))
    rowIndex=1
    for row in cursor:
        for columnIndex in range(0,len(row)):
            sheet.write(rowIndex,columnIndex,row[columnIndex])
        rowIndex+=1
    wbk.save(response) 
    cursor.close()
    conn.close()
    return response

#获得当前测试用例分项的通过数柱状图
def getSubResult(request,tablename):
    conn= MySQLdb.connect(host='127.0.0.1',port=3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    countFail=[]
    countPass=[]
    superClassList=['手游上线App Store公司内审标准','手游上线MTL质量标准','手游上线QA推荐标准（非强制）','手游上线QA质量标准','手游上线UE质量标准','手游上线必过标准','手游上线SA质量标准']
    mainClassList=['安装卸载','安全性','登录界面','中断测试','兼容性','其他']

    if '质量保障通过率' in tablename:
        for i in range(0,len(superClassList)):
            cursor.execute("select count(*) from "+tablename+" where superClass='"+superClassList[i]+"' and ifPass=0")
            countFail.append(cursor.fetchall()[0][0])
            cursor.execute("select count(*) from "+tablename+" where superClass='"+superClassList[i]+"' and ifPass=1")
            countPass.append(cursor.fetchall()[0][0])
        res=[{"name":"通过数量","data":countPass},{"name":"未通过数量","data":countFail}]

    if '雷火内测用例' in tablename:
        for i in range(0,len(mainClassList)):
            cursor.execute("select count(*) from "+tablename+" where mainClass='"+mainClassList[i]+"' and ifPass=0")
            countFail.append(cursor.fetchall()[0][0])
            cursor.execute("select count(*) from "+tablename+" where mainClass='"+mainClassList[i]+"' and ifPass=1")
            countPass.append(cursor.fetchall()[0][0])
        res=[{"name":"通过数量","data":countPass},{"name":"未通过数量","data":countFail}]

    cursor.close()
    conn.close()
    return HttpResponse(JSONEncoder().encode(res))

def getResultIndex(request,tablename):
    if '质量保障通过率' in tablename:
        categories=['手游上线App Store公司内审标准','手游上线MTL质量标准','手游上线QA推荐标准（非强制）','手游上线QA质量标准','手游上线UE质量标准','手游上线必过标准','手游上线SA质量标准']
    if '雷火内测用例' in tablename:
        categories=['安装卸载','安全性','登录界面','中断测试','兼容性','其他']
    return render_to_response('assign_test_case/drawResult.html',{'tablename':json.dumps(tablename),'category':json.dumps(categories)})
	

#获得当前项目的通过率结果（包括按月的总通过率和分项通过率）
def getTrend(request,projectname):
    starttime_year=2016
    starttime_month=1
    pass_rate=[]
    month_from_begin=[]
    table_names=[]
    res=[]

    sub_res=[]
    pass_rate_all=[]

    latestTable=''
    maxMonth=0

    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor=conn.cursor()
    cursor.execute('SHOW TABLES')
    allSQLname=cursor.fetchall()
    
    for name in allSQLname:
        if projectname in name[0] and '质量保障通过率' in name[0]:
            cursor.execute("select count(*) from "+name[0]+" where ifPass=1")
            count_pass=cursor.fetchall()[0][0]
            cursor.execute("select count(*) from "+name[0])
            count_all=cursor.fetchall()[0][0]
            table_names.append(name[0])
            pass_rate.append(float(count_pass)/count_all*100)

    for table_name in table_names:
        temp=int(table_name.split('_')[2][4:6])-starttime_month+(int(table_name.split('_')[2][0:4])-starttime_year)*12
        month_from_begin.append(temp)
        if temp>maxMonth:
            maxMonth=temp
            latestTable=table_name        
    month_from_begin=sorted(month_from_begin)

    if(len(table_names)==0):
        return render_to_response('assign_test_case/drawTrend_MTL.html',{'data':json.dumps(res),'sub_res':sub_res,'projectname':projectname})
    j=0
    for i in range(1,month_from_begin[-1]+1):
        if i in month_from_begin:
            res.append(round(pass_rate[j],1))
            j+=1
        else:
            res.append(None)

    superClassList=['手游上线App Store公司内审标准','手游上线MTL质量标准','手游上线QA推荐标准（非强制）','手游上线QA质量标准','手游上线UE质量标准','手游上线必过标准','手游上线SA质量标准']
    for table_name in table_names:
        pass_rate_sub=[]
        for m in range(0,len(superClassList)):
            cursor.execute("select count(*) from "+table_name+" where superClass='"+superClassList[m]+"' and ifPass=1")
            count_pass=cursor.fetchall()[0][0]
            cursor.execute("select count(*) from "+table_name+" where superClass='"+superClassList[m]+"'")
            count_all=cursor.fetchall()[0][0]
            pass_rate_sub.append(float(count_pass)/count_all*100)
        cursor.execute("select count(*) from 雷火内测用例_"+table_name[8:]+" where  ifPass=1")
        count_pass=cursor.fetchall()[0][0]
        cursor.execute("select count(*) from 雷火内测用例_"+table_name[8:])
        count_all=cursor.fetchall()[0][0]
        pass_rate_sub.append(float(count_pass)/count_all*100)
        pass_rate_all.append(pass_rate_sub)
    sub_res=dict(zip(month_from_begin,pass_rate_all))

    #安卓用例通过率和苹果用例通过率
    androidPass=[]
    iphonePass=[]
    for m in range(0,len(superClassList)):
        cursor.execute("select count(*) from "+latestTable+" where superClass='"+superClassList[m]+"' and phonetype like '%A%' and ifPass=1")
        count_pass=cursor.fetchall()[0][0]
        cursor.execute("select count(*) from "+latestTable+" where superClass='"+superClassList[m]+"' and phonetype like '%A%'")
        count_all=cursor.fetchall()[0][0]
        if count_all==0:
            androidPass.append(0)
        else:
            androidPass.append(float(count_pass)/count_all*100)

        cursor.execute("select count(*) from "+latestTable+" where superClass='"+superClassList[m]+"' and phonetype like '%B%' and ifPass=1")
        count_pass=cursor.fetchall()[0][0]
        cursor.execute("select count(*) from "+latestTable+" where superClass='"+superClassList[m]+"' and phonetype like '%B%'")
        count_all=cursor.fetchall()[0][0]
        if count_all==0:
            iphonePass.append(0)
        else:
            iphonePass.append(float(count_pass)/count_all*100)

    cursor.execute("select count(*) from 雷火内测用例_"+latestTable[8:]+" where phonetype like '%A%' and ifPass=1")
    count_pass=cursor.fetchall()[0][0]
    cursor.execute("select count(*) from 雷火内测用例_"+latestTable[8:]+" where phonetype like '%A%'")
    count_all=cursor.fetchall()[0][0]
    if count_all==0:
        androidPass.append(0)
    else:
        androidPass.append(float(count_pass)/count_all*100)

    cursor.execute("select count(*) from 雷火内测用例_"+latestTable[8:]+" where phonetype like '%B%' and ifPass=1")
    count_pass=cursor.fetchall()[0][0]
    cursor.execute("select count(*) from 雷火内测用例_"+latestTable[8:]+" where phonetype like '%B%'")
    count_all=cursor.fetchall()[0][0]
    if count_all==0:
        iphonePass.append(0)
    else:
        iphonePass.append(float(count_pass)/count_all*100)
    #排除不适用L13的用例后通过率
    allPass=[]
    usefulPass=[]

    for m in range(0,len(superClassList)):
        cursor.execute("select count(*) from "+latestTable+" where superClass='"+superClassList[m]+"' and ifPass=1")
        count_pass=cursor.fetchall()[0][0]
        cursor.execute("select count(*) from "+latestTable+" where superClass='"+superClassList[m]+"'")
        count_all=cursor.fetchall()[0][0]
        if count_all==0:
            allPass.append(0)
        else:
            allPass.append(float(count_pass)/count_all*100)

        cursor.execute("select count(*) from "+latestTable+" where superClass='"+superClassList[m]+"' and ifExists='是' and ifPass=1")
        count_pass=cursor.fetchall()[0][0]
        cursor.execute("select count(*) from "+latestTable+" where superClass='"+superClassList[m]+"' and ifExists='是'")
        count_all=cursor.fetchall()[0][0]
        if count_all==0:
            usefulPass.append(0)
        else:
            usefulPass.append(float(count_pass)/count_all*100)

    cursor.execute("select count(*) from 雷火内测用例_"+latestTable[8:]+" where ifPass=1")
    count_pass=cursor.fetchall()[0][0]
    cursor.execute("select count(*) from 雷火内测用例_"+latestTable[8:])
    count_all=cursor.fetchall()[0][0]
    if count_all==0:
        allPass.append(0)
    else:
        allPass.append(float(count_pass)/count_all*100)


    cursor.execute("select count(*) from 雷火内测用例_"+latestTable[8:]+" where ifExists='是' and ifPass=1")
    count_pass=cursor.fetchall()[0][0]
    cursor.execute("select count(*) from 雷火内测用例_"+latestTable[8:]+" where ifExists='是'")
    count_all=cursor.fetchall()[0][0]
    if count_all==0:
        usefulPass.append(0)
    else:
        usefulPass.append(float(count_pass)/count_all*100)
        
    return render_to_response('assign_test_case/drawTrend_MTL.html',{'data':json.dumps(res),'sub_res':sub_res,'projectname':projectname,'androidPass':androidPass,'iphonePass':iphonePass,'allPass':allPass,'usefulPass':usefulPass})



#获得某项目通过率的中间结果，用于下面两个函数
def getTrendRes(projectname,subproject):
    starttime_year=2016
    starttime_month=1
    pass_rate=[]
    month_from_begin=[]
    table_names=[]
    res=[]

    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor=conn.cursor()
    cursor.execute('SHOW TABLES')
    allSQLname=cursor.fetchall()

    if subproject=='':
        for name in allSQLname:
            if projectname in name[0] and '质量保障通过率' in name[0]:
                cursor.execute("select count(*) from "+name[0]+" where ifPass=1")
                count_pass=cursor.fetchall()[0][0]
                cursor.execute("select count(*) from "+name[0])
                count_all=cursor.fetchall()[0][0]
                table_names.append(name[0])
                pass_rate.append(float(count_pass)/count_all*100)
    else:
        for name in allSQLname:
            if projectname in name[0] and '质量保障通过率' in name[0]:
                cursor.execute("select count(*) from "+name[0]+" where superClass='"+subproject+"' and ifPass=1")
                count_pass=cursor.fetchall()[0][0]
                cursor.execute("select count(*) from "+name[0]+" where superClass='"+subproject+"'")
                count_all=cursor.fetchall()[0][0]
                table_names.append(name[0])
                pass_rate.append(float(count_pass)/count_all*100)

    if(len(table_names)==0):
        return res
    for table_name in table_names:
        month_from_begin.append(int(table_name.split('_')[2][4:6])-starttime_month+(int(table_name.split('_')[2][0:4])-starttime_year)*12)
    month_from_begin=sorted(month_from_begin)
    j=0
    for i in range(1,month_from_begin[-1]+1):
        if i in month_from_begin:
            res.append(pass_rate[j])
            j+=1
        else:
            res.append(None)
    return res


#获得所有项目的通过率
def getTrendAll(request):
    projects='L12L13L14L15LH01'
    res=[]
    if(request.GET.has_key('projects')):
        projects=request.GET.get('projects',"")
    if 'L12' in projects:
        res.append({'connectNulls':'true','name': 'L12质量保障通过率','data':getTrendRes('L12','')})
    if 'L13' in projects:
        res.append({'connectNulls':'true','name': 'L13质量保障通过率','data':getTrendRes('L13','')})
    if 'L14' in projects:
        res.append({'connectNulls':'true','name': 'L14质量保障通过率','data':getTrendRes('L14','')})
    if 'L15' in projects:
        res.append({'connectNulls':'true','name': 'L15质量保障通过率','data':getTrendRes('L15','')})
    if 'LH01' in projects:
        res.append({'connectNulls':'true','name': 'LH01质量保障通过率','data':getTrendRes('LH01','')})
    return HttpResponse(JSONEncoder().encode(res))

#获得所有项目的子项通过率
def getTrendSub(request):
    projects='L12L13L14L15LH01'
    subproject=''
    res=[]
    if(request.GET.has_key('projects')):
        projects=request.GET.get('projects',"")
    if(request.GET.has_key('subproject')):
        subproject=request.GET.get('subproject',"")
    if 'L12' in projects:
        res.append({'connectNulls':'true','name': 'L12'+subproject+'通过率','data':getTrendRes('L12',subproject)})
    if 'L13' in projects:
        res.append({'connectNulls':'true','name': 'L13'+subproject+'通过率','data':getTrendRes('L13',subproject)})
    if 'L14' in projects:
        res.append({'connectNulls':'true','name': 'L14'+subproject+'通过率','data':getTrendRes('L14',subproject)})
    if 'L15' in projects:
        res.append({'connectNulls':'true','name': 'L15'+subproject+'通过率','data':getTrendRes('L15',subproject)})
    if 'LH01' in projects:
        res.append({'connectNulls':'true','name': 'LH01'+subproject+'通过率','data':getTrendRes('LH01',subproject)})
    return HttpResponse(JSONEncoder().encode(res))

def getTrendAllIndex(request):
    return render_to_response('assign_test_case/drawTrend_ALL.html')

def scenePC(request):
    if request.method == 'POST':
        new_img = PicModel(
            model_pic=request.FILES.get('picfile'),
            model_des=request.POST['sceneabstract'],
            model_PC=request.POST['powerconsumption']
        )
        new_img.save()
    return render_to_response('assign_test_case/temp.html')
    
def sceneIndex(request):
    imgs=PicModel.objects.all()
    conn= MySQLdb.connect(host='127.0.0.1',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    sql="select * from assign_test_case_picmodel"
    cursor.execute(sql)
    PCList=[]
    desList=[]
    picList=[]
    for entry in cursor:
        PCList.append(entry['model_PC'])
        desList.append(entry['model_des'])
        picList.append(entry['model_pic'])
    return render_to_response('assign_test_case/scenePC.html', {'imgs':imgs,'PCList':PCList,'desList':desList,'picList':picList})
    #return render_to_response('assign_test_case/scenePC.html')