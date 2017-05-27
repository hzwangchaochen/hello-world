#!usr/bin/python
import time
from zipfile import * 
import zipfile 
import shutil
import os
import sys
foldername=sys.argv[1]
target_dir="/var/www/LX6/"+foldername+"/"
def unzip():
    source_zip="/var/www/LX6/"+foldername+"/log.zip" 
    myzip=ZipFile(source_zip) 
    myfilelist=myzip.namelist() 
    for name in myfilelist: 
        f_handle=open(target_dir+name,"wb") 
        f_handle.write(myzip.read(name))       
        f_handle.close() 
    myzip.close() 

def copyScripts():
    #shutil.copy("/var/www/Checker/logParser.lua",  target_dir)
    shutil.copy("/var/www/Checker/logParser.py",  target_dir)
    shutil.copy("/var/www/Checker/SendResultMail.py",  target_dir)

def processScripts():
    os.chdir(target_dir)
    #cmd='lua -e "timestamp=\''+foldername+'\'" '+target_dir+'logParser.lua'
    cmd="python "+target_dir+"logParser.py "+foldername
    print(cmd)
    os.system(cmd)
    os.system("python "+target_dir+"SendResultMail.py")
if __name__ == '__main__':
    unzip()
    copyScripts()
    processScripts()