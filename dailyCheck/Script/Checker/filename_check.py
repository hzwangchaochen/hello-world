# 功能：检查项目下所有的文件是否正确命名
# 原理: 遍历项目下所有的文件，如果发现文件名中出现以下内容：中文、@、空格，则表示文件名没有正确命名
import os
import re
import sys

import log

#all_path_list = ['../../../Client/Assets/Res/Sound']
all_path_list = ['../../../Client/Assets/Res']


path = os.path.dirname(os.path.realpath(__file__))
#print(path)

OUT_LOG_PATH = (path + '/FileNameCheck.log').replace('/',os.sep)
#print(OUT_LOG_PATH)
#LOG_INFO("BuildMonitor","BuildMonitor","deleted client,gametest")

for i in range(0, len(all_path_list)):
    all_path_list[i] = path + os.sep + all_path_list[i].replace('/', os.sep)
    #print(all_path_list[i])

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

def listDir(path):

    if path.endswith(os.sep):
        path = path[0:-1]
    for dirpath, dirnames, filenames in os.walk(path):
        show=re.findall("Client(.*)$",dirpath)
        if dirpath.find(".svn") != -1:
            continue
        for dirname in dirnames:
            if dirname.find(".svn") != -1:
                continue
            if dirname.find(" ") != -1:
                pass
                #log.LOG_ERR("filenameCheck","filenameCheck_dir_kongge",dirname)
            #is chinese
            match = zhPattern.search(dirname)
            if match:
                log.LOG_ERR("FileNameCheck","FileNameCheck","【dir_chinese】" + dirname)
            if dirname.find("@") != -1:
                log.LOG_ERR("FileNameCheck","FileNameCheck","【dir_@】" + dirname)
            #if dirname.find("#") != -1 and filename.find("Animation") != -1:
                #log.LOG_ERR("filenameCheck","filenameCheck","【dir_#】" + dirname)
            if len(dirname) != len(dirname.strip()):
                log.LOG_ERR("FileNameCheck","FileNameCheck","【dir_space】" + dirname)
        for filename in filenames:
            if filename.endswith("meta"):
                pass
            else:
                if filename.find(" ") != -1:
                    pass
                    #log.LOG_ERR("filenameCheck","filenameCheck_file_kongge",show[0] + os.sep + filename)
                match = zhPattern.search(filename)
                if match:
                    log.LOG_ERR("FileNameCheck","FileNameCheck","【file_chinese】" + show[0] + os.sep + filename)
                if filename.find("@") != -1:
                    log.LOG_ERR("FileNameCheck","FileNameCheck","【file_@】" + show[0] + os.sep + filename)
                #if filename.find("#") != -1 and show[0].find("Animation") == -1:
                    #log.LOG_ERR("filenameCheck","filenameCheck","【file_#】" + show[0] + os.sep + filename)
                filename2 = filename.split('.')[0]
                if len(filename2) != len(filename2.strip()):
                    log.LOG_ERR("FileNameCheck","FileNameCheck","【file_space】" + show[0] + os.sep + filename)


if __name__ == '__main__':
    
    log.LOG_START("FileNameCheck","FileNameCheck")
    for t in all_path_list:
        listDir(t)
    log.LOG_END("FileNameCheck","FileNameCheck")

    #if(len(sys.argv) > 1):
     #   print(log_str)
    #else:
     #   f = open(OUT_LOG_PATH, 'a', encoding='utf-8')
     #   f.write(log_str)
     #   f.flush()
     #   f.close()


