# 功能：检查项目下所有scene使用的mat是不是正确的设置过color
# 原理: 查找scene目录下的mat文件，匹配到name:_Color second: {r:1,g:1,b:1,a:1}，
#       second后面大括号里面就表示mat文件使用的颜色，如果不是白色则表示没有正确设置
# 备注：目前LX6项目scene使用的mat地址还不明确，待以后确认之后就进行相应的更改
import sys
import os
import re
import log


path = os.path.dirname(os.path.realpath(__file__))

TARGET_FOLDER = path +os.sep+ "../../../Client/Assets/Res/Scenes"
 
def _check_mat_color_setting(path_str):
	print(path_str)
	for root,dirs,files in os.walk(path_str):
		print(root)
		for filename in files:
			fpath = os.path.join(root + os.sep + filename)
			endstr = os.path.splitext(fpath)[1]
			print(fpath)
			print(endstr)
			if endstr.lower() == '.mat':
				f = open(fpath,'r')
				meta_txt = f.read()
				f.close()
				rs = re.findall('name\:\ _Color\n.*second\:\ \{(.*?)\}', meta_txt)
				# 不符合白色_Color都是错的
				if len(rs) > 0 and rs[0] != 'r: 1, g: 1, b: 1, a: 1':
					print('fpath:'+fpath+' 颜色没有设置成白色\n')
					log.LOG_ERR("SceneMatColorCheck","SceneMatColorCheck",'fpath:'+fpath+' 颜色没有设置成白色\n')

if __name__ == '__main__':
	log.LOG_START("SceneMatColorCheck","SceneMatColorCheck")
	#_check_mat_color_setting(TARGET_FOLDER)
	log.LOG_END("SceneMatColorCheck","SceneMatColorCheck")
