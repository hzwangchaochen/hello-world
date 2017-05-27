# -*- coding: utf-8 -*-
#在资源提交前进行检查：
#1、对于add文件的提交，则资源文件要和对应的meta文件一起提交；
#2、对于delete文件的提交，则资源文件要和对应的meta文件一起删除。
import sys
import subprocess
import os
#argv[0] script
#argv[1] file list
#argv[2]  
#argv[3] Log Message File
#argv[4] work path   
commitFile=sys.argv[1]
workPath=sys.argv[4]
fileList=[]

def getCommitFileList():
    global fileList
    if(os.path.isfile(commitFile)):
        data=open(commitFile,"r")
        for line in data:
            fileList.append(os.path.basename(line).strip())
def main():
    flag=True
    command="svn status"
    sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,cwd=workPath)
    res=sp.stdout.readlines()

    for line in res:
        line=line.decode('utf-8')
        commitType=line.split('   ')[0].strip()
        if commitType=='A':
            fileName=line.split('   ')[2].strip()
            if os.path.splitext(fileName)[1]!='.meta':
                if fileName+'.meta' not in fileList:
                    flag=False
                    sys.stderr.write('you must add '+fileName+'.meta if you want to add file '+fileName+'\r\n')

        if commitType=='D':
            fileName=line.split('   ')[2].strip()
            if os.path.splitext(fileName)[1]!='.meta':
                if fileName+'.meta' not in fileList:
                    flag=False
                    sys.stderr.write('you must delete '+fileName+'.meta if you want to delete file '+fileName+'\r\n')

    if flag==False:
        exit(1)
    else:
        exit(0)

if __name__ == '__main__':
    getCommitFileList()
    main()
    
