# 功能：检查scene文件夹下面的mat文件的命名是否正确
# 原理: 检查Scene文件夹下的mat文件，如果mat文件中名字或相应的路径中出现lx_demo，则报错
# 备注：目前此检查不适合lx6项目，暂时不做处理
import log
import os

path = os.path.dirname(os.path.realpath(__file__))
TARGET_FOLDER = path + "../../development/client/lx_demo/Assets/Scene"
log_str = ''

def begincheck():
	global log_str
	matdict = {}

	for dirpath,dirnames,filenames in os.walk(TARGET_FOLDER):
		for filename in filenames:
			if filename.endswith(".mat"):
				res=matdict.setdefault(filename,dirpath+filename)
				if res!=(dirpath+filename):
					show1=re.findall(r"lx_demo(.*)$",res)
					log_str+="error :"+show1[0]+"\n"
					
					show2=re.findall(r"lx_demo(.*)$",dirpath)
					log_str+="error !:"+show2[0]+filename+"\n"
					

if __name__ == '__main__':
    log.LOG_START("MatNameCheck","MatNameCheck")
    log.LOG_END("MatNameCheck","MatNameCheck")