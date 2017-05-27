#!/usr/bin/python  
# coding=utf-8
import xml.etree.cElementTree as ET
import os
import sys

tree = ET.ElementTree(file='/var/www/Checker/DailyCheckMap.xml')

resultFile=open("Result.html","w")
allResults=[]
fileNameResults=[]

def write(info):
    global resultFile
    resultFile.write(info)

def generateHeader(title):
    write("<html><head><title>")
    write(title+"</title>")
    write("<meta http-equiv=Content-Type content=\"text/html charset=utf-8\">")
    write("</head><body>\r\n")
    write("<p><span style='font-size:26.0pt'>")
    write(title)
    write("</span></p>\r\n")
    write("<p><span style='font-size:15.0pt'>")
    write("对游戏内用到的各类资源按照既定规则进行检查，并生成报告；不含游戏逻辑检查。")
    write("</span></p>\r\n")

def generateTableCell(text, bgColor, fgColor, width,position):
    write("<td align=top style='width:")
    write(width)
    write("pt;border:solid black 1.0pt;background:")
    write(bgColor)
    write("'>\r\n")
    write("<p align=center style='text-align:")
    write(position)
    write("'><b><span style='font-size:12.0pt;color:")
    write(fgColor)
    write("'>")
    if text:
        write(text)
    else:
        write("no data")
    write("</span></b></p>\r\n</td>\r\n")

def generateHrefTableCell(text, bgColor, fgColor, width):
    write("<td align=top style='width:")
    write(width)
    write("pt;border:solid black 1.0pt;background:")
    write(bgColor)
    write("'>\r\n")

    write("<a href=\"http://192.168.131.107/LX6/")
    write(sys.argv[1])
    write("/")
    write(text)
    write("\" target=_blank>")
    write(text)
    write("</a>\r\n</td>\r\n")


def generateTestFailureDetailTable(ErrorMsg):
    write("<table style='border-collapse:collapse;border:none;mso-border-alt:solid black .5pt'>")
    write("<tr>\r\n")
    generateTableCell("Failures", "red", "white", '120',"center")
    generateTableCell(''.join(ErrorMsg), "white", "black", '1000',"left")
    write("</tr>\r\n")
    write("</table>\r\n")

def generateTestWarningDetailTable(ErrorMsg):
    write("<table style='border-collapse:collapse;border:none;mso-border-alt:solid black .5pt'>")
    write("<tr>\r\n")
    generateTableCell("Warnings", "#F77626", "white",'120',"center")
    generateTableCell(''.join(ErrorMsg), "white", "black", '1000',"left")
    write("</tr>\r\n")
    write("</table>\r\n")

def generateTail():
    write("</body></html>")


def parseResultFile(fileName):
    global allResults
    global fileNameResults

    suiteResult = {}
    curCaseResult = ""
    try:
        file=open(fileName,"r")
        for line in file:
            t=line.split("|")
            logLevel=t[1]
            caseName=t[2]
            logMessage=t[3]
            if logMessage:
                if "TestCaseStarted" in logMessage:
                    localResult={"TestCaseName":caseName,"Pass":1,"Fail":0,"Warning":0,"ErrorLines":[],"WarningLines":[],"LogPaths":[]}
                    suiteResult[caseName]=localResult
                elif logLevel=="ERR":
                    suiteResult[caseName]["Pass"]=0
                    suiteResult[caseName]["Fail"]=1
                    suiteResult[caseName]["ErrorLines"].append(logMessage)
                elif logLevel=="WARN":
                    suiteResult[caseName]["Pass"]=0
                    suiteResult[caseName]["Warning"]=1
                    suiteResult[caseName]["WarningLines"].append(logMessage)
                elif "TestCaseEnded" in logMessage:
                    suiteResult[caseName]["LogPaths"].append(fileName)
        allResults.append(suiteResult)
        fileNameResults.append(fileName)
        file.close()

    except IOError:
        print(fileName+" not found")


def generateSummaryTable():
    global allResults
    firstColumnWidth = 220
    write("<p><span style='font-size:16.0pt'>1. Summary</span></p>\r\n")   
    totalPass = 0
    totalFail = 0
    totalWarning = 0
    for suiteResult in allResults:
        for (caseName,caseResult) in suiteResult.items():
            totalPass=totalPass+caseResult["Pass"]
            totalFail=totalFail+caseResult["Fail"]
            totalWarning=totalWarning+caseResult["Warning"]

    if totalFail!=0:
        write("<p><span><font style='font-size:18.0pt' color='red'>今日检查没有全部通过，需要QA跟进检查</font></span></p>\r\n")
    else:
        write("<p><span><font style='font-size:18.0pt' color='green'>今日检查全部通过</font></span></p>\r\n")

    write("<font style='font-size:18.0pt'>Total cases passed: "+str(totalPass)+"</font><br>")
    write("<font style='font-size:18.0pt'>Total cases failed: "+str(totalFail)+"</font><br>")
    write("<font style='font-size:18.0pt'>Total cases Warning: "+str(totalWarning)+"</font><br><br>\n")

    write("<table style='border-collapse:collapse;border:none;mso-border-alt:solid black .5pt'>")
    write("<tr>\n")

    generateTableCell("TestSuite Name", "black", "white", str(firstColumnWidth),"center") 
    generateTableCell("Total","#330000","white", '120',"center")
    generateTableCell("Pass", "#00B050", "white", '120',"center")
    generateTableCell("Fail", "red", "white", '120',"center")
    generateTableCell("Warning", "#F77626", "white", '120',"center")
    generateTableCell("Description", "blue", "white", '400',"center")
    generateTableCell("TestCase Type", "purple", "white", '200',"center")
    write("</tr>\n")

    darkerBackground = False
    fileIndex=0

    for suiteResult in allResults:
        curPass = 0
        curFail = 0
        curWarning=0
        backColor= ""
        backColorForEditor= ""
        logIntro=""
        fileName = ""
        for (caseName,caseResult) in suiteResult.items():
            curPass = curPass + caseResult["Pass"]
            curFail = curFail + caseResult["Fail"]
            curWarning = curWarning+caseResult["Warning"]

        if darkerBackground:
            backColor = "#E5E5FF"
            darkerBrackground = False
        else:
            backColor = "white"
            darkerBrackground=True
        fileName = fileNameResults[fileIndex][0:-4]
        for elem in tree.iter(tag=fileName):
            logIntro = elem.text

        if "InEditor" not in fileNameResults[fileIndex]:
            generateHrefTableCell(fileNameResults[fileIndex],  "white", "black", str(firstColumnWidth))
            generateTableCell(str(curPass+curFail+curWarning), "white",  "#330000", '120',"center")
            generateTableCell(str(curPass),  "white", "#00B050", '120',"center")
            generateTableCell(str(curFail),  "white", "red", '120',"center")
            generateTableCell(str(curWarning),  "white", "#F77626", '120',"center")
            generateTableCell(logIntro.encode('utf-8'), "white", "black", '400',"center")
            generateTableCell("通过外部脚本进行检查", "white", "black",'200',"center")
        else:
            generateHrefTableCell(fileNameResults[fileIndex], "#E5E5FF", "black", str(firstColumnWidth))
            generateTableCell(str(curPass+curFail+curWarning), "#E5E5FF" ,"#330000",'120',"center")
            generateTableCell(str(curPass),  "#E5E5FF", "#00B050",'120',"center")
            generateTableCell(str(curFail),  "#E5E5FF", "red",'120',"center")
            generateTableCell(str(curWarning),  "#E5E5FF", "#F77626",'120',"center")
            generateTableCell(logIntro.encode('utf-8'),"#E5E5FF", "black",'400',"center")
            generateTableCell("通过unity editor进行检查","#E5E5FF", "black",'200',"center")
        write("</tr>\n")
        fileIndex+=1
    write("</tr>\n")
    write("<td align=top style='width:220pt;border:solid black 1.0pt;background:white'>\r\n")
    write("<a href='http://192.168.131.107/Checker/ResourcesOutline/display.php' target=_blank>点击查看资源文件统计结果</a></td>")
    generateTableCell('1',"white" ,"#330000",'120',"center")
    generateTableCell('1',"white", "#00B050", '120',"center")
    generateTableCell('0',"white", "red", '120',"center")
    generateTableCell('0',"white", "#F77626", '120',"center")
    generateTableCell("查看资源文件统计结果","white", "black", '400',"center")
    generateTableCell("资源统计","white", "black", '200',"center")
    write("</tr>\n")
    write("</tr></table>")

def generateFailureDetail():
    write("<p><span style='font-size:16.0pt'>2.Failures</span></p>\r\n")
    CurrentSuiteTitle = ""
    fileIndex=0
    for suiteResult in allResults:
        for (caseName,caseResult) in suiteResult.items():
            if caseResult["Fail"]>0:
                write("<p><b><u><a name=\"" +fileNameResults[fileIndex]+"\">")
                write("<h2>TestSuiteName : "+fileNameResults[fileIndex]+"</h2>")
                write("</a></u></b></p>\r\n")
                CurrentSuiteTitle = fileNameResults[fileIndex]
                write("<p><b><u><a name=\""+caseName+"\">")
                write("TestCaseName : "+caseName)
                write("</a></u></b></p>\r\n")   
                #Write Failures
                write("Failed")
                write("<br>\r\n")
                generateTestFailureDetailTable(caseResult["ErrorLines"])
                for LogPath in caseResult["LogPaths"]:
                    generateHrefTableCell(LogPath,"#E5E5FF", "black",'220')
                write("<br>")
        fileIndex+=1


def generateWarningDetail():
    write("<p><span style='font-size:16.0pt'>3.Warnings</span></p>\r\n")
    CurrentSuiteTitle = ""
    fileIndex=0
    for suiteResult in allResults:
        for (caseName,caseResult) in suiteResult.items():
            if caseResult["Warning"]>0:
                write("<p><b><u><a name=\"" +fileNameResults[fileIndex]+"\">")
                write("<h2>TestSuiteName : "+fileNameResults[fileIndex]+"</h2>")
                write("</a></u></b></p>\r\n")
                CurrentSuiteTitle = fileNameResults[fileIndex]
                write("<p><b><u><a name=\""+caseName+"\">")
                write("TestCaseName : "+caseName)
                write("</a></u></b></p>\r\n")   
                #Write Failures
                write("Warned")
                write("<br>\r\n")
                generateTestWarningDetailTable(caseResult["WarningLines"])
                for LogPath in caseResult["LogPaths"]:
                    generateHrefTableCell(LogPath,"#E5E5FF", "black",'220')
                write("<br>")
        fileIndex+=1

# 2017.2.6  add function processStatFile() : to dispylay the statistics of all resources file
def processStatFile(fileName):
    try:
        file=io.open(fileName,"r")
        write("<p><span style='font-size:16.0pt'>4. Resource Statistical Table</span></p>\r\n")
        write("<table style='border-collapse:collapse;border:none;mso-border-alt:solid black .5pt'>")
        #Write table header row
        write("<tr>\n")
        generateTableCell("Extension Name", "blue", "white", '120',"center")    
        generateTableCell("File Type", "blue", "white", '120',"center")
        generateTableCell("Number of File", "blue", "white", '120',"center")
        generateTableCell("Total Size (MB)", "blue", "white", '120',"center")
        generateTableCell("Maximal Size (MB)", "blue", "white", '120',"center")
        generateTableCell("Minimal Size (MB)", "blue", "white", '120',"center")
        write("</tr>\n")

        for line in file:
            write("<tr>\n")
            statList=line.split("|")
            for stat in statList:
                GenerateTableCell(stat, "white", "black",'120',"center")
            write("</tr>\n")
        write("</table>\n")
        file.close()

    except IOError:
        print("没有文件："+fileName)

def main():
    # filepath=r"C:\Users\hzwangchaochen\Desktop\luaToPython"
    # if os.path.isdir(filepath):  #如果filepath是目录，则再列出该目录下的所有文件
    #     for file in os.listdir(filepath):
    #         if ".log" in file:
    #             parseResultFile(file)
    externalLogs = os.popen("ls *.log | grep -v InEditor").read()
    externalLogs = externalLogs.split("\n")
    for file in externalLogs:
        if ".log" in file:
            parseResultFile(file)  
            
    editorLogs = os.popen("ls *.log | grep InEditor").read()
    editorLogs = editorLogs.split("\n")
    for file in editorLogs:
        if ".log" in file:
            parseResultFile(file) 



    generateHeader("Resource Check for LX6: ")
    generateSummaryTable()
    generateFailureDetail()
    generateWarningDetail()
    generateTail()


if __name__ == '__main__':
    main()
    