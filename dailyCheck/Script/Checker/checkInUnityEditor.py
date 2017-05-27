import log
import sys
import os
import time
unity = '/Applications/Unity/Unity.app/Contents/MacOS/Unity'
#client_directory = os.path.abspath(os.curdir) + "\\..\\..\\..\\Client"
client_directory = "/Users/build_leiting/LX6/trunk/Client"
configuration = 'Debug'
project_code = 'lx6'
         
try:
    if sys.platform == 'win32':
        unity= 'unity'
except:
    e = sys.exc_info()[0]



def run_rc(cmd):
    rc = -1
    print(cmd)
    rc = os.system(cmd)
    if rc != 0:
        raise Exception(cmd)
    return rc

def UnityEditorCheck(scriptname):
    cmd = '{0} -quit -batchmode -projectPath {1} -executeMethod {2}'.format(unity, client_directory,scriptname)
    #cmd= '{0} -quit -batchmode -nographics -projectPath {1} -executeMethod leiting_AutoQA.AutoQAChecker.AutoQA_CheckShardeName'.format(unity, client_directory)
    print(cmd)
    rc = run_rc(cmd)

if __name__ == '__main__':
    #log.LOG_START("UnityEditorCheck","UnityEditorCheck")
    print("begin to check shader name in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckShaderName")
    time.sleep(5)

    print("begin to check model slot body transform in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckModelSlotInPrefab")
    time.sleep(5)

    print("begin to check missing scripts in prefab in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckMissingScriptInPrefab")
    time.sleep(5)

    print("begin to check missing scripts in scene in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckMissingScriptInScene")
    time.sleep(5)

    print("begin to check mesh collider in scene in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckMeshColliderInScene")
    time.sleep(5)

    print("begin to check terrain in scene in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckTerrainInScene")
    time.sleep(5)

    print("begin to check animation name in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckAnimName")
    time.sleep(5)

    print("begin to check repeated mesh in FBX in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckRepeatedMesh")
    time.sleep(5)

    print("begin to check compressed atlas in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckAtlasCompressed")
    time.sleep(5)

    print("begin to check animation in prefab and in config in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckAnimInConfig")
    time.sleep(5)

    print("begin to check renderer along with animation in characters in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckRendererWithAnimation")
    time.sleep(5)

    print("begin to check animation culling type in characters in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckCullingTypeInAnim")
    time.sleep(5)

    print("begin to check submesh count in prefab in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckSubMeshInPrefab")
    time.sleep(5)
    

    #下面的检查只挖了坑
    print("begin to check texture size in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckTextureSize")
    time.sleep(5)

    
    print("begin to check vertex and triangles in prefab in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckVertexAndTrigsInPrefab")
    time.sleep(5)

    print("begin to check the number of material in MeshRenderer in prefab in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckMatNumInMeshRenderer")
    time.sleep(5)

    print("begin to check the number of SkinnedMeshRenderer in prefab in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckSkinnedMeshRendererNumInPrefab")
    time.sleep(5)

    print("begin to check bone number in animation in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckBoneNumInAnim")
    time.sleep(5)

    print("begin to check bone number in characters in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckBoneNumInPrefab")
    time.sleep(5)

    print("begin to check AnimClip in prefab stripping in editor")
    UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckAnimClipInPrefabIsStripping")
    time.sleep(5)

    # print("begin to check animationclip legacy in editor")
    # UnityEditorCheck("leiting_AutoQA.AutoQAChecker.AutoQA_CheckAnimClipLegacy")
    # time.sleep(10)