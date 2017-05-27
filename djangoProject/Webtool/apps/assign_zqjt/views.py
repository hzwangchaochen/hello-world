# coding:utf-8
import json
from json import *
import MySQLdb
import MySQLdb.cursors
import xlrd,xlwt
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


password='leiting_qa_163'
@login_required
def index(request):
    return render_to_response(r'assign_zqjt/assign_zqjt.html',{'currentuser':request.user.username})


def getDataFromMysql(request):
    res={}
    conn= MySQLdb.connect(host='192.168.131.233',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
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
    table='ust_hangulstrings'
    sort ='column0'
    order='asc'
    column2=''
	
    if(request.POST.has_key('Sheet')):
        table=request.POST.get('Sheet',"")
    if(request.POST.has_key('QA')):
        qa = request.POST.get('QA',"")
    if(request.POST.has_key('state')):
        state = request.POST.get('state',"")


    if(request.POST.has_key('sort')):
        sort = request.POST.get('sort',"")
    if(request.POST.has_key('order')):
        order = request.POST.get('order',"")
    if(qa=='所有'):
        qa=''
    if(state=='所有'):
        state=''
    sqlcountstr="select count(*) from "+table
    sqlstr="select * from "+table
    cursor.execute(sqlcountstr+" where QAer like '"+str(qa)+"%' and isFinished like '"+str(state)+"%'")
    total=cursor.fetchall()[0][u'count(*)']  
    cursor.execute(sqlstr+" where QAer like '"+str(qa)+"%' and isFinished like '"+str(state)+"%' order by "+sort+" "+order+" limit "+str(offset)+","+str(rows))
    data=cursor.fetchall()
    res['total']=total
    res['rows']=data   
    jsonRes=JSONEncoder().encode(res)


    #cursor.execute("update currentSheet set currentSheetName='"+table+"' where id=1")
    #conn.commit()
    cursor.close()
    conn.close()
    return HttpResponse(jsonRes)

def searchDataFromMysql(request):
    res={}
    conn= MySQLdb.connect(host='192.168.131.233',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
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
    table='ust_hangulstrings'
    sort ='column0'
    order='asc'
    column0=''
    column1=''
    column2=''
    column4=''
    
    if(request.POST.has_key('Sheet')):
        table=request.POST.get('Sheet',"")

    if(request.POST.has_key('QA')):
        qa = request.POST.get('QA',"")
    if(request.POST.has_key('state')):
        state = request.POST.get('state',"")
    if(qa=='所有'):
        qa=''
    if(state=='所有'):
        state=''

    if(request.POST.has_key('sort')):
        sort = request.POST.get('sort',"")
    if(request.POST.has_key('order')):
        order = request.POST.get('order',"")

    if(request.POST.has_key('column0')):
        column0=request.POST.get('column0',"")
        
    if(request.POST.has_key('column1')):
        column1=request.POST.get('column1',"")

    if(request.POST.has_key('column2')):
        column2=request.POST.get('column2',"")

    if(request.POST.has_key('column4')):
        column4=request.POST.get('column4',"")

    sqlcountstr="select count(*) from "+table
    sqlstr="select * from "+table
    cursor.execute(sqlcountstr+" where QAer like '"+str(qa)+"%' and isFinished like '"+str(state)+"%' and column0 like '%"+str(column0)+"%' and column1 like '%"+str(column1)+"%' and column2 like '%"+str(column2)+"%' and column4 like '%"+str(column4)+"%'")
    total=cursor.fetchall()[0][u'count(*)']  
    cursor.execute(sqlstr+" where QAer like '"+str(qa)+"%' and isFinished like '"+str(state)+"%' and column0 like '%"+str(column0)+"%' and column1 like '%"+str(column1)+"%' and column2 like '%"+str(column2)+"%' and column4 like '%"+str(column4)+"%' order by "+sort+" "+order+" limit "+str(offset)+","+str(rows))
    data=cursor.fetchall()
    res['total']=total
    res['rows']=data   
    jsonRes=JSONEncoder().encode(res)
    
    
    #cursor.execute("update currentSheet set currentSheetName='"+table+"' where id=1")
    #conn.commit()
    cursor.close()
    conn.close()
    return HttpResponse(jsonRes)

def updateDataToMysql(request):
    column0=''
    qa=''
    state=''
    table=''
    if(request.POST.has_key('Sheet')):
        table=request.POST.get('Sheet',"")
    if(request.POST.has_key('column0')):
        column0 = request.POST.get('column0',"")
    if(request.POST.has_key('QAer')):
        qa = request.POST.get('QAer',"")
    if(request.POST.has_key('isFinished')):
        state = request.POST.get('isFinished',"")
    conn= MySQLdb.connect(host='192.168.131.233',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    cursor.execute('update '+table+' set isFinished="'+str(state)+'", QAer="'+str(qa)+'" where column0="'+str(column0)+'"')
    conn.commit()
    cursor.close()
    conn.close()
    return HttpResponse('')

def deleteTable(request,tablename):
    conn= MySQLdb.connect(host='192.168.131.233',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    cursor.execute("drop table if exists "+tablename)
    conn.commit
    cursor.close()
    conn.close()
    return HttpResponse('')

def exportToExcel(request,tablename):
    #table='herowarz_wang1'
    conn= MySQLdb.connect(host='192.168.131.233',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursors=conn.cursor()

    response = HttpResponse(content_type='application/vnd.ms-excel') 
    response['Content-Disposition'] = "attachment; filename="+tablename+".xls"	
    wbk = xlwt.Workbook()
    excelSheet = wbk.add_sheet(tablename)   
    row_list=[]
    cursors.execute("select column0,column1,column2,column3,column4,column5,column6,QAer,isFinished from "+tablename)
    row_list=cursors.fetchall()
    rowlen=len(row_list)
    for i in range(rowlen):
        for j in range(9):
            excelSheet.write(i,j,row_list[i][j])            
    wbk.save(response) 
    cursors.close()
    conn.close()
    return response

def findAllSqlName(request):
    conn= MySQLdb.connect(host='192.168.131.233',port = 3306,user='leiting',passwd=password,db ='leiting',charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
    cursors=conn.cursor()
    cursors.execute('SHOW TABLES')
    allSQLname=cursors.fetchall()
    tableres=[]
    sortedres=[]
    for tablename in allSQLname:
        if 'hw_' in tablename['Tables_in_leiting']:
            sql="show table status where name ='"+tablename['Tables_in_leiting']+"'"
            cursors.execute(sql)
            tableres.append({'tablename':tablename['Tables_in_leiting'],'Create_time':cursors.fetchall()[0]['Create_time']})
    tableres=sorted(tableres,key = lambda x:x['Create_time'],reverse=True)
    for sub in tableres:
        sortedres.append({'Tables_in_leiting':sub['tablename']})
    jsonRes=JSONEncoder().encode(sortedres)
    cursors.close()
    conn.close()
    return HttpResponse(jsonRes)


def getTotalResult(request,tablename):
    conn= MySQLdb.connect(host='192.168.131.233',port=3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    cursor.execute("select count(*) from "+tablename+" where isFinished='完成'")
    count_0=cursor.fetchall()[0][0]

    cursor.execute("select count(*) from "+tablename+" where isFinished='未完成'")
    count_1=cursor.fetchall()[0][0]

    cursor.execute("select count(*) from "+tablename+" where isFinished='文本已测'")
    count_2=cursor.fetchall()[0][0]

    cursor.execute("select count(*) from "+tablename+" where isFinished='暂未找到'")
    count_3=cursor.fetchall()[0][0]
    
    cursor.execute("select count(*) from "+tablename+" where isFinished='未翻译'")
    count_4=cursor.fetchall()[0][0]

    res=[{"name":"完成","y":count_0},{"name":"未完成","y":count_1},{"name":"文本已测","y":count_2},{"name":"暂未找到","y":count_3},{"name":"未翻译","y":count_4}]
    return HttpResponse(JSONEncoder().encode(res))

def getSubResult(request,tablename):
    conn= MySQLdb.connect(host='192.168.131.233',port=3306,user='leiting',passwd=password,db ='leiting',charset='utf8')
    cursor = conn.cursor()
    count_0=[]
    count_1=[]
    count_2=[]
    count_3=[]
    count_4=[]
    QAList=['黄超群','汪斌','朱军','徐勇军','请选择']
    for i in range(0,len(QAList)):
        cursor.execute("select count(*) from "+tablename+" where QAer='"+QAList[i]+"' and isFinished='完成'")
        count_0.append(cursor.fetchall()[0][0])
        cursor.execute("select count(*) from "+tablename+" where QAer='"+QAList[i]+"' and isFinished='未完成'")
        count_1.append(cursor.fetchall()[0][0])
        cursor.execute("select count(*) from "+tablename+" where QAer='"+QAList[i]+"' and isFinished='文本已测'")
        count_2.append(cursor.fetchall()[0][0])
        cursor.execute("select count(*) from "+tablename+" where QAer='"+QAList[i]+"' and isFinished='暂未找到'")
        count_3.append(cursor.fetchall()[0][0])
        cursor.execute("select count(*) from "+tablename+" where QAer='"+QAList[i]+"' and isFinished='未翻译'")
        count_4.append(cursor.fetchall()[0][0])


    res=[{"name":"完成","data":count_0},{"name":"未完成","data":count_1},{"name":"文本已测","data":count_2},{"name":"暂未找到","data":count_3},{"name":"未翻译","data":count_4}]
    
    return HttpResponse(JSONEncoder().encode(res))

def getResultIndex(request,tablename):
    return render_to_response('assign_zqjt/draw_result.html',{'tablename':json.dumps(tablename)})


