# 功能：检查项目中.meta文件的guid是否发生变化
# 原理: 1、通过shell的diff功能，找到所有meta文件中guid是否有变化
#       2、shell脚本参考checkguid.sh文件
# 备注：目前以下.meta文件的guid发生变化可以忽略
#       1、cs文件、dll文件和unity文件的guid改变可以忽略
#       2、Animation底下的FBX.meta文件不会被引用，可以过滤掉这个检查
import os
import log

if __name__ == '__main__':
    log.LOG_START("GuidCheck","GuidCheck")
    ss=os.popen("sh checkguid.sh").readlines()
    for index in range(0,int(len(ss)/2)):
        log.LOG_ERR("GuidCheck","GuidCheck","【guid_changed】"+ss[2*index+1].strip('\n')+"@"+ss[2*index].strip('\n'))
    log.LOG_END("GuidCheck","GuidCheck")


