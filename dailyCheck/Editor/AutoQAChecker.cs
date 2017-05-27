#define DETACH_SHADER

using LX6.Utils;
using LX6.Share;
using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;
using System.IO;
using System.Collections.Generic;
using LX6.Engine;
using LT.ConfigGen;
using LTClient.Action;

#pragma warning disable 0618
#pragma warning disable 1692

namespace leiting_AutoQA
{
    public class AutoQAChecker : ScriptableObject
    {
        public static List<string> logList = new List<string>();
        public static List<string> logErrorList = new List<string>();
        public static string curDir = Directory.GetCurrentDirectory();
        public static string dirPath = curDir + "/../Tool/Script/Checker/";

        //用于检查特效
        public static Dictionary<string, EffectConfig> effectDict;

        public static void LogWarning(string log, Object context = null)
        {
            if (!logList.Contains(log))
            {
                logList.Add(log);
                Debug.LogWarning(log, context);
            }
        }

        public static void LogError(string log, Object context = null)
        {
            //log = EditorApplication.currentScene + log;
            if (!logErrorList.Contains(log))
            {
                logErrorList.Add(log);
                if (context != null)
                    Debug.LogError(log, context);
                else
                    Debug.LogError(log);
            }
        }

        public static bool ShouldDetach(string assetPath)
        {
            if (string.IsNullOrEmpty(assetPath))
            {
                return false;
            }

            foreach (string str in BundleConsts.BUILT_IN_MESH_NAME)
            {
                if (assetPath.Contains(str))
                {
                    return false;
                }
            }
            return true;
        }


        static string GetRelativeAssetPath(string _fullPath)
        {
            _fullPath = GetRightFormatPath(_fullPath);
            int idx = _fullPath.IndexOf("Assets");
            string assetRelativePath = _fullPath.Substring(idx);
            return assetRelativePath;
        }

        static string GetRightFormatPath(string _path)
        {
            return _path.Replace("\\", "/");
        }

        [MenuItem("Tools/AutoQA/CheckShaderName", false, 1)]
        public static void AutoQA_CheckShaderName()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckShaderNameInEditor");
            autoQALog.LOG_START("CheckShaderNameInEditor", "CheckShaderNameInEditor");
            string[] matpaths = Directory.GetFiles("Assets/Res", "*.mat", SearchOption.AllDirectories);
            foreach (string matpath in matpaths)
            {
                if (matpath.Contains("Test") ||
                    matpath.Contains("test") ||
                    matpath.Contains("Res/Font") ||
                    matpath.Contains("Res/Textures/UI") ||
                    matpath.Contains("Res/Prefab/GUI"))
                {
                    continue;
                }

                string propermatpath = GetRelativeAssetPath(matpath);
                //Debug.Log("now check the file: " + matpath + "   the relative path is : " + propermatpath);
                Material mat = (Material)AssetDatabase.LoadAssetAtPath(propermatpath, typeof(Material));
                if (mat && !mat.shader)
                {
                    autoQALog.LOG_ERR("CheckShaderNameInEditor", "CheckShaderNameInEditor", matpath + " 材质球的shader丢失");
                }
                else
                {
                    if (!mat.shader.name.Contains("LX6") && !mat.shader.name.Contains("L10"))
                    {
                        autoQALog.LOG_ERR("CheckShaderNameInEditor", "CheckShaderNameInEditor", matpath + " 材质球使用了错误的shader类型: " + mat.shader.name);
                    }
                }
            }
            autoQALog.LOG_END("CheckShaderNameInEditor", "CheckShaderNameInEditor");
            autoQALog.closeFile();
        }


        //项目中所有prefab中ModelSlot脚本中body节点的Transform的Position、Rotation都为（0,0,0），Scale为（1,1,1）
        [MenuItem("Tools/AutoQA/CheckModelSlotInPrefab", false, 2)]
        public static void AutoQA_CheckModelSlotInPrefab()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckModelSlotInPrefabInEditor");
            autoQALog.LOG_START("CheckModelSlotInPrefabInEditor", "CheckModelSlotInPrefabInEditor");
            string[] prefabsPath = Directory.GetFiles("Assets/Res/Prefab/Character", "*.prefab", SearchOption.AllDirectories);
            foreach (var path in prefabsPath)
            {
                GameObject prefab = AssetDatabase.LoadMainAssetAtPath(path) as GameObject;
                List<GameObject> list = new List<GameObject>();
                list.AddRange(UnitUtils.GetAllChild(prefab));
                foreach (GameObject go in list)
                {
                    var component = go.GetComponent<ModelSlot>();
                    if (component != null)
                    {
                        if (component.body == null)
                        {
                            Debug.LogWarning(path + "的" + go.name + "上modelSlot脚本中没有配置body");
                            autoQALog.LOG_WARN("CheckModelSlotInPrefabInEditor", "CheckModelSlotInPrefabInEditor", path + "的" + go.name + "上modelSlot脚本中没有配置body");
                            continue;
                        }
                        if (component.body.localPosition != new Vector3(0.0f, 0.0f, 0.0f))
                        {
                            autoQALog.LOG_WARN("CheckModelSlotInPrefabInEditor", "CheckModelSlotInPrefabInEditor", path + "的" + go.name + "上modelSlot脚本中body的Position不等于（0,0,0）");
                            //Debug.LogWarning(path + "的" + go.name + "上modelSlot脚本中body的Position不等于（0,0,0）");
                        }
                    }
                }
            }
            autoQALog.LOG_END("CheckModelSlotInPrefabInEditor", "CheckModelSlotInPrefabInEditor");
            autoQALog.closeFile();
        }

        //查找项目中所有prefab里面是否有丢失的脚本
        [MenuItem("Tools/AutoQA/CheckMissingScriptInPrefab", false, 3)]
        public static void AutoQA_CheckMissingScriptInPrefab()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckMissingScriptInPrefabInEditor");
            autoQALog.LOG_START("CheckMissingScriptInPrefabInEditor", "CheckMissingScriptInPrefabInEditor");

            int missingNum = 0;
            int goNum = 0;

            string[] prefabsPath = Directory.GetFiles("Assets", "*.prefab", SearchOption.AllDirectories);

            List<GameObject> list = new List<GameObject>();
            foreach (var path in prefabsPath)
            {
                GameObject prefab = AssetDatabase.LoadMainAssetAtPath(path) as GameObject;
                list.Clear();
                list.AddRange(UnitUtils.GetAllChild(prefab));

                goNum += list.Count;
                for (int i = 0; i < list.Count; i++)
                {
                    //var components = list[i].GetComponents<Component>();
                    var components = list[i].GetComponents<MonoBehaviour>();
                    for (int j = 0; j < components.Length; j++)
                    {
                        // Check if the ref is null
                        if (components[j] == null)
                        {
                            autoQALog.LOG_ERR("CheckMissingScriptInPrefabInEditor", "CheckMissingScriptInPrefabInEditor", path + "的" + list[i].name + "上丢失脚本");
                            Debug.LogWarning("需要清理脚本的prefab路径：" + path);
                            missingNum++;
                            break;
                        }
                    }
                }
            }
            autoQALog.LOG_END("CheckMissingScriptInPrefabInEditor", "CheckMissingScriptInPrefabInEditor");
            autoQALog.closeFile();
            Debug.Log(string.Format("遍历{0}个prefab，一共有{1}个prefab脚本丢失", goNum, missingNum));
        }

        //查找项目中所有scene里面是否有丢失的脚本
        [MenuItem("Tools/AutoQA/CheckMissingScriptInScene", false, 4)]
        public static void AutoQA_CheckMissingScriptInScene()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckMissingScriptInSceneInEditor");
            autoQALog.LOG_START("CheckMissingScriptInSceneInEditor", "CheckMissingScriptInSceneInEditor");
            foreach (EditorBuildSettingsScene S in EditorBuildSettings.scenes)
            {
                //在built setting中是否已经开启
                if (S.enabled)
                {
                    //得到场景的名称
                    string name = S.path;
                    Debug.Log(name);
                    //打开这个场景
                    try
                    {
                        EditorSceneManager.OpenScene(name);
                        //EditorApplication.OpenScene(name);
                        //遍历场景中的GameObject
                        foreach (GameObject obj in FindObjectsOfType(typeof(GameObject)))
                        {
                            var components = obj.GetComponents<MonoBehaviour>();
                            for (int j = 0; j < components.Length; j++)
                            {

                                // Check if the ref is null
                                if (components[j] == null)
                                {
                                    //Debug.Log("场景" + name + "的" + obj.name + "中丢失脚本");
                                    autoQALog.LOG_ERR("CheckMissingScriptInSceneInEditor", "CheckMissingScriptInSceneInEditor", "场景：" + name + "的" + obj.name + "中丢失脚本");
                                }
                                else
                                {
                                    //Debug.Log(components[j].name);
                                }
                            }
                        }
                    }
                    catch (System.Exception e)
                    {
                        autoQALog.LOG_ERR("CheckMissingScriptInSceneInEditor", "CheckMissingScriptInSceneInEditor", "场景：" + name + "无法打开");
                        //Debug.LogError(e.Message);
                    }

                }
            }
            autoQALog.LOG_END("CheckMissingScriptInSceneInEditor", "CheckMissingScriptInSceneInEditor");
            autoQALog.closeFile();
        }

        //查找项目中所有scene里面是否有mesh collider
        [MenuItem("Tools/AutoQA/CheckMeshColliderInScene", false, 5)]
        public static void AutoQA_CheckMeshColliderInScene()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckMeshColliderInSceneInEditor");
            autoQALog.LOG_START("CheckMeshColliderInSceneInEditor", "CheckMeshColliderInSceneInEditor");
            foreach (EditorBuildSettingsScene S in EditorBuildSettings.scenes)
            {
                //在built setting中是否已经开启
                if (S.enabled)
                {
                    //得到场景的名称
                    string name = S.path;
                    Debug.Log(name);
                    //打开这个场景
                    try
                    {
                        EditorSceneManager.OpenScene(name);
                        //EditorApplication.OpenScene(name);
                        //遍历场景中的GameObject
                        foreach (GameObject obj in FindObjectsOfType(typeof(GameObject)))
                        {
                            MeshCollider[] meshColliders = obj.GetComponents<MeshCollider>();
                            if (meshColliders != null && meshColliders.Length > 0)
                            {
                                autoQALog.LOG_WARN("CheckMeshColliderInSceneInEditor", "CheckMeshColliderInSceneInEditor", "场景：" + name + "的" + obj.name + "中包含MeshCollider");
                                //Debug.LogWarning("场景：" + name + "的" + obj.name + "中包含MeshCollider");
                            }
                        }
                    }
                    catch (System.Exception e)
                    {
                        //autoQALog.LOG_WARN("CheckMeshColliderInSceneInEditor", "CheckMeshColliderInSceneInEditor", "场景：" + name + "无法打开");
                        Debug.LogWarning(e.Message);
                    }
                }
            }
            autoQALog.LOG_END("CheckMeshColliderInSceneInEditor", "CheckMeshColliderInSceneInEditor");
            autoQALog.closeFile();
        }

        //查找项目中所有scene里面是否有Terrain
        [MenuItem("Tools/AutoQA/CheckTerrainInScene", false, 16)]
        public static void AutoQA_CheckTerrainInScene()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckTerrainInSceneInEditor");
            autoQALog.LOG_START("CheckTerrainInSceneInEditor", "CheckTerrainInSceneInEditor");
            foreach (EditorBuildSettingsScene S in EditorBuildSettings.scenes)
            {
                //在built setting中是否已经开启
                if (S.enabled)
                {
                    //得到场景的名称
                    string name = S.path;
                    Debug.Log(name);
                    //打开这个场景
                    try
                    {
                        EditorSceneManager.OpenScene(name);
                        //EditorApplication.OpenScene(name);
                        //遍历场景中的GameObject
                        foreach (GameObject obj in FindObjectsOfType(typeof(GameObject)))
                        {
                            var Terrains = obj.GetComponents<Terrain>();
                            if (Terrains != null && Terrains.Length > 0)
                            {
                                autoQALog.LOG_WARN("CheckTerrainInSceneInEditor", "CheckTerrainInSceneInEditor", "场景：" + name + "包含Terrain，应该转成模型");
                                //Debug.LogWarning("场景：" + name + "包含Terrain，应该转成模型");
                            }
                        }
                    }
                    catch (System.Exception e)
                    {
                        //autoQALog.LOG_WARN("CheckTerrainInSceneInEditor", "CheckTerrainInSceneInEditor", "场景：" + name + "无法打开");
                        Debug.LogWarning(e.Message);
                    }
                }
            }
            autoQALog.LOG_END("CheckTerrainInSceneInEditor", "CheckTerrainInSceneInEditor");
            autoQALog.closeFile();
        }


        //查找项目中所有的animation的名字（m_Name）是否与文件名一致
        [MenuItem("Tools/AutoQA/CheckAnimName", false, 17)]
        public static void AutoQA_CheckAnimName()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckAnimNameInEditor");
            autoQALog.LOG_START("CheckAnimNameInEditor", "CheckAnimNameInEditor");
            //var path = curDir+ "\\Assets\\Res\\Prefab\\Animation\\B002_bianbai10.anim";
            string[] AnimsPath = Directory.GetFiles("Assets", "*.anim", SearchOption.AllDirectories);
            foreach (var path in AnimsPath)
            {
                Debug.LogWarning(path);
                AnimationClip Anim = AssetDatabase.LoadAssetAtPath<AnimationClip>(path);
                string[] pathArray = path.Split(new char[2] { '\\', '/' });
                Debug.LogWarning(pathArray[pathArray.Length - 1]);
                if (Anim.name != pathArray[pathArray.Length - 1].Split('.')[0])
                {
                    autoQALog.LOG_ERR("CheckAnimNameInEditor", "CheckAnimNameInEditor", "The animation name in " + path + " is not equal to its file name");
                    Debug.LogWarning("not equal");
                }
                //Debug.LogWarning(Anim.name);             
                //var serializedObject = new SerializedObject(Anim);
                //var prop = serializedObject.FindProperty("m_Name");
                //Debug.LogWarning(prop.stringValue);
            }
            autoQALog.LOG_END("CheckAnimNameInEditor", "CheckAnimNameInEditor");
            autoQALog.closeFile();
        }

        //检查fbx中是否重复引用相同的mesh
        [MenuItem("Tools/AutoQA/CheckRepeatedMesh", false, 18)]
        public static void AutoQA_CheckRepeatedMesh()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckRepeatedMeshInEditor");
            autoQALog.LOG_START("CheckRepeatedMeshInEditor", "CheckRepeatedMeshInEditor");

            string[] FBXPath = Directory.GetFiles("Assets", "*.FBX", SearchOption.AllDirectories);

            string[] fbxPath = Directory.GetFiles("Assets", "*.fbx", SearchOption.AllDirectories);

            string[] Fbxpath = new string[FBXPath.Length + fbxPath.Length];

            FBXPath.CopyTo(Fbxpath, 0);
            fbxPath.CopyTo(Fbxpath, FBXPath.Length);

            foreach (var path in Fbxpath)
            {
                CheckRepeatedMesh(path, autoQALog);
            }
            autoQALog.LOG_END("CheckRepeatedMeshInEditor", "CheckRepeatedMeshInEditor");
            autoQALog.closeFile();
        }

        private static void CheckRepeatedMesh(string path, AutoQALog autoQALog)
        {
            GameObject go = AssetDatabase.LoadAssetAtPath<GameObject>(path);
            List<Mesh> mhs = new List<Mesh>();
            MeshFilter[] mfs = go.GetComponentsInChildren<MeshFilter>();
            SkinnedMeshRenderer[] smrs = go.GetComponentsInChildren<SkinnedMeshRenderer>();


            if (mfs.Length > 0)
            {
                foreach (var mf in mfs)
                {
                    Mesh m = mf.sharedMesh;
                    if (!mhs.Contains(m))
                        mhs.Add(m);
                }
            }
            if (smrs.Length > 0)
            {
                foreach (var smr in smrs)
                {
                    Mesh m = smr.sharedMesh;
                    if (!mhs.Contains(m))
                        mhs.Add(m);
                }
            }
            if (mhs.Count > 0)
            {
                for (int i = 0; i < mhs.Count; i++)
                {
                    for (int j = i + 1; j < mhs.Count; j++)
                    {
                        string path1 = AssetDatabase.GetAssetPath(mhs[i]);
                        string path2 = AssetDatabase.GetAssetPath(mhs[j]);
                        string name1 = mhs[i].name;
                        string name2 = mhs[j].name;
                        if (name1 == name2 && path1 == path2 && mhs[i] != mhs[j])
                        {
                            autoQALog.LOG_ERR("CheckRepeatedMeshInEditor", "CheckRepeatedMeshInEditor", path + " uses identical copies of the same mesh file");
                            return;
                            //Debug.LogError("模型不允许出现同名子面片，返回去修改！" + "错误文件：" + path, go);
                        }
                    }
                }
            }

        }

        //检查特效中每个anim中的骨骼数是否超标
        //检查骨骼的数量有两种方法：一个是检索动画文件，然后遍历其中path关键词有多少个，一个path就相当于一个节点。一个就是用unity自带的函数
        //todo ：动作文件大小检查（1M临界点）
        [MenuItem("Tools/AutoQA/CheckBoneNumInAnim", false, 19)]
        public static void AutoQA_CheckBoneNumInAnim()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckBoneNumInAnimInEditor");
            autoQALog.LOG_START("CheckBoneNumInAnimInEditor", "CheckBoneNumInAnimInEditor");

            //string[] effectsFilePath = Directory.GetFiles("Assets/Res/Effects", "*.prefab", SearchOption.AllDirectories);
            //foreach (string path in effectsFilePath)
            //{
            //    CheckBoneNumInAnim(path, 0, autoQALog);
            //}

            autoQALog.LOG_END("CheckBoneNumInAnimInEditor", "CheckBoneNumInAnimInEditor");
            autoQALog.closeFile();
        }

        public static void CheckBoneNumInAnim(string path, int type, AutoQALog autoQALog)
        {
            GameObject tmpPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(path);
            Animation[] anims = tmpPrefab.GetComponentsInChildren<Animation>();
            if (anims == null || anims.Length < 1)
            {
                //Debug.LogWarning(path + " 里面没有animation");
                return;
            }
            for (int i = 0; i < anims.Length; i++)
            {
                foreach (AnimationState animState in anims[i])
                {
                    AnimationClip currentClip = animState.clip;
                    if (currentClip == null) break;
                    try
                    {
                        AnimationClipCurveData[] animCurve = AnimationUtility.GetAllCurves(currentClip);
                        List<string> bonePathList = new List<string>();
                        if (animCurve == null || animCurve.Length < 1) break;
                        for (int k = 0; k < animCurve.Length; k++)
                        {
                            if (!bonePathList.Contains(animCurve[k].path))
                            {
                                bonePathList.Add(animCurve[k].path);
                            }
                        }
                        if (type == 0 && bonePathList.Count > 10)
                            autoQALog.LOG_WARN("CheckBoneNumInAnimInEditor", "CheckBoneNumInAnimInEditor", "【特效动作的骨骼数大于10】" + path + ": The num of bone in " + currentClip.name + ".anim is " + bonePathList.Count + ".");
                        else if (type == 1 && bonePathList.Count > 50)
                            autoQALog.LOG_WARN("CheckBoneNumInAnimInEditor", "CheckBoneNumInAnimInEditor", "【角色动作的骨骼数大于50】" + path + ": The num of bone in " + currentClip.name + ".anim is " + bonePathList.Count + ".");
                    }
                    catch (System.Exception e)
                    {
                        Debug.LogWarning(e.Message);
                    }
                }
            }
        }


        //检查character中的animation组件上要有一个Renderer组件
        [MenuItem("Tools/AutoQA/CheckRendererWithAnimation", false, 20)]
        public static void AutoQA_CheckRendererWithAnimation()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckRendererWithAnimationInEditor");
            autoQALog.LOG_START("CheckRendererWithAnimationInEditor", "CheckRendererWithAnimationInEditor");
            string[] characterFilePaths = Directory.GetFiles("Assets/Res/Prefab/Character", "*.prefab", SearchOption.AllDirectories);
            foreach (var path in characterFilePaths)
            {
                GameObject prefab = AssetDatabase.LoadMainAssetAtPath(path) as GameObject;
                Animation[] anims = prefab.GetComponentsInChildren<Animation>();
                foreach (Animation anim in anims)
                {
                    if (anim.GetComponent<MeshRenderer>() == null && anim.GetComponent<SkinnedMeshRenderer>() == null)
                    {
                        autoQALog.LOG_ERR("CheckRendererWithAnimationInEditor", "CheckRendererWithAnimationInEditor", path + "的" + anim.name + "上没有相应的MeshRenderer或SkinnedMeshRenderer");
                        //Debug.LogWarning("Prefab:"+prefab.name+"的"+anim.name+ "上没有相应的MeshRenderer或SkinnedMeshRenderer");
                    }
                    //Debug.LogWarning(anim.GetComponent<MeshRenderer>());
                }
            }
            autoQALog.LOG_END("CheckRendererWithAnimationInEditor", "CheckRendererWithAnimationInEditor");
            autoQALog.closeFile();
        }

        //检查character中的骨骼数
        [MenuItem("Tools/AutoQA/CheckBoneNumInPrefab", false, 31)]
        public static void AutoQA_CheckBoneNumInPrefab()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckBoneNumInPrefabInEditor");
            autoQALog.LOG_START("CheckBoneNumInPrefabInEditor", "CheckBoneNumInPrefabInEditor");
            string[] characterFilePath = Directory.GetFiles("Assets/Res/Prefab/Character", "*.prefab", SearchOption.AllDirectories);
            foreach (string path in characterFilePath)
            {
                GameObject currentPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(path);
                Animation anim = currentPrefab.GetComponentInChildren<Animation>();
                if (anim == null) continue;
                Transform[] childrenTrans = anim.GetComponentsInChildren<Transform>();
                int boneNum = childrenTrans.Length;
                foreach (Transform trans in childrenTrans)
                {
                    if (trans.GetComponent<MeshFilter>() || trans.GetComponent<SkinnedMeshRenderer>())
                    {
                        boneNum--;
                    }
                }

                if (boneNum > 50)
                {
                    //autoQALog.LOG_ERR("CheckBoneNumInPrefabInEditor", "CheckBoneNumInPrefabInEditor", "【角色模型的骨骼数大于50】The num of bone in " + path + " is " + boneNum + ".");
                }
            }
            autoQALog.LOG_END("CheckBoneNumInPrefabInEditor", "CheckBoneNumInPrefabInEditor");
            autoQALog.closeFile();
        }

        //检查Prefab上的Animation组件中的AnimationClip是否已抽取
        [MenuItem("Tools/AutoQA/CheckAnimClipInPrefabIsStripping", false, 32)]
        public static void AutoQA_CheckAnimClipInPrefabIsStripping()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckAnimClipInPrefabIsStrippingInEditor");
            autoQALog.LOG_START("CheckAnimClipInPrefabIsStrippingInEditor", "CheckAnimClipInPrefabIsStrippingInEditor");
            //string root = "Assets/Res";
            //string[] paths = Directory.GetFiles(root, "*.prefab", SearchOption.AllDirectories);
            //foreach (string path in paths)
            //{
            //    GameObject currentPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(path);
            //    Animation[] anims = currentPrefab.GetComponentsInChildren<Animation>();
            //    if (anims == null || anims.Length == 0) continue;
            //    foreach (Animation anim in anims)
            //    {
            //        foreach (AnimationState animState in anim)
            //        {
            //            AnimationClip currentClip = animState.clip;
            //            if (currentClip == null) break;
            //            string acPath = AssetDatabase.GetAssetPath(currentClip);
            //            string pathSuffix = Path.GetExtension(acPath).ToLower();
            //            if (pathSuffix == ".fbx")
            //                autoQALog.LOG_ERR("CheckAnimClipInPrefabIsStrippingInEditor", "CheckAnimClipInPrefabIsStrippingInEditor", path + " 中有未抽取的AnimationClip: " + currentClip.name);
            //        }
            //    }
            //}
            autoQALog.LOG_END("CheckAnimClipInPrefabIsStrippingInEditor", "CheckAnimClipInPrefabIsStrippingInEditor");
            autoQALog.closeFile();
        }

        //检查AnimationClip是否legacy
        [MenuItem("Tools/AutoQA/CheckAnimClipLegacy", false, 33)]
        public static void AutoQA_CheckAnimClipLegacy()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckAnimClipLegacyInEditor");
            autoQALog.LOG_START("CheckAnimClipLegacyInEditor", "CheckAnimClipLegacyInEditor");
            string root = "Assets/Res";
            string[] paths = Directory.GetFiles(root, "*.anim", SearchOption.AllDirectories);
            foreach (string path in paths)
            {
                if (path.Contains("Test") || path.Contains("test")) continue;
                AnimationClip animClip = AssetDatabase.LoadAssetAtPath<AnimationClip>(path);
                if (!animClip.legacy)
                {
                    Debug.LogWarning(animClip.name);
                    autoQALog.LOG_ERR("CheckAnimClipLegacyInEditor", "CheckAnimClipLegacyInEditor", path + " used for animation must be legacy");
                }
            }
            autoQALog.LOG_END("CheckAnimClipLegacyInEditor", "CheckAnimClipLegacyInEditor");
            autoQALog.closeFile();
        }

        //1.检查prefab中是否存在没有配置的动作文件 2.检查prefab中是否丢失已经配置的动作文件
        //配置文件已经批量由excel转换为dll文件，基本上每个文件都是一个类，动作文件：Action_主角.xlsx和Action_Sheet2.xlsx
        //GetActionDicForModleId函数通过模型ID获得对应的动作列表，然后与prefab上的动作进行对比，找到缺失的和多余的动作
        [MenuItem("Tools/AutoQA/CheckAnimInConfig", false, 34)]
        public static void AutoQA_CheckAnimInConfig()
        {
            string filterFileName = "Animation";
            ConfigMgr.Instance.LoadConfigData();
            GameDataMgr.CreateActionDict();

            var info = new DirectoryInfo(Application.dataPath + "/Res/Characters/");
            string characterPath = "/Res/Prefab/Character/";
            FileInfo[] fileNames = info.GetFiles("*#*.FBX", SearchOption.AllDirectories);


            Dictionary<string, bool> prefabNoconfig = new Dictionary<string, bool>();
            Dictionary<string, bool> characterNoPrefabDict = new Dictionary<string, bool>();

            Dictionary<string, Dictionary<string, bool>> hasList = new Dictionary<string, Dictionary<string, bool>>();

            //prefab中存在没有配置的动作
            AutoQALog autoQALog1 = new AutoQALog(dirPath, "CheckAnimNotInConfigInEditor");
            autoQALog1.LOG_START("CheckAnimNotInConfigInEditor", "CheckAnimNotInConfigInEditor");
            for (int i = 0; i < fileNames.Length; i++)
            {
                FileInfo fileInfo = fileNames[i];
                if (fileInfo.Directory.Name != filterFileName)
                {
                    //Debug.LogWarning("这个文件不是动作,路径是" + fileInfo.DirectoryName);
                    continue;
                }
                string characterName = fileInfo.Directory.Parent.Name;
                if (!string.IsNullOrEmpty(characterName))
                {
                    Dictionary<uint, BaseActionConfigData> actiondata = GameDataMgr.GetActionDicForModleId(characterName);
                    if (!characterNoPrefabDict.ContainsKey(characterName))
                    {
                        characterNoPrefabDict.Add(characterName, true);
                        string characterRes = characterPath + characterName + ".prefab";
                        if (actiondata != null && File.Exists(Application.dataPath + characterRes))
                        {
                            GameObject obj = AssetDatabase.LoadAssetAtPath("Assets" + characterRes, typeof(GameObject)) as GameObject;
                            ModelSlot slot = obj.GetComponent<ModelSlot>();
                            if (slot != null && slot.action != null && actiondata != null)
                            {
                                prefabNoconfig.Clear();
                                foreach (AnimationState actionItem in slot.action)
                                {
                                    bool find = false;
                                    foreach (var item in actiondata)
                                    {
                                        if (string.IsNullOrEmpty(item.Value.AniName))
                                        {
                                            continue;
                                        }
                                        if (item.Value.AniName == actionItem.name)
                                        {
                                            find = true;
                                            continue;
                                        }
                                    }
                                    if (!find)
                                    {
                                        if (!prefabNoconfig.ContainsKey(actionItem.name))
                                        {
                                            prefabNoconfig.Add(actionItem.name, true);
                                        }
                                    }
                                }
                                foreach (var item in prefabNoconfig)
                                {
                                    autoQALog1.LOG_WARN("CheckAnimNotInConfigInEditor", "CheckAnimNotInConfigInEditor", characterRes + " 中的动作文件 " + item.Key + " 没有配置，需要删除");
                                }
                            }
                        }
                    }

                    Dictionary<string, bool> nohasList = new Dictionary<string, bool>();
                    string animationName = fileInfo.Name.Substring(0, fileInfo.Name.Length - 4);
                    int temp = animationName.LastIndexOf("#") + 1;
                    animationName = animationName.Substring(temp, animationName.Length - temp).ToLower();
                    if (actiondata != null && actiondata.Count > 0)
                    {
                        Dictionary<string, bool> chaterDict;
                        if (!hasList.ContainsKey(characterName))
                        {
                            chaterDict = new Dictionary<string, bool>();
                            hasList.Add(characterName, chaterDict);
                        }
                        else
                        {
                            chaterDict = hasList[characterName];
                        }
                        //先找到两边都有的动作,产生一个列表
                        foreach (var item in actiondata)
                        {
                            if (animationName == item.Value.AniName)
                            {
                                if (!chaterDict.ContainsKey(animationName))
                                {
                                    chaterDict.Add(animationName, true);
                                }
                            }
                        }
                    }
                }
            }
            autoQALog1.LOG_END("CheckAnimNotInConfigInEditor", "CheckAnimNotInConfigInEditor");
            autoQALog1.closeFile();

            //已经配置好但在prefab中不存在的动作
            AutoQALog autoQALog2 = new AutoQALog(dirPath, "CheckAnimNotInPrefabInEditor");
            autoQALog2.LOG_START("CheckAnimNotInPrefabInEditor", "CheckAnimNotInPrefabInEditor");

            Dictionary<string, Dictionary<uint, BaseActionConfigData>> actionDict = GameDataMgr.GetAllActionDict();
            Dictionary<string, Dictionary<string, bool>> nohasResList = new Dictionary<string, Dictionary<string, bool>>();
            foreach (var item in actionDict)
            {
                string charaterName = item.Key;
                string characterRes = characterPath + charaterName + ".prefab";
                if (hasList.ContainsKey(charaterName))
                {
                    Dictionary<uint, BaseActionConfigData> actionconfig = item.Value;
                    foreach (var cofigItem in actionconfig)
                    {
                        Dictionary<string, bool> charaterDict = hasList[charaterName];
                        bool has = false;
                        foreach (var charaterItem in charaterDict)
                        {
                            if (charaterItem.Key == cofigItem.Value.AniName)
                            {
                                has = true;
                                break;
                            }
                        }
                        if (!has)
                        {
                            Dictionary<string, bool> nohasc;
                            if (nohasResList.ContainsKey(charaterName))
                            {
                                nohasc = nohasResList[charaterName];
                            }
                            else
                            {
                                nohasc = new Dictionary<string, bool>();
                                nohasResList.Add(charaterName, nohasc);
                            }
                            if (!string.IsNullOrEmpty(cofigItem.Value.AniName) && !nohasc.ContainsKey(cofigItem.Value.AniName))
                            {
                                nohasc.Add(cofigItem.Value.AniName, true);
                                autoQALog1.LOG_WARN("CheckAnimNotInPrefabInEditor", "CheckAnimNotInPrefabInEditor", characterRes + " 中的缺少已经配置的动作文件 " + cofigItem.Value.AniName + "，需要添加");
                            }
                        }
                    }
                }
            }
            autoQALog2.LOG_END("CheckAnimNotInPrefabInEditor", "CheckAnimNotInPrefabInEditor");
            autoQALog2.closeFile();
        }

        //检查需要压缩的图集是否被压缩，是否支持读写，mipmap等
        [MenuItem("Tools/AutoQA/CheckAtlasCompressed", false, 35)]
        public static void AutoQA_CheckAtlasCompressed()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckAtlasCompressedInEditor");
            autoQALog.LOG_START("CheckAtlasCompressedInEditor", "CheckAtlasCompressedInEditor");

            string[] IconPath = Directory.GetFiles("Assets/Res/Textures/UI/Content/Icon", "*Atlas*.png", SearchOption.AllDirectories);
            string[] ItemPath = Directory.GetFiles("Assets/Res/Textures/UI/Content/Item", "*Atlas*.png", SearchOption.AllDirectories);
            string[] NPCPath = Directory.GetFiles("Assets/Res/Textures/UI/Content/NPC", "*Atlas*.png", SearchOption.AllDirectories);

            int numOfPath = IconPath.Length + ItemPath.Length + NPCPath.Length;
            string[] texturePath = new string[numOfPath];
            IconPath.CopyTo(texturePath, 0);
            ItemPath.CopyTo(texturePath, IconPath.Length);
            NPCPath.CopyTo(texturePath, ItemPath.Length + IconPath.Length);
            foreach (string path in texturePath)
            {
                TextureImporter currentAtlas = AssetImporter.GetAtPath(path) as TextureImporter;
                if (currentAtlas.isReadable)
                {
                    autoQALog.LOG_ERR("CheckAtlasCompressedInEditor", "CheckAtlasCompressedInEditor", path + "不能支持读写");
                }

                if (currentAtlas.mipmapEnabled)
                {
                    autoQALog.LOG_ERR("CheckAtlasCompressedInEditor", "CheckAtlasCompressedInEditor", path + "不能支持mipmap");
                }

                if (currentAtlas.textureCompression == 0)
                {
                    autoQALog.LOG_ERR("CheckAtlasCompressedInEditor", "CheckAtlasCompressedInEditor", path + "没有进行压缩");
                }
                //Debug.Log("最大尺寸:" + currentAtlas.maxTextureSize);
                //Debug.Log("是否可读可写:" + currentAtlas.isReadable);
                //Debug.Log("是否支持mipmap:" + currentAtlas.mipmapEnabled);
                //Debug.Log("压缩方式:" + currentAtlas.textureCompression);
            }
            autoQALog.LOG_END("CheckAtlasCompressedInEditor", "CheckAtlasCompressedInEditor");
            autoQALog.closeFile();

        }


        //检查贴图的大小是否符合要求
        [MenuItem("Tools/AutoQA/CheckTextureSize", false, 46)]
        public static void AutoQA_CheckTextureSize()
        {

            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckTextureSizeInEditor");
            autoQALog.LOG_START("CheckTextureSizeInEditor", "CheckTextureSizeInEditor");

            //List<string> textrues = new List<string>();
            //string[] files = Directory.GetFiles("Assets/Res", "*", SearchOption.AllDirectories);
            //foreach (string file in files)
            //{
            //    string assetExt = Path.GetExtension(file).ToLower();
            //    if (assetExt == ".jpg" || assetExt == ".jpeg" || assetExt == ".tga" || assetExt == ".bmp" || assetExt == ".png" || assetExt == ".psd" || assetExt == ".tiff" || assetExt == ".gif")
            //    {
            //        textrues.Add(file);
            //    }
            //}
            //foreach (string file in textrues)
            //{
            //    string nfile = file.Replace("\\", "/");
            //    FileInfo f = new FileInfo(nfile);
            //    if(f.Length>(1024*1024))
            //        Debug.LogWarning(nfile);
            //}

            autoQALog.LOG_END("CheckTextureSizeInEditor", "CheckTextureSizeInEditor");
            autoQALog.closeFile();

        }

        //检查模型的子面片数
        [MenuItem("Tools/AutoQA/CheckSubMeshInPrefab", false, 47)]
        public static void AutoQA_CheckSubMeshInPrefab()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckSubMeshInPrefabInEditor");
            autoQALog.LOG_START("CheckSubMeshInPrefabInEditor", "CheckSubMeshInPrefabInEditor");

            //string[] prefabsPaths = Directory.GetFiles("Assets/Res/Prefab", "*.prefab", SearchOption.AllDirectories);
            //foreach (string prefabpath in prefabsPaths)
            //{
            //    GameObject prefab = AssetDatabase.LoadMainAssetAtPath(prefabpath) as GameObject;
            //    MeshFilter[] mfs = prefab.GetComponentsInChildren<MeshFilter>();
            //    foreach (MeshFilter mf in mfs)
            //    {
            //        Mesh mesh = mf.sharedMesh;
            //        if (mesh.subMeshCount > 1) {
            //            Debug.LogWarning(prefabpath+"的"+mf.name+"上的submesh大于1");
            //        }
            //    }
            //}

            autoQALog.LOG_END("CheckSubMeshInPrefabInEditor", "CheckSubMeshInPrefabInEditor");
            autoQALog.closeFile();
        }

        //角色Animation组件的CullingType应该为BasedOnRenderers
        [MenuItem("Tools/AutoQA/CheckCullingTypeInAnim", false, 48)]
        public static void AutoQA_CheckCullingTypeInAnim()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckCullingTypeInAnimInEditor");
            autoQALog.LOG_START("CheckCullingTypeInAnimInEditor", "CheckCullingTypeInAnimInEditor");
            string[] files = Directory.GetFiles("Assets/Res/Prefab/Character", "*.prefab", SearchOption.AllDirectories);
            foreach (string file in files)
            {
                GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(file);
                Animation[] animations = prefab.GetComponentsInChildren<Animation>();
                if (animations.Length > 0)
                {
                    foreach (var animation in animations)
                    {
                        if (animation.cullingType != AnimationCullingType.BasedOnRenderers)
                        {
                            autoQALog.LOG_ERR("CheckCullingTypeInAnimInEditor", "CheckCullingTypeInAnimInEditor", file + "的" + animation.name + "中animation组件的CullingType应该为BasedOnRenderers");
                            //Debug.LogWarning(file+"的"+ animation.name+ " animation组件的CullingType应该为BasedOnRenderers");
                        }
                    }
                }
            }
            autoQALog.LOG_END("CheckCullingTypeInAnimInEditor", "CheckCullingTypeInAnimInEditor");
            autoQALog.closeFile();
        }

        //检查模型的顶点数、面数、三角形数
        [MenuItem("Tools/AutoQA/CheckVertexAndTrigsInPrefab", false, 48)]
        public static void AutoQA_CheckVertexAndTrigsInPrefab()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckVertexAndTrigsInPrefabInEditor");
            autoQALog.LOG_START("CheckVertexAndTrigsInPrefabInEditor", "CheckVertexAndTrigsInPrefabInEditor");
            //string[] prefabsPaths = Directory.GetFiles("Assets/Res/Prefab/Character", "*.prefab", SearchOption.AllDirectories);

            //foreach (string prefabpath in prefabsPaths) {
            //    GameObject prefab = AssetDatabase.LoadMainAssetAtPath(prefabpath) as GameObject;
            //    MeshFilter []mfs = prefab.GetComponentsInChildren<MeshFilter>();
            //    foreach (MeshFilter mf in mfs) {
            //        Mesh mesh = mf.sharedMesh;
            //        int tris = mesh.triangles.Length/3;
            //    } 
            //}

            autoQALog.LOG_END("CheckVertexAndTrigsInPrefabInEditor", "CheckVertexAndTrigsInPrefabInEditor");
            autoQALog.closeFile();
        }

        //检查粒子系统的规范
        [MenuItem("Tools/AutoQA/CheckParticleSystem", false, 50)]
        public static void AutoQA_CheckParticleSystem()
        {

        }

        //检查mesh renderer中material数量是否是一(warning级别)
        [MenuItem("Tools/AutoQA/CheckMatNumInMeshRenderer", false, 61)]
        public static void AutoQA_CheckMatNumInMeshRenderer()
        {

            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckMatNumInMeshRendererInEditor");
            autoQALog.LOG_START("CheckMatNumInMeshRendererInEditor", "CheckMatNumInMeshRendererInEditor");

            string[] prefabPaths = Directory.GetFiles("Assets/Res/Prefab", "*.prefab", SearchOption.AllDirectories);
            foreach (string prefabPath in prefabPaths)
            {
                GameObject go = AssetDatabase.LoadAssetAtPath<GameObject>(prefabPath);
                MeshRenderer[] mfs = go.GetComponentsInChildren<MeshRenderer>();
                SkinnedMeshRenderer[] smrs = go.GetComponentsInChildren<SkinnedMeshRenderer>();
                if (mfs.Length > 0)
                {
                    foreach (MeshRenderer mf in mfs)
                    {
                        Material[] mats = mf.sharedMaterials;
                        if (mats != null && mats.Length > 1)
                        {
                            autoQALog.LOG_WARN("CheckMatNumInMeshRendererInEditor", "CheckMatNumInMeshRendererInEditor", prefabPath + "的" + mf.name + "中MeshRenderer上的材质球不唯一");
                            //Debug.LogWarning(prefabPath+"的"+mf.name+"中MeshRenderer上的材质球不唯一");
                        }
                    }
                }

                if (smrs.Length > 0)
                {
                    foreach (SkinnedMeshRenderer smr in smrs)
                    {
                        Material[] mats = smr.sharedMaterials;
                        if (mats != null && mats.Length > 1)
                        {
                            autoQALog.LOG_WARN("CheckMatNumInMeshRendererInEditor", "CheckMatNumInMeshRendererInEditor", prefabPath + "的" + smr.name + "中SkinnedMeshRenderer上的材质球不唯一");
                            //Debug.LogWarning(prefabPath + "的" + smr.name + "中SkinnedMeshRenderer上的材质球不唯一");
                        }
                    }
                }

            }
            autoQALog.LOG_END("CheckMatNumInMeshRendererInEditor", "CheckMatNumInMeshRendererInEditor");
            autoQALog.closeFile();
        }

        //检查模型中的蒙皮数量
        [MenuItem("Tools/AutoQA/CheckSkinnedMeshRendererNumInPrefab", false, 62)]
        public static void AutoQA_CheckSkinnedMeshRendererNumInPrefab()
        {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckSkinnedMeshRendererNumInPrefabInEditor");
            autoQALog.LOG_START("CheckSkinnedMeshRendererNumInPrefabInEditor", "CheckSkinnedMeshRendererNumInPrefabInEditor");

            autoQALog.LOG_END("CheckSkinnedMeshRendererNumInPrefabInEditor", "CheckSkinnedMeshRendererNumInPrefabInEditor");
            autoQALog.closeFile();
        }

        //检查特效中多余的collider和rigidbody
        [MenuItem("Tools/AutoQA/CheckNeedlessColliderAndRigidbodyInEffect", false, 63)]
        public static void AutoQA_CheckNeedlessColliderAndRigidbodyInEffect() {
            AutoQALog autoQALog = new AutoQALog(dirPath, "CheckNeedlessColliderAndRigidbodyInEffectInEditor");
            autoQALog.LOG_START("CheckNeedlessColliderAndRigidbodyInEffectInEditor", "CheckNeedlessColliderAndRigidbodyInEffectInEditor");

            autoQALog.LOG_END("CheckNeedlessColliderAndRigidbodyInEffectInEditor", "CheckNeedlessColliderAndRigidbodyInEffectInEditor");
            autoQALog.closeFile();
        }
    }
}

