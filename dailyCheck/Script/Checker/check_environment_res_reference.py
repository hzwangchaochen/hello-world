#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 检查项目Client/Assets/Res/下面的图片是否在项目存在引用
#规则就是guid应该被其他文件引用到
# 功能：检查项目Client/Assets/Res/下的部分美术资源是否被正常引用
# 原理: 需要被其他文件引用的美术资源文件的guid应该被相应的其他文件引用到，包括：
#       1、tag、psd等图片文件的guid被mat文件引用
#       2、mat文件的guid被prefab或者unity引用
#       
# 备注：1、目前只有两种格式的图片被检查，后续还要根据实际情况添加其他美术资源
#       2、Animation资源也会被prefab直接引用
#       3、UI texture里面会出现直接引用图片的情况，情况很少，LX6也不到1%是这样做的

import os
import re
import sys

import log

path = os.path.dirname(os.path.realpath(__file__))

TARGET_FOLDER = path + "/../../../Client/Assets/Res/"
#PREFAB_FOLDER = path + "/../../development/client/lx_demo/Assets/Resources/Prefab/"

NEED_CHECK_RES_ENDS = ['.tga']

MATRIALS_ENDS = ['.mat']

PREFAB_ENDS = ['.prefab']


all_res_guid_dic = {}
all_mat_guid_dic = {}
all_matrials_txt_list = []
all_prefab_txt_list = []


def _check_res(folder_path):
    global all_matrials_txt_list
    global all_mat_guid_dic
    global all_prefab_txt_list
    for root,dirs,files in os.walk(folder_path):
        for filename in files:
            fpath = os.path.join(root + os.sep + filename)
            endstr = os.path.splitext(fpath)[1]
            if endstr.lower() in NEED_CHECK_RES_ENDS:
                f = open(fpath + '.meta', 'r', encoding='utf-8')
                meta_txt = f.read()
                f.close()
                rs = re.findall('guid\: (\w+)', meta_txt)
                if len(rs) <= 0:
                    print('res:'+fpath+' meta文件存在问题') 
                    log.LOG_ERR("ResourcesReferenceCheck","ResourcesReferenceCheck",'res:'+fpath+' meta file has error')
                else:
                    all_res_guid_dic[fpath] = rs[0]
                    
            if endstr.lower() in MATRIALS_ENDS:
                f = open(fpath, 'r', encoding='utf-8')
                mat_str = f.read()
                f.close()
                all_matrials_txt_list.append(mat_str)

                f = open(fpath + '.meta', 'r', encoding='utf-8')
                meta_txt = f.read()
                f.close()
                rs = re.findall('guid\: (\w+)', meta_txt)
                if len(rs) <= 0:
                    #log_str += 'res:'+fpath+' meta文件存在问题'
                    log.LOG_ERR("ResourcesReferenceCheck","ResourcesReferenceCheck",'res:'+fpath+' meta file has error')
                else:
                    all_mat_guid_dic[fpath] = rs[0]

            if endstr.lower() in PREFAB_ENDS:
                f = open(fpath, 'r', encoding='utf-8')
                prefab_txt = f.read()
                f.close()
                all_prefab_txt_list.append(prefab_txt)


def _check_res_guid_in_matrials():
    global all_matrials_txt_list
    global all_mat_guid_dic
    global all_prefab_txt_list
    for keys in all_res_guid_dic.keys():
        find = False
        for mat_str in all_matrials_txt_list:
            if all_res_guid_dic[keys] in mat_str:
                find = True
                break
        if find is False:
            #log_str += 'res:' + keys + ' 没有被任何材质球引用\n'
            #(keys)
            log.LOG_ERR("ResourcesReferenceCheck","ResourcesReferenceCheck",'res:' + keys + ' not reference by any matrials')
            
            
def _check_mat_in_prefab_and_scene():
    global all_matrials_txt_list
    global all_mat_guid_dic
    global all_prefab_txt_list

    for keys in all_mat_guid_dic.keys():
        find = False
        for prefab_txt in all_prefab_txt_list:
            if all_mat_guid_dic[keys] in prefab_txt:
                find = True
                break
        if find is False:
            #print(keys)
            log.LOG_ERR("ResourcesReferenceCheck","ResourcesReferenceCheck",'res:' + keys + ' not reference by any prefab')            

if __name__ == '__main__':
    
    log.LOG_START("ResourcesReferenceCheck","ResourcesReferenceCheck")

    _check_res(TARGET_FOLDER)
    #resguidFile=open('resguidFile.txt','w')
    #resguidFile.write(''.join('{0}\nguid:{1}'.format(key, val)+'\n' for key, val in all_res_guid_dic.items()))
    #resguidFile.close()
    
    # allMatFile=open('allMatFile.txt','w')
    # allMatFile.write(''.join(r'{0}\n'.format(val) for val in all_matrials_txt_list))
    # allMatFile.close()

    #allMatDictFile=open('allMatDictFile.txt','w')
    #allMatDictFile.write(''.join(r'{0}\n{1}\n'.format(key,val) for key,val in all_mat_guid_dic.items()))
    #allMatDictFile.close()
    
    #_check_res(PREFAB_FOLDER)

    #_check_res_guid_in_matrials()
    #_check_mat_in_prefab_and_scene() 
    
    log.LOG_END("ResourcesReferenceCheck","ResourcesReferenceCheck")





