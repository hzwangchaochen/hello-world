# -*- coding: utf-8 -*-
import os
import re
import log

pattern=re.compile(r"r[0-9]+")
path = os.path.dirname(os.path.realpath(__file__))
ResPath=path+"/../../../Client/Assets/Res/"

def processFile(ResPath):
    global res
    for root,dirs,files in os.walk(ResPath):
        for filename in files:
            suffix=os.path.splitext(filename)[1][1:]
            suffix=suffix.lower()
            if pattern.search(suffix):
                log.LOG_ERR("CheckConflictInMac", "CheckConflictInMac", "SVN conflicts on MAC. Path:" + filename);

if __name__ == '__main__':
    log.LOG_START("CheckConflictInMac","CheckConflictInMac")
    processFile(ResPath)
    log.LOG_END("CheckConflictInMac","CheckConflictInMac")