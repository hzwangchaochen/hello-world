//MTL profiler 统计工具
//使用方法：请放在Unity 工程文件夹中“Assets”中新建“Editor”目录，并将本文件放入该目录，正常情况下在Unity的工具栏中会出现“Sprofiler”按钮
//使用Profiler开始记录性能数据并点击Sprofiler就会在对应的工程目录下产生log文件，将log上传：http://192.168.131.233:9090/webtool/unity_profiling/index/#可以看到统计结果


using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEditorInternal;
using System.Text;

namespace MemoryProfiler
{
    public class MemoryProfiler
    {
        [MenuItem("SProfiler/MemoryProfiler")]
        public static void action()
        {
            EditorWindow.GetWindow(typeof(StartMemoryProfile));
        }
    }
    
    public class StartMemoryProfile : EditorWindow
    {
        bool record = false;

        System.IO.FileStream fps_file;
        System.IO.StreamWriter fps_sw;

        System.IO.FileStream rendering_file;
        System.IO.StreamWriter rendering_sw;

        System.IO.FileStream memory_file;
        System.IO.StreamWriter memory_sw;

        int lastFrameIndex = -10;
		System.DateTime LastTime = System.DateTime.Now;
		System.DateTime CurTime = System.DateTime.Now;
		ProfilerProperty property = new ProfilerProperty();

		bool IsFrameDataReady  = false; //如果是true，说明已经开始统计过了，那么如果设备断开需要重连
		long BaseFrameIndex = 0; //由于断开重连，需要设置一个基础的index
        long LogFrameIndex = 0;
        
        void Update()
        {
            //当前时间
			CurTime = System.DateTime.Now;

            //设置采样时间间隔，采样太快了有问题(ms)
            if ((CurTime - LastTime).TotalMilliseconds > 100)
            {
                LastTime = CurTime;
            }
            else
            { //没有到采样时间，返回
                return;
            }

            //已经开始统计
            if (record)
            {
                property.SetRoot(lastFrameIndex, ProfilerColumn.SelfTime, ProfilerViewType.Hierarchy);
               
                //这里需要注意的是，当你按下Start后，可以一直会显示下面的变量为false，这样就无法捕获信息了
                //这时候，你需要按下unity profile界面的clear按钮才可以
          
				//Debug.Log("record..... :" + property.frameDataReady + "      IsFrameDataReady :" + IsFrameDataReady );
				//只要有一次frameDataReady 就设置标志位，说明已经开始统计了
				if (property.frameDataReady == true)
				{
				    IsFrameDataReady  = true;					  
				}			

	            //能走到这里，说明需要重连
		        if(property.frameDataReady == false && IsFrameDataReady == true)
		        {
                    Debug.Log("re try connect.... :" + property.frameDataReady);

                    int p = ProfilerDriver.connectedProfiler;
                    bool enable = ProfilerDriver.IsIdentifierConnectable(p);
                    string name = ProfilerDriver.GetConnectionIdentifier(p);

                    if (enable)
                        Debug.Log("enabled profilder: " + name);
                    else
                        Debug.Log("disabled profilder: " + name);


                    ProfilerDriver.ClearAllFrames();
                    BaseFrameIndex = lastFrameIndex + BaseFrameIndex + 1;

                    lastFrameIndex = ProfilerDriver.firstFrameIndex;
                    property.SetRoot(lastFrameIndex, ProfilerColumn.SelfTime, ProfilerViewType.Hierarchy);
                    return;
                }
 		        
 		        if(property.frameDataReady == false || property.frameFPS == "--" )
 		        {
 		            Debug.Log("no data can be recorded.... :" + property.frameDataReady + "fps:  " + property.frameFPS);
 		            return;
 		        }

                LogFrameIndex = (BaseFrameIndex + lastFrameIndex);
                StringBuilder sb1 = new StringBuilder();
                sb1.Append(LogFrameIndex.ToString());
                sb1.Append("|");
                sb1.Append(property.frameFPS);
                sb1.Append("|");
                sb1.Append(CurTime);
                fps_sw.WriteLine(sb1.ToString());
                sb1.Remove(0, sb1.Length);

                StringBuilder sb2 = new StringBuilder();
                sb2.Append(LogFrameIndex.ToString());
                sb2.Append("|");
                sb2.Append(ProfilerDriver.GetOverviewText(ProfilerArea.Rendering, lastFrameIndex));
                rendering_sw.WriteLine(sb2.ToString());

                StringBuilder sb3 = new StringBuilder();
                sb3.Append(LogFrameIndex.ToString());
                sb3.Append("|");
                sb3.Append(ProfilerDriver.GetOverviewText(ProfilerArea.Memory, lastFrameIndex));
                memory_sw.WriteLine(sb3.ToString());
                lastFrameIndex++;
                property.Cleanup();                
            }
        }

        void OnGUI()
        {
            GUILayout.Label("开启前，请确认手机已经连接unity，并开启了profile");
            GUILayout.Label("  ");


            if (!record)
            {
				IsFrameDataReady  = false;
				BaseFrameIndex = 1;

                if (GUILayout.Button("Start"))
                {
                    
                    int p = ProfilerDriver.connectedProfiler;
                    bool enable = ProfilerDriver.IsIdentifierConnectable(p);
                    string name = ProfilerDriver.GetConnectionIdentifier(p);

                    ProfilerDriver.ClearAllFrames();

                    lastFrameIndex = ProfilerDriver.firstFrameIndex;

					//Debug.Log("=========================" + lastFrameIndex + "        IsFrameDataReady " + IsFrameDataReady   +  "   BaseFrameIndex  " + BaseFrameIndex + "    lastFrameIndex  " + lastFrameIndex );

                    ProfilerDriver.selectedPropertyPath = "BehaviourUpdate";

                    if (enable)
                        Debug.Log("enabled profilder: " + name);
                    else
                        Debug.Log("disabled profilder: " + name);
                    if (System.IO.File.Exists("fps.log"))
                        System.IO.File.Delete("fps.log");

                    if (System.IO.File.Exists("rendering.log"))
                        System.IO.File.Delete("rendering.log");

                    if (System.IO.File.Exists("memory.log"))
                        System.IO.File.Delete("memory.log");

                    fps_file = System.IO.File.OpenWrite("fps.log");
                    fps_sw = new System.IO.StreamWriter(fps_file);

                    memory_file = System.IO.File.OpenWrite("memory.log");
                    memory_sw = new System.IO.StreamWriter(memory_file);

                    rendering_file = System.IO.File.OpenWrite("rendering.log");
                    rendering_sw = new System.IO.StreamWriter(rendering_file);

                    record = true;
                }
            }
            else
            {
                if (GUILayout.Button("Stop"))
                {
                    record = false;

                    fps_sw.Close();
                    fps_sw.Dispose();
                    fps_sw = null;

                    fps_file.Close();
                    fps_file.Dispose();
                    fps_file = null;

                    rendering_sw.Close();
                    rendering_sw.Dispose();
                    rendering_sw = null;


                    rendering_file.Close();
                    rendering_file.Dispose();
                    rendering_file = null;

                    memory_sw.Close();
                    memory_sw.Dispose();
                    memory_sw = null;

                    memory_file.Close();
                    memory_file.Dispose();
                    memory_file = null;
                }
            }
        }

    }

}