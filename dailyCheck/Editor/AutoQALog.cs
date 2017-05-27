using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace leiting_AutoQA
{
    public class AutoQALog
    {
        public string dirPath;
        public string suiteName;
        public static FileStream fs;
        public static StreamWriter sw; 
        //AutoQALog 
        public AutoQALog(string dirPath, string suiteName)
        {

            string filePath = dirPath + suiteName + ".log";
            if (File.Exists(filePath))
            {
                File.Delete(filePath);
            }
            fs = new FileStream(filePath, FileMode.Create);
            sw = new StreamWriter(fs);
        }

        private void LOG(string level, string suiteName, string caseName, string caseResult)
        {
            DateTime dateTime = DateTime.Now;
            string currentTime = dateTime.ToString();
            string logMsg = currentTime + "|" + level + "|" + caseName + "|" + caseResult + "<br>\r\n";
            //using (File.Create(@filePath));
            sw.Write(logMsg);
            
        }

        public void LOG_ERR(string suiteName, string caseName, string caseResult)
        {
            LOG("ERR", suiteName, caseName, caseResult);
        }

        public void LOG_WARN(string suiteName, string caseName, string caseResult)
        {
            LOG("WARN", suiteName, caseName, caseResult);
        }

        public void LOG_START(string suiteName, string caseName)
        {
            LOG("StartTest", suiteName, caseName, "TestCaseStarted");
        }

        public void LOG_END(string suiteName, string caseName)
        {
            LOG("EndTest", suiteName, caseName, "TestCaseEnded");
        }

        public void closeFile()
        {
            sw.Close();
            fs.Close();
            
        }

    }
}
