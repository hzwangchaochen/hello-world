package.path = '/var/www/Checker/LuaXml/?.lua'
package.cpath='/var/www/Checker/LuaXml/?.so'
require "LuaXml"
local lx=xml.load("/var/www/Checker/DailyCheckMap.xml")
local allResults = {}
local fileNameResults={}

local sNum = 0
local dateTime
local InsertTag=true

local function Write(szFormat,...)
    if szFormat ~= nil then
        local msg=string.format(szFormat,...)
        resultfile:write(msg)
    end
end

-- 2017.2.6  add function mysplit() : to split a string with certain mark
local function mysplit(inputstr, sep)
    if sep == nil then
        sep = "%s"
    end
    local t={}  i=1
    for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
        t[i] = str
        i = i + 1
    end
    return t
end

local function GenerateHeader(testTitle)
    Write("<html><head><title>")
    Write(testTitle .. "</title>")
    Write("<meta http-equiv=Content-Type content=\"text/html charset=utf-8\">")
    Write("</head><body>\r\n")
    -- Now parse the test run ID to figure out the actual date
    Write("<p><span style='font-size:26.0pt'>")
    Write(testTitle)
    Write("</span></p>\r\n")
    Write("<p><span style='font-size:15.0pt'>")
    Write("对游戏内用到的各类资源按照既定规则进行检查，并生成报告；不含游戏逻辑检查。")
    Write("</span></p>\r\n")
end

local function GenerateTableCell(text, bgColor, fgColor, width,position)
        Write("<td align=top style='width:")
        Write(width)
        Write("pt;border:solid black 1.0pt;background:")
        Write(bgColor)
        Write("'>\r\n")
        Write("<p align=center style='text-align:")
        Write(position)
        Write("'><b><span style='font-size:12.0pt;color:")
        Write(fgColor)
        Write("'>")
    if text then
            Write(text)
    else
        Write("no data")
    end
        Write("</span></b></p>\r\n</td>\r\n")
end

--generate a table cell which supplies a href-link
local function GenerateHrefTableCell(text, bgColor, fgColor, width)
    Write("<td align=top style='width:")
    Write(width)
    Write("pt;border:solid black 1.0pt;background:")
    Write(bgColor)
    Write("'>\r\n")

    Write("<a href=\"http://192.168.131.107/LX6/")
    Write(timestamp)
    Write("/")
    Write(text)
    Write("\" target=_blank>")
    Write(text)
    Write("</a>\r\n</td>\r\n")
end

local function GenerateTestFailureDetailTable(ErrorMsg)
    --ErrorMsg = ErrorMsg.Substring(0, ErrorMsg.Length - 4)
    Write("<table style='border-collapse:collapse;border:none;mso-border-alt:solid black .5pt'>")
    Write("<tr>\r\n")
    GenerateTableCell("Failures", "red", "white", 120,"center")
    GenerateTableCell(table.concat(ErrorMsg), "white", "black", 1000,"left")
    Write("</tr>\r\n")
    Write("</table>\r\n")
end

local function GenerateTestWarningDetailTable(ErrorMsg)
    --ErrorMsg = ErrorMsg.Substring(0, ErrorMsg.Length - 4)
    Write("<table style='border-collapse:collapse;border:none;mso-border-alt:solid black .5pt'>")
    Write("<tr>\r\n")
    GenerateTableCell("Warnings", "#F77626", "white",120,"center")
    GenerateTableCell(table.concat(ErrorMsg), "white", "black", 1000,"left")
    Write("</tr>\r\n")
    Write("</table>\r\n")
end

local function GenerateTail()
    Write("</body></html>")
end


local function ParseResultFile(fileName)
    local suiteResult = {}
    local file=io.open(fileName,"r")
    local curCaseResult = ""

    for line in file:lines() do
        local t = {}      -- table to store the indices
        if not dateTime then
           dateTime = string.sub(line, 1, 10)
        end
        t=mysplit(line,"|")

        local runningTime = t[1]
        local logLevel = t[2]
        local caseName = t[3]
        local logMessage = t[4]

        if logMessage ~= nil then
            -- parse keywords
            if string.find(logMessage, "TestCaseStarted") then  -- start test
                if suiteResult[caseName] == nil then
                    local result = {
                        TestCaseName = caseName,
                        Pass = 1,
                        Fail = 0,
                        Warning = 0,
                        ErrorLines = { },
                        WarningLines={ },
                        LogPaths = { }
                    }
                    --table.insert(suiteResult, caseName, result)
                    suiteResult[caseName] = result
                end
            elseif logLevel == "ERR" then   -- mark current test case as FAIL
                curCaseResult = "ERR"
                suiteResult[caseName].Pass=0
                suiteResult[caseName].Fail=1
                table.insert(suiteResult[caseName].ErrorLines, logMessage)

            elseif logLevel == "WARN" then   -- mark current test case as FAIL
                curCaseResult = "WARN"
                suiteResult[caseName].Pass=0
                suiteResult[caseName].Warning=1
                table.insert(suiteResult[caseName].WarningLines, logMessage)

            elseif string.find(logMessage, "TestCaseEnded") then
                table.insert(suiteResult[caseName].LogPaths, fileName)
            end
        end
    end
        file:close()
        table.insert(allResults,suiteResult)
        table.insert(fileNameResults,fileName)
        --table.foreach(suiteResult, function(k, v) table.foreach(v, function(u, w) --[[print(u,w)]] end) end)
end

local function GenerateSummaryTable()
    local firstColumnWidth = 220
    Write("<p><span style='font-size:16.0pt'>1. Summary</span></p>\r\n")     
    local totalPass = 0
    local totalFail = 0
    local totalWarning=0
    table.foreach(allResults, function(fileIndex,suiteResult)
        table.foreach(suiteResult, function(caseName,caseResult)
            totalPass = totalPass + caseResult.Pass
            totalFail = totalFail + caseResult.Fail
            totalWarning=totalWarning+caseResult.Warning
        end)
    end)

    if totalFail ~= 0 then
        Write("<p><span><font style='font-size:18.0pt' color='red'>今日检查没有全部通过，需要QA跟进检查</font></span></p>\r\n")
    else 
        Write("<p><span><font style='font-size:18.0pt' color='green'>今日检查全部通过</font></span></p>\r\n")
    end
    Write("<font style='font-size:18.0pt'>Total cases passed: "..totalPass.."</font><br>")
    Write("<font style='font-size:18.0pt'>Total cases failed: "..totalFail.."</font><br>")
    Write("<font style='font-size:18.0pt'>Total cases Warning: "..totalWarning.."</font><br><br>\n")
    --Write("<font color='red'>Total cases blocked:"..totalBlocked.."</font><br><br>\n")
            
    Write("<table style='border-collapse:collapse;border:none;mso-border-alt:solid black .5pt'>")
    -- Write table header row
    Write("<tr>\n")
    GenerateTableCell("TestSuite Name", "black", "white", firstColumnWidth,"center") 
    GenerateTableCell("Total","#330000","white", 120,"center")
    GenerateTableCell("Pass", "#00B050", "white", 120,"center")
    GenerateTableCell("Fail", "red", "white", 120,"center")
    GenerateTableCell("Warning", "#F77626", "white", 120,"center")
    GenerateTableCell("Description", "blue", "white", 400,"center")
    GenerateTableCell("TestCase Type", "purple", "white", 200,"center")
    Write("</tr>\n")
    -- Now iterate through all test result and write the lines
    local darkerBrackground = false -- To make the table more readable
    table.foreach(allResults, function(fileIndex,suiteResult)
        local curPass = 0
        local curFail = 0
        local curWarning=0
        local backColor= ""
        local backColorForEditor= ""
        
        local logIntro=""
        table.foreach (suiteResult, function(caseName,caseResult)
            curPass = curPass + caseResult.Pass
            curFail = curFail + caseResult.Fail
            curWarning = curWarning+caseResult.Warning
        end)
        -- First calculate percentages
        if curPass ~= 0 or curFail ~= 0 or curWarning ~= 0 then
            -- Backcolor will be a light gray if darkerBrackGround is true, white otherwise
            if darkerBrackground then
                backColor = "#E5E5FF"
            else
                backColor = "white"
            end
            if darkerBrackground then
                darkerBrackground = false
            else
                darkerBrackground = true
            end
            local logIntro=string.sub(fileNameResults[fileIndex],1,-5)
            logIntro=lx:find(logIntro)[1]
            if string.find(fileNameResults[fileIndex],"InEditor")==nil 
            then
                GenerateHrefTableCell(fileNameResults[fileIndex],  "white", "black", firstColumnWidth)
                GenerateTableCell(curPass+curFail+curWarning, "white",  "#330000", 120,"center")
                GenerateTableCell(curPass,  "white", "#00B050", 120,"center")
                GenerateTableCell(curFail,  "white", "red", 120,"center")
                GenerateTableCell(curWarning,  "white", "#F77626", 120,"center")
                GenerateTableCell(logIntro, "white", "black", 400,"center")
                GenerateTableCell("通过外部脚本进行检查", "white", "black", 200,"center")
            else
                GenerateHrefTableCell(fileNameResults[fileIndex], "#E5E5FF", "black", firstColumnWidth)
                GenerateTableCell(curPass+curFail+curWarning, "#E5E5FF" ,"#330000", 120,"center")
                GenerateTableCell(curPass,  "#E5E5FF", "#00B050", 120,"center")
                GenerateTableCell(curFail,  "#E5E5FF", "red", 120,"center")
                GenerateTableCell(curWarning,  "#E5E5FF", "#F77626", 120,"center")
                GenerateTableCell(logIntro,"#E5E5FF", "black", 400,"center")
                GenerateTableCell("通过unity editor进行检查","#E5E5FF", "black", 200,"center")
            end
            Write("</tr>\n")
        end
     end)
    Write("<tr>\n")
    Write("<td align=top style='width:220pt;border:solid black 1.0pt;background:white'>\r\n")
    Write("<a href='http://192.168.131.107/Checker/ResourcesOutline/display.php' target=_blank>点击查看资源文件统计结果</a></td>")
    GenerateTableCell(1, "white" ,"#330000", 120,"center")
    GenerateTableCell(1, "white", "#00B050", 120,"center")
    GenerateTableCell(0,  "white", "red", 120,"center")
    GenerateTableCell(0, "white", "#F77626", 120,"center")
    GenerateTableCell("查看资源文件统计结果","white", "black", 400,"center")
    GenerateTableCell("资源统计","white", "black", 200,"center")
    Write("</tr>\n")
    Write("</tr></table>")
end


local function GenerateFailureDetail()
    Write("<p><span style='font-size:16.0pt'>2.Failures</span></p>\r\n")

    local CurrentSuiteTitle = ""
    table.foreach(allResults, function(fileIndex,suiteResult)
        table.foreach (suiteResult, function(caseName,caseResult)
            if caseResult.Fail==1 then
                Write("<p><b><u><a name=\"" .. fileNameResults[fileIndex] .. "\">")
                Write("<h2>TestSuiteName : " .. fileNameResults[fileIndex] .. "</h2>")
                Write("</a></u></b></p>\r\n")
                CurrentSuiteTitle = fileNameResults[fileIndex]
                Write("<p><b><u><a name=\"" .. caseName .. "\">")
                Write("TestCaseName : " .. caseName)
                Write("</a></u></b></p>\r\n")           
            -- Write Failures
                Write("Failed")
                Write("<br>\r\n")
                GenerateTestFailureDetailTable(caseResult.ErrorLines)
                table.foreach(caseResult.LogPaths, function(i,v)
                    GenerateHrefTableCell(v, "#E5E5FF", "black", 220)
                end)
                Write("<br>")
            end
        end)
    end)
end

local function GenerateWarningDetail()
    Write("<p><span style='font-size:16.0pt'>3.Warnings</span></p>\r\n")

    local CurrentSuiteTitle = ""
    table.foreach(allResults, function(fileIndex,suiteResult)
        table.foreach (suiteResult, function(caseName,caseResult)
            if caseResult.Warning==1 then
                Write("<p><b><u><a name=\"" .. fileNameResults[fileIndex] .. "\">")
                Write("<h2>TestSuiteName : " .. fileNameResults[fileIndex] .. "</h2>")
                Write("</a></u></b></p>\r\n")
                CurrentSuiteTitle = fileNameResults[fileIndex]
                Write("<p><b><u><a name=\"" .. caseName .. "\">")
                Write("TestCaseName : " .. caseName)
                Write("</a></u></b></p>\r\n")           
            -- Write Failures
                Write("Warned")
                Write("<br>\r\n")
                GenerateTestWarningDetailTable(caseResult.WarningLines)
                table.foreach(caseResult.LogPaths, function(i,v)
                    GenerateHrefTableCell(v, "#E5E5FF", "black", 220)
                end)
                Write("<br>")
            end
        end)
    end)
end

local function displayResult()
    Write("<p><span style='font-size:16.0pt'>2. Resource Outline</span></p>\r\n")
    Write("<a href='http://192.168.131.107/Checker/ResourcesOutline/display.php' target=_blank>点击查看资源文件统计结果</a>\r\n")
end

-- 2017.2.6  add function processStatFile() : to dispylay the statistics of all resources file
local function processStatFile(fileName)
    local file=io.open(fileName,"r")
    if file then
        Write("<p><span style='font-size:16.0pt'>4. Resource Statistical Table</span></p>\r\n")
        Write("<table style='border-collapse:collapse;border:none;mso-border-alt:solid black .5pt'>")
        -- Write table header row
        Write("<tr>\n")
        GenerateTableCell("Extension Name", "blue", "white", 120,"center")    
        GenerateTableCell("File Type", "blue", "white", 120,"center")
        GenerateTableCell("Number of File", "blue", "white", 120,"center")
        GenerateTableCell("Total Size (MB)", "blue", "white", 120,"center")
        GenerateTableCell("Maximal Size (MB)", "blue", "white", 120,"center")
        GenerateTableCell("Minimal Size (MB)", "blue", "white", 120,"center")
        Write("</tr>\n")
        for line in file:lines() do
            Write("<tr>\n")
            list=mysplit(line,"|")
            for i = 1,#list do
                GenerateTableCell(list[i], "white", "black", 120,"center")
            end
            Write("</tr>\n")
        end
        Write("</table>\n")
        file:close()
    end
end


--main starts from here
local files=io.popen("ls *.log | grep -v InEditor" )
local file=files:read()
while file do
		--print(file)
	if file~="ClientQARunner.log" and file~="ServerQARunner.log" then
		ParseResultFile(file)
        end
	file=files:read()
end
files:close()

local files=io.popen("ls *.log | grep InEditor" )
local file=files:read()
while file do
		--print(file)
	if file~="ClientQARunner.log" and file~="ServerQARunner.log" then
		ParseResultFile(file)
        end
	file=files:read()
end
files:close()

resultfile=io.open("Result.html","w")
GenerateHeader("Resource Check for LX6: ")
GenerateSummaryTable()
GenerateFailureDetail()
GenerateWarningDetail()
GenerateTail()

resultfile:close()
