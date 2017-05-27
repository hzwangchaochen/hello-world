# 功能：检查项目下png为后缀的UI资源是否符合要求
# 原理: 1、检查png文件名的后缀名，要求是小写的png
#         2、通过文件头判断图片是否为png格式，png文件的头标识是89 50 4E 47 0D 0A 1A 0A
#         3、检查button目录，button目录下的png文件要长宽一致
# 备注：LX6的png文件和button目录还不明确，明确后再加入到静态资源检查中

import os
import re
import struct
import sys
import log

path = os.path.dirname(os.path.realpath(__file__))
TARGET_FOLDER = {(path + "/../../development/client/lx_demo/Assets/Art/UI").replace('/',os.sep),
 (path + "/../../development/client/lx_demo/Assets/Resources/Images").replace('/',os.sep)}
BUTTON_FOLDER = {(path + "/../../development/client/lx_demo/Assets/Resources/Images/Icon").replace('/',os.sep)}

# 字节码转16进制字符串 
def bytes2hex(bytes): 
    num = len(bytes) 
    hexstr = u"" 
    for i in range(num): 
        t = u"%x" % bytes[i] 
        if len(t) % 2: 
            hexstr += u"0"
        hexstr += t 
    return hexstr.upper() 

def begincheck():
    for folder in TARGET_FOLDER:
        for root, dirs, files in os.walk(folder):
            for filename in files:
                fpath = os.path.join(root + os.sep + filename)
                endstr = os.path.splitext(fpath)[1]
                if endstr == '.PNG' or endstr == '.Png':
                    log.LOG_ERR("UIResourcesCheck","UIResourcesCheck",fpath+' 后缀名错误\n')
                if endstr == ".png":
                    fb = open(fpath, 'rb')
                    png_head = fb.read(8)
                    fb.close()
                    hbytes = struct.unpack_from("B"*8, png_head) 
                    f_hcode = bytes2hex(hbytes) 
                    if f_hcode != "89504E470D0A1A0A":
                        log.LOG_ERR("UIResourcesCheck","UIResourcesCheck",fpath+' 不是真的png\n')
    for folder in BUTTON_FOLDER:
        for root, dirs, files in os.walk(folder):
            for filename in files:
                fpath = os.path.join(root + os.sep + filename)
                endstr = os.path.splitext(fpath)[1]
                if endstr == ".png":
                    f = open(fpath, 'rb')
                    f.seek(16)
                    width = f.read(4)
                    f.seek(20)
                    height = f.read(4)
                    f.close()
                    if width != height:
                        log.LOG_ERR("UIResourcesCheck","UIResourcesCheck",fpath+' 宽高不一致\n')

if __name__ == '__main__':
    log.LOG_START("UIResourcesCheck","UIResourcesCheck")
    log.LOG_END("UIResourcesCheck","UIResourcesCheck")