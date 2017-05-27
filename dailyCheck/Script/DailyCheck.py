import os
import os.path
import subprocess
import time

# default values

def run(cmd):
    print(cmd)
    with os.popen(cmd) as proc:
        return proc.read()


def checkProj(bUsePython3,fileName):
    processor = fileName
    INTERPRETER = "/usr/bin/python"
    if bUsePython3: 
        INTERPRETER = "/usr/local/bin/python3"
    pargs = [INTERPRETER, processor]
    subprocess.call(pargs)

def main():
    try:
        DailyCheck()
    except Exception as e:
        print('failed', e)
        os.abort()

def DailyCheck():
    os.chdir(r"Checker")
    run('sh updateRes.sh')
    time.sleep(10)
    print("begin to analyse resources")
    checkProj(False,"analyseRes.py")

    print("begin to check guid")
    checkProj(True,"check_guid.py")

    print("begin to ui resources")
    checkProj(True,"check_ui_resource.py")

    print("begin to check materials")
    checkProj(True,"checkmat.py")

    print("begin to check file name")
    checkProj(True,"filename_check.py")

    print("begin to check material color")
    checkProj(True,"scene_mat_color_check.py")

    print("begin to check invalid file type")
    checkProj(True,"checkInvalidFileType.py")

    print("begin to check lightmap name")
    checkProj(False,"checkLightmapName.py")

    print("begin to check conflict on MAC")
    checkProj(True,"checkConflictInMac.py")

    checkProj(True,"checkInUnityEditor.py")

    os.chdir(r"../")
    print("begin to uploadLogs")
    checkProj(True,"uploadLogsNew.py")
    
if __name__ == '__main__':
    main()
