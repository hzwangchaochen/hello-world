import time
import os
import glob
import zipfile
import shutil

foldername = time.strftime('%y-%m-%d-%H-%M' + '_AutoQACheck',time.localtime(time.time()))

def run(cmd):
    print(cmd)
    with os.popen(cmd) as proc:
        return proc.read()
        
def createFolder(foldername):
    run('sh Checker/CreateFolder.sh {0}'.format(foldername))

def UpLoadLogs():
    os.chdir("Checker")
    zipFile = zipfile.ZipFile("log.zip", "w", zipfile.ZIP_DEFLATED, True)
    for fileName in glob.iglob("*.log"):
        zipFile.write(fileName)
        os.remove(fileName)
    zipFile.close()
    #upload logs
    os.system("scp -i /Users/build_leiting/jenkinsApp -P 32200  /Users/build_leiting/LX6/trunk/Tool/Script/Checker/log.zip jenkinsApp@192.168.131.107:/var/www/LX6/"+str(foldername))

    #shutil.move("log.zip","log/log_" + foldername + ".zip")
    #process log files and send emails
    os.system("ssh -i /Users/build_leiting/jenkinsApp -p 32200 jenkinsApp@192.168.131.107 'python /var/www/Checker/Process.py "+str(foldername)+"'")

if __name__ == '__main__':
    createFolder(foldername)
    UpLoadLogs()