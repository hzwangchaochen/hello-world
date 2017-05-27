# -*- coding: utf-8 -*-
# 功能：做一个烘焙的lightmap静态扫描
# 原理: 1：目录 ： Assets\Res\Scenes\ 2: 所有lightmap开头的，light.exr结尾的费meta文件 3、Lightmap-后面的数字一定是0
import os
import log27

def checkLightmapName(ResPath):
    for root,dirs,files in os.walk(ResPath):
        for filename in files:
            if filename[:8]=='Lightmap' and filename[-4:]=='.exr':
                if filename[:10]!='Lightmap-0':
                    log27.LOG_ERR("CheckLightmapName", "CheckLightmapName", root+filename+" 同一个场景中烘焙的lightmap数量大于1");

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    ResPath=path+"/../../../Client/Assets/Res/Scenes/"
    os.chdir(ResPath)
    processPath=os.getcwd()
    os.chdir(path)
    log27.LOG_START("CheckLightmapName","CheckLightmapName")
    checkLightmapName(processPath)
    log27.LOG_END("CheckLightmapName","CheckLightmapName")


