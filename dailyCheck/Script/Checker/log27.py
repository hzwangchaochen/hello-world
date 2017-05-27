import time
import datetime
import os
import shutil


def LOG(level,suiteName,caseName,caseResult):
    caseResult=caseResult or "NULL"
    logmsg = time.strftime('%Y-%m-%d %H%M%S',time.localtime(time.time()))
    logmsg=logmsg + "|" + level + "|" + caseName + "|" + caseResult + "<br>\r\n"
    
    logfile = open(suiteName + ".log","a+")
    #logfile = open(suiteName + ".log","a+",encoding='utf-8')  
    logfile.write(logmsg)
    logfile.close()


def LOG_INFO(suiteName,caseName,caseResult):
    LOG("INFO",suiteName,caseName,caseResult)

def LOG_ERR(suiteName,caseName,caseResult):
    LOG("ERR",suiteName,caseName,caseResult)

def LOG_START(suiteName,caseName):
    LOG("StartTest",suiteName,caseName,"TestCaseStarted")
    
    
def LOG_END(suiteName,caseName):
    LOG("EndTest",suiteName,caseName,"TestCaseEnded")
