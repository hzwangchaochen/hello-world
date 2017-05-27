#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# 功能：检查一个FBX文件中，不能有两个相同的mesh文件
# 原因：因为打包会拆mesh，然后记路径，如果路径完全一样，就没办法分辨是哪一个mesh
# 原理: 还没看懂
# 备注：在检查的时候，遇到一些文件，不能从FBX文件中得到字符串后，判断是否是mesh文件的文件名，所以加了一些我自己认为的特殊检查
#       比如这个文件名后面的一个应该是Model关键词，再后面一个是Mesh关键词
#       这个是雷霆特有的规则，目前找mesh文件名的方法还不一定是完全正确的，需要找程序确认

import os
import re
import sys
import log27

import codecs

all_path_list = ['../../../Client/Assets/Res/Characters/Hero']
#all_path_list = ['../../../Client/Assets/Res/Characters','../../../Client/Assets/Res/Scenes','../../../Client/Assets/Res/Effects','../../../Client/Assets/Res/Fx']


path = os.path.dirname(os.path.realpath(__file__))


for i in range(0, len(all_path_list)):
    all_path_list[i] = path + os.sep + all_path_list[i].replace('/', os.sep)
    #print(all_path_list[i])

    

def checkWithSameFilename(filename):
    fp = open(filename,"rb")
    content = fp.read()
    fp.close()
    shows=re.findall("([\\\d\w_.<(]{4,})",content)
    b={}
    m=0
    for i in shows:
        m=m+1
        for j in range(m,len(shows)):
            if shows[j] == i and j < len(shows) -2 and shows[j+1].find("Model") != -1 and shows[j+2].find("Mesh") != -1 and len(shows[j]) > 10 and shows[j].find("_"):
                #print("=======")
                #print(shows[j])
                #print(shows[j+1])
                #print(shows[j+2])
                #print("same mesh file in fbx "+ filename + ":" + shows[j])
                log.LOG_ERR("FbxMeshCheck","FbxMeshCheck","same mesh file in fbx "+ filename + ":" + shows[j])


def listDir(path):

    if path.endswith(os.sep):
        path = path[0:-1]
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith("FBX"):
                print("begin check "+filename)
                checkWithSameFilename(dirpath + os.sep + filename)

if __name__ == '__main__':
    
    log27.LOG_START("FbxMeshCheck","FbxMeshCheck")
    for t in all_path_list:
        listDir(t)
    log27.LOG_END("FbxMeshCheck","FbxMeshCheck")


