//MTL profiler 统计工具
//使用方法：请放在Unity 工程文件夹中“Assets”中新建“Editor”目录，并将本文件放入该目录，正常情况下在Unity的工具栏中会出现“Sprofiler”按钮
//使用Profiler开始记录性能数据并点击Sprofiler就会在对应的工程目录下产生log文件，将log上传：http://192.168.131.233:9090/webtool/unity_profiling/index/#可以看到统计结果


using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEditorInternal;
using System.Text;

namespace SProfiler
{
    public class SProfiler
    {
        [MenuItem("SProfiler/Start")]
        public static void action()
        {
            EditorWindow.GetWindow(typeof(StartProfile));
        }
    }
    public class StartProfile : EditorWindow
    {
        bool record = false;
        System.IO.FileStream cpu_stack_file;
        System.IO.StreamWriter cpu_stack_sw;

        System.IO.FileStream fps_file;
        System.IO.StreamWriter fps_sw;


        System.IO.FileStream rendering_file;
        System.IO.StreamWriter rendering_sw;

        System.IO.FileStream cpu_file;
        System.IO.StreamWriter cpu_sw;

        System.IO.FileStream gpu_file;
        System.IO.StreamWriter gpu_sw;

        System.IO.FileStream memory_file;
        System.IO.StreamWriter memory_sw;

        System.IO.FileStream audio_file;
        System.IO.StreamWriter audio_sw;

        System.IO.FileStream physics_file;
        System.IO.StreamWriter physics_sw;

        System.IO.FileStream physics2D_file;
        System.IO.StreamWriter physics2D_sw;

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
          
				Debug.Log("record..... :" + property.frameDataReady + "      IsFrameDataReady :" + IsFrameDataReady );
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
 		        
                LogFrameIndex = (BaseFrameIndex+lastFrameIndex);
				StringBuilder sb1 = new StringBuilder();
				sb1.Append(LogFrameIndex.ToString());
                sb1.Append("|");
                sb1.Append(property.frameFPS);
				sb1.Append("|");
				sb1.Append(CurTime);
                fps_sw.WriteLine(sb1.ToString());
				sb1.Remove(0,sb1.Length);

                StringBuilder sb2 = new StringBuilder();
                sb2.Append(LogFrameIndex.ToString());
                sb2.Append("|");
                sb2.Append(ProfilerDriver.GetOverviewText(ProfilerArea.Rendering, lastFrameIndex));
                rendering_sw.WriteLine(sb2.ToString());

                //本来是通过下面的方法得到drawcalls的信息的，后来又想获取其他的信息，比如面片数等
                //发现其实在unity中，Profiler中，其实每一帧的信息就是一个长的字符串，这样，我们可以把每一帧的信息字符串先全部保存下来，后期再分析就可以了

                //sb1.Append(property.frameGpuTime);
                //sb1.Append("|");
                //sb1.Append(property.frameGpuTime);
                //sb1.Append("|");
                //sb1.Append(property.GetColumn(ProfilerColumn.DrawCalls));

                StringBuilder sb3 = new StringBuilder();
                sb3.Append(LogFrameIndex.ToString());
                sb3.Append("|");
                sb3.Append(ProfilerDriver.GetOverviewText(ProfilerArea.CPU, lastFrameIndex));
                cpu_sw.WriteLine(sb3.ToString());

                StringBuilder sb4 = new StringBuilder();
                sb4.Append(LogFrameIndex.ToString());
                sb4.Append("|");
                sb4.Append(ProfilerDriver.GetOverviewText(ProfilerArea.GPU, lastFrameIndex));
                gpu_sw.WriteLine(sb4.ToString());

                StringBuilder sb5 = new StringBuilder();
                sb5.Append(LogFrameIndex.ToString());
                sb5.Append("|");
                sb5.Append(ProfilerDriver.GetOverviewText(ProfilerArea.Memory, lastFrameIndex));
                memory_sw.WriteLine(sb5.ToString());


                StringBuilder sb6 = new StringBuilder();
                sb6.Append(LogFrameIndex.ToString());
                sb6.Append("|");
                sb6.Append(ProfilerDriver.GetOverviewText(ProfilerArea.Audio, lastFrameIndex));
                audio_sw.WriteLine(sb6.ToString());


                StringBuilder sb7 = new StringBuilder();
                sb7.Append(LogFrameIndex.ToString());
                sb7.Append("|");
                sb7.Append(ProfilerDriver.GetOverviewText(ProfilerArea.Physics, lastFrameIndex));
                physics_sw.WriteLine(sb7.ToString());


                StringBuilder sb8 = new StringBuilder();
                sb8.Append(LogFrameIndex.ToString());
                sb8.Append("|");
                sb8.Append(ProfilerDriver.GetOverviewText(ProfilerArea.Physics2D, lastFrameIndex));
                physics2D_sw.WriteLine(sb8.ToString());

                bool c = true;
                while (property.Next(c))
                {
                    if (property.instanceIDs != null && property.instanceIDs.Length > 0 && property.instanceIDs[0] != 0)
                    {    
                        continue;
                    } 
                    
                    if (property.HasChildren)
                    {
                        c = true;
                    }
                    StringBuilder sb = new StringBuilder();
                    sb.Append(LogFrameIndex.ToString());
                    sb.Append("|");
                    sb.Append(property.propertyPath);
                    sb.Append("|");
                    sb.Append(property.GetColumn(ProfilerColumn.GCMemory));
                    sb.Append("|");
                    sb.Append(property.GetColumn(ProfilerColumn.SelfTime));
                    sb.Append("|");
                    sb.Append(property.GetColumn(ProfilerColumn.TotalTime));
                    //string s = property.propertyPath + "|" + property.GetColumn(ProfilerColumn.FunctionName) + "|" + property.GetColumn(ProfilerColumn.GCMemory);
                    cpu_stack_sw.WriteLine(sb.ToString());
                    //Debug.LogError(s);

                }
                lastFrameIndex++;
                property.Cleanup();                
            }
        }


        void OnGUI()
        {

            //GUILayout.BeginHorizontal();
            //GUILayout.EndHorizontal();
            //GUILayout.TextArea("aaa");
            GUILayout.Label("开启前，请确认手机已经连接unity，并开启了profile");
            GUILayout.Label("  ");

            //GUILayout.BeginHorizontal();
            //GUILayout.EndHorizontal();


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

                    


					Debug.Log("=========================" + lastFrameIndex + "        IsFrameDataReady " + IsFrameDataReady   +  "   BaseFrameIndex  " + BaseFrameIndex + "    lastFrameIndex  " + lastFrameIndex );

                    ProfilerDriver.selectedPropertyPath = "BehaviourUpdate";

                    if (enable)
                        Debug.Log("enabled profilder: " + name);
                    else
                        Debug.Log("disabled profilder: " + name);

                    if (System.IO.File.Exists("cpu_stack.log"))
                        System.IO.File.Delete("cpu_stack.log");

                    if (System.IO.File.Exists("fps.log"))
                        System.IO.File.Delete("fps.log");

                    if (System.IO.File.Exists("cpu.log"))
                        System.IO.File.Delete("cpu.log");

                    if (System.IO.File.Exists("gpu.log"))
                        System.IO.File.Delete("gpu.log");

                    if (System.IO.File.Exists("memory.log"))
                        System.IO.File.Delete("memory.log");

                    if (System.IO.File.Exists("audio.log"))
                        System.IO.File.Delete("audio.log");

                    if (System.IO.File.Exists("physics.log"))
                        System.IO.File.Delete("physics.log");

                    if (System.IO.File.Exists("physics2D.log"))
                        System.IO.File.Delete("physics2D.log");

                    if (System.IO.File.Exists("rendering.log"))
                        System.IO.File.Delete("rendering.log");



                    cpu_stack_file = System.IO.File.OpenWrite("cpu_stack.log");
                    cpu_stack_sw = new System.IO.StreamWriter(cpu_stack_file);

                    fps_file = System.IO.File.OpenWrite("fps.log");
                    fps_sw =  new System.IO.StreamWriter(fps_file);

                    cpu_file = System.IO.File.OpenWrite("cpu.log");
                    cpu_sw = new System.IO.StreamWriter(cpu_file);

                    gpu_file = System.IO.File.OpenWrite("gpu.log");
                    gpu_sw = new System.IO.StreamWriter(gpu_file);

                    memory_file = System.IO.File.OpenWrite("memory.log");
                    memory_sw = new System.IO.StreamWriter(memory_file);

                    audio_file = System.IO.File.OpenWrite("audio.log");
                    audio_sw = new System.IO.StreamWriter(audio_file);

                    physics_file = System.IO.File.OpenWrite("physics.log");
                    physics_sw = new System.IO.StreamWriter(physics_file);

                    physics2D_file = System.IO.File.OpenWrite("physics2D.log");
                    physics2D_sw = new System.IO.StreamWriter(physics2D_file);

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
                    cpu_stack_sw.Close();
                    cpu_stack_sw.Dispose();
                    cpu_stack_sw = null;

                    cpu_stack_file.Close();
                    cpu_stack_file.Dispose();
                    cpu_stack_file = null;

                    fps_sw.Close();
                    fps_sw.Dispose();
                    fps_sw = null;

                    fps_file.Close();
                    fps_file.Dispose();
                    fps_file = null;

                    cpu_sw.Close();
                    cpu_sw.Dispose();
                    cpu_sw = null;

                    cpu_file.Close();
                    cpu_file.Dispose();
                    cpu_file = null;

                    gpu_sw.Close();
                    gpu_sw.Dispose();
                    gpu_sw = null;

                    gpu_file.Close();
                    gpu_file.Dispose();
                    gpu_file = null;


                    memory_sw.Close();
                    memory_sw.Dispose();
                    memory_sw = null;

                    memory_file.Close();
                    memory_file.Dispose();
                    memory_file = null;


                    audio_sw.Close();
                    audio_sw.Dispose();
                    audio_sw = null;

                    audio_file.Close();
                    audio_file.Dispose();
                    audio_file = null;

                    physics_sw.Close();
                    physics_sw.Dispose();
                    physics_sw = null;

                    physics_file.Close();
                    physics_file.Dispose();
                    physics_file = null;


                    physics2D_sw.Close();
                    physics2D_sw.Dispose();
                    physics2D_sw = null;

                    physics2D_file.Close();
                    physics2D_file.Dispose();
                    physics2D_file = null;


                    rendering_sw.Close();
                    rendering_sw.Dispose();
                    rendering_sw = null;


                    rendering_file.Close();
                    rendering_file.Dispose();
                    rendering_file = null;
                }
            }


        }

    }

}