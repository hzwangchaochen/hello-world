# -*- coding: utf-8 -*-
# 功能：检查项目中是否有不符合要求的文件类型
# 原理: 目前常见的不符合要求的文件类型包括dds等
import os
import log


path = os.path.dirname(os.path.realpath(__file__))
ResPath=path+"/../../../Client/Assets/Res/"

def checkInvalidFileType(ResPath):
    for root,dirs,files in os.walk(ResPath):
        for filename in files:
            suffix=os.path.splitext(filename)[1][1:]
            suffix=suffix.lower()
            if suffix=='dds':
                log.LOG_ERR("CheckInvalidFileType", "CheckInvalidFileType", "【fileType *.dds】" + path);


if __name__ == '__main__':
    log.LOG_START("CheckInvalidFileType","CheckInvalidFileType")
    checkInvalidFileType(ResPath)
    log.LOG_END("CheckInvalidFileType","CheckInvalidFileType")


